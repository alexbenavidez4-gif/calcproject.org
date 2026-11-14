# Compact definitions for the large set of calculators. Each X(...) call adds one calculator page.
import re, html
from defs import F

MCATS = [
    # key, name, home blurb, eyebrow, disclaimer
    ('finance', 'Loans, Savings &amp; Money', 'Payments, interest, savings growth, and everyday money math.', 'Money &middot; Estimates only',
     'These results are estimates for planning only and are not financial, tax, or legal advice. Rates, fees, and taxes vary, so confirm the numbers with your lender or a licensed professional before you decide.'),
    ('business', 'Business &amp; Pricing', 'Margin, markup, break-even, pay, and marketing numbers.', 'Business &middot; Estimates only',
     'These results are estimates for planning only and are not financial, tax, or legal advice. Check important figures with an accountant.'),
    ('percent', 'Percent, Fractions &amp; Numbers', 'Percent change, ratios, fractions, decimals, roots, and number tools.', 'Math &middot; Formula shown', 'Results are for learning and checking your work. Always double-check anything important.'),
    ('geometry', 'Geometry', 'Area, perimeter, volume, and surface area of common shapes.', 'Geometry &middot; Formula shown', 'Results are for learning and checking your work. Always double-check anything important.'),
    ('stats', 'Statistics &amp; Probability', 'Averages, spread, z-scores, probability, and sample size.', 'Statistics &middot; Formula shown', 'Results are for learning and checking your work. Always double-check anything important.'),
    ('physics', 'Physics &amp; Science', 'Motion, force, energy, electricity, and chemistry formulas.', 'Science &middot; Formula shown', 'Results are for learning and checking your work. They are not a substitute for engineering review.'),
    ('convert', 'Unit Converters', 'Length, weight, volume, temperature, area, speed, and more.', 'Converter &middot; Free', 'Conversions use standard exact or accepted factors and are rounded for display.'),
    ('time', 'Time &amp; Date', 'Ages, days between dates, hours worked, and time math.', 'Time &amp; date &middot; Free', 'Date math uses the calendar dates you enter and does not account for time zones or holidays unless stated.'),
    ('health', 'Health &amp; Fitness', 'BMI, calories, heart rate, pace, and strength estimates.', 'Health &middot; Estimates only',
     'These are general estimates from published formulas and are not medical advice. Talk with a doctor or registered dietitian before changing your diet, training, or medication.'),
    ('everyday', 'Everyday &amp; School', 'Grades, GPA, fuel, cooking, and other daily math.', 'Everyday &middot; Free', 'Results are estimates. Always double-check anything important.'),
]
M = []
_cat = [None]
def cat(k): _cat[0] = k

def parse_fields(spec):
    rows, cur = [], []
    for part in [p.strip() for p in spec.split(';') if p.strip()]:
        bits = [b.strip() for b in part.split('|')]
        k, label, d = bits[0], bits[1], bits[2] if len(bits) > 2 else ''
        kind = bits[3] if len(bits) > 3 else None
        hint = None
        m = re.match(r'^(.*?)\s*(\([^()]*\))$', label)
        if m and not kind in ('ft', 'in', 'sqft', 'cuft'):
            label, hint = m.group(1), m.group(2)
        f = F(k, label, d, None, hint, 'any')
        if kind and kind.startswith('sel:'):
            opts = []
            for o in kind[4:].split(','):
                val, txt = o.split('=', 1)
                opts.append((val.strip(), txt.strip()))
            f['opts'] = opts; f['d'] = str(d)
        elif kind in ('text', 'date', 'time'):
            f['type'] = kind
        elif kind:
            f['u'] = kind; f['step'] = None
        f['free'] = True
        wide = f.get('type') == 'text' or (f.get('opts') and max(len(t) for _, t in f['opts']) > 26)
        if wide:
            if cur: rows.append(cur); cur = []
            rows.append([f])
        else:
            cur.append(f)
            if len(cur) == 2: rows.append(cur); cur = []
    if cur: rows.append(cur)
    return rows

