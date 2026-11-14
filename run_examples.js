// Runs every calculator with its starting numbers and prints the formatted results as JSON.
const fs = require('fs');
const Core = require('./calc-core.js');
const specs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const s of specs) {
  try {
    const R = (rows, total, note) => ({ rows, total, note: note || '' });
    const f = new Function('v', 'H', 'R', s.js);
    const r = f(s.v, Core.H, R);
    const bad = [];
    const rows = (r.rows || []).map(x => { const t = Core.show(x, 'imperial'); if (/—|NaN|undefined|Infinity/.test(t)) bad.push(x[0]); return [x[0], t]; });
    const tt = Core.show(r.total, 'imperial'); if (/—|NaN|undefined|Infinity/.test(tt)) bad.push(r.total[0]);
    out[s.id] = { rows, total: [r.total[0], tt], note: r.note || '', bad };
  } catch (e) { out[s.id] = { error: String(e) }; }
}
console.log(JSON.stringify(out));
