/* CalcProject.org calculator engine.
   Each calculator page sets window.CP_CALC = { id, title, calc(v) } before this file loads.
   calc(v) gets every input in imperial units and returns
   { rows: [[label, value, unit, decimals, 'imp'?]], total: [label, value, unit, decimals], note: 'optional text' }.
   This file handles reading inputs, the Imperial/Metric switch, the result receipt,
   and the Save or print sheet (which collects every calculator used in one visit). */
(function () {
  'use strict';
  var cfg = window.CP_CALC;
  if (!cfg) return;

  var U = CPCore.U;
  window.CPH = CPCore.H;
  var STORE_UNITS = 'cp-units', STORE_SHEET = 'cp-sheet';
  var sys = 'imperial';
  var used = false;
  var box = document.getElementById('calc');
  var receipt = document.getElementById('receipt');
  if (!box || !receipt) return;

  function $(id) { return document.getElementById(id); }
  function store(kind) { try { return kind === 'local' ? window.localStorage : window.sessionStorage; } catch (e) { return null; } }
  function getItem(kind, key) { try { var s = store(kind); return s ? s.getItem(key) : null; } catch (e) { return null; } }
  function setItem(kind, key, val) { try { var s = store(kind); if (s) s.setItem(key, val); } catch (e) {} }

  function show(row) { return CPCore.show(row, sys); }

  function fields() { return box.querySelectorAll('.calc-inputs input[id], .calc-inputs select[id]'); }
  function key(id) { return id.slice(id.indexOf('-') + 1); }

  // The value of one input in imperial units. After a unit switch the box shows a rounded number,
  // so the exact value is remembered and used until the visitor types something different.
  function imperial(el, n) {
    if (!el.dataset.factor) return n;
    if (el._shown !== undefined && el.value === el._shown) return el._exact;
    return sys === 'metric' ? n / parseFloat(el.dataset.factor) : n;
  }

  function readValues() {
    var v = {};
    fields().forEach(function (el) {
      var raw = el.value, n = parseFloat(raw);
      if (el.tagName !== 'SELECT' && el.type !== 'number') { v[key(el.id)] = raw; return; }
      if (el.tagName === 'SELECT' && (isNaN(n) || String(n) !== raw)) { v[key(el.id)] = raw; return; }
      if (isNaN(n)) n = 0;
      v[key(el.id)] = imperial(el, n);
    });
    var rooms = box.querySelectorAll('#rooms .room-row');
    if (rooms.length) {
      v.rooms = [];
      rooms.forEach(function (r) {
        var a = r.querySelector('.room-length'), b = r.querySelector('.room-width');
        v.rooms.push([imperial(a, parseFloat(a.value) || 0), imperial(b, parseFloat(b.value) || 0)]);
      });
    }
    return v;
  }

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  var last = null;
  function calculate() {
    var r;
    try { r = cfg.calc(readValues()); } catch (e) { r = null; }
    if (!r || !r.total) { receipt.innerHTML = '<div class="label">Check your numbers</div><p class="receipt-note">Enter a value in every box to see the result.</p>'; return; }
    var rows = (r.rows || []).filter(function (row) { return !(row[4] === 'imp' && sys === 'metric'); });
    var h = '<div class="label">' + esc(cfg.label || 'Estimate') + '</div>';
    rows.forEach(function (row) { h += '<div class="result-line"><span>' + esc(row[0]) + '</span><span>' + esc(show(row)) + '</span></div>'; });
    h += '<div class="total"><span>' + esc(r.total[0]) + '</span><span class="amount">' + esc(show(r.total)) + '</span></div>';
    if (r.note) h += '<p class="receipt-note">' + esc(r.note) + '</p>';
    receipt.innerHTML = h;
    last = { rows: rows.map(function (row) { return [row[0], show(row)]; }), total: [r.total[0], show(r.total)], note: r.note || '' };
    if (used) saveToSheet();
  }

  // ---- Imperial / Metric ----
  function setUnits(next, quiet) {
    if (next === sys) return;
    var toMetric = next === 'metric';
    box.querySelectorAll('input[data-factor]').forEach(function (inp) {
      var f = parseFloat(inp.dataset.factor), val = parseFloat(inp.value);
      if (isNaN(val)) return;
      var exact = imperial(inp, val);                    // exact imperial value before the switch
      var shown = toMetric ? exact * f : exact;
      inp.value = String(Math.round(shown * 100) / 100);
      inp._exact = exact; inp._shown = inp.value;
    });
    sys = next;
    document.querySelectorAll('.u').forEach(function (el) { el.innerHTML = toMetric ? el.dataset.met : el.dataset.imp; });
    document.querySelectorAll('[data-unit-btn]').forEach(function (b) {
      var on = b.dataset.unitBtn === next;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (!quiet) setItem('local', STORE_UNITS, next);
    calculate();
  }

  // ---- Room rows (square footage calculator) ----
  function renumber() {
    box.querySelectorAll('#rooms .room-row').forEach(function (row, i) { row.querySelector('.room-name').textContent = 'Room ' + (i + 1); });
  }
  window.addRoomRow = function () {
    var wrap = $('rooms'); if (!wrap) return;
    var metric = sys === 'metric', def = metric ? (10 * 0.3048).toFixed(2) : 10, lab = metric ? 'm' : 'ft';
    var row = document.createElement('div');
    row.className = 'room-row';
    row.innerHTML = '<div class="room-row-head"><span class="room-name"></span><button type="button" class="remove-room" onclick="removeRoom(this)">Remove</button></div>' +
      '<div class="field-row">' +
      '<div class="field"><label>Length (<span class="u" data-imp="ft" data-met="m">' + lab + '</span>)</label><input type="number" class="room-length" min="0" step="0.1" value="' + def + '" data-factor="0.3048"></div>' +
      '<div class="field"><label>Width (<span class="u" data-imp="ft" data-met="m">' + lab + '</span>)</label><input type="number" class="room-width" min="0" step="0.1" value="' + def + '" data-factor="0.3048"></div>' +
      '</div>';
    wrap.appendChild(row);
    renumber(); markUsed(); calculate();
  };
  window.removeRoom = function (btn) {
    var wrap = $('rooms');
    if (!wrap || wrap.querySelectorAll('.room-row').length <= 1) return;
    btn.closest('.room-row').remove();
    renumber(); markUsed(); calculate();
  };

  // ---- Save or print sheet ----
  function readSheet() {
    try { var s = JSON.parse(getItem('session', STORE_SHEET) || '[]'); return Array.isArray(s) ? s : []; } catch (e) { return []; }
  }
  function writeSheet(list) { setItem('session', STORE_SHEET, JSON.stringify(list)); }
  function labelText(el) {
    var c = el.cloneNode(true);
    c.querySelectorAll('.hint:not(.u)').forEach(function (hint) { hint.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  function currentInputs() {
    var out = [];
    box.querySelectorAll('.calc-inputs .field').forEach(function (f) {
      var el = f.querySelector('input, select'), label = f.querySelector('label');
      if (!el || !label) return;
      var room = f.closest('.room-row');
      var prefix = room ? room.querySelector('.room-name').textContent.trim() + ' ' : '';
      var val = el.tagName === 'SELECT' ? (el.options[el.selectedIndex] ? el.options[el.selectedIndex].text : '') : (el.value === '' ? '—' : el.value);
      out.push([prefix + labelText(label), val]);
    });
    return out;
  }
  function entry() {
    return { id: cfg.id, title: cfg.title, units: sys, inputs: currentInputs(), rows: last ? last.rows : [], total: last ? last.total : ['', ''] };
  }
  function saveToSheet() {
    var list = readSheet().filter(function (e) { return e && e.id !== cfg.id; });
    list.push(entry());
    writeSheet(list);
  }
  function markUsed() { used = true; }

  function addRow(tbody, a, b, cls) {
    var tr = document.createElement('tr'); if (cls) tr.className = cls;
    var x = document.createElement('td'); x.textContent = a;
    var y = document.createElement('td'); y.textContent = b;
    tr.appendChild(x); tr.appendChild(y); tbody.appendChild(tr);
  }
  function makeCol(title) {
    var col = document.createElement('div');
    var h = document.createElement('p'); h.className = 'ps-col-title'; h.textContent = title;
    var table = document.createElement('table'), tbody = document.createElement('tbody');
    table.appendChild(tbody); col.appendChild(h); col.appendChild(table);
    return { col: col, tbody: tbody };
  }
  function sheetEntries() {
    var list = readSheet();
    if (!list.some(function (e) { return e.id === cfg.id; })) list.push(entry());
    return list;
  }
  function buildSheet() {
    calculate();
    var sheet = $('print-sheet'); if (!sheet) return;
    sheet.innerHTML = '';
    var date = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
    var name = ($('project-name').value || '').trim() || 'My project estimate';
    var head = document.createElement('div'); head.className = 'ps-head';
    head.innerHTML = '<div class="ps-brand"><img src="logo-header.png" alt="" onerror="this.remove()"><div><p class="ps-title">CalcProject.org</p><p class="ps-site" id="ps-project"></p></div></div><div class="ps-meta"><strong></strong></div>';
    sheet.appendChild(head);
    $('ps-project').textContent = name;
    head.querySelector('.ps-meta strong').textContent = date;
    if (!window._origTitle) window._origTitle = document.title;
    document.title = 'CalcProject.org - ' + name;
    sheetEntries().forEach(function (e) {
      var sec = document.createElement('section'); sec.className = 'ps-calc';
      var h = document.createElement('h2'); h.textContent = e.title + (e.units === 'metric' ? ' (metric)' : '');
      var grid = document.createElement('div'); grid.className = 'ps-grid';
      var a = makeCol('What you entered'), b = makeCol('Results');
      (e.inputs || []).forEach(function (r) { addRow(a.tbody, r[0], r[1]); });
      (e.rows || []).forEach(function (r) { addRow(b.tbody, r[0], r[1]); });
      if (e.total) addRow(b.tbody, e.total[0], e.total[1], 'ps-buy');
      grid.appendChild(a.col); grid.appendChild(b.col);
      sec.appendChild(h); sec.appendChild(grid); sheet.appendChild(sec);
    });
    var end = document.createElement('div'); end.className = 'ps-end';
    end.innerHTML = '<div class="ps-notes"><p class="ps-col-title">Notes, prices &amp; store</p><div class="ps-line"></div><div class="ps-line"></div><div class="ps-line"></div></div>' +
      '<p class="ps-foot">Estimates are a starting point for shopping, not a substitute for a contractor\'s exact measurement. Always round up and keep your receipt for returns.</p>' +
      '<p class="ps-comeback">Free calculators anytime at CalcProject.org</p>';
    sheet.appendChild(end);
  }
  function doPrint() {
    buildSheet();
    if (typeof window.gtag === 'function') window.gtag('event', 'save_or_print', { calculators: sheetEntries().length });
    window.print();
  }
  function openSave() {
    markUsed(); calculate();
    var dlg = $('save-dialog');
    $('sd-on').textContent = 'On your sheet: ' + sheetEntries().map(function (e) { return e.title.replace(/\s*Calculator\s*$/, ''); }).join(', ');
    if (!dlg || typeof dlg.showModal !== 'function') { doPrint(); return; }
    dlg.showModal();
    $('project-name').focus();
  }

  // ---- Wire everything up ----
  function init() {
    box.querySelectorAll('[data-unit-btn]').forEach(function (b) {
      b.addEventListener('click', function () { setUnits(b.dataset.unitBtn); });
    });
    box.addEventListener('input', function () { markUsed(); calculate(); });
    box.addEventListener('change', function () { markUsed(); calculate(); });
    var btn = box.querySelector('.calc-btn');
    if (btn) btn.addEventListener('click', function () {
      markUsed(); calculate();
      if (typeof window.gtag === 'function') window.gtag('event', 'calculate', { calculator: cfg.id });
    });
    var save = box.querySelector('.save-ticket-btn');
    if (save) save.addEventListener('click', openSave);
    if ($('sd-cancel')) $('sd-cancel').addEventListener('click', function () { $('save-dialog').close(); });
    if ($('sd-print')) $('sd-print').addEventListener('click', function () { $('save-dialog').close(); doPrint(); });
    if ($('sd-clear')) $('sd-clear').addEventListener('click', function () {
      writeSheet([]); used = true; saveToSheet();
      $('sd-on').textContent = 'On your sheet: ' + cfg.title.replace(/\s*Calculator\s*$/, '');
    });
    if ($('project-name')) $('project-name').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); $('sd-print').click(); }
    });
    if ($('save-dialog')) $('save-dialog').addEventListener('click', function (e) { if (e.target.id === 'save-dialog') e.target.close(); });
    window.addEventListener('beforeprint', buildSheet);
    window.addEventListener('afterprint', function () { if (window._origTitle) document.title = window._origTitle; });
    if (box.querySelector('[data-unit-btn]') && getItem('local', STORE_UNITS) === 'metric') setUnits('metric', true); else calculate();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
