/* CalcProject.org math calculators (page logic shared by each math calculator page; the math itself is in math-engine.js). */

  const FN={"linear": {"l": "linear"}, "quadratic": {"q": "quadratic"}, "slope": {"m": "slope"}, "derivative": {"d": "derivative"}, "integral": {"i": "integral"}, "pythagorean": {"h": "pythagHyp", "l": "pythagLeg"}, "trig": {"s": "trig", "a": "trigAngle"}, "percent": {"of": "percentOf", "is": "percentIs", "chg": "percentChange"}, "fraction": {"f": "fraction"}, "gcf-lcm": {"g": "gcdlcm"}, "statistics": {"s": "stats"}};
  const $=id=>document.getElementById(id);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const tickets=[...document.querySelectorAll('.ticket[data-tid]')];
  const used=new Set();

  function mode(t){ const s=t.querySelector('.mode-sel'); return s?s.value:Object.keys(FN[t.dataset.tid])[0]; }
  function showMode(t){
    const m=mode(t);
    t.querySelectorAll('.field[data-mode]').forEach(f=>{ f.style.display=(f.dataset.mode===m)?'':'none'; });
  }
  function values(t){
    const m=mode(t), v={};
    t.querySelectorAll('.field').forEach(f=>{
      if(f.dataset.mode && f.dataset.mode!==m) return;
      const el=f.querySelector('[data-f]'); if(!el) return;
      const raw=el.value.trim();
      v[el.dataset.f]=(el.tagName==='SELECT'||el.type==='text')?raw:(raw===''?NaN:Number(raw));
    });
    return v;
  }
  function solve(t){
    const fn=FN[t.dataset.tid][mode(t)], r=window.CalcMath[fn](values(t));
    const rc=t.querySelector('[data-receipt]'), st=t.querySelector('[data-steps]');
    if(r.error){
      rc.innerHTML='<div class="label">Check your numbers</div><div class="err">'+esc(r.error)+'</div>';
      st.style.display='none'; st.innerHTML=''; t._last=null; return;
    }
    const first=r.answers[0], rest=r.answers.slice(1);
    let h='<div class="label">Your answer</div><div class="total"><span>'+esc(first.label)+'</span><span class="amount">'+esc(first.value)+'</span></div>';
    rest.forEach(a=>{ h+='<div class="result-line"><span>'+esc(a.label)+'</span><span>'+esc(a.value)+'</span></div>'; });
    rc.innerHTML=h;
    st.innerHTML='<h3>Step-by-step solution</h3><ol>'+r.steps.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ol>';
    st.style.display='block';
    t._last={inputs:inputsText(t),answers:r.answers,steps:r.steps,mode:mode(t)};
    used.add(t.id);
    if(typeof gtag==='function') gtag('event','math_solve',{calculator:t.id});
  }
  function inputsText(t){
    const m=mode(t), rows=[];
    const s=t.querySelector('.mode-sel'); if(s) rows.push(['Finding',s.options[s.selectedIndex].text]);
    t.querySelectorAll('.field').forEach(f=>{
      if(f.dataset.mode && f.dataset.mode!==m) return;
      const el=f.querySelector('[data-f]'); if(!el) return;
      const lab=f.querySelector('label').childNodes[0].textContent.trim();
      rows.push([lab, el.tagName==='SELECT'?el.options[el.selectedIndex].text:(el.value||'—')]);
    });
    return rows;
  }
  tickets.forEach(t=>{
    showMode(t);
    const s=t.querySelector('.mode-sel'); if(s) s.addEventListener('change',()=>{ showMode(t); });
    t.querySelector('[data-solve]').addEventListener('click',()=>solve(t));
    t.querySelectorAll('input').forEach(i=>i.addEventListener('keydown',e=>{ if(e.key==='Enter') solve(t); }));
    t.querySelector('[data-save]').addEventListener('click',()=>{ solve(t); saveOrPrint(); });
  });

  // ---- Save / print ----
  function buildSheet(){
    const sheet=$('print-sheet'); sheet.innerHTML='';
    const date=new Date().toLocaleDateString(undefined,{year:'numeric',month:'long',day:'numeric'});
    const name=$('project-name').value.trim();
    const head=document.createElement('div'); head.className='ps-head';
    head.innerHTML='<div class="ps-brand"><img src="logo-header.png" alt="" onerror="this.remove()"><div><p class="ps-title">CalcProject.org</p><p class="ps-site">'+esc(name||'My math solutions')+'</p></div></div><div class="ps-meta"><strong>'+date+'</strong>Math solutions</div>';
    sheet.appendChild(head);
    if(!window._origTitle) window._origTitle=document.title;
    document.title='CalcProject.org - '+(name||'My math solutions');
    tickets.filter(t=>used.has(t.id)&&t._last).forEach(t=>{
      const box=document.createElement('section'); box.className='ps-calc';
      const h=document.createElement('h2'); h.textContent=t.querySelector('.ticket-head h2').textContent.trim(); box.appendChild(h);
      const grid=document.createElement('div'); grid.className='ps-grid';
      const mk=(title,rows,total)=>{
        const col=document.createElement('div');
        col.innerHTML='<p class="ps-col-title">'+title+'</p>';
        const tb=document.createElement('table'), body=document.createElement('tbody'); tb.appendChild(body);
        rows.forEach((r,i)=>{ const tr=document.createElement('tr'); if(total&&i===0) tr.className='ps-buy'; const a=document.createElement('td'); a.textContent=r[0]; const b=document.createElement('td'); b.textContent=r[1]; tr.append(a,b); body.appendChild(tr); });
        col.appendChild(tb); return col;
      };
      grid.append(mk('What you entered',t._last.inputs,false), mk('Answer',t._last.answers.map(a=>[a.label,a.value]),true));
      box.appendChild(grid);
      const ol=document.createElement('ol'); ol.className='ps-steps';
      t._last.steps.forEach(s=>{ const li=document.createElement('li'); li.textContent=s; ol.appendChild(li); });
      box.appendChild(ol); sheet.appendChild(box);
    });
    const back=document.createElement('p'); back.className='ps-comeback'; back.textContent='Free math calculators with steps at CalcProject.org';
    sheet.appendChild(back);
  }
  function doPrint(){ buildSheet(); window.print(); }
  function saveOrPrint(){
    const dlg=$('save-dialog');
    $('sd-on').textContent='On your sheet: '+tickets.filter(t=>used.has(t.id)&&t._last).map(t=>t.querySelector('.ticket-head h2').textContent.trim()).join(', ');
    if(!dlg||typeof dlg.showModal!=='function'){ doPrint(); return; }
    dlg.showModal(); $('project-name').focus();
  }
  $('sd-cancel').addEventListener('click',()=>$('save-dialog').close());
  $('sd-print').addEventListener('click',()=>{ $('save-dialog').close(); doPrint(); });
  $('project-name').addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); $('sd-print').click(); } });
  window.addEventListener('afterprint',()=>{ if(window._origTitle) document.title=window._origTitle; });

  // fade-in + back to top
  if('IntersectionObserver' in window){
    const obs=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('visible'); obs.unobserve(e.target); } }); },{threshold:0.15});
    document.querySelectorAll('.ticket').forEach(t=>obs.observe(t));
  } else { document.querySelectorAll('.ticket').forEach(t=>t.classList.add('visible')); }
  window.addEventListener('scroll',()=>{ const b=$('back-to-top'); if(!b) return; if(window.scrollY>400) b.classList.add('show'); else b.classList.remove('show'); });
