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
    var all = [n1, d1, n2, d2];
    for (var i = 0; i < 4; i++) {
      if (!isNum(all[i]) || !Number.isInteger(all[i])) return err('Use whole numbers for the tops and bottoms of both fractions.');
    }
    if (d1 === 0 || d2 === 0) return err('A denominator (the bottom number) cannot be 0.');
    if (d1 < 0) { n1 = -n1; d1 = -d1; }
    if (d2 < 0) { n2 = -n2; d2 = -d2; }
    var f1 = n1 + '/' + d1, f2 = n2 + '/' + d2, steps = [], rn, rd;

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

  var api = {
    percentOf: percentOf, percentIs: percentIs, percentChange: percentChange,
    fraction: fraction, linear: linear, quadratic: quadratic,
    pythagHyp: pythagHyp, pythagLeg: pythagLeg, slope: slope,
    gcdlcm: gcdlcm, stats: stats, trig: trig, trigAngle: trigAngle,
    derivative: derivative, integral: integral
  };
  root.CalcMath = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
