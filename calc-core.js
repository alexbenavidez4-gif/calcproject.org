/* CalcProject.org shared math helpers and number formatting (no page code in this part). */
var CPCore = (function () {
  'use strict';
  // unit: [imperial label, metric label, multiply imperial by this to get metric]
  var U = {
    sqft: ['sq ft', 'm²', 0.09290304],
    sqyd: ['sq yd', 'm²', 0.83612736],
    ft: ['ft', 'm', 0.3048],
    inch: ['in', 'cm', 2.54],
    cuft: ['cu ft', 'L', 28.316846592],
    cuyd: ['cu yd', 'm³', 0.764554857984],
    gal: ['gal', 'L', 3.785411784],
    ton: ['tons', 'tonnes', 0.90718474],
    lb: ['lb', 'kg', 0.45359237],
    bf: ['board ft', 'm³', 0.002359737]
  };
  var ONE = { bags: 'bag', boxes: 'box', tiles: 'tile', sheets: 'sheet', rolls: 'roll', boards: 'board', panels: 'panel', pallets: 'pallet',
    bundles: 'bundle', blocks: 'block', bricks: 'brick', pavers: 'paver', bars: 'bar', studs: 'stud', packages: 'package', squares: 'square',
    pieces: 'piece', gallons: 'gallon', quarts: 'quart', steps: 'step', pickets: 'picket', screws: 'screw', sections: 'section', years: 'year',
    months: 'month', days: 'day', weeks: 'week', hours: 'hour', minutes: 'minute', payments: 'payment', people: 'person', cans: 'can', fixtures: 'fixture' };

  function fmt(n, d) {
    if (typeof n !== 'number' || !isFinite(n)) return '—';
    if (d === 'auto') {
      var a = Math.abs(n);
      if (a !== 0 && (a >= 1e12 || a < 1e-6)) return n.toExponential(4).replace('e+', ' × 10^').replace('e-', ' × 10^-');
      d = a >= 1000 ? 2 : a >= 1 ? 4 : 6;
      return n.toLocaleString('en-US', { maximumFractionDigits: d });
    }
    return n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  // Turn one result row [label, value, unit, decimals] into display text.
  function show(row, sys) {
    var val = row[1], unit = row[2], d = row[3] === undefined ? 0 : row[3];
    if (typeof val === 'string') return val;
    if (unit === '$') return (val < 0 ? '-$' : '$') + fmt(Math.abs(val), typeof row[3] === 'number' ? row[3] : 2);
    if (U[unit]) {
      var metric = sys === 'metric';
      var dd = Array.isArray(d) ? d[metric ? 1 : 0] : d;
      return fmt(metric ? val * U[unit][2] : val, dd) + ' ' + U[unit][metric ? 1 : 0];
    }
    if (val === 1 && ONE[unit]) unit = ONE[unit];
    return fmt(val, Array.isArray(d) ? d[0] : d) + (unit ? (unit === '%' || unit === 'x' || unit === '°' ? '' : ' ') + unit : '');
  }

  var H = {};
  H.nums = function (s) {
    return String(s == null ? '' : s).split(/[\s,;]+/).filter(function (p) { return p !== ''; }).map(Number).filter(function (n) { return isFinite(n); });
  };
  H.sum = function (a) { return a.reduce(function (x, y) { return x + y; }, 0); };
  H.mean = function (a) { return a.length ? H.sum(a) / a.length : 0; };
  H.variance = function (a, pop) {
    var n = a.length; if (n < (pop ? 1 : 2)) return 0;
    var m = H.mean(a);
    return H.sum(a.map(function (x) { return (x - m) * (x - m); })) / (pop ? n : n - 1);
  };
  H.sd = function (a, pop) { return Math.sqrt(H.variance(a, pop)); };
  H.sorted = function (a) { return a.slice().sort(function (x, y) { return x - y; }); };
  H.median = function (a) { var s = H.sorted(a), n = s.length; if (!n) return 0; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
  H.fact = function (n) { n = Math.floor(n); if (n < 0) return NaN; var r = 1; for (var i = 2; i <= n; i++) r *= i; return r; };
  H.comb = function (n, r) { n = Math.floor(n); r = Math.floor(r); if (r < 0 || r > n) return 0; r = Math.min(r, n - r); var c = 1; for (var i = 1; i <= r; i++) c = c * (n - r + i) / i; return Math.round(c); };
  H.perm = function (n, r) { n = Math.floor(n); r = Math.floor(r); if (r < 0 || r > n) return 0; var p = 1; for (var i = 0; i < r; i++) p *= (n - i); return p; };
  H.gcd = function (a, b) { a = Math.abs(Math.round(a)); b = Math.abs(Math.round(b)); while (b) { var t = a % b; a = b; b = t; } return a; };
  H.lcm = function (a, b) { var g = H.gcd(a, b); return g ? Math.abs(Math.round(a) * Math.round(b)) / g : 0; };
  H.isPrime = function (n) { n = Math.round(n); if (n < 2) return false; for (var i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; };
  H.factors = function (n) { n = Math.abs(Math.round(n)); var lo = [], hi = []; for (var i = 1; i * i <= n; i++) if (n % i === 0) { lo.push(i); if (i * i !== n) hi.unshift(n / i); } return lo.concat(hi); };
  H.primeFactors = function (n) { n = Math.abs(Math.round(n)); var out = []; for (var p = 2; p * p <= n; p++) while (n % p === 0) { out.push(p); n /= p; } if (n > 1) out.push(n); return out; };
  // decimal -> "n/d" in lowest terms
  H.frac = function (x, maxDen) {
    maxDen = maxDen || 10000;
    if (!isFinite(x)) return '—';
    var neg = x < 0; x = Math.abs(x);
    var whole = Math.floor(x), f = x - whole, bn = 0, bd = 1, be = 1;
    for (var d = 1; d <= maxDen; d++) { var n = Math.round(f * d), e = Math.abs(f - n / d); if (e < be - 1e-12) { be = e; bn = n; bd = d; if (e < 1e-10) break; } }
    var num = whole * bd + bn;
    return (neg ? '-' : '') + (bd === 1 ? String(num) : num + '/' + bd);
  };
  H.pmt = function (P, r, n) { if (n <= 0) return 0; return r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n)); };
  H.erf = function (x) {
    var s = x < 0 ? -1 : 1; x = Math.abs(x);
    var t = 1 / (1 + 0.3275911 * x);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  };
  H.ncdf = function (z) { return 0.5 * (1 + H.erf(z / Math.SQRT2)); };
  // date helpers ("YYYY-MM-DD"); an empty value means today
  H.date = function (s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || ''));
    if (m) return new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
    var n = new Date(); return new Date(Date.UTC(n.getFullYear(), n.getMonth(), n.getDate()));
  };
  H.days = function (a, b) { return Math.round((H.date(b) - H.date(a)) / 86400000); };
  H.fmtDate = function (d) { return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }); };
  H.addDays = function (s, n) { var d = H.date(s); d.setUTCDate(d.getUTCDate() + Math.round(n)); return d; };
  // full years, months, days between two dates
  H.ymd = function (a, b) {
    var d1 = H.date(a), d2 = H.date(b); if (d2 < d1) { var t = d1; d1 = d2; d2 = t; }
    var y = d2.getUTCFullYear() - d1.getUTCFullYear(), m = d2.getUTCMonth() - d1.getUTCMonth(), d = d2.getUTCDate() - d1.getUTCDate();
    if (d < 0) { m--; d += new Date(Date.UTC(d2.getUTCFullYear(), d2.getUTCMonth(), 0)).getUTCDate(); }
    if (m < 0) { y--; m += 12; }
    return [y, m, d];
  };
  // "HH:MM" -> minutes after midnight
  H.mins = function (s) { var m = /^(\d{1,2}):(\d{2})/.exec(String(s || '')); return m ? (+m[1]) * 60 + (+m[2]) : 0; };
  H.hm = function (mins) { mins = Math.round(mins); var neg = mins < 0; mins = Math.abs(mins); return (neg ? '-' : '') + Math.floor(mins / 60) + ' h ' + (mins % 60) + ' min'; };
  H.hms = function (sec) { sec = Math.round(sec); var h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60; return h + ':' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s; };
  H.ms = function (sec) { sec = Math.round(sec); return Math.floor(sec / 60) + ':' + (sec % 60 < 10 ? '0' : '') + (sec % 60); };
  H.clock = function (mins) { mins = ((Math.round(mins) % 1440) + 1440) % 1440; var h = Math.floor(mins / 60), m = mins % 60, ap = h < 12 ? 'AM' : 'PM'; return ((h + 11) % 12 + 1) + ':' + (m < 10 ? '0' : '') + m + ' ' + ap; };
  H.roman = function (n) {
    n = Math.round(n); if (n < 1 || n > 3999) return '—';
    var t = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']], o = '';
    t.forEach(function (p) { while (n >= p[0]) { o += p[1]; n -= p[0]; } });
    return o;
  };
  H.fromRoman = function (s) {
    var m = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 }, t = 0; s = String(s || '').toUpperCase().replace(/[^IVXLCDM]/g, '');
    for (var i = 0; i < s.length; i++) { var a = m[s[i]], b = m[s[i + 1]] || 0; t += a < b ? -a : a; }
    return t;
  };
  H.sci = function (x) { if (!isFinite(x) || x === 0) return '0'; var e = Math.floor(Math.log10(Math.abs(x))), m = x / Math.pow(10, e); return (Math.round(m * 1e6) / 1e6) + ' × 10^' + e; };
  H.fmtN = function (n) { return fmt(n, 'auto'); };
  H.list = function (a) { return a.length ? a.join(', ') : 'none'; };
  H.rad = function (deg) { return deg * Math.PI / 180; };
  H.deg = function (rad) { return rad * 180 / Math.PI; };
  return { U: U, ONE: ONE, fmt: fmt, show: show, H: H };
})();
if (typeof module !== 'undefined') module.exports = CPCore;
