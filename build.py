#!/usr/bin/env python3
"""Builds the CalcProject.org static pages. Usage: python3 build.py /path/to/repo /path/to/original-snapshot"""
import sys, re, json, html, os, datetime
import subprocess
from defs import C, CATS as HOME_CATS
import mass, m1, m2, m3
mass.make_converters()
from extras import E as EXTRA
HOMECATS = ('measure', 'walls', 'floors', 'concrete', 'yard', 'exterior', 'electrical')
# Staged release: CP_CATS lists which groups of the additional calculators are published ("home" = the home-improvement groups, "all" = everything).
_rel = os.environ.get('CP_CATS', 'all').split(',')
_relcats = set(HOMECATS if 'home' in _rel else ()) | set(_rel)
MASS = [c for c in mass.M if 'all' in _rel or c['cat'] in _relcats]
GENERAL = any(c['cat'] not in HOMECATS for c in MASS)
C = C + MASS
MDISC = {k: d for k, n, b, e, d in mass.MCATS}
MEYE = {k: e for k, n, b, e, d in mass.MCATS}
_m = {k: (k, n, b) for k, n, b, e, d in mass.MCATS}
_h = {k: (k, n, b) for k, n, b in HOME_CATS}
_live = {c['cat'] for c in C} | {'electrical', 'math'}
CATS = [_h[k] for k in ('measure', 'walls', 'floors', 'concrete', 'yard', 'exterior', 'electrical')] + [_m[k] for k in ('finance', 'business', 'percent', 'geometry', 'stats')] + [_h['math']] + [_m[k] for k in ('physics', 'convert', 'time', 'health', 'everyday')]
CATS = [c for c in CATS if c[0] in _live]

REPO, ORIG = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://calcproject.org/'
TODAY = datetime.date.today().isoformat()

def rd(p, root=ORIG): return open(os.path.join(root, p), encoding='utf-8').read()
def wr(p, s):
    open(os.path.join(REPO, p), 'w', encoding='utf-8').write(s)

orig_index, orig_adv, orig_math = rd('index.html'), rd('advanced-tools.html'), rd('math-tools.html')

# ------------------------------------------------------------------ CSS
def css_blocks(src):
    s = src[src.index('<style>') + 7:src.index('</style>')]
    out, depth, start = [], 0, 0
    for i, ch in enumerate(s):
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                out.append(s[start:i + 1].strip()); start = i + 1
    return out
seen, blocks = set(), []
for src in (orig_index, orig_adv, orig_math):
    for b in css_blocks(src):
        k = re.sub(r'\s+', ' ', b)
        if k not in seen:
            seen.add(k); blocks.append(b)
site_css = '/* CalcProject.org shared styles for calculator pages */\n' + '\n'.join(blocks) + '\n' + rd('extra.css', HERE)
wr('site.css', site_css)
wr('calc.js', rd('calc-core.js', HERE).replace("if (typeof module !== 'undefined') module.exports = CPCore;\n", '') + '\n' + rd('calc.js', HERE))

# ------------------------------------------------------------------ shared chrome
HEAD_TOP = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3049181732703221"
     crossorigin="anonymous"></script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-L7VM2GPNKZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-L7VM2GPNKZ');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
def attr(s): return html.escape(plain(s), quote=True)

def head(title, desc, path, ld, extra=''):
    url = BASE + path
    lds = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace('</', '<\\/') + '</script>\n' for x in ld)
    return (HEAD_TOP + f'''<title>{attr(title)}</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CalcProject">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}logo-large.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
{extra}{lds}</head>
<body>
''')

NAV = '''<div class="site-header">
  <div class="site-header-inner">
    <a href="index.html" class="brand" aria-label="CalcProject.org home">
      <img src="logo-header.png" alt="CalcProject.org logo" width="52" height="52">
    </a>
    <nav class="site-nav" aria-label="Site">
      <a href="index.html">Calculators</a>
      <a href="advanced-tools.html">Electrical</a>
      <a href="math-tools.html">Math</a>
      <a href="guides.html">Guides</a>
      <a href="about.html">About &amp; Contact</a>
    </nav>
  </div>
</div>
'''
FOOT_LINKS = ' '.join(f'<a href="index.html#{k}">{n}</a>' for k, n, _ in CATS)
def footer(note):
    return f'''<div class="ruler" role="presentation"></div>

<footer>
  <p class="foot-links">{FOOT_LINKS}</p>
  <p>{note}</p>
  <p><a href="index.html">All calculators</a> &middot; <a href="guides.html">Guides</a> &middot; <a href="privacy-policy.html">Privacy Policy</a> &middot; <a href="about.html">About &amp; Contact</a></p>
</footer>
'''
def save_dialog(label='Name your project', ph="e.g. Back deck, kids' bedroom", clear=True):
    c = '\n    <button type="button" class="sd-clear" id="sd-clear">Start a new sheet with only this calculator</button>' if clear else ''
    return f'''<dialog id="save-dialog" aria-labelledby="sd-title">
  <div class="sd-inner">
    <h2 id="sd-title">Save or print your results</h2>
    <p class="sd-on" id="sd-on"></p>
    <label for="project-name">{label} <span>(optional)</span></label>
    <input type="text" id="project-name" maxlength="60" placeholder="{ph}" autocomplete="off">
    <p class="sd-tip">On a phone, choose <strong>Save as PDF</strong> on the next screen to keep a copy.</p>
    <div class="sd-actions">
      <button type="button" class="btn-outline" id="sd-cancel">Cancel</button>
      <button type="button" class="calc-btn" id="sd-print">Print or save</button>
    </div>{c}
  </div>
</dialog>

<div id="print-sheet" aria-hidden="true"></div>
'''
CATNAME = {k: n for k, n, _ in CATS}
def crumbs(cat, name):
    return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="index.html#{cat}">{CATNAME[cat]}</a> &rsaquo; <span>{name}</span></nav>'
def ld_crumbs(cat, name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": plain(CATNAME[cat]), "item": BASE + 'index.html#' + cat},
        {"@type": "ListItem", "position": 3, "name": plain(name), "item": BASE + path}]}
def ld_app(name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": plain(name), "url": BASE + path, "description": plain(desc),
            "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
            "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@type": "Organization", "name": "CalcProject", "url": BASE}}
