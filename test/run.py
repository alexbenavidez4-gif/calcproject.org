import asyncio, re, json, os, sys, html
from playwright.async_api import async_playwright
REPO='/home/claude/calcproject.org'; ORIG='/home/claude/orig'
sys.path.insert(0,'/home/claude/build')
from defs import C
LEG={'room-size':'rsf','paint':'p','flooring':'f','tile':'t','drywall':'d','wallpaper':'w','trim':'b','mulch':'m','concrete':'c','gravel':'g','fence':'fc','deck':'dk','sod':'s','roofing':'r','siding':'sd'}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context()
        async def route(r):
            u=r.request.url
            if u.startswith('http://127.0.0.1'): await r.continue_()
            else: await r.abort()
        await ctx.route('**/*',route)
        errs=[]
        pg=await ctx.new_page()
        pg.on('pageerror',lambda e: errs.append(('pageerror',pg.url,str(e))))
        pg.on('console',lambda m: errs.append(('console',pg.url,m.text)) if m.type=='error' and 'ERR_FAILED' not in m.text and 'Failed to load resource' not in m.text else None)
        # old results
        await pg.goto('http://127.0.0.1:8802/index.html'); await pg.wait_for_timeout(400)
        old={}
        for sid,pre in LEG.items():
            old[sid]=await pg.evaluate("id=>{const r=document.getElementById(id+'-receipt');return [...r.querySelectorAll('.result-line,.total')].map(l=>[...l.querySelectorAll('span')].map(s=>s.textContent))}",pre)
        await pg.evaluate("setUnitSystem('metric')")
        oldm={sid:await pg.evaluate("id=>{const r=document.getElementById(id+'-receipt');return [...r.querySelectorAll('.result-line,.total')].map(l=>[...l.querySelectorAll('span')].map(s=>s.textContent))}",pre) for sid,pre in LEG.items()}
        errs.clear()
        bad=0
        num=lambda s: float(re.sub(r'[^0-9.\-]','',s.replace(',','')) or 0)
        for c in C:
            await pg.goto(f'http://127.0.0.1:8801/{c["slug"]}.html'); await pg.wait_for_timeout(120)
            get="()=>[...document.querySelectorAll('#receipt .result-line,#receipt .total')].map(l=>[...l.querySelectorAll('span')].map(s=>s.textContent))"
            imp=await pg.evaluate(get)
            note=await pg.evaluate("()=>{const n=document.querySelector('#receipt .receipt-note');return n?n.textContent:''}")
            await pg.click('[data-unit-btn=metric]'); met=await pg.evaluate(get)
            await pg.click('[data-unit-btn=imperial]'); imp2=await pg.evaluate(get)
            print(f"{c['slug']:34s} {' | '.join(a+': '+b for a,b in imp)}{'  NOTE: '+note if note else ''}")
            print(f"{'':34s} metric: {' | '.join(a+': '+b for a,b in met)}")
            if imp!=imp2: print('   !! round trip mismatch', imp2); bad+=1
            if not re.search(r'(gal|sq yd|tons?|board ft|lb|in|BTU/hr|ft)$',imp[-1][-1]) and num(imp[-1][-1])!=num(met[-1][-1]): print('   !! metric count differs',imp[-1],met[-1]); bad+=1
            if c.get('legacy'):
                o=old[c['legacy']]; om=oldm[c['legacy']]
                # compare totals numerically
                if abs(num(o[-1][-1])-num(imp[-1][-1]))>0.011: print('   !! legacy total differs: old',o[-1],'new',imp[-1]); bad+=1
                pass
                for (a,b_),(x,y) in zip(o[:-1],imp[:-1]):
                    if a==x and abs(num(b_)-num(y))>0.051: print('   !! legacy row differs',a,b_,y); bad+=1
        import glob
        legacy_slugs={c['slug'] for c in C}
        allp=sorted(os.path.basename(f) for f in glob.glob(REPO+'/*.html'))
        swept=0
        for f in allp:
            src=open(REPO+'/'+f).read()
            if 'window.CP_CALC' not in src or f[:-5] in legacy_slugs: continue
            await pg.goto('http://127.0.0.1:8801/'+f); 
            tot=await pg.evaluate("()=>{const t=document.querySelector('#receipt .total');return t?t.innerText:''}")
            if not tot or '\u2014' in tot or 'NaN' in tot or 'undefined' in tot: print('   !! bad result',f,repr(tot)); bad+=1
            if await pg.locator('[data-unit-btn=metric]').count():
                g="()=>document.querySelector('#receipt').innerText"
                a1=await pg.evaluate(g); await pg.click('[data-unit-btn=metric]'); m1=await pg.evaluate(g); await pg.click('[data-unit-btn=imperial]'); a2=await pg.evaluate(g)
                if a1!=a2: print('   !! unit round trip',f); bad+=1
                if 'NaN' in m1 or '\u2014' in m1: print('   !! metric bad',f); bad+=1
            await pg.click('.calc-btn')
            swept+=1
        print('SWEPT',swept)
        # save/print sheet across pages
        await pg.goto('http://127.0.0.1:8801/paint-calculator.html'); await pg.fill('#p-length','20'); 
        await pg.goto('http://127.0.0.1:8801/mulch-calculator.html'); await pg.fill('#m-depth','4')
        await pg.click('.save-ticket-btn'); on=await pg.text_content('#sd-on'); print('SHEET:',on)
        await pg.evaluate("document.getElementById('save-dialog').close(); window.print=()=>{}; document.getElementById('sd-print').click()")
        sheet=await pg.evaluate("()=>document.getElementById('print-sheet').innerText"); print(sheet[:600].replace('\n',' / '))
        # square footage add/remove room
        await pg.goto('http://127.0.0.1:8801/square-footage-calculator.html'); await pg.click('text=+ Add another room'); print('ROOMS:',await pg.evaluate(get))
        await pg.click('.remove-room >> nth=0'); print('ROOMS after remove:',await pg.evaluate(get))
        # electrical + math + home + hub
        for u in ['electricity-cost-calculator','watts-amps-calculator','circuit-load-calculator','wire-size-calculator','generator-size-calculator']:
            await pg.goto(f'http://127.0.0.1:8801/{u}.html'); await pg.wait_for_timeout(150)
            r=await pg.evaluate("()=>document.querySelector('.receipt').innerText.replace(/\\n/g,' | ')"); print(f'{u:30s}',r[:230])
            n=await pg.locator('.save-ticket-btn').count(); 
            if n!=1: print('   !! save button count',n); bad+=1
        await pg.goto('http://127.0.0.1:8801/advanced-tools.html'); await pg.wait_for_timeout(150)
        o={}
        for m in ['linear-equation-solver','quadratic-formula-calculator','slope-calculator','derivative-calculator','integral-calculator','pythagorean-theorem-calculator','right-triangle-calculator','percentage-calculator','fraction-calculator','gcf-lcm-calculator','mean-median-mode-calculator']:
            await pg.goto(f'http://127.0.0.1:8801/{m}.html'); await pg.click('[data-solve]')
            r=await pg.evaluate("()=>document.querySelector('[data-receipt]').innerText.replace(/\\n/g,' | ')"); st=await pg.locator('[data-steps] li').count()
            print(f'{m:32s}',r[:120],'steps',st)
            if st<1: bad+=1
        await pg.goto('http://127.0.0.1:8801/math-tools.html'); await pg.wait_for_timeout(200)
        await pg.goto('http://127.0.0.1:8801/index.html'); await pg.fill('#calc-search','concrete'); print('SEARCH concrete ->',await pg.evaluate("()=>[...document.querySelectorAll('.calc-card:not([hidden]) strong')].map(e=>e.textContent)"))
        await pg.goto('http://127.0.0.1:8801/index.html#paint'); await pg.wait_for_timeout(300); print('REDIRECT #paint ->',pg.url)
        await pg.goto('http://127.0.0.1:8801/advanced-tools.html#wire-size'); await pg.wait_for_timeout(300); print('REDIRECT #wire-size ->',pg.url)
        # screenshots
        for name,u,w,h in [('home','index.html',1280,900),('paint','paint-calculator.html',1280,900),('paint-m','paint-calculator.html',390,844),('home-m','index.html',390,844),('stairs','stair-calculator.html',1280,900)]:
            pg2=await ctx.new_page(); await pg2.set_viewport_size({'width':w,'height':h}); await pg2.goto(f'http://127.0.0.1:8801/{u}'); await pg2.wait_for_timeout(300)
            await pg2.screenshot(path=f'/home/claude/build/test/{name}.png',full_page=True); await pg2.close()
        print('ERRORS:',len(errs)); [print('  ',e) for e in errs[:20]]
        print('BAD:',bad)
        await b.close()
asyncio.run(main())