def X(slug, name, blurb, fields, js, formula, note='', units=None, cat_=None, label=None, table=None, example=None):
    if not re.search(r'(calculator|converter|solver|generator|roller|checker|flip)$', slug): slug += '-calculator'
    c = _cat[0] if cat_ is None else cat_
    short = re.sub(r'\s*(Calculator|Converter)$', '', name)
    M.append(dict(slug=slug, cat=c, id=re.sub(r'-(calculator|converter)$', '', slug), name=name, short=short, card=blurb, lead=blurb,
                  fields=parse_fields(fields), js=js, formula=formula, note=note, auto=True, example=example, units=units, label=label, table=table,
                  stamp=short if len(short) <= 22 else short[:20].rstrip() + '.', btn='Calculate'))

# ------------------------------------------------------------------ unit converters
# category: (title noun, base note, [(key, plural name, abbreviation, factor to base)])
UNITSETS = {
 'length': ('Length', [('mm', 'millimeters', 'mm', 0.001), ('cm', 'centimeters', 'cm', 0.01), ('m', 'meters', 'm', 1), ('km', 'kilometers', 'km', 1000),
            ('in', 'inches', 'in', 0.0254), ('ft', 'feet', 'ft', 0.3048), ('yd', 'yards', 'yd', 0.9144), ('mi', 'miles', 'mi', 1609.344), ('nmi', 'nautical miles', 'nmi', 1852)]),
 'area': ('Area', [('sqmm', 'square millimeters', 'mm&sup2;', 1e-6), ('sqcm', 'square centimeters', 'cm&sup2;', 1e-4), ('sqm', 'square meters', 'm&sup2;', 1), ('ha', 'hectares', 'ha', 1e4),
          ('sqkm', 'square kilometers', 'km&sup2;', 1e6), ('sqin', 'square inches', 'sq in', 0.00064516), ('sqft', 'square feet', 'sq ft', 0.09290304), ('sqyd', 'square yards', 'sq yd', 0.83612736),
          ('acre', 'acres', 'ac', 4046.8564224), ('sqmi', 'square miles', 'sq mi', 2589988.110336)]),
 'volume': ('Volume', [('ml', 'milliliters', 'mL', 0.001), ('l', 'liters', 'L', 1), ('m3', 'cubic meters', 'm&sup3;', 1000), ('tsp', 'teaspoons', 'tsp', 0.00492892159375),
            ('tbsp', 'tablespoons', 'tbsp', 0.01478676478125), ('floz', 'fluid ounces', 'fl oz', 0.0295735295625), ('cup', 'cups', 'cups', 0.2365882365), ('pt', 'pints', 'pt', 0.473176473),
            ('qt', 'quarts', 'qt', 0.946352946), ('gal', 'gallons', 'gal', 3.785411784), ('cuin', 'cubic inches', 'cu in', 0.016387064), ('cuft', 'cubic feet', 'cu ft', 28.316846592),
            ('cuyd', 'cubic yards', 'cu yd', 764.554857984)]),
 'weight': ('Weight', [('mg', 'milligrams', 'mg', 1e-6), ('g', 'grams', 'g', 0.001), ('kg', 'kilograms', 'kg', 1), ('t', 'metric tons', 't', 1000), ('oz', 'ounces', 'oz', 0.028349523125),
            ('lb', 'pounds', 'lb', 0.45359237), ('st', 'stone', 'st', 6.35029318), ('ton', 'US tons', 'tons', 907.18474)]),
 'speed': ('Speed', [('mps', 'meters per second', 'm/s', 1), ('kph', 'kilometers per hour', 'km/h', 1 / 3.6), ('mph', 'miles per hour', 'mph', 0.44704), ('fps', 'feet per second', 'ft/s', 0.3048),
           ('kn', 'knots', 'kn', 1852 / 3600)]),
 'pressure': ('Pressure', [('pa', 'pascals', 'Pa', 1), ('kpa', 'kilopascals', 'kPa', 1000), ('bar', 'bar', 'bar', 100000), ('psi', 'pounds per square inch', 'psi', 6894.757293168),
              ('atm', 'atmospheres', 'atm', 101325), ('mmhg', 'millimeters of mercury', 'mmHg', 133.322387415), ('inhg', 'inches of mercury', 'inHg', 3386.389)]),
 'energy': ('Energy', [('j', 'joules', 'J', 1), ('kj', 'kilojoules', 'kJ', 1000), ('cal', 'calories', 'cal', 4.184), ('kcal', 'kilocalories', 'kcal', 4184), ('wh', 'watt-hours', 'Wh', 3600),
            ('kwh', 'kilowatt-hours', 'kWh', 3.6e6), ('btu', 'BTU', 'BTU', 1055.05585262), ('ftlb', 'foot-pounds', 'ft-lb', 1.3558179483)]),
 'power': ('Power', [('w', 'watts', 'W', 1), ('kw', 'kilowatts', 'kW', 1000), ('hp', 'horsepower', 'hp', 745.6998715823), ('btuh', 'BTU per hour', 'BTU/hr', 0.29307107),
           ('tr', 'tons of refrigeration', 'tons', 3516.8528)]),
 'time': ('Time', [('ms', 'milliseconds', 'ms', 0.001), ('s', 'seconds', 's', 1), ('min', 'minutes', 'min', 60), ('hr', 'hours', 'hr', 3600), ('day', 'days', 'days', 86400),
          ('wk', 'weeks', 'weeks', 604800), ('yr', 'years', 'years', 31536000)]),
 'data': ('Data Storage', [('bit', 'bits', 'bits', 0.125), ('b', 'bytes', 'B', 1), ('kb', 'kilobytes', 'KB', 1024), ('mb', 'megabytes', 'MB', 1048576), ('gb', 'gigabytes', 'GB', 1073741824),
          ('tb', 'terabytes', 'TB', 1099511627776)]),
 'angle': ('Angle', [('deg', 'degrees', '&deg;', 1), ('rad', 'radians', 'rad', 57.29577951308232), ('grad', 'gradians', 'grad', 0.9), ('rev', 'revolutions', 'rev', 360)]),
 'force': ('Force', [('n', 'newtons', 'N', 1), ('kn', 'kilonewtons', 'kN', 1000), ('lbf', 'pounds-force', 'lbf', 4.4482216152605), ('kgf', 'kilograms-force', 'kgf', 9.80665)]),
 'torque': ('Torque', [('nm', 'newton-meters', 'N&middot;m', 1), ('ftlb', 'foot-pounds', 'ft-lb', 1.3558179483), ('inlb', 'inch-pounds', 'in-lb', 0.112984829)]),
 'density': ('Density', [('kgm3', 'kilograms per cubic meter', 'kg/m&sup3;', 1), ('gcm3', 'grams per cubic centimeter', 'g/cm&sup3;', 1000), ('lbft3', 'pounds per cubic foot', 'lb/ft&sup3;', 16.01846337),
             ('lbgal', 'pounds per gallon', 'lb/gal', 119.826427)]),
 'flow': ('Flow Rate', [('lpm', 'liters per minute', 'L/min', 1), ('gpm', 'gallons per minute', 'gpm', 3.785411784), ('m3h', 'cubic meters per hour', 'm&sup3;/h', 1000 / 60),
          ('cfm', 'cubic feet per minute', 'cfm', 28.316846592)]),
 'frequency': ('Frequency', [('hz', 'hertz', 'Hz', 1), ('khz', 'kilohertz', 'kHz', 1e3), ('mhz', 'megahertz', 'MHz', 1e6), ('ghz', 'gigahertz', 'GHz', 1e9), ('rpm', 'revolutions per minute', 'rpm', 1 / 60)]),
 'cooking': ('Cooking Measurement', [('tsp', 'teaspoons', 'tsp', 4.92892159375), ('tbsp', 'tablespoons', 'tbsp', 14.78676478125), ('floz', 'fluid ounces', 'fl oz', 29.5735295625), ('cup', 'cups', 'cups', 236.5882365),
             ('pt', 'pints', 'pt', 473.176473), ('qt', 'quarts', 'qt', 946.352946), ('ml', 'milliliters', 'mL', 1), ('l', 'liters', 'L', 1000)]),
}
def unitrow(setk, key):
    return next(u for u in UNITSETS[setk][1] if u[0] == key)