def ld_faq(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]}

# every page that can be linked as a "related" card: slug -> (name, blurb, cat)
PAGES = {}

# ------------------------------------------------------------------ guides
GUIDES = {}
for fn in sorted(os.listdir(ORIG)):
    if fn.endswith('.html') and (fn.endswith('-guide.html') or fn.startswith('how-')):
        t = re.search(r'<h1[^>]*>(.*?)</h1>', rd(fn), re.S)
        GUIDES[fn[:-5]] = plain(t.group(1)) if t else fn

# ------------------------------------------------------------------ home-improvement calculator pages
UNITS = {'ft': ('ft', 'm', '0.3048'), 'in': ('in', 'cm', '2.54'), 'sqft': ('sq ft', 'm&sup2;', '0.09290304'),
         'cuft': ('cu ft', 'L', '28.316846592'), 'sqftgal': ('sq ft per gallon', 'm&sup2; per liter', '0.0245424'),
         'tpy': ('tons per cubic yard', 'kg per m&sup3;', '1186.55'), 'lbk': ('lb per 1,000 sq ft', 'kg per 100 m&sup2;', '0.488243')}

def field_html(f):
    fid = 'c-' + f['k']
    hint = f' <span class="hint">{f["hint"]}</span>' if f.get('hint') else ''
    if f.get('opts'):
        o = ''.join(f'<option value="{v}"{" selected" if str(v) == str(f["d"]) else ""}>{t}</option>' for v, t in f['opts'])
        return f'<div class="field"><label for="{fid}">{f["label"]}{hint}</label><select id="{fid}">{o}</select></div>'
    if f.get('type'):
        t = f['type']
        extra = ' autocomplete="off" spellcheck="false"' if t == 'text' else ''
        return f'<div class="field"><label for="{fid}">{f["label"]}{hint}</label><input type="{t}" id="{fid}" value="{html.escape(str(f["d"]), quote=True)}"{extra}></div>'
    if f.get('u'):
        a, b, fac = UNITS[f['u']]
        unit = f' (<span class="u" data-imp="{a}" data-met="{b}">{a}</span>)'
        fa = f' data-factor="{fac}"'
    else:
        unit, fa = '', ''
    step = f.get('step') or ('0.1' if f.get('u') else '1')
    mn = '' if (f.get('free') and not f.get('u')) else ' min="0"'
    if f.get('free'): step = 'any'
    return f'<div class="field"><label for="{fid}">{f["label"]}{unit}{hint}</label><input type="number" id="{fid}"{mn} step="{step}" value="{f["d"]}"{fa} inputmode="decimal"></div>'

def inputs_html(c):
    if c.get('rooms'):
        row = lambda i, L, W: f'''<div class="room-row">
            <div class="room-row-head"><span class="room-name">Room {i}</span><button type="button" class="remove-room" onclick="removeRoom(this)">Remove</button></div>
            <div class="field-row">
              <div class="field"><label>Length (<span class="u" data-imp="ft" data-met="m">ft</span>)</label><input type="number" class="room-length" min="0" step="0.1" value="{L}" data-factor="0.3048" inputmode="decimal"></div>
              <div class="field"><label>Width (<span class="u" data-imp="ft" data-met="m">ft</span>)</label><input type="number" class="room-width" min="0" step="0.1" value="{W}" data-factor="0.3048" inputmode="decimal"></div>
            </div>
          </div>'''
        return f'<div id="rooms">{row(1, 12, 10)}{row(2, 10, 8)}</div>\n        <button type="button" class="btn-outline" onclick="addRoomRow()">+ Add another room</button>'
    if c.get('legacy'):
        sec = re.search(r'<section class="ticket" id="%s">(.*?)</section>' % c['legacy'], orig_index, re.S).group(1)
        inner = sec[sec.index('<div class="calc-inputs">') + len('<div class="calc-inputs">'):sec.index('<button class="calc-btn"')]
        inner = inner.replace('data-factor="0.0929"', 'data-factor="0.09290304"').replace('data-factor="28.3168"', 'data-factor="28.316846592"')
        return inner.strip()
    out = []
    for row in c['fields']:
        cells = ''.join(field_html(f) for f in row)
        out.append(f'<div class="field-row">{cells}</div>' if len(row) > 1 else cells)
    return '\n        '.join(out)

def legacy_note(c):
    sec = re.search(r'<section class="ticket" id="%s">(.*?)</section>' % c['legacy'], orig_index, re.S).group(1)
    note = re.search(r'<div class="formula-note">(.*?)</div>\s*<div class="guide-link">', sec, re.S).group(1)
    m = re.match(r'<strong>How it works:</strong>\s*(.*?)\s*<strong>Example:</strong>\s*(.*)$', note.strip(), re.S)
    how, ex = m.group(1).strip(), m.group(2).strip()
    return how[0].upper() + how[1:], ex

def card(slug):
    name, blurb, _ = PAGES[slug]
    return f'<a class="calc-card" href="{slug}.html"><strong>{name}</strong><span>{blurb}</span></a>'

for c in C:
    PAGES[c['slug']] = (c['name'], c['card'], c['cat'])

