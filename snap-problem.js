/* Snap a Problem: reads a photo (OCR in the browser) or typed text, works out what kind of
   problem it is, fills in the matching calculator and solves it. Photos never leave the device. */
(function (root) {
  'use strict';

  /* ------------------------------------------------------------------ text cleanup */
  function normalize(text, photo) {
    var notes = [];
    var s = String(text || '');
    s = s.replace(/[−–—‒]/g, '-')
         .replace(/[·•⋅]/g, '*')
         .replace(/÷/g, '/')
         .replace(/[‘’´`]/g, "'")
         .replace(/²/g, '^2').replace(/³/g, '^3').replace(/⁴/g, '^4')
         .replace(/√/g, 'sqrt');
    // a multiplication sign that sits where an "x" should be (OCR often does this)
    s = s.replace(/×(?=\s*(?:[+\-=)^]|$))/g, 'x').replace(/×/g, '*');
    s = s.replace(/[“”]/g, '"');
    s = s.toLowerCase();
    if (photo) {
      // photo readers often turn the little raised 2 in x^2 into a quote mark, a star or a question mark
      var before = s;
      s = s.replace(/x\s*["'\u201C\u201D`*]\s*([2-6])(?!\d)/g, 'x^$1');
      s = s.replace(/x\?(?=\s*(?:[-+=)]|\n|$))/g, 'x^2');
      if (s !== before) notes.push('The photo reader mixed up the small raised number, so I read it as a power like x^2. Please check it.');
    }
    // "x2" is usually x squared that lost its little 2
    if (/x[234](?![\d.])/.test(s)) {
      s = s.replace(/x([234])(?![\d.])/g, 'x^$1');
      notes.push('I read the small raised number as a power, like x^2.');
    }
    // lone capital X used as the variable is already handled by toLowerCase
    return { text: s, notes: notes };
  }

  /* ------------------------------------------------------------------ tiny polynomial parser */
  // A polynomial is an array of coefficients: p[0] + p[1] x + p[2] x^2 ...
  function clean(p) {
    var out = p.map(function (c) { return Math.abs(c) < 1e-12 ? 0 : Math.round(c * 1e9) / 1e9; });
    while (out.length > 1 && out[out.length - 1] === 0) out.pop();
    return out;
  }
  function add(a, b, sign) {
    var n = Math.max(a.length, b.length), r = [];
    for (var i = 0; i < n; i++) r[i] = (a[i] || 0) + sign * (b[i] || 0);
    return clean(r);
  }
  function mul(a, b) {
    var r = [];
    for (var i = 0; i < a.length; i++) for (var j = 0; j < b.length; j++) r[i + j] = (r[i + j] || 0) + a[i] * b[j];
    for (var k = 0; k < r.length; k++) if (r[k] === undefined) r[k] = 0;
    return clean(r);
  }
  function parsePoly(str) {
    var toks = [], re = /\s*(\d+\.?\d*|\.\d+|x|[+\-*\/^()])/y, m, pos = 0;
    str = str.replace(/\s+/g, ' ').trim();
    while (pos < str.length) {
      re.lastIndex = pos; m = re.exec(str);
      if (!m) return { error: 'I could not read "' + str.slice(pos, pos + 6).trim() + '".' };
      toks.push(m[1]); pos = re.lastIndex;
    }
    if (!toks.length) return { error: 'Nothing to read.' };
    var i = 0;
    function peek() { return toks[i]; }
    function isNum(t) { return t !== undefined && /^[\d.]/.test(t); }
    function expr() {
      var neg = false, t = peek();
      if (t === '+' || t === '-') { neg = (t === '-'); i++; }
      var v = term(); if (v.error) return v;
      if (neg) v = v.map(function (c) { return -c; });
      while (peek() === '+' || peek() === '-') {
        var op = toks[i++], w = term(); if (w.error) return w;
        v = add(v, w, op === '+' ? 1 : -1);
      }
      return v;
    }
    function term() {
      var v = power(); if (v.error) return v;
      for (;;) {
        var t = peek();
        if (t === '*') { i++; var w = power(); if (w.error) return w; v = mul(v, w); }
        else if (t === '/') {
          i++; var d = power(); if (d.error) return d;
          if (d.length !== 1 || d[0] === 0) return { error: 'I can only divide by a plain number (not by x).' };
          v = v.map(function (c) { return c / d[0]; }); v = clean(v);
        }
        else if (t === 'x' || t === '(') { var w2 = power(); if (w2.error) return w2; v = mul(v, w2); }
        else break;
      }
      return v;
    }
    function power() {
      var b = atom(); if (b.error) return b;
      if (peek() === '^') {
        i++; var neg = false;
        if (peek() === '-') { neg = true; i++; }
        var e = toks[i++];
        if (!isNum(e) || !/^\d+$/.test(e) || neg) return { error: 'Powers need to be whole numbers like x^2.' };
        e = parseInt(e, 10);
        if (e > 6) return { error: 'Keep powers at 6 or below.' };
        var r = [1]; for (var k = 0; k < e; k++) r = mul(r, b);
        return r;
      }
      return b;
    }
    function atom() {
      var t = toks[i++];
      if (t === undefined) return { error: 'The problem seems to stop too early.' };
      if (isNum(t)) { var n = parseFloat(t); return isNaN(n) ? { error: 'Could not read the number "' + t + '".' } : [n]; }
      if (t === 'x') return [0, 1];
      if (t === '(') { var v = expr(); if (v.error) return v; if (toks[i++] !== ')') return { error: 'A bracket is not closed.' }; return v; }
      return { error: 'I did not expect "' + t + '" there.' };
    }
    var res = expr();
    if (res.error) return res;
    if (i < toks.length) return { error: 'I did not understand "' + toks.slice(i).join(' ') + '".' };
    return { poly: res };
  }
  function fmtN(n) { return String(Math.round(n * 1e9) / 1e9); }
  // canonical string the calculators accept: 3x^4-2x^2+5x-7
  function polyString(p) {
    var out = '';
    for (var e = p.length - 1; e >= 0; e--) {
      var c = p[e]; if (c === 0) continue;
      var mag = Math.abs(c), body;
      if (e === 0) body = fmtN(mag);
      else body = (mag === 1 ? '' : fmtN(mag)) + 'x' + (e > 1 ? '^' + e : '');
      out += (out === '' ? (c < 0 ? '-' : '') : (c < 0 ? '-' : '+')) + body;
    }
    return out === '' ? '0' : out;
  }
  function polyPretty(p) { return polyString(p).replace(/([+\-])/g, function (m, g, off) { return off === 0 ? m : ' ' + m + ' '; }); }

  /* ------------------------------------------------------------------ pick the math out of the text */
  var MATH_RUN = /[0-9x+\-*\/^().=\s]{2,}/g;
  function bestRun(s, needEq) {
    var runs = s.match(MATH_RUN) || [], best = '';
    runs.forEach(function (r) {
      var t = r.trim();
      if (needEq && t.indexOf('=') < 0) return;
      if (!/[0-9x]/.test(t)) return;
      if (t.length > best.length) best = t;
    });
    // drop a leading problem number like "3." or "12)"
    best = best.replace(/^\(?\d{1,2}[.)]\s+/, '');
    return best.trim();
  }
  var NUM = '(-?\\d*\\.?\\d+)';

  function analyze(raw, opts) {
    var photo = !!(opts && opts.photo);
    var n = normalize(raw, photo), s = n.text.replace(/\s+/g, ' ').trim(), notes = n.notes.slice(), m;
    var res = analyzeCore(raw, s, n, notes, m, photo);
    res.shown = s;
    res.uncertain = looksUncertain(n.text);
    return res;
  }
  var VOCAB = /^(solve|find|the|derivative|differentiate|integral|integrate|antiderivative|of|what|is|percent|percentage|change|increase|decrease|from|to|for|and|dx|at|when|line|through|slope|points?|between|equation|simplify|evaluate|calculate|compute|answer|problem|number|quadratic|linear|out|if|sqrt|then|with|respect|value|determine|using|by|x|y)$/;
  function looksUncertain(t) {
    if (/[|"_~\[\]{}<>\\@#&$`]/.test(t)) return true;
    if (/\?(?!\s*(?:\n|$))/.test(t)) return true;
    var words = t.match(/[a-z]{2,}/g) || [], unknown = words.filter(function (w) { return !VOCAB.test(w); });
    return unknown.length >= 2;
  }
  function analyzeCore(raw, s, n, notes, m, photo) {
    if (!s) return { error: 'Type or snap a problem first.' };
    var hasX = /x/.test(s.replace(/\bexplain|exp|next|extra|exact|expand|box|six|maximum|fix|index/g, ''));

    // --- percent
    if ((m = s.match(new RegExp(NUM + '\\s*%\\s*of\\s*' + NUM)))) {
      return ok('percent', 'of', { x: +m[1], y: +m[2] }, 'Percentage Calculator', notes);
    }
    if ((m = s.match(new RegExp('what\\s*(?:percent|%)\\s*(?:is|of)\\s*' + NUM + '\\s*(?:of|out of)\\s*' + NUM))) ||
        (m = s.match(new RegExp(NUM + '\\s*is\\s*what\\s*(?:percent|%)\\s*of\\s*' + NUM)))) {
      return ok('percent', 'is', { x: +m[1], y: +m[2] }, 'Percentage Calculator', notes);
    }
    if (/%|percent/.test(s) && (m = s.match(new RegExp('from\\s*' + NUM + '\\s*to\\s*' + NUM)))) {
      return ok('percent', 'chg', { x: +m[1], y: +m[2] }, 'Percentage Calculator', notes);
    }

    // --- two points -> slope
    if ((m = s.match(new RegExp('\\(\\s*' + NUM + '\\s*,\\s*' + NUM + '\\s*\\)[^()]*?\\(\\s*' + NUM + '\\s*,\\s*' + NUM + '\\s*\\)')))) {
      return ok('slope', 'm', { x1: +m[1], y1: +m[2], x2: +m[3], y2: +m[4] }, 'Slope Calculator', notes);
    }

    // --- fractions
    if (!hasX && (m = s.match(/(-?\d+)\s*\/\s*(\d+)\s*([+\-*\/])\s*(-?\d+)\s*\/\s*(\d+)/))) {
      var op = { '+': 'add', '-': 'sub', '*': 'mul', '/': 'div' }[m[3]];
      return ok('fraction', 'f', { n1: +m[1], d1: +m[2], op: op, n2: +m[4], d2: +m[5] }, 'Fraction Calculator', notes);
    }

    // --- integral
    if (/∫|integra|antiderivative/.test(s)) {
      var lo = '', hi = '', t = s;
      if ((m = t.match(new RegExp('from\\s*' + NUM + '\\s*to\\s*' + NUM)))) { lo = +m[1]; hi = +m[2]; t = t.replace(m[0], ' '); }
      t = t.replace(/∫|integral of|integrate|antiderivative of|\bof\b|\bdx\b|f\s*\(\s*x\s*\)\s*=/g, ' ');
      var ex = bestRun(t, false);
      return withPoly('integral', 'i', ex, 'Integral Calculator', notes, { lo: lo, hi: hi });
    }

    // --- derivative
    if (/d\s*\/\s*dx|derivative|differentiat|f\s*'/.test(s)) {
      var at = '', u = s;
      if ((m = u.match(new RegExp('(?:at|when)\\s*x\\s*=\\s*' + NUM)))) { at = +m[1]; u = u.replace(m[0], ' '); }
      u = u.replace(/d\s*\/\s*dx|find the derivative of|derivative of|derivative|differentiate|f\s*'\s*\(\s*x\s*\)\s*=?|f\s*\(\s*x\s*\)\s*=|\by\s*=/g, ' ');
      var ex2 = bestRun(u, false);
      return withPoly('derivative', 'd', ex2, 'Derivative Calculator', notes, { at: at });
    }

    // --- equations in x
    if (hasX || /=/.test(s)) {
      var run = bestRun(s, true);
      var noEq = false;
      if (!run) { run = bestRun(s, false); noEq = true; }
      if (!run || !/x/.test(run)) return fail(notes);
      var sides, L, R;
      if (noEq) { sides = [run, '0']; notes.push('There was no equals sign, so I solved it as "= 0".'); }
      else {
        sides = run.split('=');
        if (sides.length !== 2 || !sides[0].trim() || !sides[1].trim()) return { error: 'I need exactly one equals sign with something on both sides.', text: run };
      }
      L = parsePoly(sides[0]); if (L.error) return { error: L.error, text: run };
      R = parsePoly(sides[1]); if (R.error) return { error: R.error, text: run };
      var p = add(L.poly, R.poly, -1), deg = p.length - 1;
      if (deg === 2) {
        var std = sides[1].trim() === '0' && L.poly.length === 3 && /^[^()]*$/.test(sides[0]);
        if (!std) notes.push('I moved everything to one side: ' + polyPretty(p) + ' = 0.');
        return ok('quadratic', 'q', { a: p[2], b: p[1], c: p[0] }, 'Quadratic Formula Calculator', notes, run);
      }
      if (deg === 1) {
        if (R.poly.length === 1 && L.poly.length === 2) {
          return ok('linear', 'l', { a: L.poly[1], b: L.poly[0], c: R.poly[0] }, 'Linear Equation Solver', notes, run);
        }
        notes.push('I moved everything to one side and combined like terms: ' + polyPretty(p) + ' = 0.');
        return ok('linear', 'l', { a: p[1], b: p[0], c: 0 }, 'Linear Equation Solver', notes, run);
      }
      if (deg <= 0) return { error: 'After simplifying, the x\'s cancel out, so there is nothing to solve for.', text: run };
      return { error: 'That one has x to the power ' + deg + '. I can solve equations up to x^2 (quadratics) for now.', text: run };
    }
    return fail(notes);
  }
  function ok(tid, mode, values, label, notes, text) { return { tid: tid, mode: mode, values: values, label: label, notes: notes || [], text: text || '' }; }
  function fail(notes) {
    return { error: 'I could not tell what kind of problem this is. I can solve: linear and quadratic equations, slope between two points, derivatives, integrals, percent problems, and fraction math. Try fixing the text, or pick a calculator below.', notes: notes };
  }
  function withPoly(tid, mode, ex, label, notes, extra) {
    if (!ex || !/[0-9x]/.test(ex)) return { error: 'I could not find the expression. Type it like 3x^4 - 2x^2 + 5x - 7.', notes: notes };
    var r = parsePoly(ex);
    if (r.error) return { error: r.error + ' Type it like 3x^4 - 2x^2 + 5x - 7.', text: ex, notes: notes };
    var str = polyString(r.poly), values = { poly: str };
    for (var k in extra) values[k] = extra[k];
    if (str.replace(/\s/g, '') !== ex.replace(/\s/g, '')) notes.push('I wrote your function as ' + polyPretty(r.poly) + '.');
    return ok(tid, mode, values, label, notes, ex);
  }

  var api = { normalize: normalize, parsePoly: parsePoly, polyString: polyString, analyze: analyze };
  root.SnapParse = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);

/* ====================================================================== page UI */
(function () {
  'use strict';
  if (typeof document === 'undefined') return;
  var P = window.SnapParse;
  var TESS_SRC = 'https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js';

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function track(name, params) { try { if (typeof gtag === 'function') gtag('event', name, params || {}); } catch (e) {} }

  /* ---- try the whole text, then line by line ---- */
  function analyzeText(text, opts) {
    var whole = P.analyze(String(text).replace(/\s*\n+\s*/g, ' '), opts);
    if (!whole.error) return whole;
    var lines = String(text).split(/\n+/).map(function (l) { return l.trim(); }).filter(Boolean);
    if (lines.length > 1) {
      for (var i = 0; i < lines.length; i++) {
        var r = P.analyze(lines[i], opts);
        if (!r.error) { r.notes = (r.notes || []).concat(['I found ' + lines.length + ' lines and solved this one: ' + lines[i]]); return r; }
      }
    }
    return whole;
  }

  /* ---- photo preparation: grey, then clean black-and-white so shadows do not fool the reader ---- */
  function loadBitmap(file) {
    if (window.createImageBitmap) {
      return createImageBitmap(file, { imageOrientation: 'from-image' }).catch(function () { return viaImg(file); });
    }
    return viaImg(file);
  }
  function viaImg(file) {
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), im = new Image();
      im.onload = function () { res(im); setTimeout(function () { URL.revokeObjectURL(url); }, 3000); };
      im.onerror = function () { rej(new Error('bad image')); };
      im.src = url;
    });
  }
  function prep(file) {
    return loadBitmap(file).then(function (bmp) {
      var w = bmp.width, h = bmp.height, big = Math.max(w, h), sc = Math.min(1, 1800 / big);
      if (big * sc < 1000) sc = 1000 / big;
      var cw = Math.round(w * sc), ch = Math.round(h * sc);
      var c = document.createElement('canvas'); c.width = cw; c.height = ch;
      var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cw, ch); g.drawImage(bmp, 0, 0, cw, ch);
      var img = g.getImageData(0, 0, cw, ch), d = img.data, n = cw * ch, gray = new Float32Array(n), i, p;
      for (i = 0, p = 0; p < n; p++, i += 4) gray[p] = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
      var W1 = cw + 1, ii = new Float64Array(W1 * (ch + 1)), x, y, row;
      for (y = 1; y <= ch; y++) {
        row = 0;
        for (x = 1; x <= cw; x++) { row += gray[(y - 1) * cw + (x - 1)]; ii[y * W1 + x] = ii[(y - 1) * W1 + x] + row; }
      }
      var r = Math.max(15, Math.round(cw / 30));
      for (y = 0; y < ch; y++) {
        var y0 = Math.max(0, y - r), y1 = Math.min(ch, y + r + 1);
        for (x = 0; x < cw; x++) {
          var x0 = Math.max(0, x - r), x1 = Math.min(cw, x + r + 1);
          var sum = ii[y1 * W1 + x1] - ii[y0 * W1 + x1] - ii[y1 * W1 + x0] + ii[y0 * W1 + x0];
          var mean = sum / ((x1 - x0) * (y1 - y0));
          var v = gray[y * cw + x] < mean * 0.86 ? 0 : 255, o = (y * cw + x) * 4;
          d[o] = d[o + 1] = d[o + 2] = v; d[o + 3] = 255;
        }
      }
      var gc = document.createElement('canvas'); gc.width = cw; gc.height = ch;
      gc.getContext('2d').drawImage(c, 0, 0);
      g.putImageData(img, 0, 0);
      return { bin: c, gray: gc };
    });
  }

  /* ---- the reader (Tesseract.js), downloaded only when someone actually uses a photo ---- */
  var workerP = null, onLog = null;
  function loadScript(src) {
    return new Promise(function (res, rej) {
      if (window.Tesseract) return res();
      var s = document.createElement('script'); s.src = src; s.async = true;
      s.onload = function () { res(); }; s.onerror = function () { rej(new Error('Could not download the reader.')); };
      document.head.appendChild(s);
    });
  }
  function getWorker() {
    if (workerP) return workerP;
    var o = window.SNAP_OCR || {};
    workerP = loadScript(o.src || TESS_SRC).then(function () {
      var opts = { logger: function (m) { if (onLog) onLog(m); } };
      ['workerPath', 'corePath', 'langPath', 'workerBlobURL', 'gzip'].forEach(function (k) { if (o[k] !== undefined) opts[k] = o[k]; });
      return window.Tesseract.createWorker('eng', 1, opts);
    }).then(function (w) {
      return w.setParameters({ tessedit_pageseg_mode: '6', preserve_interword_spaces: '1' }).then(function () { return w; });
    }).catch(function (e) { workerP = null; throw e; });
    return workerP;
  }

  window.SnapUI = { prep: prep, getWorker: getWorker };
  function init() {
    var box = document.getElementById('snap'); if (!box) return;
    var file = document.getElementById('snap-file'), prev = document.getElementById('snap-prev'),
        status = document.getElementById('snap-status'), bar = status.querySelector('.snap-bar span'), stText = status.querySelector('.snap-st'),
        text = document.getElementById('snap-text'), go = document.getElementById('snap-go'), msg = document.getElementById('snap-msg');
    var defaultMsg = msg.innerHTML;

    function setStatus(t, pct) {
      status.hidden = !t; stText.textContent = t || '';
      bar.style.width = (pct == null ? 0 : Math.max(0, Math.min(100, pct))) + '%';
      status.classList.toggle('busy', pct != null && pct < 100);
    }
    function showMsg(html) { msg.innerHTML = html; }

    function applyResult(a) {
      var t = document.getElementById(a.tid); if (!t) return;
      var sel = t.querySelector('.mode-sel');
      if (sel) sel.value = a.mode;
      if (typeof showMode === 'function') showMode(t);
      t.querySelectorAll('.field').forEach(function (f) {
        if (f.dataset.mode && f.dataset.mode !== a.mode) return;
        var el = f.querySelector('[data-f]'); if (!el) return;
        var v = a.values[el.dataset.f];
        if (v !== undefined) el.value = String(v);
      });
      t.classList.add('visible');
      if (typeof solve === 'function') solve(t);
      t.style.scrollMarginTop = '84px';
      setTimeout(function () { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60);
    }

    function runSolve(viaPhoto, pre) {
      var a = pre || analyzeText(text.value, { photo: !!viaPhoto });
      if (a.error) {
        track('snap_failed', { photo: !!viaPhoto });
        showMsg('<div class="label">Could not solve that yet</div><div class="err">' + esc(a.error) + '</div>' +
          '<p class="snap-small">Tip: fix the text in the box and tap Solve again. Use <code>^</code> for powers, like <code>x^2</code>.</p>');
        return;
      }
      applyResult(a);
      track('snap_solved', { type: a.tid, photo: !!viaPhoto });
      var vals = Object.keys(a.values).filter(function (k) { return a.values[k] !== ''; }).map(function (k) { return esc(k) + ' = ' + esc(a.values[k]); }).join(', ');
      showMsg('<div class="label">We solved it</div>' +
        (viaPhoto ? '<p class="snap-small">We read: <code>' + esc(a.shown || text.value) + '</code></p>' : '') +
        '<p class="snap-small"><strong>' + esc(a.label) + '</strong><br>We used: <code>' + esc(vals) + '</code></p>' +
        (a.notes && a.notes.length ? '<p class="snap-small">' + a.notes.map(esc).join('<br>') + '</p>' : '') +
        '<p class="snap-small">Your answer and every step are in the <strong>' + esc(a.label) + '</strong> just below. If this is not the problem you meant, fix the text and tap Solve again.</p>');
    }

    go.addEventListener('click', function () { runSolve(false); });
    text.addEventListener('keydown', function (e) { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); runSolve(false); } });

    file.addEventListener('change', function () {
      var f = file.files && file.files[0]; if (!f) return;
      if (!/^image\//.test(f.type)) { setStatus('That file is not a picture. Please choose a photo.', null); return; }
      track('snap_photo', {});
      try { prev.src = URL.createObjectURL(f); prev.hidden = false; } catch (e) {}
      showMsg(defaultMsg);
      setStatus('Getting your photo ready…', 3);
      prep(f).then(function (canv) {
        setStatus('Loading the reader… (first time only, about 10 MB)', 8);
        onLog = function (m) {
          if (m.status === 'recognizing text') setStatus('Reading your problem…', 50 + (m.progress || 0) * 45);
          else if (/loading|initializ/.test(m.status || '')) setStatus('Loading the reader… (first time only, about 10 MB)', 8 + (m.progress || 0) * 40);
        };
        return getWorker().then(function (w) {
          // read the picture a few different ways and keep the reading that makes the most sense
          var tries = [['gray', canv.gray, '6'], ['bin', canv.bin, '6'], ['gray', canv.gray, '7'], ['bin', canv.bin, '7']], best = null, chain = Promise.resolve();
          tries.forEach(function (t) {
            chain = chain.then(function () {
              return w.setParameters({ tessedit_pageseg_mode: t[2] }).then(function () { return w.recognize(t[1]); }).then(function (res) {
                var txt = (res && res.data && res.data.text || '').trim(); if (!txt) return;
                var a = analyzeText(txt, { photo: true });
                var score = (a.error ? 0 : 1000) - (a.uncertain ? 600 : 0) + (t[0] === 'gray' ? 40 : 0) + (res.data.confidence || 0) * 0.2;
                if (!best || score > best.score) best = { score: score, raw: txt, a: a };
              });
            });
          });
          return chain.then(function () { return best; });
        });
      }).then(function (best) {
        if (!best) { setStatus('We could not find any writing. Try a closer, brighter photo of just one problem.', null); showMsg(defaultMsg); return; }
        text.value = best.a.shown || best.raw;
        if (best.a.error) {
          setStatus('We read some text, but could not make sense of it. Fix it below and tap Solve.', null);
          runSolve(true, best.a);
        } else if (best.a.uncertain) {
          setStatus('Please check the text below. Some of it was hard to read.', null);
          showMsg('<div class="label">Check what we read</div><p class="snap-small">Some of the writing was hard to read. We did <strong>not</strong> solve it yet, so you do not get a wrong answer by mistake.</p><p class="snap-small">Fix anything that looks wrong in the box, then tap <strong>Solve this problem</strong>.</p>');
        } else {
          setStatus('Done. Check that the text below matches your problem.', 100);
          runSolve(true, best.a);
        }
      }).catch(function (e) {
        setStatus('Sorry, the photo reader could not start (' + (e && e.message ? e.message : 'unknown error') + '). You can type the problem in the box instead.', null);
        track('snap_error', {});
      });
      file.value = '';
    });
  }

  /* ---- "Add to home screen" (web app) ---- */
  function initInstall() {
    var bar = document.getElementById('snap-install'); if (!bar) return;
    var btn = document.getElementById('snap-install-btn'), help = document.getElementById('snap-install-help');
    var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
    if (standalone) { bar.hidden = true; return; }
    var ua = navigator.userAgent || '';
    var isIOS = /iphone|ipad|ipod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var isAndroid = /android/i.test(ua);
    var deferred = null;
    function steps(kind) {
      if (kind === 'ios') return '<strong>On iPhone or iPad:</strong><ol><li>Tap the <strong>Share</strong> button (the square with an arrow pointing up) in Safari.</li><li>Scroll down and tap <strong>Add to Home Screen</strong>.</li><li>Tap <strong>Add</strong>. The Snap Math icon now sits on your home screen.</li></ol>';
      return '<strong>On Android:</strong><ol><li>Tap the <strong>menu</strong> button (three dots) in your browser.</li><li>Tap <strong>Install app</strong> or <strong>Add to Home screen</strong>.</li><li>Tap <strong>Install</strong>. The Snap Math icon now sits on your home screen.</li></ol>';
    }
    window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; bar.hidden = false; });
    window.addEventListener('appinstalled', function () { bar.hidden = true; track('snap_installed', {}); });
    if (isIOS) bar.hidden = false;
    else if (isAndroid) setTimeout(function () { if (!deferred) bar.hidden = false; }, 1500);
    btn.addEventListener('click', function () {
      track('snap_install_click', { ios: isIOS });
      if (deferred) {
        deferred.prompt();
        deferred.userChoice.then(function (r) { track('snap_install_choice', { outcome: r && r.outcome }); deferred = null; if (r && r.outcome === 'accepted') bar.hidden = true; });
        return;
      }
      if (isIOS) { try { history.replaceState(null, '', location.pathname + '#snap'); } catch (e) {} }  // older iPhones save the address you are on
      help.innerHTML = steps(isIOS ? 'ios' : 'android'); help.hidden = false;
    });
    if ('serviceWorker' in navigator) {
      var reg = function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); };
      if (document.readyState === 'complete') reg(); else window.addEventListener('load', reg);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); initInstall(); }); else { init(); initInstall(); }
})();
