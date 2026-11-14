/* CalcProject.org electrical calculators (shared by each electrical calculator page). */

  let unitSystem='imperial';
  const $=id=>document.getElementById(id);
  const num=(id,d=0)=>{const v=parseFloat($(id).value);return isNaN(v)?d:v;};
  const fmt=(n,d=0)=>n.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
  const money=n=>'$'+fmt(n,2);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const line=(a,b)=>`<div class="result-line"><span>${a}</span><span>${b}</span></div>`;

  // ---- Electricity cost ----
  function calcElecCost(){
    const w=num('ec-watts'),h=Math.min(num('ec-hours'),24),d=Math.min(num('ec-days',30),31),r=num('ec-rate');
    const kwhDay=w/1000*h, costDay=kwhDay*r, costMonth=costDay*d, costYear=costMonth*12;
    $('ec-receipt').innerHTML=`<div class="label">Estimate</div>${line('Energy per day',fmt(kwhDay,2)+' kWh')}${line('Energy per month',fmt(kwhDay*d,1)+' kWh')}${line('Cost per day',money(costDay))}${line('Cost per year',money(costYear))}<div class="total"><span>Per month</span><span class="amount">${money(costMonth)}</span></div>`;
  }

  // ---- Watts & amps ----
  function waMode(){
    const m=$('wa-mode').value;
    $('wa-watts-wrap').style.display=m==='amps'?'':'none';
    $('wa-amps-wrap').style.display=m==='watts'?'':'none';
    calcWattsAmps();
  }
  function calcWattsAmps(){
    const m=$('wa-mode').value,v=parseFloat($('wa-volts').value);
    if(m==='amps'){
      const w=num('wa-watts'),a=v?w/v:0;
      $('wa-receipt').innerHTML=`<div class="label">Result</div>${line('Watts',fmt(w)+' W')}${line('Voltage',v+' V')}<div class="total"><span>Amps</span><span class="amount">${fmt(a,2)} A</span></div>`;
    }else{
      const a=num('wa-amps'),w=a*v;
      $('wa-receipt').innerHTML=`<div class="label">Result</div>${line('Amps',fmt(a,1)+' A')}${line('Voltage',v+' V')}${line('Kilowatts',fmt(w/1000,2)+' kW')}<div class="total"><span>Watts</span><span class="amount">${fmt(w)} W</span></div>`;
    }
  }

  // ---- Circuit load ----
  let devCount=0;
  function addDevice(name='',watts=''){
    devCount++;
    const row=document.createElement('div');row.className='room-row';
    row.innerHTML=`<div class="room-row-head"><span class="room-name">Device ${devCount}</span><button type="button" class="remove-room" onclick="this.closest('.room-row').remove();calcCircuit()">Remove</button></div>
      <div class="field-row"><div class="field"><label>Name</label><input type="text" class="cl-name" value="${esc(name)}" placeholder="e.g. Space heater" style="width:100%;padding:10px 12px;font-family:'IBM Plex Mono',monospace;font-size:0.95rem;border:1.5px solid rgba(42,42,40,0.25);border-radius:2px;"></div>
      <div class="field"><label>Watts</label><input type="number" class="cl-watts" min="0" step="1" value="${watts}"></div></div>`;
    $('cl-devices').appendChild(row);
  }
  function calcCircuit(){
    const b=parseFloat($('cl-breaker').value),v=parseFloat($('cl-volts').value);
    let total=0,lines='';
    document.querySelectorAll('#cl-devices .room-row').forEach((r,i)=>{
      const w=parseFloat(r.querySelector('.cl-watts').value)||0,n=r.querySelector('.cl-name').value.trim()||('Device '+(i+1));
      total+=w; if(w) lines+=line(esc(n),fmt(w)+' W');
    });
    const amps=total/v,limit=b*0.8,pct=amps/b*100;
    let status;
    if(amps>b) status='<span class="status-bad">Over the breaker. It will likely trip.</span>';
    else if(amps>limit) status='<span class="status-warn">OK for short use, but over the 80% limit for things that run 3+ hours.</span>';
    else status='<span class="status-ok">Within the safe range for this breaker.</span>';
    $('cl-receipt').innerHTML=`<div class="label">Circuit check</div>${lines}${line('Total watts',fmt(total)+' W')}${line('Breaker capacity',fmt(b*v)+' W')}${line('Steady-use limit (80%)',fmt(limit,1)+' A')}<div class="total"><span>Load</span><span class="amount">${fmt(amps,1)} A</span></div><p style="margin:10px 0 0;font-family:Inter,sans-serif;font-size:0.88rem">${fmt(pct)}% of the breaker. ${status}</p>`;
  }

  // ---- Wire size & voltage drop ----
  const GAUGES=['14','12','10','8','6','4','3','2','1','1/0','2/0'];
  const OHMS={cu:{'14':3.07,'12':1.93,'10':1.21,'8':0.764,'6':0.491,'4':0.308,'3':0.245,'2':0.194,'1':0.154,'1/0':0.122,'2/0':0.0967},
              al:{'12':3.18,'10':2.00,'8':1.26,'6':0.808,'4':0.508,'3':0.403,'2':0.319,'1':0.253,'1/0':0.201,'2/0':0.159}};
  const AMPACITY={cu:{'14':15,'12':20,'10':30,'8':40,'6':55,'4':70,'3':85,'2':95,'1':110,'1/0':125,'2/0':145},
                  al:{'12':15,'10':25,'8':35,'6':40,'4':55,'3':65,'2':75,'1':85,'1/0':100,'2/0':115}};
  function drop(metal,g,amps,len){return 2*len*(OHMS[metal][g]/1000)*amps;}
  function calcWire(){
    const amps=num('ws-amps'),v=parseFloat($('ws-volts').value),len=num('ws-length')/(unitSystem==='metric'?0.3048:1),metal=$('ws-metal').value,g=$('ws-gauge').value;
    let out='<div class="label">Your wire</div>';
    if(!OHMS[metal][g]){
      out+=`<p style="margin:8px 0;font-family:Inter,sans-serif;font-size:0.9rem">${g} AWG aluminum isn't used for branch circuits. Pick 12 AWG or larger.</p>`;
    }else{
      const vd=drop(metal,g,amps,len),pct=vd/v*100,rated=amps<=AMPACITY[metal][g];
      out+=line('Voltage drop',fmt(vd,2)+' V')+line('Drop percent',`<span class="${pct<=3?'status-ok':pct<=5?'status-warn':'status-bad'}">${fmt(pct,1)}%</span>`)+line('Voltage at the load',fmt(v-vd,1)+' V')+line('Rated for your amps?',rated?'<span class="status-ok">Yes</span>':'<span class="status-bad">No, too small</span>');
    }
    const best=GAUGES.find(x=>OHMS[metal][x]&&amps<=AMPACITY[metal][x]&&drop(metal,x,amps,len)/v*100<=3);
    out+=`<div class="total"><span>Smallest wire for &le;3% drop</span><span class="amount">${best?best+' AWG':'Larger than 2/0'}</span></div>`;
    out+=`<p style="margin:10px 0 0;font-family:Inter,sans-serif;font-size:0.82rem;color:var(--graphite-soft)">${metal==='cu'?'Copper':'Aluminum'} wire, ${unitSystem==='metric'?fmt(len*0.3048,1)+' m':fmt(len)+' ft'} one way. Drop over 3% can make motors run hot and lights dim.</p>`;
    $('ws-receipt').innerHTML=out;
  }

  // ---- Generator size ----
  const GEN=[
    ['Refrigerator',700,2200,true],['Chest freezer',500,1500,false],['Sump pump (1/2 hp)',1050,2150,true],
    ['Well pump (1/2 hp)',1000,2100,false],['Furnace fan (1/2 hp)',800,2350,false],['Window AC (10,000 BTU)',1200,3600,false],
    ['Space heater',1500,1500,false],['Microwave',1000,1000,false],['Coffee maker',1000,1000,false],
    ['Washing machine',1150,2250,false],['Electric water heater',4000,4000,false],['Lights (about 10 LED bulbs)',100,100,true],
    ['TV',200,200,true],['Wi-Fi router and modem',50,50,true],['Phone and laptop charging',100,100,false],['CPAP machine',60,60,false]
  ];
  function buildGen(){
    $('gen-list').innerHTML=GEN.map((g,i)=>`<label class="gen-item"><input type="checkbox" id="gen-${i}" ${g[3]?'checked':''} onchange="calcGenerator()"><span>${g[0]} <span class="w">${fmt(g[1])} W${g[2]>g[1]?' / '+fmt(g[2])+' start':''}</span></span><input type="number" id="genq-${i}" min="1" step="1" value="1" aria-label="How many ${g[0]}" oninput="calcGenerator()"></label>`).join('');
  }
  function calcGenerator(){
    let run=0,surge=0,count=0;
    GEN.forEach((g,i)=>{if($('gen-'+i).checked){const q=Math.max(1,parseInt($('genq-'+i).value)||1);run+=g[1]*q;surge=Math.max(surge,g[2]-g[1]);count+=q;}});
    const cw=num('gen-cw'),cs=num('gen-cs');
    if(cw>0){run+=cw;surge=Math.max(surge,Math.max(cs-cw,0));count++;}
    const start=run+surge,recRun=Math.ceil(run*1.2/100)*100,recStart=Math.ceil(start*1.2/100)*100;
    $('gen-receipt').innerHTML=`<div class="label">Estimate</div>${line('Items selected',count)}${line('Total running watts',fmt(run)+' W')}${line('Biggest startup jump',fmt(surge)+' W')}${line('Starting watts needed',fmt(start)+' W')}<div class="total"><span>Look for about</span><span class="amount">${fmt(recRun)} W</span></div><p style="margin:10px 0 0;font-family:Inter,sans-serif;font-size:0.85rem">Running watts, with at least <b>${fmt(recStart)} W</b> starting (peak) watts. Numbers include about 20% headroom.</p>`;
  }

  function recalcAll(){ if($('ec-receipt')) calcElecCost(); if($('wa-receipt')) calcWattsAmps(); if($('cl-receipt')) calcCircuit(); if($('ws-receipt')) calcWire(); if($('gen-receipt')) calcGenerator(); }

  window.addEventListener('DOMContentLoaded',()=>{
    if($('cl-devices')){ addDevice('Space heater',1500); addDevice('TV',100); addDevice('Lamp',60); }
    if($('gen-list')) buildGen(); recalcAll();
    document.querySelectorAll('.calc-inputs input, .calc-inputs select').forEach(el=>el.addEventListener('change',recalcAll));
    if($('cl-devices')) $('cl-devices').addEventListener('input',calcCircuit);
  });

  const tickets=document.querySelectorAll('.ticket');
  if('IntersectionObserver' in window){
    const obs=new IntersectionObserver((entries)=>{ entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('visible'); obs.unobserve(e.target); } }); }, {threshold:0.15});
    tickets.forEach(t=>obs.observe(t));
  } else { tickets.forEach(t=>t.classList.add('visible')); }

  window.addEventListener('scroll', ()=>{
    const btn=document.getElementById('back-to-top'); if(!btn) return;
    if(window.scrollY>400){ btn.classList.add('show'); } else { btn.classList.remove('show'); }
  });
  // ---- Feet / meters switch (wire distance) ----
  function setUnitSystem(sys){
    if(sys===unitSystem) return;
    const inp=$('ws-length'), v=parseFloat(inp.value);
    if(!isNaN(v)) inp.value = sys==='metric' ? Math.round(v*0.3048*10)/10 : Math.round(v/0.3048);
    unitSystem=sys;
    $('ws-length-unit').textContent = sys==='metric' ? '(meters, from the panel to the load)' : '(feet, from the panel to the load)';
    document.querySelectorAll('[data-unit-btn]').forEach(b=>{
      const on=b.dataset.unitBtn===sys; b.classList.toggle('active',on); b.setAttribute('aria-pressed',on?'true':'false');
    });
    calcWire();
  }

  // ---- Save / print my results ----
  const sessionUsed = new Set();
  const calcTickets = [...document.querySelectorAll('.ticket')].filter(t=>t.querySelector('.calc-btn'));
  function shortName(t){ return t.querySelector('.ticket-head h2').textContent.replace(/\s*Calculator\s*$/,'').trim(); }
  function cleanText(el){
    const c=el.cloneNode(true);
    c.querySelectorAll('.hint:not(.u)').forEach(h=>h.remove());
    return c.textContent.replace(/\s+/g,' ').trim();
  }
  function markUsed(t){ sessionUsed.add(t.id); }
  function addRow(tbody,label,value,cls){
    const tr=document.createElement('tr'); if(cls) tr.className=cls;
    const a=document.createElement('td'); a.textContent=label;
    const b=document.createElement('td'); b.textContent=value;
    tr.append(a,b); tbody.appendChild(tr);
  }
  function makeCol(title){
    const col=document.createElement('div');
    const h=document.createElement('p'); h.className='ps-col-title'; h.textContent=title;
    const table=document.createElement('table'), tbody=document.createElement('tbody');
    table.appendChild(tbody); col.append(h,table);
    return {col,tbody};
  }
  function fieldValue(el){
    if(el.tagName==='SELECT') return el.options[el.selectedIndex] ? el.options[el.selectedIndex].text.replace(/\s*\(.*\)\s*$/,'') : '';
    return el.value==='' ? '—' : el.value;
  }

  function buildSheet(){
    recalcAll();
    const sheet=$('print-sheet'); sheet.innerHTML='';
    const date=new Date().toLocaleDateString(undefined,{year:'numeric',month:'long',day:'numeric'});
    const head=document.createElement('div'); head.className='ps-head';
    head.innerHTML=`<div class="ps-brand"><img src="logo-header.png" alt="" onerror="this.remove()"><div><p class="ps-title">CalcProject.org</p><p class="ps-site" id="ps-project"></p></div></div><div class="ps-meta"><strong>${date}</strong>Electrical estimate</div>`;
    sheet.appendChild(head);
    const projectName=$('project-name').value.trim();
    $('ps-project').textContent = projectName || 'My electrical estimate';
    if(!window._origTitle) window._origTitle=document.title;
    document.title='CalcProject.org - '+(projectName || 'My electrical estimate');

    const warn=document.createElement('p'); warn.className='ps-warn';
    warn.textContent='Estimates only. Electrical code varies by city, county, and state. Check your local code and use a licensed electrician for any wiring work.';
    sheet.appendChild(warn);

    calcTickets.filter(t=>sessionUsed.has(t.id)).forEach(t=>{
      const box=document.createElement('section'); box.className='ps-calc';
      const h=document.createElement('h2'); h.textContent=t.querySelector('.ticket-head h2').textContent.trim();
      const grid=document.createElement('div'); grid.className='ps-grid';
      const inp=makeCol('What you entered'), res=makeCol('Results');
      const inputs=t.querySelector('.calc-inputs');

      // Generator checklist
      inputs.querySelectorAll('.gen-item').forEach(item=>{
        const cb=item.querySelector('input[type=checkbox]'); if(!cb || !cb.checked) return;
        const i=parseInt(cb.id.replace('gen-',''),10);
        const q=item.querySelector('input[type=number]');
        addRow(inp.tbody, GEN[i] ? GEN[i][0] : 'Item', '× ' + (q ? (parseInt(q.value)||1) : 1));
      });
      // Circuit devices
      inputs.querySelectorAll('.room-row').forEach((row,i)=>{
        const n=row.querySelector('.cl-name'), w=row.querySelector('.cl-watts');
        if(!w) return;
        addRow(inp.tbody, (n && n.value.trim()) || ('Device '+(i+1)), (w.value||'0')+' W');
      });
      // Normal fields
      inputs.querySelectorAll('.field').forEach(f=>{
        if(f.closest('.room-row') || f.closest('.gen-item')) return;
        if(f.offsetParent===null && f.style.display==='none') return;
        if(f.closest('[style*="display: none"], [style*="display:none"]')) return;
        const el=f.querySelector('input, select'), label=f.querySelector('label');
        if(!el || !label) return;
        if((el.id==='gen-cw' || el.id==='gen-cs') && !(parseFloat(el.value)>0)) return;
        addRow(inp.tbody, cleanText(label), fieldValue(el));
      });

      const receipt=t.querySelector('.receipt');
      receipt.querySelectorAll('.result-line, .total').forEach(line=>{
        const kids=[...line.children].filter(c=>c.tagName==='SPAN');
        if(kids.length>=2) addRow(res.tbody, kids[0].textContent, kids[kids.length-1].textContent, line.classList.contains('total')?'ps-buy':'');
      });
      grid.append(inp.col,res.col);
      box.append(h,grid);
      receipt.querySelectorAll('p').forEach(p=>{
        const n=document.createElement('p'); n.className='ps-note'; n.textContent=p.textContent.replace(/\s+/g,' ').trim(); box.appendChild(n);
      });
      const tw=t.querySelector('.ticket-warn');
      if(tw){ const n=document.createElement('p'); n.className='ps-note'; n.textContent=tw.textContent.replace(/^\W+/,'').trim(); box.appendChild(n); }
      sheet.appendChild(box);
    });

    const notes=document.createElement('div'); notes.className='ps-notes';
    notes.innerHTML='<p class="ps-col-title">Notes for your electrician</p>'+'<div class="ps-line"></div>'.repeat(3);
    const foot=document.createElement('p'); foot.className='ps-foot';
    foot.textContent='These calculators give general estimates for planning only and may not account for every factor in your situation. Working with electricity can cause serious injury, death, or fire.';
    const back=document.createElement('p'); back.className='ps-comeback'; back.textContent='Free calculators anytime at CalcProject.org';
    const end=document.createElement('div'); end.className='ps-end'; end.append(notes,foot,back);
    sheet.appendChild(end);
  }

  function doPrint(){
    buildSheet();
    if(typeof gtag==='function') gtag('event','save_or_print',{calculators:sessionUsed.size, page:'advanced'});
    window.print();
  }
  function saveOrPrint(){
    const dlg=$('save-dialog');
    $('sd-on').textContent='On your sheet: '+calcTickets.filter(t=>sessionUsed.has(t.id)).map(shortName).join(', ');
    if(!dlg || typeof dlg.showModal!=='function'){ doPrint(); return; }
    dlg.showModal(); $('project-name').focus();
  }
  $('sd-cancel').addEventListener('click',()=>$('save-dialog').close());
  $('sd-print').addEventListener('click',()=>{ $('save-dialog').close(); doPrint(); });
  $('project-name').addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); $('sd-print').click(); } });
  $('save-dialog').addEventListener('click',e=>{ if(e.target.id==='save-dialog') e.target.close(); });

  calcTickets.forEach(t=>{
    if(t.id==='wire-size'){
      const stamp=t.querySelector('.ticket-head .stamp');
      const side=document.createElement('div'); side.className='ticket-side';
      stamp.replaceWith(side); side.appendChild(stamp);
      const sw=document.createElement('div'); sw.className='ticket-units'; sw.setAttribute('role','group'); sw.setAttribute('aria-label','Distance units');
      [['imperial','Feet'],['metric','Meters']].forEach(([sys,lbl])=>{
        const b=document.createElement('button'); b.type='button'; b.dataset.unitBtn=sys; b.textContent=lbl;
        const on=unitSystem===sys; b.classList.toggle('active',on); b.setAttribute('aria-pressed',on?'true':'false');
        b.addEventListener('click',()=>setUnitSystem(sys)); sw.appendChild(b);
      });
      side.appendChild(sw);
    }
    const btn=t.querySelector('.calc-btn');
    t.addEventListener('input',()=>markUsed(t));
    t.addEventListener('change',()=>markUsed(t));
    btn.addEventListener('click',()=>markUsed(t));
    const save=document.createElement('button'); save.type='button'; save.className='btn-outline save-ticket-btn'; save.textContent='Save or print results';
    save.addEventListener('click',()=>{ markUsed(t); saveOrPrint(); });
    btn.insertAdjacentElement('afterend',save);
  });
  window.addEventListener('beforeprint',buildSheet);
  window.addEventListener('afterprint',()=>{ if(window._origTitle) document.title=window._origTitle; });