def P(s): return html.unescape(s)

def make_converters():
    cat('convert')
    for setk, (noun, units) in UNITSETS.items():
        opts = ','.join(f'{k}={n[0].upper() + n[1:]}' for k, n, a, f in units)
        tbl = '{' + ','.join(f'{k}:[{f!r},{P(a)!r}]' for k, n, a, f in units) + '}'
        d1, d2 = units[0][0], units[1][0]
        pick = {'length': ('ft', 'm'), 'area': ('sqft', 'sqm'), 'volume': ('gal', 'l'), 'weight': ('lb', 'kg'), 'speed': ('mph', 'kph'), 'pressure': ('psi', 'bar'), 'energy': ('kwh', 'btu'),
                'power': ('hp', 'kw'), 'time': ('hr', 'min'), 'data': ('gb', 'mb'), 'angle': ('deg', 'rad'), 'force': ('lbf', 'n'), 'torque': ('ftlb', 'nm'), 'density': ('lbft3', 'kgm3'),
                'flow': ('gpm', 'lpm'), 'frequency': ('rpm', 'hz'), 'cooking': ('cup', 'ml')}[setk]
        js = f"""var T={tbl},a=T[v.from],b=T[v.to],x=v.value*a[0]/b[0];
var rows=Object.keys(T).filter(function(k){{return k!==v.from&&k!==v.to;}}).slice(0,6).map(function(k){{return ['In '+T[k][1],v.value*a[0]/T[k][0],'','auto'];}});
return R(rows,[H.fmtN(v.value)+' '+a[1]+' =',x,b[1],'auto']);"""
        names = ', '.join(n for k, n, a, f in units[:6])
        X(f'{setk.replace("data", "data-storage").replace("flow", "flow-rate").replace("cooking", "cooking-measurement")}-converter', f'{noun} Converter',
          f'Convert between {names}, and more.', f'value|Value|1;from|From|{pick[0]}|sel:{opts};to|To|{pick[1]}|sel:{opts}', js,
          f'Each unit is turned into a common base unit, then into the unit you want: result = value &times; (factor of the starting unit) &divide; (factor of the target unit).',
          'Pick the unit you have under From and the unit you want under To. The other common units are listed above the answer.', label='Conversion')
    # temperature
    X('temperature-converter', 'Temperature Converter', 'Convert between Fahrenheit, Celsius, and Kelvin.',
      'value|Temperature|72;from|From|f|sel:f=Fahrenheit,c=Celsius,k=Kelvin;to|To|c|sel:f=Fahrenheit,c=Celsius,k=Kelvin',
      """var c=v.from==='f'?(v.value-32)*5/9:v.from==='k'?v.value-273.15:v.value,o={f:c*9/5+32,c:c,k:c+273.15},n={f:'\\u00b0F',c:'\\u00b0C',k:'K'};
return R([['Fahrenheit',o.f,'\\u00b0F',2],['Celsius',o.c,'\\u00b0C',2],['Kelvin',o.k,'K',2]],[H.fmtN(v.value)+' '+n[v.from]+' =',o[v.to],n[v.to],2]);""",
      '&deg;C = (&deg;F &minus; 32) &times; 5 &divide; 9. &deg;F = &deg;C &times; 9 &divide; 5 + 32. K = &deg;C + 273.15.', 'Water freezes at 32 &deg;F (0 &deg;C) and boils at 212 &deg;F (100 &deg;C) at sea level.', label='Conversion')
    X('fuel-economy-converter', 'Fuel Economy Converter', 'Convert between miles per gallon, liters per 100 km, and km per liter.',
      'value|Fuel economy|30;from|From|mpg|sel:mpg=Miles per gallon (US),l100=Liters per 100 km,kml=Kilometers per liter',
      """var mpg=v.from==='mpg'?v.value:v.from==='l100'?235.214583/v.value:v.value*2.352145833;
return R([['Miles per gallon (US)',mpg,'mpg',2],['Kilometers per liter',mpg/2.352145833,'km/L',2],['Miles per gallon (UK)',mpg*1.200949925,'mpg',2]],['Liters per 100 km',235.214583/mpg,'L/100 km',2]);""",
      'L/100 km = 235.215 &divide; mpg (US). km/L = mpg &divide; 2.352. A UK gallon is larger, so UK mpg = US mpg &times; 1.201.', 'Lower L/100 km means better fuel economy, while higher mpg means better fuel economy.', label='Conversion')
    pairs = [('length', 'cm', 'in'), ('length', 'in', 'cm'), ('length', 'ft', 'm'), ('length', 'm', 'ft'), ('length', 'mm', 'in'), ('length', 'in', 'mm'), ('length', 'km', 'mi'), ('length', 'mi', 'km'),
             ('length', 'yd', 'm'), ('length', 'm', 'yd'), ('length', 'in', 'ft'), ('length', 'ft', 'in'), ('length', 'cm', 'ft'), ('length', 'ft', 'yd'), ('length', 'mi', 'ft'),
             ('weight', 'kg', 'lb'), ('weight', 'lb', 'kg'), ('weight', 'g', 'oz'), ('weight', 'oz', 'g'), ('weight', 'lb', 'oz'), ('weight', 'oz', 'lb'), ('weight', 'st', 'lb'), ('weight', 'kg', 'st'),
             ('weight', 'ton', 'lb'), ('weight', 'g', 'kg'),
             ('volume', 'l', 'gal'), ('volume', 'gal', 'l'), ('volume', 'ml', 'floz'), ('volume', 'floz', 'ml'), ('volume', 'cup', 'ml'), ('volume', 'ml', 'cup'), ('volume', 'tbsp', 'ml'), ('volume', 'tsp', 'ml'),
             ('volume', 'cup', 'floz'), ('volume', 'qt', 'l'), ('volume', 'cuft', 'gal'), ('volume', 'cuyd', 'cuft'), ('volume', 'gal', 'qt'), ('volume', 'tbsp', 'tsp'), ('volume', 'cup', 'tbsp'),
             ('area', 'sqft', 'sqm'), ('area', 'sqm', 'sqft'), ('area', 'acre', 'sqft'), ('area', 'sqft', 'acre'), ('area', 'ha', 'acre'), ('area', 'acre', 'ha'), ('area', 'sqft', 'sqyd'), ('area', 'sqin', 'sqft'),
             ('speed', 'mph', 'kph'), ('speed', 'kph', 'mph'), ('speed', 'kn', 'mph'), ('speed', 'mps', 'mph'),
             ('pressure', 'psi', 'bar'), ('pressure', 'bar', 'psi'), ('pressure', 'psi', 'kpa'),
             ('power', 'kw', 'hp'), ('power', 'hp', 'kw'), ('power', 'w', 'btuh'), ('energy', 'kwh', 'btu'), ('energy', 'kcal', 'kj'),
             ('time', 'hr', 'min'), ('time', 'min', 'hr'), ('time', 'day', 'hr'), ('time', 'min', 's'), ('time', 'wk', 'day'),
             ('data', 'mb', 'gb'), ('data', 'gb', 'mb'), ('data', 'gb', 'tb')]
    short = {'in': 'Inches', 'ft': 'Feet', 'cm': 'CM', 'mm': 'MM', 'm': 'Meters', 'km': 'KM', 'mi': 'Miles', 'yd': 'Yards', 'kg': 'KG', 'lb': 'Pounds', 'g': 'Grams', 'oz': 'Ounces', 'st': 'Stone',
             'ton': 'Tons', 'l': 'Liters', 'gal': 'Gallons', 'ml': 'mL', 'floz': 'Fluid Ounces', 'cup': 'Cups', 'tbsp': 'Tablespoons', 'tsp': 'Teaspoons', 'qt': 'Quarts', 'cuft': 'Cubic Feet',
             'cuyd': 'Cubic Yards', 'sqft': 'Square Feet', 'sqm': 'Square Meters', 'acre': 'Acres', 'ha': 'Hectares', 'sqyd': 'Square Yards', 'sqin': 'Square Inches', 'mph': 'MPH', 'kph': 'KM/H',
             'kn': 'Knots', 'mps': 'Meters per Second', 'psi': 'PSI', 'bar': 'Bar', 'kpa': 'kPa', 'kw': 'kW', 'hp': 'Horsepower', 'w': 'Watts', 'btuh': 'BTU per Hour', 'kwh': 'kWh', 'btu': 'BTU',
             'kcal': 'Calories (kcal)', 'kj': 'Kilojoules', 'hr': 'Hours', 'min': 'Minutes', 'day': 'Days', 's': 'Seconds', 'wk': 'Weeks', 'mb': 'MB', 'gb': 'GB', 'tb': 'TB'}
    for setk, a, b in pairs:
        ua, ub = unitrow(setk, a), unitrow(setk, b)
        k = ua[3] / ub[3]
        slug = f'{ua[1].replace(" ", "-")}-to-{ub[1].replace(" ", "-")}-converter'
        name = f'{short[a]} to {short[b]} Converter'
        ks = f'{k:.10g}'
        X(slug, name, f'Convert {ua[1]} to {ub[1]}.', f'value|{ua[1][0].upper() + ua[1][1:]}|{ {"mb": 500, "min": 90, "hr": 2, "s": 90}.get(a, 10) }',
          f"""var k={k!r};return R([['1 {P(ua[2])} equals',k,{P(ub[2])!r},'auto'],['1 {P(ub[2])} equals',1/k,{P(ua[2])!r},'auto']],[H.fmtN(v.value)+' {P(ua[2])} =',v.value*k,{P(ub[2])!r},'auto']);""",
          f'{ub[1][0].upper() + ub[1][1:]} = {ua[1]} &times; {ks}. One {ua[1].rstrip("s") if ua[1] not in ("feet", "inches", "stone", "bar", "BTU") else {"feet": "foot", "inches": "inch", "stone": "stone", "bar": "bar", "BTU": "BTU"}[ua[1]]} equals {ks} {ub[1]}.',
          f'To go the other way, divide by {ks} or use the <a href="{setk.replace("data", "data-storage")}-converter.html">{UNITSETS[setk][0].lower()} converter</a>.', label='Conversion',
          table=(P(ua[2]), P(ub[2]), k, [1, 2, 5, 10, 20, 25, 50, 75, 100, 250, 500, 1000]))
    # temperature pairs
    for a, b, an, bn, f, expr, defv in [('f', 'c', 'Fahrenheit', 'Celsius', '&deg;C = (&deg;F &minus; 32) &times; 5 &divide; 9', '(v.value-32)*5/9', 72),
                                        ('c', 'f', 'Celsius', 'Fahrenheit', '&deg;F = &deg;C &times; 9 &divide; 5 + 32', 'v.value*9/5+32', 20),
                                        ('c', 'k', 'Celsius', 'Kelvin', 'K = &deg;C + 273.15', 'v.value+273.15', 25)]:
        sym = {'f': '\\u00b0F', 'c': '\\u00b0C', 'k': 'K'}
        X(f'{an.lower()}-to-{bn.lower()}-converter', f'{an} to {bn} Converter', f'Convert degrees {an} to {bn}.', f'value|Degrees {an}|{defv}',
          f"return R([],[H.fmtN(v.value)+' {sym[a]} =',{expr},'{sym[b]}',2]);", f + '.', 'See the <a href="temperature-converter.html">temperature converter</a> for all three scales.', label='Conversion')