ELEC = [
 dict(tid='electricity-cost', slug='electricity-cost-calculator', name='Electricity Cost Calculator', card='What an appliance costs to run per day, month, and year.',
      title='Electricity Cost Calculator: Cost to Run Any Appliance',
      desc='Free electricity cost calculator. Enter watts, hours per day, and your rate per kWh to see what an appliance costs to run per day, month, and year.',
      lead='Enter the wattage of an appliance, how long it runs, and your electric rate to see what it costs per day, month, and year.',
      faqs=[('How do I calculate the cost to run an appliance?', 'Multiply the watts by the hours used and divide by 1,000 to get kilowatt-hours. Multiply the kilowatt-hours by your rate per kWh. A 1,500 W heater running 8 hours uses 12 kWh, which costs $1.80 at $0.15 per kWh.'),
            ('Where do I find the wattage of an appliance?', 'On the label or nameplate, usually on the back or bottom. If only amps are listed, multiply the amps by the voltage (120 V for most outlets) to get watts.'),
            ('What is a kilowatt-hour?', 'A kilowatt-hour (kWh) is 1,000 watts used for one hour. It is the unit your electric company bills you for.')]),
 dict(tid='watts-amps', slug='watts-amps-calculator', name='Watts to Amps Calculator', card='Convert between watts, amps, and volts for any device.',
      title='Watts to Amps Calculator: Convert Watts, Amps and Volts',
      desc='Free watts to amps calculator. Convert watts to amps or amps to watts at 120 V, 240 V, or 12 V to see how much current a device draws.',
      lead='Convert watts to amps, or amps to watts, at 120, 240, or 12 volts. Use it to check whether a device fits on a circuit.',
      faqs=[('How do I convert watts to amps?', 'Divide the watts by the volts. A 1,500 W heater on a 120 V outlet draws 1,500 &divide; 120 = 12.5 amps.'),
            ('How many watts can a 15 amp circuit handle?', 'A 15 amp, 120 V circuit carries 1,800 watts at most, and 1,440 watts for loads that run 3 hours or more (80 percent of the breaker rating).'),
            ('How many amps does a 1,500 watt heater use?', 'About 12.5 amps at 120 volts. That nearly fills a 15 amp circuit, so run it on a circuit with little else plugged in.')]),
 dict(tid='circuit-load', slug='circuit-load-calculator', name='Circuit Load Calculator', card='Add up devices on one circuit and check the breaker.',
      title='Circuit Load Calculator: Will It Trip the Breaker?',
      desc='Free circuit load calculator. Add up the watts of everything on one circuit and see whether a 15, 20, or 30 amp breaker can handle the load.',
      lead='List what is plugged into one circuit and see the total amps, the steady-use limit, and whether the breaker can handle it.',
      faqs=[('How many outlets can be on a 20 amp circuit?', 'There is no fixed number for homes in the National Electrical Code. What matters is the total load. Keep steady loads under 16 amps (1,920 watts at 120 V) on a 20 amp circuit.'),
            ('What is the 80 percent rule for breakers?', 'A load that runs for 3 hours or more should not exceed 80 percent of the breaker rating: 12 amps on a 15 amp breaker and 16 amps on a 20 amp breaker.'),
            ('Why does my breaker keep tripping?', 'Usually because too much is running on one circuit at once. A breaker that trips with a light load can point to a wiring fault and should be checked by an electrician.')]),
 dict(tid='wire-size', slug='wire-size-calculator', name='Wire Size &amp; Voltage Drop Calculator', card='Voltage drop and the smallest wire for a long run.',
      title='Wire Size Calculator: Voltage Drop and Gauge for a Run',
      desc='Free wire size and voltage drop calculator. Enter amps, voltage, and distance to find the voltage drop and the smallest copper or aluminum wire gauge.',
      lead='Check a wire run to a shed, garage, or RV hookup. See the voltage drop for the wire you plan to use and the smallest gauge that keeps the drop under 3 percent.',
      faqs=[('What size wire do I need for a 100 foot run?', 'It depends on the amps. For 20 amps at 120 V over 100 feet, 8 AWG copper keeps voltage drop under 3 percent. For 30 amps at 240 V over 100 feet, 8 AWG copper also works.'),
            ('How much voltage drop is acceptable?', 'The National Electrical Code recommends, but does not require, no more than 3 percent drop on a branch circuit and 5 percent in total for feeder plus branch.'),
            ('Does voltage drop depend on one-way or round-trip distance?', 'Current travels out and back, so the math uses twice the one-way distance. Enter the one-way distance here and the calculator doubles it.')]),
 dict(tid='generator', slug='generator-size-calculator', name='Generator Size Calculator', card='Running and starting watts for a power outage.',
      title='Generator Size Calculator: What Size Generator Do I Need?',
      desc='Free generator size calculator. Check off the appliances you want to run in an outage to get the running watts and starting watts your generator needs.',
      lead='Check off what you want to keep running during an outage and see the running watts, starting watts, and the generator size that covers them.',
      faqs=[('What size generator do I need to run a refrigerator?', 'A refrigerator runs on about 700 watts but needs around 2,200 watts for a moment when the compressor starts. A 3,000 watt generator handles a fridge plus lights and chargers.'),
            ('What is the difference between running watts and starting watts?', 'Running watts are what an appliance uses steadily. Starting watts are the short surge a motor needs to start, often two to three times the running watts.'),
            ('Can I plug a generator into a wall outlet?', 'No. Backfeeding through an outlet can electrocute utility workers and start fires. Use a transfer switch or interlock installed by a licensed electrician.')]),
]
MATH = [
 ('linear', 'linear-equation-solver', 'Linear Equation Solver', 'Solve ax + b = c for x, with steps.', 'Linear Equation Solver: Solve for x With Steps', 'Free linear equation solver. Enter a, b, and c to solve ax + b = c for x and see every step of the solution.'),
 ('quadratic', 'quadratic-formula-calculator', 'Quadratic Formula Calculator', 'Roots, discriminant, and vertex of a quadratic.', 'Quadratic Formula Calculator With Steps', 'Free quadratic formula calculator. Enter a, b, and c to solve ax^2 + bx + c = 0 and see the discriminant, roots, vertex, and every step.'),
 ('slope', 'slope-calculator', 'Slope Calculator', 'Slope, line equation, distance, and midpoint.', 'Slope Calculator: Slope and Line Equation From Two Points', 'Free slope calculator. Enter two points to get the slope, the equation of the line, the distance, and the midpoint, with steps.'),
 ('derivative', 'derivative-calculator', 'Derivative Calculator', 'Differentiate polynomials with the power rule.', 'Derivative Calculator With Steps (Power Rule)', 'Free derivative calculator for polynomials. Enter a function to see its derivative worked out step by step with the power rule.'),
 ('integral', 'integral-calculator', 'Integral Calculator', 'Antiderivatives and definite integrals of polynomials.', 'Integral Calculator With Steps for Polynomials', 'Free integral calculator for polynomials. Get the antiderivative or a definite integral between two limits, with every step shown.'),
 ('pythagorean', 'pythagorean-theorem-calculator', 'Pythagorean Theorem Calculator', 'Find a missing side of a right triangle.', 'Pythagorean Theorem Calculator With Steps', 'Free Pythagorean theorem calculator. Find the hypotenuse or a missing leg of a right triangle and see every step.'),
 ('trig', 'right-triangle-calculator', 'Right Triangle Trig Calculator', 'Sides and angles with sine, cosine, and tangent.', 'Right Triangle Calculator: Sides and Angles With Trig', 'Free right triangle trig calculator. Use sine, cosine, and tangent to find missing sides and angles, with steps.'),
 ('percent', 'percentage-calculator', 'Percentage Calculator', 'Percent of a number, what percent, and percent change.', 'Percentage Calculator: Percent Of, What Percent, Change', 'Free percentage calculator. Find a percent of a number, what percent one number is of another, or the percent change, with steps.'),
 ('fraction', 'fraction-calculator', 'Fraction Calculator', 'Add, subtract, multiply, and divide fractions.', 'Fraction Calculator With Steps', 'Free fraction calculator. Add, subtract, multiply, or divide two fractions and see the answer in lowest terms with every step.'),
 ('gcf-lcm', 'gcf-lcm-calculator', 'GCF &amp; LCM Calculator', 'Greatest common factor and least common multiple.', 'GCF and LCM Calculator With Steps', 'Free GCF and LCM calculator. Find the greatest common factor and least common multiple of two numbers, with steps.'),
 ('statistics', 'mean-median-mode-calculator', 'Mean, Median &amp; Mode Calculator', 'Average, median, mode, range, and standard deviation.', 'Mean, Median and Mode Calculator With Steps', 'Free mean, median, and mode calculator. Enter a list of numbers to get the average, median, mode, range, and standard deviation.'),
]
for e in ELEC: PAGES[e['slug']] = (e['name'], e['card'], 'electrical')
for tid, slug, name, blurb, title, desc in MATH: PAGES[slug] = (name, blurb, 'math')
assert len(PAGES) == len(C) + len(ELEC) + len(MATH), 'duplicate slug'

