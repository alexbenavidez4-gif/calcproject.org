/* ShowWork Math - calculation engine.
   Every function takes an object of values and returns either
   { error: "message" } or { answers: [{label, value}], steps: ["..."] }. */
(function (root) {
  'use strict';

  function isNum(x) { return typeof x === 'number' && isFinite(x); }
  function fmt(n) {
    if (!isNum(n)) return String(n);
    var r = Number(n.toFixed(6));
    if (r === 0) r = 0; // turns -0 into 0
    return String(r);
  }
  function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { var t = a % b; a = b; b = t; }
    return a;
  }
  function err(m) { return { error: m }; }
  function par(n) { return n < 0 ? '(' + n + ')' : String(n); }
  function coefX(a) {
    if (a === 1) return 'x';
    if (a === -1) return '-x';
    return fmt(a) + 'x';
  }
  function frac(n, d) {
    var g = gcd(n, d); n /= g; d /= g;
    if (d < 0) { n = -n; d = -d; }
    return d === 1 ? String(n) : n + '/' + d;
  }
  function parseList(str) {
    if (typeof str !== 'string') return null;
    var parts = str.split(/[\s,;]+/).filter(function (p) { return p !== ''; });
    if (!parts.length) return null;
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var n = Number(parts[i]);
      if (!isFinite(n)) return null;
      out.push(n);
    }
    return out;
  }

  /* ---------- Percentages ---------- */
  function percentOf(v) {
    if (!isNum(v.x) || !isNum(v.y)) return err('Enter both numbers.');
    var dec = v.x / 100, ans = dec * v.y;
    return {
      answers: [{ label: fmt(v.x) + '% of ' + fmt(v.y) + ' =', value: fmt(ans) }],
      steps: [
        'Turn the percent into a decimal by dividing by 100: ' + fmt(v.x) + ' ÷ 100 = ' + fmt(dec) + '.',
        'Multiply the decimal by ' + fmt(v.y) + ': ' + fmt(dec) + ' × ' + fmt(v.y) + ' = ' + fmt(ans) + '.'
      ]
    };
  }
  function percentIs(v) {
    if (!isNum(v.x) || !isNum(v.y)) return err('Enter both numbers.');
    if (v.y === 0) return err('The "out of" number cannot be 0.');
    var ratio = v.x / v.y, ans = ratio * 100;
    return {
      answers: [{ label: fmt(v.x) + ' is what % of ' + fmt(v.y) + '?', value: fmt(ans) + '%' }],
      steps: [
        'Divide the part by the whole: ' + fmt(v.x) + ' ÷ ' + fmt(v.y) + ' = ' + fmt(ratio) + '.',
        'Multiply by 100 to turn it into a percent: ' + fmt(ratio) + ' × 100 = ' + fmt(ans) + '%.'
      ]
    };
  }
  function percentChange(v) {
    if (!isNum(v.x) || !isNum(v.y)) return err('Enter both numbers.');
    if (v.x === 0) return err('The old value cannot be 0 (you cannot measure a percent change from zero).');
    var diff = v.y - v.x, ratio = diff / Math.abs(v.x), pct = ratio * 100;
    var word = pct > 0 ? 'increase' : (pct < 0 ? 'decrease' : 'change');
    return {
      answers: [{ label: 'Percent ' + word + ':', value: fmt(Math.abs(pct)) + '%' + (pct === 0 ? '' : (pct > 0 ? ' up' : ' down')) }],
      steps: [
        'Find the difference: new − old = ' + fmt(v.y) + ' − ' + par(Number(fmt(v.x))) + ' = ' + fmt(diff) + '.',
        'Divide by the old value: ' + fmt(diff) + ' ÷ ' + fmt(Math.abs(v.x)) + ' = ' + fmt(ratio) + '.',
        'Multiply by 100: ' + fmt(ratio) + ' × 100 = ' + fmt(pct) + '%.',
        pct > 0 ? 'The value went up by ' + fmt(pct) + '%.' : (pct < 0 ? 'The value went down by ' + fmt(-pct) + '%.' : 'The value did not change.')
      ]
    };
  }

  /* ---------- Fractions ---------- */
  function fraction(v) {
    var n1 = v.n1, d1 = v.d1, n2 = v.n2, d2 = v.d2, op = v.op;
    var w1 = isNum(v.w1) ? v.w1 : 0, w2 = isNum(v.w2) ? v.w2 : 0;
    var all = [n1, d1, n2, d2, w1, w2];
    for (var i = 0; i < 6; i++) {
      if (!isNum(all[i]) || !Number.isInteger(all[i])) return err('Use whole numbers for the whole parts, tops and bottoms.');
    }
    if (d1 === 0 || d2 === 0) return err('A denominator (the bottom number) cannot be 0.');
    if (d1 < 0) { n1 = -n1; d1 = -d1; }
    if (d2 < 0) { n2 = -n2; d2 = -d2; }
    var steps = [];
    if (w1 !== 0) {
      if (n1 < 0) return err('For a mixed number, put the minus sign on the whole number and keep the top positive.');
      var m1 = (w1 < 0 ? -1 : 1) * (Math.abs(w1) * d1 + n1);
      steps.push('Turn the mixed number ' + w1 + ' ' + n1 + '/' + d1 + ' into an improper fraction: ' + (w1 < 0 ? '−' : '') + '(' + Math.abs(w1) + ' × ' + d1 + ' + ' + n1 + ') ÷ ' + d1 + ' = ' + m1 + '/' + d1 + '.');
      n1 = m1;
    }
    if (w2 !== 0) {
      if (n2 < 0) return err('For a mixed number, put the minus sign on the whole number and keep the top positive.');
      var m2 = (w2 < 0 ? -1 : 1) * (Math.abs(w2) * d2 + n2);
      steps.push('Turn the mixed number ' + w2 + ' ' + n2 + '/' + d2 + ' into an improper fraction: ' + (w2 < 0 ? '−' : '') + '(' + Math.abs(w2) + ' × ' + d2 + ' + ' + n2 + ') ÷ ' + d2 + ' = ' + m2 + '/' + d2 + '.');
      n2 = m2;
    }
    var f1 = n1 + '/' + d1, f2 = n2 + '/' + d2, rn, rd;

    if (op === 'add' || op === 'sub') {
      var L = d1 / gcd(d1, d2) * d2, a = n1 * (L / d1), b = n2 * (L / d2);
      steps.push('Find a common denominator: the least common multiple of ' + d1 + ' and ' + d2 + ' is ' + L + '.');
      steps.push('Rewrite each fraction over ' + L + ': ' + f1 + ' = ' + a + '/' + L + ' and ' + f2 + ' = ' + b + '/' + L + '.');
      rn = op === 'add' ? a + b : a - b; rd = L;
      steps.push((op === 'add' ? 'Add' : 'Subtract') + ' the tops and keep the bottom: ' + a + (op === 'add' ? ' + ' : ' − ') + par(b) + ' = ' + rn + ', so the result is ' + rn + '/' + rd + '.');
    } else if (op === 'mul') {
      rn = n1 * n2; rd = d1 * d2;
      steps.push('Multiply the tops: ' + n1 + ' × ' + par(n2) + ' = ' + rn + '.');
      steps.push('Multiply the bottoms: ' + d1 + ' × ' + d2 + ' = ' + rd + '.');
    } else if (op === 'div') {
      if (n2 === 0) return err('You cannot divide by a fraction whose top is 0.');
      steps.push('Dividing by a fraction means multiplying by its reciprocal (flip it): ' + f1 + ' ÷ ' + f2 + ' = ' + f1 + ' × ' + d2 + '/' + n2 + '.');
      rn = n1 * d2; rd = d1 * n2;
      if (rd < 0) { rn = -rn; rd = -rd; }
      steps.push('Multiply across: ' + n1 + ' × ' + d2 + ' = ' + rn + ' on top and ' + d1 + ' × ' + Math.abs(n2) + ' = ' + rd + ' on the bottom.');
    } else {
      return err('Pick an operation.');
    }

    var sn, sd;
    if (rn === 0) {
      sn = 0; sd = 1;
      steps.push('The top is 0, so the answer is 0.');
    } else {
      var g = gcd(rn, rd);
      sn = rn / g; sd = rd / g;
      if (g > 1) steps.push('Simplify: the greatest common factor of ' + Math.abs(rn) + ' and ' + rd + ' is ' + g + ', so divide the top and bottom by ' + g + ' to get ' + sn + '/' + sd + '.');
      else steps.push(rn + '/' + rd + ' is already in lowest terms.');
    }
    var answers = [{ label: 'Answer:', value: sd === 1 ? String(sn) : sn + '/' + sd }];
    if (sd !== 1 && Math.abs(sn) > sd) {
      var whole = Math.trunc(sn / sd), rem = Math.abs(sn) % sd;
      answers.push({ label: 'Mixed number:', value: whole + ' ' + rem + '/' + sd });
      steps.push('As a mixed number: ' + Math.abs(sn) + ' ÷ ' + sd + ' = ' + Math.abs(whole) + ' remainder ' + rem + ', so ' + whole + ' ' + rem + '/' + sd + '.');
    }
    if (sd !== 1) answers.push({ label: 'Decimal:', value: fmt(sn / sd) });
    return { answers: answers, steps: steps };
  }

  /* ---------- Linear equation ---------- */
  function linear(v) {
    if (!isNum(v.a) || !isNum(v.b) || !isNum(v.c)) return err('Enter a, b and c.');
    if (v.a === 0) return err('"a" cannot be 0. If a is 0 there is no x left to solve for.');
    var a = v.a, b = v.b, c = v.c;
    var eq = coefX(a) + (b < 0 ? ' - ' + fmt(-b) : ' + ' + fmt(b)) + ' = ' + fmt(c);
    var rhs = c - b, x = rhs / a;
    var steps = ['Start with: ' + eq + '.'];
    if (b === 0) steps.push('There is nothing to move: b is 0, so ' + coefX(a) + ' = ' + fmt(c) + '.');
    else steps.push((b > 0 ? 'Subtract ' + fmt(b) : 'Add ' + fmt(-b)) + ' on both sides: ' + coefX(a) + ' = ' + fmt(c) + (b > 0 ? ' - ' + fmt(b) : ' + ' + fmt(-b)) + ' = ' + fmt(rhs) + '.');
    if (a === 1) steps.push('x is already alone: x = ' + fmt(x) + '.');
    else steps.push('Divide both sides by ' + fmt(a) + ': x = ' + fmt(rhs) + ' ÷ ' + par(Number(fmt(a))) + ' = ' + fmt(x) + '.');
    var check = a * x + b;
    steps.push('Check: ' + fmt(a) + ' × ' + par(Number(fmt(x))) + ' + ' + par(Number(fmt(b))) + ' = ' + fmt(check) + (Math.abs(check - c) < 1e-9 ? ', which matches the right side (' + fmt(c) + '). ✓' : ' (rounded).'));
    return { answers: [{ label: 'x =', value: fmt(x) }], steps: steps };
  }

  /* ---------- Quadratic ---------- */
  function quadratic(v) {
    var a = v.a, b = v.b, c = v.c;
    if (!isNum(a) || !isNum(b) || !isNum(c)) return err('Enter a, b and c.');
    if (a === 0) return err('"a" cannot be 0. That makes it a straight line, not a quadratic. Try the Linear Equation Solver.');
    var D = b * b - 4 * a * c, steps = [], ans = [];
    steps.push('Match your equation to ax² + bx + c = 0: a = ' + fmt(a) + ', b = ' + fmt(b) + ', c = ' + fmt(c) + '.');
    steps.push('Find the discriminant: D = b² − 4ac = ' + par(Number(fmt(b))) + '² − 4 × ' + par(Number(fmt(a))) + ' × ' + par(Number(fmt(c))) + ' = ' + fmt(D) + '.');
    var h = -b / (2 * a), k = a * h * h + b * h + c;
    if (D > 0) {
      var s = Math.sqrt(D), x1 = (-b + s) / (2 * a), x2 = (-b - s) / (2 * a);
      steps.push('D is positive, so there are two real solutions. Use x = (−b ± √D) ÷ (2a), where √D = ' + fmt(s) + '.');
      steps.push('x1 = (' + fmt(-b) + ' + ' + fmt(s) + ') ÷ ' + fmt(2 * a) + ' = ' + fmt(x1) + '.');
      steps.push('x2 = (' + fmt(-b) + ' − ' + fmt(s) + ') ÷ ' + fmt(2 * a) + ' = ' + fmt(x2) + '.');
      ans.push({ label: 'x1 =', value: fmt(x1) }, { label: 'x2 =', value: fmt(x2) });
    } else if (D === 0) {
      steps.push('D is 0, so there is exactly one solution (a repeated root): x = −b ÷ (2a) = ' + fmt(-b) + ' ÷ ' + fmt(2 * a) + ' = ' + fmt(h) + '.');
      ans.push({ label: 'x =', value: fmt(h) });
    } else {
      var im = Math.abs(Math.sqrt(-D) / (2 * a));
      steps.push('D is negative, so there are no real solutions. The two solutions are complex numbers: x = −b ÷ (2a) ± (√(−D) ÷ (2a)) i.');
      steps.push('Real part: ' + fmt(-b) + ' ÷ ' + fmt(2 * a) + ' = ' + fmt(h) + '. Imaginary part: √' + fmt(-D) + ' ÷ ' + fmt(Math.abs(2 * a)) + ' = ' + fmt(im) + '.');
      ans.push({ label: 'x1 =', value: fmt(h) + ' + ' + fmt(im) + 'i' }, { label: 'x2 =', value: fmt(h) + ' − ' + fmt(im) + 'i' });
    }
    steps.push('Bonus: the vertex of the parabola is at x = −b ÷ (2a) = ' + fmt(h) + ', and y = ' + fmt(k) + ' there.');
    ans.push({ label: 'Vertex:', value: '(' + fmt(h) + ', ' + fmt(k) + ')' });
    return { answers: ans, steps: steps };
  }

  /* ---------- Pythagorean theorem ---------- */
  function pythagHyp(v) {
    if (!isNum(v.a) || !isNum(v.b)) return err('Enter both legs.');
    if (v.a <= 0 || v.b <= 0) return err('Side lengths must be greater than 0.');
    var s = v.a * v.a + v.b * v.b, c = Math.sqrt(s);
    return {
      answers: [
        { label: 'Hypotenuse c =', value: fmt(c) },
        { label: 'Area:', value: fmt(v.a * v.b / 2) },
        { label: 'Perimeter:', value: fmt(v.a + v.b + c) }
      ],
      steps: [
        'Use a² + b² = c², where a and b are the legs and c is the hypotenuse.',
        'Square each leg and add: ' + fmt(v.a) + '² + ' + fmt(v.b) + '² = ' + fmt(v.a * v.a) + ' + ' + fmt(v.b * v.b) + ' = ' + fmt(s) + '.',
        'Take the square root: c = √' + fmt(s) + ' = ' + fmt(c) + '.',
        'Area of the triangle = ½ × a × b = ' + fmt(v.a * v.b / 2) + '. Perimeter = a + b + c = ' + fmt(v.a + v.b + c) + '.'
      ]
    };
  }
  function pythagLeg(v) {
    if (!isNum(v.a) || !isNum(v.c)) return err('Enter the known leg and the hypotenuse.');
    if (v.a <= 0 || v.c <= 0) return err('Side lengths must be greater than 0.');
    if (v.c <= v.a) return err('The hypotenuse is always the longest side, so it must be bigger than the leg.');
    var s = v.c * v.c - v.a * v.a, b = Math.sqrt(s);
    return {
      answers: [
        { label: 'Missing leg b =', value: fmt(b) },
        { label: 'Area:', value: fmt(v.a * b / 2) },
        { label: 'Perimeter:', value: fmt(v.a + b + v.c) }
      ],
      steps: [
        'Use a² + b² = c². Rearranged, b² = c² − a².',
        'Square and subtract: ' + fmt(v.c) + '² − ' + fmt(v.a) + '² = ' + fmt(v.c * v.c) + ' − ' + fmt(v.a * v.a) + ' = ' + fmt(s) + '.',
        'Take the square root: b = √' + fmt(s) + ' = ' + fmt(b) + '.',
        'Area of the triangle = ½ × a × b = ' + fmt(v.a * b / 2) + '. Perimeter = a + b + c = ' + fmt(v.a + b + v.c) + '.'
      ]
    };
  }

  /* ---------- Slope ---------- */
  function lineEq(m, b) {
    m = Number(m.toFixed(6)); b = Number(b.toFixed(6));
    if (m === 0) return 'y = ' + fmt(b);
    var s = 'y = ' + coefX(m);
    if (b > 0) s += ' + ' + fmt(b); else if (b < 0) s += ' - ' + fmt(-b);
    return s;
  }
  function slope(v) {
    var x1 = v.x1, y1 = v.y1, x2 = v.x2, y2 = v.y2;
    if (!isNum(x1) || !isNum(y1) || !isNum(x2) || !isNum(y2)) return err('Enter all four coordinates.');
    if (x1 === x2 && y1 === y2) return err('The two points are the same point. Enter two different points.');
    var dx = x2 - x1, dy = y2 - y1, dist = Math.sqrt(dx * dx + dy * dy);
    var mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
    var steps = [], ans = [];
    steps.push('Slope is rise over run: m = (y2 − y1) ÷ (x2 − x1).');
    if (dx === 0) {
      steps.push('Run = ' + fmt(x2) + ' − ' + par(Number(fmt(x1))) + ' = 0. You cannot divide by 0, so the slope is undefined and the line is vertical.');
      steps.push('Every point on the line has x = ' + fmt(x1) + ', so the equation is x = ' + fmt(x1) + '.');
      ans.push({ label: 'Slope:', value: 'undefined (vertical line)' }, { label: 'Equation:', value: 'x = ' + fmt(x1) });
    } else {
      var m = dy / dx, b = y1 - m * x1;
      var mText = (Number.isInteger(dx) && Number.isInteger(dy)) ? frac(dy, dx) : fmt(m);
      steps.push('Rise = ' + fmt(y2) + ' − ' + par(Number(fmt(y1))) + ' = ' + fmt(dy) + ' and run = ' + fmt(x2) + ' − ' + par(Number(fmt(x1))) + ' = ' + fmt(dx) + '.');
      steps.push('m = ' + fmt(dy) + ' ÷ ' + par(Number(fmt(dx))) + ' = ' + mText + (mText.indexOf('/') > -1 ? ' ≈ ' + fmt(m) : '') + '.');
      steps.push('Find the y-intercept with b = y1 − m × x1 = ' + fmt(y1) + ' − ' + par(Number(fmt(m))) + ' × ' + par(Number(fmt(x1))) + ' = ' + fmt(b) + '.');
      steps.push('Put it in y = mx + b form: ' + lineEq(m, b) + '.');
      ans.push({ label: 'Slope m =', value: mText + (mText.indexOf('/') > -1 ? ' ≈ ' + fmt(m) : '') }, { label: 'Equation:', value: lineEq(m, b) });
    }
    steps.push('Distance between the points = √((x2 − x1)² + (y2 − y1)²) = √(' + fmt(dx * dx) + ' + ' + fmt(dy * dy) + ') = ' + fmt(dist) + '.');
    steps.push('Midpoint = ((x1 + x2) ÷ 2, (y1 + y2) ÷ 2) = (' + fmt(mx) + ', ' + fmt(my) + ').');
    ans.push({ label: 'Distance:', value: fmt(dist) }, { label: 'Midpoint:', value: '(' + fmt(mx) + ', ' + fmt(my) + ')' });
    return { answers: ans, steps: steps };
  }

  /* ---------- GCF and LCM ---------- */
  function primeFactors(n) {
    var out = [];
    while (n % 2 === 0) { out.push(2); n /= 2; }
    for (var p = 3; p * p <= n; p += 2) {
      while (n % p === 0) { out.push(p); n /= p; }
    }
    if (n > 1) out.push(n);
    return out;
  }
  function euclid(a, b, steps) {
    var x = Math.max(a, b), y = Math.min(a, b);
    while (y) {
      var q = Math.floor(x / y), r = x % y;
      steps.push(x + ' = ' + q + ' × ' + y + ' + ' + r);
      x = y; y = r;
    }
    return x;
  }
  function gcdlcm(v) {
    var xs = parseList(v.list);
    if (!xs) return err('Type whole numbers separated by commas or spaces, like 12, 18, 24.');
    if (xs.length < 2) return err('Enter at least two numbers.');
    if (xs.length > 10) return err('Enter ten numbers or fewer.');
    for (var i = 0; i < xs.length; i++) {
      if (!Number.isInteger(xs[i]) || xs[i] < 1 || xs[i] > 1e9) return err('Use whole numbers from 1 to 1,000,000,000.');
    }
    var steps = ['Prime factors of each number:'];
    xs.forEach(function (n) {
      var pf = primeFactors(n);
      steps.push(n + (pf.length ? ' = ' + pf.join(' × ') : ' has no prime factors'));
    });
    steps.push("Greatest common factor, using Euclid's method (divide, then repeat with the remainder until it is 0; the last divisor is the answer):");
    var g = xs[0];
    for (var j = 1; j < xs.length; j++) {
      steps.push('gcd(' + g + ', ' + xs[j] + '):');
      g = euclid(g, xs[j], steps);
      steps.push('= ' + g);
    }
    steps.push('Least common multiple: lcm(a, b) = a × b ÷ gcd(a, b).');
    var l = xs[0];
    for (var k = 1; k < xs.length; k++) {
      var gg = gcd(l, xs[k]), next = l / gg * xs[k];
      if (next > 9007199254740991) return err('Those numbers are too large for an exact LCM.');
      steps.push('lcm(' + l + ', ' + xs[k] + ') = ' + l + ' × ' + xs[k] + ' ÷ ' + gg + ' = ' + next);
      l = next;
    }
    return { answers: [{ label: 'GCF =', value: String(g) }, { label: 'LCM =', value: String(l) }], steps: steps };
  }

  /* ---------- Statistics ---------- */
  function stats(v) {
    var xs = parseList(v.list);
    if (!xs) return err('Type numbers separated by commas or spaces, like 3, 7, 7, 2, 9.');
    if (xs.length > 500) return err('Enter 500 numbers or fewer.');
    var n = xs.length, sum = 0, i;
    for (i = 0; i < n; i++) sum += xs[i];
    var mean = sum / n;
    var sorted = xs.slice().sort(function (a, b) { return a - b; });
    var median = n % 2 ? sorted[(n - 1) / 2] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
    var counts = {}, order = [];
    xs.forEach(function (x) { var key = fmt(x); if (!counts[key]) { counts[key] = { v: x, c: 0 }; order.push(key); } counts[key].c++; });
    var maxC = 0;
    order.forEach(function (key) { if (counts[key].c > maxC) maxC = counts[key].c; });
    var modes = [];
    if (maxC > 1) order.forEach(function (key) { if (counts[key].c === maxC) modes.push(counts[key].v); });
    modes.sort(function (a, b) { return a - b; });
    var range = sorted[n - 1] - sorted[0];
    var ssq = 0;
    for (i = 0; i < n; i++) ssq += (xs[i] - mean) * (xs[i] - mean);
    var popVar = ssq / n, popSd = Math.sqrt(popVar);
    var sampVar = n > 1 ? ssq / (n - 1) : NaN, sampSd = n > 1 ? Math.sqrt(sampVar) : NaN;
    var list = function (a) { return a.map(fmt).join(', '); };

    var steps = [];
    steps.push('Sort the numbers from smallest to largest: ' + list(sorted) + '.');
    steps.push('Count = ' + n + '. Sum = ' + fmt(sum) + '.');
    steps.push('Mean = sum ÷ count = ' + fmt(sum) + ' ÷ ' + n + ' = ' + fmt(mean) + '.');
    if (n % 2) steps.push('Median: there are ' + n + ' numbers (an odd count), so the median is the middle one: ' + fmt(median) + '.');
    else steps.push('Median: there are ' + n + ' numbers (an even count), so average the two middle ones: (' + fmt(sorted[n / 2 - 1]) + ' + ' + fmt(sorted[n / 2]) + ') ÷ 2 = ' + fmt(median) + '.');
    steps.push(modes.length ? 'Mode: ' + list(modes) + ' appears ' + maxC + ' times, more than any other value.' : 'Mode: every value appears only once, so there is no mode.');
    steps.push('Range = largest − smallest = ' + fmt(sorted[n - 1]) + ' − ' + par(Number(fmt(sorted[0]))) + ' = ' + fmt(range) + '.');
    steps.push('Add up the squared distances from the mean: ' + fmt(ssq) + '.');
    steps.push('Population variance = ' + fmt(ssq) + ' ÷ ' + n + ' = ' + fmt(popVar) + ', so population standard deviation = √' + fmt(popVar) + ' = ' + fmt(popSd) + '.');
    if (n > 1) steps.push('Sample variance = ' + fmt(ssq) + ' ÷ ' + (n - 1) + ' = ' + fmt(sampVar) + ', so sample standard deviation = √' + fmt(sampVar) + ' = ' + fmt(sampSd) + '.');
    var ans = [
      { label: 'Mean:', value: fmt(mean) },
      { label: 'Median:', value: fmt(median) },
      { label: 'Mode:', value: modes.length ? list(modes) : 'none' },
      { label: 'Range:', value: fmt(range) },
      { label: 'Sum:', value: fmt(sum) },
      { label: 'Count:', value: String(n) },
      { label: 'Std dev (population):', value: fmt(popSd) }
    ];
    if (n > 1) ans.push({ label: 'Std dev (sample):', value: fmt(sampSd) });
    return { answers: ans, steps: steps };
  }

  /* ---------- Right triangle trig ---------- */
  function trig(v) {
    var A = v.angle, len = v.len, known = v.known;
    if (!isNum(A) || !isNum(len)) return err('Enter the angle and the side length.');
    if (A <= 0 || A >= 90) return err('The angle must be between 0 and 90 degrees (the other angle is the right angle).');
    if (len <= 0) return err('The side length must be greater than 0.');
    var rad = A * Math.PI / 180, s = Math.sin(rad), c = Math.cos(rad), t = Math.tan(rad);
    var opp, adj, hyp, steps = [];
    steps.push('Remember SOH-CAH-TOA: sin = opposite ÷ hypotenuse, cos = adjacent ÷ hypotenuse, tan = opposite ÷ adjacent.');
    steps.push('For ' + fmt(A) + '°: sin = ' + fmt(s) + ', cos = ' + fmt(c) + ', tan = ' + fmt(t) + '.');
    if (known === 'opposite') {
      opp = len; hyp = len / s; adj = len / t;
      steps.push('You know the opposite side. From sin: hypotenuse = opposite ÷ sin(' + fmt(A) + '°) = ' + fmt(len) + ' ÷ ' + fmt(s) + ' = ' + fmt(hyp) + '.');
      steps.push('From tan: adjacent = opposite ÷ tan(' + fmt(A) + '°) = ' + fmt(len) + ' ÷ ' + fmt(t) + ' = ' + fmt(adj) + '.');
    } else if (known === 'adjacent') {
      adj = len; hyp = len / c; opp = len * t;
      steps.push('You know the adjacent side. From cos: hypotenuse = adjacent ÷ cos(' + fmt(A) + '°) = ' + fmt(len) + ' ÷ ' + fmt(c) + ' = ' + fmt(hyp) + '.');
      steps.push('From tan: opposite = adjacent × tan(' + fmt(A) + '°) = ' + fmt(len) + ' × ' + fmt(t) + ' = ' + fmt(opp) + '.');
    } else if (known === 'hypotenuse') {
      hyp = len; opp = len * s; adj = len * c;
      steps.push('You know the hypotenuse. From sin: opposite = hypotenuse × sin(' + fmt(A) + '°) = ' + fmt(len) + ' × ' + fmt(s) + ' = ' + fmt(opp) + '.');
      steps.push('From cos: adjacent = hypotenuse × cos(' + fmt(A) + '°) = ' + fmt(len) + ' × ' + fmt(c) + ' = ' + fmt(adj) + '.');
    } else {
      return err('Pick which side you know.');
    }
    var B = 90 - A;
    steps.push('The angles of a triangle add to 180°, and one is 90°, so the other angle is 90° − ' + fmt(A) + '° = ' + fmt(B) + '°.');
    return {
      answers: [
        { label: 'Opposite:', value: fmt(opp) },
        { label: 'Adjacent:', value: fmt(adj) },
        { label: 'Hypotenuse:', value: fmt(hyp) },
        { label: 'Other angle:', value: fmt(B) + '°' }
      ],
      steps: steps
    };
  }
  function trigAngle(v) {
    if (!isNum(v.opp) || !isNum(v.adj)) return err('Enter both sides.');
    if (v.opp <= 0 || v.adj <= 0) return err('Side lengths must be greater than 0.');
    var ratio = v.opp / v.adj, A = Math.atan(ratio) * 180 / Math.PI, B = 90 - A;
    var hyp = Math.sqrt(v.opp * v.opp + v.adj * v.adj);
    return {
      answers: [
        { label: 'Angle A =', value: fmt(A) + '°' },
        { label: 'Other angle:', value: fmt(B) + '°' },
        { label: 'Hypotenuse:', value: fmt(hyp) }
      ],
      steps: [
        'tan(A) = opposite ÷ adjacent = ' + fmt(v.opp) + ' ÷ ' + fmt(v.adj) + ' = ' + fmt(ratio) + '.',
        'Use the inverse tangent to get the angle: A = tan⁻¹(' + fmt(ratio) + ') = ' + fmt(A) + '°.',
        'The other angle is 90° − ' + fmt(A) + '° = ' + fmt(B) + '°.',
        'Hypotenuse (Pythagorean theorem) = √(' + fmt(v.opp) + '² + ' + fmt(v.adj) + '²) = ' + fmt(hyp) + '.'
      ]
    };
  }

  /* ---------- Polynomials: derivative and integral ---------- */
  var POLY_HELP = 'Type a polynomial using whole-number powers, like 3x^4 - 2x^2 + 5x - 7.';
  function parsePoly(str) {
    if (typeof str !== 'string' || !str.trim()) return { error: POLY_HELP };
    var s = str.toLowerCase().replace(/\s+/g, '').replace(/\*/g, '').replace(/−/g, '-');
    if (!/^[0-9x^.+\-]+$/.test(s)) return { error: 'Only numbers, x, ^, + and - are allowed. ' + POLY_HELP };
    s = s.replace(/-/g, '+-');
    var parts = s.split('+').filter(function (p) { return p !== ''; });
    if (!parts.length) return { error: POLY_HELP };
    var map = {}, num = /^-?(\d+\.?\d*|\.\d+)$/;
    for (var i = 0; i < parts.length; i++) {
      var t = parts[i], coef, exp, xi = t.indexOf('x');
      if (xi === -1) {
        if (!num.test(t)) return { error: 'Could not read "' + t + '". ' + POLY_HELP };
        coef = parseFloat(t); exp = 0;
      } else {
        var cs = t.slice(0, xi), rest = t.slice(xi + 1);
        if (cs === '') coef = 1;
        else if (cs === '-') coef = -1;
        else if (num.test(cs)) coef = parseFloat(cs);
        else return { error: 'Could not read "' + t + '". ' + POLY_HELP };
        if (rest === '') exp = 1;
        else if (/^\^\d+$/.test(rest)) exp = parseInt(rest.slice(1), 10);
        else return { error: 'Could not read "' + t + '". Use whole-number powers like x^3. ' + POLY_HELP };
        if (exp > 50) return { error: 'Keep powers at 50 or below.' };
      }
      map[exp] = (map[exp] || 0) + coef;
    }
    return { map: map };
  }
  function termBody(t) {
    var m = (t.mag.indexOf('/') > -1 && t.exp > 0) ? '(' + t.mag + ')' : t.mag;
    if (t.exp === 0) return t.mag;
    var x = t.exp === 1 ? 'x' : 'x^' + t.exp;
    return (t.one ? '' : m) + x;
  }
  function joinTerms(list) {
    var out = '';
    for (var i = 0; i < list.length; i++) {
      var t = list[i], body = termBody(t);
      if (i === 0) out += (t.neg ? '-' : '') + body;
      else out += (t.neg ? ' - ' : ' + ') + body;
    }
    return out || '0';
  }
  function polyList(map) {
    var exps = Object.keys(map).map(Number).sort(function (a, b) { return b - a; }), list = [];
    exps.forEach(function (e) {
      var c = map[e];
      if (c !== 0) list.push({ neg: c < 0, mag: fmt(Math.abs(c)), one: Math.abs(c) === 1, exp: e });
    });
    return list;
  }
  function evalPoly(map, x) {
    var s = 0;
    Object.keys(map).forEach(function (k) { s += map[k] * Math.pow(x, Number(k)); });
    return s;
  }
  function oneTerm(c, e) { return joinTerms([{ neg: c < 0, mag: fmt(Math.abs(c)), one: Math.abs(c) === 1, exp: e }]); }
  function xPart(e) { return e === 0 ? '' : (e === 1 ? 'x' : 'x^' + e); }

  function derivative(v) {
    var p = parsePoly(v.poly);
    if (p.error) return err(p.error);
    var map = p.map, f = joinTerms(polyList(map));
    var steps = ['Your function: f(x) = ' + f + '.',
      'Power rule: the derivative of c·x^n is c·n·x^(n−1). Multiply by the power, then lower the power by 1. The derivative of a plain number is 0.'];
    var d = {}, exps = Object.keys(map).map(Number).sort(function (a, b) { return b - a; });
    exps.forEach(function (e) {
      var c = map[e];
      if (c === 0) return;
      if (e === 0) {
        steps.push('d/dx[' + fmt(c) + '] = 0, because a constant does not change.');
      } else {
        var nc = c * e;
        d[e - 1] = (d[e - 1] || 0) + nc;
        steps.push('d/dx[' + oneTerm(c, e) + '] = ' + fmt(c) + ' × ' + e + xPart(e - 1) + ' = ' + oneTerm(nc, e - 1) + '.');
      }
    });
    var res = joinTerms(polyList(d));
    steps.push('Add the pieces together: f\'(x) = ' + res + '.');
    var ans = [{ label: "f'(x) =", value: res }];
    if (isNum(v.at)) {
      var val = evalPoly(d, v.at);
      steps.push('Plug in x = ' + fmt(v.at) + ': f\'(' + fmt(v.at) + ') = ' + fmt(val) + '.');
      ans.push({ label: "f'(" + fmt(v.at) + ') =', value: fmt(val) });
    }
    return { answers: ans, steps: steps };
  }

  function integTerm(c, e) {
    var n1 = e + 1;
    if (Number.isInteger(c)) {
      var g = gcd(Math.abs(c), n1), p = c / g, q = n1 / g;
      return { neg: p < 0, mag: q === 1 ? String(Math.abs(p)) : Math.abs(p) + '/' + q, one: q === 1 && Math.abs(p) === 1, exp: n1 };
    }
    var val = c / n1;
    return { neg: val < 0, mag: fmt(Math.abs(val)), one: Math.abs(val) === 1, exp: n1 };
  }
  function integral(v) {
    var p = parsePoly(v.poly);
    if (p.error) return err(p.error);
    var hasLo = isNum(v.lo), hasHi = isNum(v.hi);
    if (hasLo !== hasHi) return err('Enter both limits for a definite integral, or leave both blank.');
    var map = p.map, f = joinTerms(polyList(map));
    var steps = ['Your function: f(x) = ' + f + '.',
      'Reverse power rule: the integral of c·x^n is c·x^(n+1) ÷ (n+1). Raise the power by 1, then divide by the new power. Add + C at the end.'];
    var terms = [], F = {}, exps = Object.keys(map).map(Number).sort(function (a, b) { return b - a; });
    exps.forEach(function (e) {
      var c = map[e];
      if (c === 0) return;
      var t = integTerm(c, e);
      terms.push(t);
      F[e + 1] = c / (e + 1);
      steps.push('∫ ' + oneTerm(c, e) + ' dx = ' + fmt(c) + xPart(e + 1) + ' ÷ ' + (e + 1) + ' = ' + joinTerms([t]) + '.');
    });
    var body = terms.length ? joinTerms(terms) + ' + C' : 'C';
    steps.push('Add the pieces and the constant of integration: ∫ f(x) dx = ' + body + '.');
    var ans = [{ label: '∫ f(x) dx =', value: body }];
    if (hasLo) {
      var Fhi = evalPoly(F, v.hi), Flo = evalPoly(F, v.lo);
      steps.push('Definite integral from ' + fmt(v.lo) + ' to ' + fmt(v.hi) + ': find F(upper) − F(lower), where F is the antiderivative (the + C cancels).');
      steps.push('F(' + fmt(v.hi) + ') = ' + fmt(Fhi) + ' and F(' + fmt(v.lo) + ') = ' + fmt(Flo) + '.');
      steps.push(fmt(Fhi) + ' − ' + par(Number(fmt(Flo))) + ' = ' + fmt(Fhi - Flo) + '.');
      ans.push({ label: 'From ' + fmt(v.lo) + ' to ' + fmt(v.hi) + ' =', value: fmt(Fhi - Flo) });
    }
    return { answers: ans, steps: steps };
  }

  /* ---------- Inflation (US CPI-U annual averages, 1982-84 = 100) ---------- */
  /* Source: U.S. Bureau of Labor Statistics CPI-U, U.S. city average, all items, not seasonally adjusted.
     1913-2024 are annual averages. 2025 is the average of the 11 months BLS published
     (October 2025 was not collected during the federal funding lapse). */
  var CPI = {
    1913:9.9,1914:10.0,1915:10.1,1916:10.9,1917:12.8,1918:15.1,1919:17.3,1920:20.0,1921:17.9,1922:16.8,
    1923:17.1,1924:17.1,1925:17.5,1926:17.7,1927:17.4,1928:17.1,1929:17.1,1930:16.7,1931:15.2,1932:13.7,
    1933:13.0,1934:13.4,1935:13.7,1936:13.9,1937:14.4,1938:14.1,1939:13.9,1940:14.0,1941:14.7,1942:16.3,
    1943:17.3,1944:17.6,1945:18.0,1946:19.5,1947:22.3,1948:24.1,1949:23.8,1950:24.1,1951:26.0,1952:26.5,
    1953:26.7,1954:26.9,1955:26.8,1956:27.2,1957:28.1,1958:28.9,1959:29.1,1960:29.6,1961:29.9,1962:30.2,
    1963:30.6,1964:31.0,1965:31.5,1966:32.4,1967:33.4,1968:34.8,1969:36.7,1970:38.8,1971:40.5,1972:41.8,
    1973:44.4,1974:49.3,1975:53.8,1976:56.9,1977:60.6,1978:65.2,1979:72.6,1980:82.4,1981:90.9,1982:96.5,
    1983:99.6,1984:103.9,1985:107.6,1986:109.6,1987:113.6,1988:118.3,1989:124.0,1990:130.7,1991:136.2,1992:140.3,
    1993:144.5,1994:148.2,1995:152.4,1996:156.9,1997:160.5,1998:163.0,1999:166.6,2000:172.2,2001:177.1,2002:179.9,
    2003:184.0,2004:188.9,2005:195.3,2006:201.6,2007:207.342,2008:215.303,2009:214.537,2010:218.056,2011:224.939,2012:229.594,
    2013:232.957,2014:236.736,2015:237.017,2016:240.007,2017:245.12,2018:251.107,2019:255.657,2020:258.811,2021:270.97,2022:292.655,
    2023:304.702,2024:313.689,2025:321.943
  };
  var CPI_FIRST = 1913, CPI_LAST = 2025;

  function commas(s) { return String(s).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function money(n) {
    var neg = n < 0, s = Math.abs(n).toFixed(2).split('.');
    return (neg ? '-' : '') + '$' + commas(s[0]) + '.' + s[1];
  }
  function pct(n) { return Number(n.toFixed(2)) + '%'; }
  function cpiText(y) { return String(CPI[y]); }

  function inflationCpi(v) {
    if (!isNum(v.amt) || v.amt <= 0) return err('Enter an amount greater than 0.');
    if (v.amt > 1e12) return err('That amount is too large. Try something under one trillion.');
    var y1 = v.y1, y2 = v.y2;
    if (!isNum(y1) || !isNum(y2) || !Number.isInteger(y1) || !Number.isInteger(y2)) return err('Enter two whole years, like 2000 and 2025.');
    if (y1 < CPI_FIRST || y1 > CPI_LAST || y2 < CPI_FIRST || y2 > CPI_LAST) return err('Pick years from ' + CPI_FIRST + ' to ' + CPI_LAST + '. That is the range of official CPI data.');
    var c1 = CPI[y1], c2 = CPI[y2], ratio = c2 / c1, out = v.amt * ratio, steps = [];
    steps.push('Look up the Consumer Price Index (CPI-U, 1982-84 = 100) for each year: ' + y1 + ' was ' + cpiText(y1) + ' and ' + y2 + ' was ' + cpiText(y2) + '.');
    steps.push('Divide the later index by the earlier one to get the price ratio: ' + cpiText(y2) + ' ÷ ' + cpiText(y1) + ' = ' + Number(ratio.toFixed(6)) + '.');
    steps.push('Multiply your amount by the ratio: ' + money(v.amt) + ' × ' + Number(ratio.toFixed(6)) + ' = ' + money(out) + '.');
    var total = (ratio - 1) * 100;
    steps.push('Total change in prices: (' + Number(ratio.toFixed(6)) + ' − 1) × 100 = ' + pct(total) + '.');
    var yrs = Math.abs(y2 - y1), ans = [
      { label: money(v.amt) + ' in ' + y1 + ' is worth', value: money(out) + ' in ' + y2 },
      { label: 'Total price change:', value: pct(total) }
    ];
    if (yrs > 0) {
      var avg = (Math.pow(ratio, 1 / yrs) - 1) * 100;
      steps.push('Average change per year, compounded over ' + yrs + ' year' + (yrs === 1 ? '' : 's') + ': ' + Number(ratio.toFixed(6)) + '^(1 ÷ ' + yrs + ') − 1 = ' + pct(avg) + '.');
      ans.push({ label: 'Average per year:', value: pct(avg) });
    }
    if (y1 === CPI_LAST || y2 === CPI_LAST) steps.push('Note: the 2025 figure is the average of the 11 months published by the Bureau of Labor Statistics (October 2025 was not collected).');
    return { answers: ans, steps: steps };
  }

  function inflationRate(v) {
    if (!isNum(v.amt) || v.amt <= 0) return err('Enter an amount greater than 0.');
    if (!isNum(v.rate) || v.rate < -50 || v.rate > 100) return err('Enter a yearly inflation rate between -50 and 100 percent.');
    if (!isNum(v.yrs) || v.yrs < 0 || v.yrs > 200) return err('Enter a number of years between 0 and 200.');
    var g = 1 + v.rate / 100, f = Math.pow(g, v.yrs), future = v.amt * f, power = v.amt / f, steps = [];
    steps.push('Turn the rate into a growth factor: 1 + ' + fmt(v.rate) + ' ÷ 100 = ' + fmt(g) + '.');
    steps.push('Raise it to the number of years: ' + fmt(g) + '^' + fmt(v.yrs) + ' = ' + Number(f.toFixed(6)) + '.');
    steps.push('Cost later of something that costs ' + money(v.amt) + ' today: ' + money(v.amt) + ' × ' + Number(f.toFixed(6)) + ' = ' + money(future) + '.');
    steps.push('Buying power later of ' + money(v.amt) + ': ' + money(v.amt) + ' ÷ ' + Number(f.toFixed(6)) + ' = ' + money(power) + ' in today\'s money.');
    return {
      answers: [
        { label: 'Something that costs ' + money(v.amt) + ' today will cost', value: money(future) },
        { label: money(v.amt) + ' will buy only', value: money(power) + ' worth' },
        { label: 'Total price change:', value: pct((f - 1) * 100) }
      ], steps: steps
    };
  }

  /* ---------- Temperature ---------- */
  function cToF(v) {
    if (!isNum(v.t)) return err('Enter a temperature in degrees Celsius.');
    if (v.t < -273.15) return err('Nothing can be colder than absolute zero, which is -273.15°C.');
    var mult = v.t * 9 / 5, f = mult + 32, k = v.t + 273.15;
    return {
      answers: [{ label: fmt(v.t) + '°C =', value: fmt(f) + '°F' }, { label: 'In Kelvin:', value: fmt(k) + ' K' }],
      steps: [
        'Use the formula: °F = °C × 9/5 + 32.',
        'Multiply the Celsius value by 9/5: ' + par(Number(fmt(v.t))) + ' × 9 ÷ 5 = ' + fmt(mult) + '.',
        'Add 32: ' + fmt(mult) + ' + 32 = ' + fmt(f) + '.',
        'So ' + fmt(v.t) + '°C is ' + fmt(f) + '°F. (Kelvin is °C + 273.15 = ' + fmt(k) + ' K.)'
      ]
    };
  }
  function fToC(v) {
    if (!isNum(v.t)) return err('Enter a temperature in degrees Fahrenheit.');
    if (v.t < -459.67) return err('Nothing can be colder than absolute zero, which is -459.67°F.');
    var sub = v.t - 32, c = sub * 5 / 9, k = c + 273.15;
    return {
      answers: [{ label: fmt(v.t) + '°F =', value: fmt(c) + '°C' }, { label: 'In Kelvin:', value: fmt(k) + ' K' }],
      steps: [
        'Use the formula: °C = (°F − 32) × 5/9.',
        'Subtract 32 from the Fahrenheit value: ' + par(Number(fmt(v.t))) + ' − 32 = ' + fmt(sub) + '.',
        'Multiply by 5/9: ' + par(Number(fmt(sub))) + ' × 5 ÷ 9 = ' + fmt(c) + '.',
        'So ' + fmt(v.t) + '°F is ' + fmt(c) + '°C. (Kelvin is °C + 273.15 = ' + fmt(k) + ' K.)'
      ]
    };
  }

  /* ---------- Time (add or subtract) ---------- */
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
  function dhms(total) {
    var d = Math.floor(total / 86400), r = total - d * 86400,
      h = Math.floor(r / 3600), m = Math.floor((r - h * 3600) / 60), s = r - h * 3600 - m * 60;
    return { d: d, h: h, m: m, s: s };
  }
  function dhmsText(p) {
    var out = [];
    if (p.d) out.push(plural(p.d, 'day'));
    if (p.h) out.push(plural(p.h, 'hour'));
    if (p.m) out.push(plural(p.m, 'minute'));
    if (p.s) out.push(plural(p.s, 'second'));
    return out.length ? out.join(', ') : '0 seconds';
  }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function timeCalc(v) {
    var keys = ['d1', 'h1', 'm1', 's1', 'd2', 'h2', 'm2', 's2'], x = {};
    for (var i = 0; i < keys.length; i++) {
      var n = v[keys[i]];
      if (n === undefined || (typeof n === 'number' && isNaN(n))) n = 0;
      if (!isNum(n) || !Number.isInteger(n) || n < 0) return err('Use whole numbers that are 0 or more in every time box. Leave a box empty for 0.');
      if (n > 1000000) return err('One of those numbers is too large. Try something under one million.');
      x[keys[i]] = n;
    }
    if (v.op !== 'add' && v.op !== 'sub') return err('Pick add or subtract.');
    var t1 = x.d1 * 86400 + x.h1 * 3600 + x.m1 * 60 + x.s1, t2 = x.d2 * 86400 + x.h2 * 3600 + x.m2 * 60 + x.s2;
    var label = function (d, h, m, s) { return d + ' d ' + h + ' h ' + m + ' m ' + s + ' s'; };
    var steps = [];
    steps.push('Turn the first time into seconds (1 day = 86,400 s, 1 hour = 3,600 s, 1 minute = 60 s): ' + label(x.d1, x.h1, x.m1, x.s1) + ' = ' + commas(t1) + ' seconds.');
    steps.push('Turn the second time into seconds: ' + label(x.d2, x.h2, x.m2, x.s2) + ' = ' + commas(t2) + ' seconds.');
    var res = v.op === 'add' ? t1 + t2 : t1 - t2, neg = res < 0, abs = Math.abs(res);
    steps.push((v.op === 'add' ? 'Add' : 'Subtract') + ' the seconds: ' + commas(t1) + (v.op === 'add' ? ' + ' : ' − ') + commas(t2) + ' = ' + commas(res) + ' seconds.');
    if (neg) steps.push('The second time is longer than the first, so the answer is negative. Convert ' + commas(abs) + ' seconds and put a minus sign in front.');
    var p = dhms(abs);
    steps.push('Convert back: ' + commas(abs) + ' ÷ 86,400 = ' + p.d + ' day' + (p.d === 1 ? '' : 's') + ', then the rest ÷ 3,600 = ' + p.h + ' hour' + (p.h === 1 ? '' : 's') + ', then ÷ 60 = ' + p.m + ' minute' + (p.m === 1 ? '' : 's') + ' and ' + p.s + ' second' + (p.s === 1 ? '' : 's') + '.');
    var sign = neg ? '-' : '', totalH = Math.floor(abs / 3600), rem = abs - totalH * 3600;
    var hms = sign + totalH + ':' + pad2(Math.floor(rem / 60)) + ':' + pad2(rem % 60);
    return {
      answers: [
        { label: 'Result:', value: neg ? '-(' + dhmsText(p) + ')' : dhmsText(p) },
        { label: 'As hours:minutes:seconds:', value: hms },
        { label: 'Total hours:', value: fmt(res / 3600) },
        { label: 'Total minutes:', value: fmt(res / 60) },
        { label: 'Total seconds:', value: commas(res) }
      ], steps: steps
    };
  }

  /* ---------- Hours worked (start/end times, breaks, decimal hours, pay) ---------- */
  function parseClock(str) {
    var s = String(str == null ? '' : str).toLowerCase().replace(/[.\s]/g, '');
    if (!s) return null;
    var ap = null, m = s.match(/^(.*?)(am|pm|a|p)$/);
    if (m) { s = m[1]; ap = m[2].charAt(0); }
    var h, mi;
    if (/^\d{1,2}$/.test(s)) { h = parseInt(s, 10); mi = 0; }
    else if (/^\d{1,2}:\d{2}$/.test(s)) { h = parseInt(s.split(':')[0], 10); mi = parseInt(s.split(':')[1], 10); }
    else if (/^\d{3,4}$/.test(s)) { mi = parseInt(s.slice(-2), 10); h = parseInt(s.slice(0, -2), 10); }
    else return null;
    if (mi > 59) return null;
    if (ap) {
      if (h < 1 || h > 12) return null;
      if (h === 12) h = 0;
      if (ap === 'p') h += 12;
    } else if (h > 23) return null;
    return h * 60 + mi;
  }
  function clockText(mins) {
    var h = Math.floor(mins / 60) % 24, m = mins % 60, ap = h >= 12 ? 'PM' : 'AM', h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + ':' + pad2(m) + ' ' + ap;
  }
  function hmText(mins) {
    var h = Math.floor(mins / 60), m = mins % 60, out = [];
    if (h) out.push(plural(h, 'hour'));
    if (m) out.push(plural(m, 'minute'));
    return out.length ? out.join(', ') : '0 minutes';
  }
  function dec2(mins) { return String(Number((mins / 60).toFixed(2))); }
  function shiftMinutes(st, en, brk, who) {
    // returns {mins, span, overnight} or {error}
    var s = parseClock(st), e = parseClock(en);
    if (s === null) return { error: who + 'Enter a start time like 9:00 AM or 17:30.' };
    if (e === null) return { error: who + 'Enter an end time like 5:30 PM or 17:30.' };
    if (e === s) return { error: who + 'The start and end times are the same. Change one of them.' };
    var overnight = e < s, span = overnight ? e + 1440 - s : e - s;
    if (brk >= span) return { error: who + 'The unpaid break is as long as, or longer than, the shift.' };
    return { s: s, e: e, span: span, mins: span - brk, overnight: overnight, brk: brk };
  }
  function cleanBreak(b) {
    if (b === undefined || b === '' || (typeof b === 'number' && isNaN(b))) return 0;
    return b;
  }
  function hoursShift(v) {
    var brk = cleanBreak(v.brk);
    if (!isNum(brk) || brk < 0 || brk > 1440 || !Number.isInteger(brk)) return err('Enter the unpaid break in whole minutes (0 or more). Leave it empty for no break.');
    var days = (v.days === undefined || (typeof v.days === 'number' && isNaN(v.days))) ? 1 : v.days;
    if (!isNum(days) || !Number.isInteger(days) || days < 1 || days > 366) return err('Enter the number of days as a whole number from 1 to 366.');
    var hasRate = isNum(v.rate);
    if (hasRate && (v.rate < 0 || v.rate > 100000)) return err('Enter an hourly pay rate of 0 or more, or leave it empty.');
    var r = shiftMinutes(v.st, v.en, brk, '');
    if (r.error) return err(r.error);
    var steps = [];
    steps.push('Turn each time into minutes after midnight: ' + clockText(r.s) + ' = ' + commas(r.s) + ' and ' + clockText(r.e) + ' = ' + commas(r.e) + '.');
    if (r.overnight) steps.push('The end time is earlier than the start time, so the shift runs past midnight. Add 24 hours (1,440 minutes) to the end: ' + commas(r.e) + ' + 1,440 − ' + commas(r.s) + ' = ' + commas(r.span) + ' minutes.');
    else steps.push('Subtract the start from the end: ' + commas(r.e) + ' − ' + commas(r.s) + ' = ' + commas(r.span) + ' minutes (' + hmText(r.span) + ').');
    if (brk) steps.push('Subtract the unpaid break: ' + commas(r.span) + ' − ' + brk + ' = ' + commas(r.mins) + ' minutes (' + hmText(r.mins) + ').');
    else steps.push('No unpaid break, so the time worked is ' + commas(r.mins) + ' minutes (' + hmText(r.mins) + ').');
    steps.push('Decimal hours: ' + commas(r.mins) + ' ÷ 60 = ' + dec2(r.mins) + ' hours.');
    var ans = [{ label: 'Time worked per day:', value: hmText(r.mins) }, { label: 'Decimal hours per day:', value: dec2(r.mins) }];
    var total = r.mins * days;
    if (days > 1) {
      steps.push('Total for ' + days + ' days: ' + commas(r.mins) + ' × ' + days + ' = ' + commas(total) + ' minutes (' + hmText(total) + ', or ' + dec2(total) + ' hours).');
      ans.push({ label: 'Total for ' + days + ' days:', value: hmText(total) });
      ans.push({ label: 'Total decimal hours:', value: dec2(total) });
    }
    if (hasRate) {
      var pay = total / 60 * v.rate;
      steps.push('Pay: ' + dec2(total) + ' hours × ' + money(v.rate) + ' per hour = ' + money(pay) + ' (before taxes, rounded to the cent).');
      ans.push({ label: 'Pay before taxes:', value: money(pay) });
    }
    return { answers: ans, steps: steps };
  }

  var DAYS = [['mo', 'Monday'], ['tu', 'Tuesday'], ['we', 'Wednesday'], ['th', 'Thursday'], ['fr', 'Friday'], ['sa', 'Saturday'], ['su', 'Sunday']];
  function hoursWeek(v) {
    var hasRate = isNum(v.rate);
    if (hasRate && (v.rate < 0 || v.rate > 100000)) return err('Enter an hourly pay rate of 0 or more, or leave it empty.');
    var rows = [], total = 0, steps = [];
    for (var i = 0; i < DAYS.length; i++) {
      var k = DAYS[i][0], name = DAYS[i][1] + ': ';
      var st = String(v[k + 's'] == null ? '' : v[k + 's']).trim(), en = String(v[k + 'e'] == null ? '' : v[k + 'e']).trim();
      if (!st && !en) continue;
      if (!st || !en) return err(name + 'Enter both a start and an end time, or leave both empty for a day off.');
      var brk = cleanBreak(v[k + 'b']);
      if (!isNum(brk) || brk < 0 || brk > 1440 || !Number.isInteger(brk)) return err(name + 'Enter the break in whole minutes, or leave it empty.');
      var r = shiftMinutes(st, en, brk, name);
      if (r.error) return err(r.error);
      rows.push({ name: DAYS[i][1], r: r });
      total += r.mins;
      steps.push(DAYS[i][1] + ': ' + clockText(r.s) + ' to ' + clockText(r.e) + (r.overnight ? ' (past midnight)' : '') + (brk ? ', minus a ' + brk + '-minute break' : '') + ' = ' + hmText(r.mins) + ' (' + commas(r.mins) + ' minutes).');
    }
    if (!rows.length) return err('Enter a start and end time for at least one day.');
    steps.push('Add the days together: ' + rows.map(function (x) { return commas(x.r.mins); }).join(' + ') + ' = ' + commas(total) + ' minutes (' + hmText(total) + ').');
    steps.push('Decimal hours: ' + commas(total) + ' ÷ 60 = ' + dec2(total) + ' hours.');
    var ans = [
      { label: 'Total time worked:', value: hmText(total) },
      { label: 'Decimal hours:', value: dec2(total) },
      { label: 'Days worked:', value: String(rows.length) },
      { label: 'Average per day worked:', value: hmText(Math.round(total / rows.length)) }
    ];
    if (hasRate) {
      var pay;
      if (v.ot === 'yes' && total > 2400) {
        var reg = 2400, ot = total - 2400;
        pay = reg / 60 * v.rate + ot / 60 * v.rate * 1.5;
        steps.push('Overtime: the first 40 hours are paid at ' + money(v.rate) + ' and the ' + dec2(ot) + ' hours over 40 are paid at 1.5 times that rate (' + money(v.rate * 1.5) + ').');
        steps.push('Pay: 40 × ' + money(v.rate) + ' + ' + dec2(ot) + ' × ' + money(v.rate * 1.5) + ' = ' + money(pay) + ' (before taxes, rounded to the cent).');
        ans.push({ label: 'Regular hours:', value: '40' });
        ans.push({ label: 'Overtime hours:', value: dec2(ot) });
      } else {
        pay = total / 60 * v.rate;
        steps.push('Pay: ' + dec2(total) + ' hours × ' + money(v.rate) + ' per hour = ' + money(pay) + ' (before taxes, rounded to the cent).');
      }
      ans.push({ label: 'Pay before taxes:', value: money(pay) });
    }
    return { answers: ans, steps: steps };
  }

  /* ---------- Minutes to decimal hours (and back) ---------- */
  function dec2n(x) { return String(Number(x.toFixed(2))); }
  function minToDec(v) {
    var m = v.mins;
    if (!isNum(m) || m < 0 || m > 1000000) return err('Enter the minutes as a number from 0 to 1,000,000.');
    var exact = m / 60, steps = [];
    steps.push('Divide the minutes by 60, because there are 60 minutes in an hour: ' + commas(m) + ' ÷ 60 = ' + String(Number(exact.toFixed(6))) + '.');
    steps.push('Round to two decimal places, the way timesheets and payroll usually do: ' + dec2n(exact) + ' hours.');
    var ans = [{ label: 'Decimal hours:', value: dec2n(exact) }, { label: 'More precisely:', value: String(Number(exact.toFixed(4))) }];
    if (Number.isInteger(m)) {
      ans.push({ label: 'Same time as:', value: hmText(m) });
      if (m >= 60) steps.push(commas(m) + ' minutes is ' + hmText(m) + ', which is ' + Math.floor(m / 60) + ' + ' + dec2n((m % 60) / 60) + ' = ' + dec2n(exact) + ' hours.');
    }
    return { answers: ans, steps: steps };
  }
  function hmToDec(v) {
    var h = cleanBreak(v.h), m = cleanBreak(v.m);
    if (!isNum(h) || h < 0 || h > 100000) return err('Enter the hours as a number from 0 to 100,000, or leave it empty.');
    if (!isNum(m) || m < 0 || m > 1000000) return err('Enter the minutes as a number from 0 to 1,000,000, or leave it empty.');
    if (h === 0 && m === 0) return err('Enter some hours or some minutes.');
    var total = h * 60 + m, exact = total / 60, steps = [];
    steps.push('Turn the minutes into a fraction of an hour: ' + commas(m) + ' ÷ 60 = ' + String(Number((m / 60).toFixed(6))) + '.');
    steps.push('Add the whole hours: ' + commas(h) + ' + ' + String(Number((m / 60).toFixed(6))) + ' = ' + String(Number(exact.toFixed(6))) + '.');
    steps.push('Round to two decimal places: ' + dec2n(exact) + ' hours.');
    var ans = [{ label: 'Decimal hours:', value: dec2n(exact) }, { label: 'More precisely:', value: String(Number(exact.toFixed(4))) }];
    if (Number.isInteger(total)) ans.push({ label: 'Total minutes:', value: commas(total) });
    return { answers: ans, steps: steps };
  }
  function decToHm(v) {
    var d = v.dec;
    if (!isNum(d) || d < 0 || d > 100000) return err('Enter the decimal hours as a number from 0 to 100,000.');
    var whole = Math.floor(d + 1e-9), frac = d - whole, mins = Math.round(frac * 60), steps = [];
    if (mins === 60) { whole += 1; mins = 0; }
    steps.push('The whole number is the hours: ' + whole + '.');
    steps.push('Multiply the part after the decimal point by 60: ' + String(Number(frac.toFixed(6))) + ' × 60 = ' + String(Number((frac * 60).toFixed(4))) + ' minutes, which rounds to ' + mins + '.');
    var total = whole * 60 + mins;
    return { answers: [
      { label: 'Hours and minutes:', value: hmText(total) },
      { label: 'As h:mm:', value: whole + ':' + pad2(mins) },
      { label: 'Total minutes:', value: commas(total) }
    ], steps: steps };
  }

  var api = {
    percentOf: percentOf, percentIs: percentIs, percentChange: percentChange,
    fraction: fraction, linear: linear, quadratic: quadratic,
    pythagHyp: pythagHyp, pythagLeg: pythagLeg, slope: slope,
    gcdlcm: gcdlcm, stats: stats, trig: trig, trigAngle: trigAngle,
    derivative: derivative, integral: integral,
    inflationCpi: inflationCpi, inflationRate: inflationRate, cToF: cToF, fToC: fToC, timeCalc: timeCalc, hoursShift: hoursShift, hoursWeek: hoursWeek, parseClock: parseClock, minToDec: minToDec, hmToDec: hmToDec, decToHm: decToHm
  };
  root.CalcMath = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