DISCLAIMER = 'Estimates are a starting point for shopping, not a substitute for a contractor\'s exact measurement. Always round up, check the coverage printed on your product, and keep your receipt for returns.'

def defaults_of(inputs, c):
    v = {}
    for m in re.finditer(r'<select([^>]*)>(.*?)</select>', inputs, re.S):
        k = re.search(r'\bid="([^"]+)"', m.group(1)).group(1).split('-', 1)[1]
        sm = re.search(r'<option value="([^"]*)" selected>', m.group(2)) or re.search(r'<option value="([^"]*)"', m.group(2))
        raw = sm.group(1)
        try:
            n = float(raw); v[k] = n if re.fullmatch(r'-?\d+(\.\d+)?', raw) else raw
        except ValueError: v[k] = raw
    for m in re.finditer(r'<input([^>]*)>', inputs):
        at = m.group(1)
        idm = re.search(r'\bid="([^"]+)"', at)
        if not idm: continue
        k = idm.group(1).split('-', 1)[1]
        ty = re.search(r'type="(\w+)"', at).group(1)
        raw = html.unescape(re.search(r'value="([^"]*)"', at).group(1))
        v[k] = float(raw or 0) if ty == 'number' else raw
    if c.get('rooms'): v['rooms'] = [[12, 10], [10, 8]]
    return v

for c in C:
    c['_inputs'] = inputs_html(c)
specs = [dict(id=c['slug'], js=c['js'], v=defaults_of(c['_inputs'], c)) for c in C]
open('/tmp/cp_specs.json', 'w').write(json.dumps(specs))
EX = json.loads(subprocess.run(['node', os.path.join(HERE, 'run_examples.js'), '/tmp/cp_specs.json'], capture_output=True, text=True, check=True).stdout)
problems = {k: e for k, e in EX.items() if e.get('error') or e.get('bad')}
for k, e in problems.items(): print('PROBLEM', k, e.get('error') or e.get('bad'))

def auto_example(c):
    e = EX[c['slug']]
    parts = []
    for row in c['fields']:
        for f in row:
            val = f['d']
            if f.get('opts'): val = next((t for v, t in f['opts'] if str(v) == str(f['d'])), val)
            if val == '': continue
            unit = ' ' + UNITS[f['u']][0] if f.get('u') else ''
            parts.append(f'{f["label"]}: {html.escape(str(val))}{unit}')
    s = f'With the starting numbers on this page ({"; ".join(parts)}), the result is <strong>{html.escape(e["total"][0])} {html.escape(e["total"][1])}</strong>.'
    if e['rows']:
        s += ' It also shows ' + '; '.join(f'{html.escape(a)}: {html.escape(b)}' for a, b in e['rows'][:5]) + '.'
    return s

def auto_title(c):
    n = plain(c['name'])
    for t in ((n + ' With Conversion Table') if c.get('table') else None, (n + ' With Formula and Example') if c['cat'] != 'convert' else n + ': Free Online Unit Conversion', n + ' | CalcProject', n):
        if t and len(t) <= 60: return t
    return n
def auto_desc(c):
    n, b = plain(c['name']), plain(c['card'])
    for d in (f'Free {n}. {b} Shows the formula and a worked example. No sign-up needed.', f'Free {n}. {b} Formula and worked example included.', f'Free {n}. {b}'):
        if len(d) <= 158: return d
    return d[:157]

def calc_page(c):
    path = c['slug'] + '.html'
    auto = c.get('auto')
    home = c['cat'] in HOMECATS
    has_units = any(f.get('u') for row in c.get('fields', []) for f in row) or not auto
    if c.get('legacy'):
        how, ex = legacy_note(c)
    else:
        how, ex = c['formula'], (c.get('example') or (auto_example(c) if auto else None))
    if auto:
        c['title'], c['desc'] = auto_title(c), auto_desc(c)
        labels = [f['label'] for row in c['fields'] for f in row]
        steps = [('Fill in ' + (', '.join(labels[:-1]) + ' and ' + labels[-1] if len(labels) > 1 else labels[0]) + '.'),
                 'The result updates as you type. Tap <strong>Calculate</strong> to run it again.',
                 'Tap <strong>Save or print results</strong> to keep a copy or add it to your project sheet.']
        if has_units: steps.insert(1, 'Use the Imperial and Metric switch if you measure in meters and centimeters.')
        xt, xf = EXTRA.get(c['slug'], ([], []))
        tips = ([c['note']] if c.get('note') else []) + list(xt)
        faqs = list(xf)
        cat_pages = [s for s, (n, bl, ct) in PAGES.items() if ct == c['cat']]
        i = cat_pages.index(c['slug'])
        related = [cat_pages[(i + k) % len(cat_pages)] for k in (1, 2, 3, 4) if cat_pages[(i + k) % len(cat_pages)] != c['slug']]
        related = list(dict.fromkeys(related))
    else:
        steps, tips, faqs, related = c['steps'], c['tips'], c['faqs'], c['related']
    steps_h = ''.join(f'<li>{s}</li>' for s in steps)
    tips_h = ('<h2>Good to know</h2>\n    ' + ('<ul>' + ''.join(f'<li>{s}</li>' for s in tips) + '</ul>' if len(tips) > 1 else f'<p>{tips[0]}</p>') + '\n') if tips else ''
    faq_h = ('<h2>Common questions</h2>\n      ' + ''.join(f'<h3>{q}</h3>\n      <p>{a}</p>\n      ' for q, a in faqs)) if faqs else ''
    rel = ''.join(card(s) for s in related)
    gl = ''
    if c.get('guides'):
        gl = '<h2>Related guides</h2>\n      <ul>' + ''.join(f'<li><a href="{g}.html">{html.escape(GUIDES[g])}</a></li>' for g in c['guides']) + '</ul>\n      '
    src = f'<p class="source">Source: <a href="{c["source"][1]}" rel="noopener" target="_blank">{c["source"][0]}</a></p>\n      ' if c.get('source') else ''
    tbl = ''
    if c.get('table'):
        ua, ub, k, vals = c['table']
        def fm(x):
            a = abs(x)
            return f'{x:,.0f}' if a >= 1000 and abs(x - round(x)) < 1e-9 else (f'{x:,.2f}' if a >= 100 else f'{x:,.4g}' if a >= 0.01 else f'{x:.3g}')
        tbl = '<h2>Conversion table</h2>\n    <ul>' + ''.join(f'<li>{v:,} {html.escape(ua)} = {fm(v * k)} {html.escape(ub)}</li>' for v in vals) + '</ul>\n    '
    ld = [ld_app(c['name'], c['desc'], path), ld_crumbs(c['cat'], c['name'], path)] + ([ld_faq(faqs)] if faqs else [])
    eyebrow = 'Free &middot; No sign-up &middot; Feet or meters' if (home and has_units) else MEYE.get(c['cat'], 'Free &middot; No sign-up')
    units_h = """
        <div class="ticket-units" role="group" aria-label="Unit system">
          <button type="button" class="active" data-unit-btn="imperial" aria-pressed="true">Imperial</button>
          <button type="button" data-unit-btn="metric" aria-pressed="false">Metric</button>
        </div>""" if has_units else ''
    headp = 'Results update as you type. Switch to metric with the button on the right.' if has_units else 'Results update as you type.'
    disc = DISCLAIMER if home else MDISC.get(c['cat'], DISCLAIMER)
    kind = 'converter' if c['cat'] == 'convert' else 'calculator'
    howto = f"How to use the {c['short'].lower() if c['short'][:2] != 'AC' else c['short']} calculator" if not auto else f'How to use this {kind}'
    exh = ex if (ex.startswith('With the starting') or auto) else (ex[0].upper() + ex[1:] if not ex.startswith('<span') else 'For example, ' + ex)
    label = c.get('label') or ('Estimate' if home else 'Result')
    pre = 'var H = window.CPH, R = function (rows, total, note) { return { rows: rows, total: total, note: note || "" }; };\n' if auto else ''
    body = head(c['title'], c['desc'], path, ld) + NAV + f"""
<header class="page-head">
  {crumbs(c['cat'], c['name'])}
  <span class="eyebrow">{eyebrow}</span>
  <h1>{c['name']}</h1>
  <p class="lead">{c['lead']}</p>
</header>

<main class="calc-main">
  <section class="ticket static" id="calc" aria-label="{attr(c['name'])}">
    <div class="ticket-head">
      <div><h2>Enter your {'measurements' if home else 'numbers'}</h2><p>{headp}</p></div>
      <div class="ticket-side">
        <span class="stamp">{'Job: ' if home else ''}{c['stamp']}</span>{units_h}
      </div>
    </div>
    <div class="ticket-body">
      <div class="calc-inputs">
        {c['_inputs']}
        <button type="button" class="calc-btn">{c['btn']}</button>
        <button type="button" class="btn-outline save-ticket-btn">Save or print results</button>
      </div>
      <div class="receipt-wrap"><div class="receipt" id="receipt" aria-live="polite"><div class="label">{label}</div><p class="receipt-note">Your result shows here once the page finishes loading.</p></div></div>
    </div>
  </section>

  <article class="content-card">
    <h2>{howto}</h2>
    <ol>{steps_h}</ol>

    <h2>The formula</h2>
    <p class="formula">{how}</p>
    <h3>Worked example</h3>
    <p>{exh}</p>
    {src}{tbl}{tips_h}
    {faq_h}
    {gl}<h2>Related calculators</h2>
    <div class="card-grid">{rel}</div>
    <p class="cat-more"><a href="index.html#{c['cat']}">More {plain(CATNAME[c['cat']]).lower()}{'' if c['cat'] == 'convert' else ' calculators'} &rarr;</a> &nbsp; <a href="index.html">All calculators &rarr;</a></p>
    <p class="disclaimer">{disc}</p>
  </article>
</main>

""" + footer('Free online calculators. No sign-up, no app.') + save_dialog() + f"""
<script>
window.CP_CALC = {{ id: {json.dumps(c['id'])}, title: {json.dumps(plain(c['name']))}, label: {json.dumps(label)}, calc: function (v) {{
{pre}{c['js']}
}} }};
</script>
<script src="calc.js"></script>
</body>
</html>
"""
    wr(path, body)


for c in C: calc_page(c)

# ------------------------------------------------------------------ electrical pages (lifted from the old page)
adv_script = orig_adv[orig_adv.rindex('<script>') + 8:orig_adv.rindex('</script>')]
def must(s, a, b):
    assert a in s, a[:60]
    return s.replace(a, b)
adv_script = must(adv_script, 'function recalcAll(){ calcElecCost(); calcWattsAmps(); calcCircuit(); calcWire(); calcGenerator(); }',
    "function recalcAll(){ if($('ec-receipt')) calcElecCost(); if($('wa-receipt')) calcWattsAmps(); if($('cl-receipt')) calcCircuit(); if($('ws-receipt')) calcWire(); if($('gen-receipt')) calcGenerator(); }")
adv_script = must(adv_script, "addDevice('Space heater',1500); addDevice('TV',100); addDevice('Lamp',60);",
    "if($('cl-devices')){ addDevice('Space heater',1500); addDevice('TV',100); addDevice('Lamp',60); }")
adv_script = must(adv_script, 'buildGen(); recalcAll();', "if($('gen-list')) buildGen(); recalcAll();")
adv_script = must(adv_script, "$('cl-devices').addEventListener('input',calcCircuit);", "if($('cl-devices')) $('cl-devices').addEventListener('input',calcCircuit);")
adv_script = must(adv_script, "const btn=document.getElementById('back-to-top');\n    if(window.scrollY>400)", "const btn=document.getElementById('back-to-top'); if(!btn) return;\n    if(window.scrollY>400)")
wr('electrical.js', '/* CalcProject.org electrical calculators (shared by each electrical calculator page). */\n' + adv_script)

ELEC_DISC = re.search(r'<section class="disclaimer-box" id="electrical-disclaimer">(.*?)</section>', orig_adv, re.S).group(1)
def elec_page(e):
    path = e['slug'] + '.html'
    sec = re.search(r'(<section class="ticket" id="%s">.*?</section>)' % e['tid'], orig_adv, re.S).group(1)
    sec = sec.replace('<section class="ticket"', '<section class="ticket static"', 1)
    sec = re.sub(r'<div><h2>.*?</h2><p>(.*?)</p></div>', lambda m: '<div><h2>Enter your numbers</h2><p>' + m.group(1) + '</p></div>', sec, count=1, flags=re.S)
    faqs = ''.join(f'<h3>{q}</h3>\n      <p>{a}</p>\n      ' for q, a in e['faqs'])
    others = [x['slug'] for x in ELEC if x['slug'] != e['slug']][:3] + ['air-conditioner-btu-calculator']
    rel = ''.join(card(s) for s in others)
    body = head(e['title'], e['desc'], path, [ld_app(e['name'], e['desc'], path), ld_crumbs('electrical', e['name'], path), ld_faq(e['faqs'])]) + NAV + f'''
<header class="page-head">
  {crumbs('electrical', e['name'])}
  <span class="eyebrow">Electrical &middot; Estimates only</span>
  <h1>{e['name']}</h1>
  <p class="lead">{e['lead']}</p>
</header>

<div class="safety-strip" role="note" style="margin-top:22px">
  <strong>Estimates only.</strong> Electrical code varies by city, county, and state. Check your local code and use a licensed electrician for any wiring work.
</div>

<main class="calc-main">
  {sec}

  <article class="content-card">
    <h2>Common questions</h2>
      {faqs}
    <h2>Related calculators</h2>
    <div class="card-grid">{rel}</div>
    <p class="cat-more"><a href="advanced-tools.html">All electrical calculators &rarr;</a> &nbsp; <a href="index.html">All calculators &rarr;</a></p>
    <h2 id="electrical-disclaimer">Electrical calculator disclaimer</h2>
    {re.sub(r'<h2>.*?</h2>', '', ELEC_DISC, flags=re.S).strip()}
  </article>
</main>

''' + footer('Electrical results are estimates. Code varies by location, so check with your local building department and a licensed electrician.') + save_dialog('Name your project', 'e.g. Garage subpanel, storm prep', clear=False) + '''
<script src="electrical.js"></script>
</body>
</html>
'''
    wr(path, body)
for e in ELEC: elec_page(e)

# ------------------------------------------------------------------ math pages (lifted from the old page)
math_script = orig_math[orig_math.index('<script src="math-engine.js"></script>\n<script>') + len('<script src="math-engine.js"></script>\n<script>'):]
math_script = math_script[:math_script.index('</script>')]
math_script = must(math_script, "window.addEventListener('scroll',()=>{ const b=$('back-to-top'); if(window.scrollY>400)", "window.addEventListener('scroll',()=>{ const b=$('back-to-top'); if(!b) return; if(window.scrollY>400)")
wr('math-page.js', '/* CalcProject.org math calculators (page logic shared by each math calculator page; the math itself is in math-engine.js). */\n' + math_script)

def math_page(tid, slug, name, blurb, title, desc):
    path = slug + '.html'
    sec = re.search(r'(<section class="ticket" id="%s" data-tid="%s">.*?</section>)' % (tid, tid), orig_math, re.S).group(1)
    sec = sec.replace('<section class="ticket"', '<section class="ticket static"', 1).replace('<details class="formula-note">', '<details class="formula-note" open>')
    p = re.search(r'<div><h2>.*?</h2><p>(.*?)</p></div>', sec, re.S).group(1)
    sec = re.sub(r'<div><h2>.*?</h2><p>.*?</p></div>', '<div><h2>Enter your numbers</h2><p>Press Solve with steps to see the answer and how to get it.</p></div>', sec, count=1, flags=re.S)
    idx = [m[1] for m in MATH]
    i = idx.index(slug)
    others = [idx[(i + k) % len(idx)] for k in (1, 2, 3, 4)]
    rel = ''.join(card(s) for s in others)
    body = head(title, desc, path, [ld_app(name, desc, path), ld_crumbs('math', name, path)]) + NAV + f'''
<header class="page-head">
  {crumbs('math', name)}
  <span class="eyebrow">Math &middot; Every step shown</span>
  <h1>{name}</h1>
  <p class="lead">{p} Free, with the full step-by-step solution and no login.</p>
</header>

<main class="calc-main">
  {sec}

  <article class="content-card">
    <h2>More math calculators</h2>
    <div class="card-grid">{rel}</div>
    <p class="cat-more"><a href="math-tools.html#snap">Snap a photo of a problem &rarr;</a> &nbsp; <a href="math-tools.html">All math tools &rarr;</a> &nbsp; <a href="index.html">All calculators &rarr;</a></p>
    <p class="disclaimer">These calculators show the method as well as the answer, so you can learn the steps and check your own work. Answers are rounded to six decimal places. If a result ever looks wrong, tell us on the <a href="about.html">Contact page</a> with the numbers you entered.</p>
  </article>
</main>

''' + footer('Results are for learning and checking your work. Always double-check anything important.') + save_dialog('Name this sheet', 'e.g. Algebra homework, Chapter 4', clear=False) + '''
<script src="math-engine.js"></script>
<script src="math-page.js"></script>
</body>
</html>
'''
    wr(path, body)
for m in MATH: math_page(*m)

# ------------------------------------------------------------------ home page
OLD_ANCHORS = {'room-size': 'square-footage-calculator', 'paint': 'paint-calculator', 'flooring': 'flooring-calculator', 'tile': 'tile-calculator',
               'drywall': 'drywall-calculator', 'wallpaper': 'wallpaper-calculator', 'trim': 'baseboard-trim-calculator', 'mulch': 'mulch-calculator',
               'concrete': None, 'gravel': 'gravel-calculator', 'fence': 'fence-calculator', 'deck': 'deck-calculator', 'sod': 'sod-calculator',
               'roofing': 'roofing-calculator', 'siding': 'siding-calculator', 'advanced-tools': 'advanced-tools', 'math-tools': None}
# '#concrete' is now a category heading on the home page, so it is not redirected.
redirect = {k: v + '.html' for k, v in OLD_ANCHORS.items() if v}

def cat_cards(cat):
    return ''.join(card(s) for s, (n, b, ct) in PAGES.items() if ct == cat)
sections = ''
for k, n, blurb in CATS:
    extra = ''
    if k == 'math':
        extra = '<a class="calc-card" href="math-tools.html#snap"><strong>Snap a Problem</strong><span>Take a photo of a math problem and get the answer with steps.</span></a>'
    more = ''
    if k == 'electrical': more = '<p class="cat-more"><a href="advanced-tools.html">Electrical calculators and safety notes &rarr;</a></p>'
    if k == 'math': more = '<p class="cat-more"><a href="math-tools.html">All math tools on one page &rarr;</a></p>'
    sections += f'''
  <section class="cat" id="{k}" aria-labelledby="h-{k}">
    <div class="cat-head"><h2 id="h-{k}">{n}</h2><p>{blurb}</p></div>
    <div class="card-grid">{extra if k == 'math' else ''}{cat_cards(k)}</div>
    {more}
  </section>
'''
N_HOME = sum(1 for s, (n, b, ct) in PAGES.items() if ct in HOMECATS)
N_ALL = len(PAGES)
home_faq = [
 ('Are these calculators free?', 'Yes. Every calculator on CalcProject is free to use, with no account, no sign-up, and no app to install.'),
 ('How accurate are the estimates?', 'The math is exact for the numbers you enter. Real projects vary with product coverage, layout, and waste, so each calculator includes a waste allowance and you should always round up.'),
 ('Can I use metric units?', 'Yes. Every home project calculator has an Imperial and Metric switch. It converts your inputs and shows results in meters, square meters, liters, and kilograms.'),
 ('Can I save or print my results?', 'Yes. Tap Save or print results on any calculator. Every home project calculator you use in one visit goes onto a single sheet that you can print or save as a PDF on your phone.'),
]
home_ld = [
 {"@context": "https://schema.org", "@type": "WebSite", "name": "CalcProject", "url": BASE, "description": "Free online calculators for home improvement, money, math, science, and unit conversion."},
 {"@context": "https://schema.org", "@type": "Organization", "name": "CalcProject", "url": BASE, "logo": BASE + "logo-large.png"},
 {"@context": "https://schema.org", "@type": "ItemList", "name": "All calculators", "itemListElement": [
     {"@type": "ListItem", "position": i + 1, "name": plain(v[0]), "url": BASE + s + '.html'} for i, (s, v) in enumerate(PAGES.items())]},
 ld_faq(home_faq)]
jump = ''.join(f'<a href="#{k}">{n}</a>' for k, n, _ in CATS) + '<a href="guides.html">Guides</a>'
guide_cards = ''.join(f'<li><a href="{g}.html">{html.escape(t)}</a></li>' for g, t in list(GUIDES.items()))
HOME_LEAD = (f'{N_ALL} free calculators, each on its own page with the formula and a worked example. Start with {N_HOME} home improvement calculators for paint, flooring, concrete, and yard projects, then money, math, science, and unit converters.' if GENERAL else f'Measure once, calculate once, and buy the right amount. {N_ALL} free calculators for paint, flooring, concrete, yard, deck, and electrical projects, each on its own page with the formula and a worked example.')
home = head('Free Online Calculators for Home, Money & Math | CalcProject' if GENERAL else 'Free Home Improvement Calculators | CalcProject',
            (f'{N_ALL} free online calculators for home improvement, loans and savings, percent and fractions, geometry, statistics, and unit conversion. No sign-up.' if GENERAL else f'{N_HOME} free home improvement calculators: paint, flooring, tile, drywall, concrete, mulch, gravel, deck, fence, roofing, and more. No sign-up. Feet or meters.'),
            '', home_ld,
            '<script>(function(){var m=' + json.dumps(redirect) + ';function go(){var h=location.hash.slice(1);if(m[h])location.replace(m[h]);}go();window.addEventListener("hashchange",go);})();</script>\n') + NAV + f'''
<header class="home-head">
  <span class="eyebrow">Free &middot; No sign-up &middot; No app</span>
  <h1>{'Free Online' if GENERAL else 'Free Home Improvement'} <span>Calculators</span></h1>
  <p class="lead">{HOME_LEAD}</p>
  <div class="calc-search">
    <label for="calc-search">Find a calculator</label>
    <input type="search" id="calc-search" placeholder="{'Try paint, mortgage, percent, cm to inches...' if GENERAL else 'Try paint, concrete, mulch, stairs...'}" autocomplete="off">
  </div>
</header>

<div class="ruler" role="presentation"></div>

<main class="home-main">
  <nav class="jump" aria-label="Calculator categories">{jump}</nav>
  <p class="search-empty" id="search-empty" hidden>No calculator matches that yet. <a href="about.html">Tell us what you need</a> and we will look at adding it.</p>
{sections}
  <article class="content-card" style="margin-top:56px">
    <h2>How these calculators work</h2>
    <p>Each calculator takes the measurements you can get with a tape measure, such as length, width, height, or depth, and turns them into what the store sells: gallons, boxes, bags, sheets, boards, bundles, pallets, cubic yards, or tons. The formula and a worked example are shown on every page, so you can check the math yourself.</p>
    <p>Every home project calculator has an Imperial and Metric switch and a waste allowance for cuts, breakage, and mistakes. When you are done, tap <strong>Save or print results</strong>. Every calculator you use in one visit goes onto one clean sheet that you can print or save as a PDF to pull up at the store.</p>

    <h2>Project guides</h2>
    <p>Short write-ups on the questions that come up right before you buy materials.</p>
    <ul>{guide_cards}</ul>
    <p class="cat-more"><a href="guides.html">Browse all project guides &rarr;</a></p>

    <h2>Common questions</h2>
      {''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in home_faq)}
    <p class="disclaimer">{DISCLAIMER}</p>
  </article>
</main>

''' + footer('Free online calculators. No sign-up, no app.') + '''
<script>
(function(){
  var box=document.getElementById('calc-search'), empty=document.getElementById('search-empty');
  var cards=[].slice.call(document.querySelectorAll('.cat .calc-card')), cats=[].slice.call(document.querySelectorAll('.cat'));
  function run(){
    var q=box.value.trim().toLowerCase(), any=false;
    cards.forEach(function(c){ var hit=!q||c.textContent.toLowerCase().indexOf(q)>-1; c.hidden=!hit; if(hit) any=true; });
    cats.forEach(function(s){ s.hidden=!s.querySelector('.calc-card:not([hidden])'); });
    empty.hidden=any;
  }
  box.addEventListener('input',run);
})();
</script>
</body>
</html>
'''
wr('index.html', home)

# ------------------------------------------------------------------ electrical hub (old advanced-tools.html URL)
eredir = {e['tid']: e['slug'] + '.html' for e in ELEC}
hub = head('Electrical Calculators: Cost, Amps, Wire Size | CalcProject',
           'Free electrical calculators: electricity cost, watts to amps, circuit load, wire size and voltage drop, generator size, and air conditioner BTU.',
           'advanced-tools.html', [ld_crumbs('electrical', 'Electrical Calculators', 'advanced-tools.html')],
           '<script>(function(){var m=' + json.dumps(eredir) + ',h=location.hash.slice(1);if(m[h])location.replace(m[h]);})();</script>\n') + NAV + f'''
<header class="page-head">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; <span>Electrical Calculators</span></nav>
  <span class="eyebrow">Electrical &middot; Estimates only</span>
  <h1>Electrical Calculators</h1>
  <p class="lead">Free electrical calculators for planning a project, checking a circuit, or sizing a generator or air conditioner before you buy.</p>
</header>

<div class="safety-strip" role="note" style="margin-top:22px">
  <strong>Estimates only.</strong> Electrical code varies by city, county, and state. Check your local code and use a licensed electrician for any wiring work.
</div>

<main class="home-main">
  <section class="cat" style="margin-top:30px">
    <div class="card-grid">{cat_cards('electrical')}</div>
  </section>
  <section class="disclaimer-box" id="electrical-disclaimer">{ELEC_DISC}</section>
</main>

''' + footer('Electrical results are estimates. Code varies by location, so check with your local building department and a licensed electrician.') + '''</body>
</html>
'''
wr('advanced-tools.html', hub)

# ------------------------------------------------------------------ patch existing pages (guides, about, math hub)
def add_canonical(s, path):
    if 'rel="canonical"' in s: return s
    return re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + f'\n<link rel="canonical" href="{BASE}{path}">', s, count=1, flags=re.S)
for fn in sorted(os.listdir(ORIG)):
    if not fn.endswith('.html') or fn in ('index.html', 'advanced-tools.html') or fn.startswith('google'): continue
    s = rd(fn)
    s = add_canonical(s, fn)
    s = s.replace('<link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png">\n', '')   # this file never existed
    for old, new in OLD_ANCHORS.items():
        target = new or {'concrete': 'concrete-calculator', 'math-tools': 'math-tools'}[old]
        s = s.replace(f'href="index.html#{old}"', f'href="{target}.html"')
    if fn == 'math-tools.html':
        for tid, slug, name, *_ in MATH:
            a = f'<section class="ticket" id="{tid}" data-tid="{tid}">'
            assert a in s
        s = s.replace('<a href="advanced-tools.html">Electrical Tools</a>', '<a href="advanced-tools.html">Electrical</a>')
    if fn == 'about.html':
        a = 'CalcProject is a free set of calculators for home improvement projects — paint, flooring, tile, drywall, wallpaper, trim, mulch, concrete, gravel, fence, deck, sod, roofing, and siding — plus a handful of guides'
        assert a in s
        s = s.replace(a, f'CalcProject is a free set of {N_ALL} calculators, most of them for home improvement projects — paint, flooring, tile, drywall, concrete, pavers, mulch, topsoil, gravel, fence, deck, roofing, siding, and more — each on <a href="index.html">its own page</a> with the formula and a worked example, plus a handful of guides')
    wr(fn, s)

# ------------------------------------------------------------------ sitemap
urls = [''] + [s + '.html' for s in PAGES] + ['advanced-tools.html', 'math-tools.html', 'guides.html'] + [g + '.html' for g in GUIDES] + ['about.html', 'contact.html', 'privacy-policy.html']
seen2, out = set(), []
for u in urls:
    if u in seen2: continue
    seen2.add(u)
    assert u == '' or os.path.exists(os.path.join(REPO, u)), u
    out.append(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>')
wr('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(out) + '\n</urlset>\n')
print('pages:', len(PAGES), 'home-improvement+electrical:', N_HOME, 'sitemap urls:', len(out), 'guides:', len(GUIDES))
