import json, os, textwrap, datetime
from PIL import Image, ImageDraw, ImageFont
from pins import P
W, H = 1000, 1500
NAVY=(22,50,74); DEEP=(13,32,49); CHALK=(243,241,232); GRAPH=(42,42,40); SOFT=(100,100,95)
ACC=[(228,87,46),(244,185,66),(86,196,222),(120,200,140)]
D='/usr/share/fonts/opentype/inter/'
def f(n,s): return ImageFont.truetype(D+n,s)
import glob
MONO=[p for p in glob.glob('/usr/share/fonts/**/*Mono*Bold*.ttf',recursive=True)+glob.glob('/usr/share/fonts/**/*Mono*.ttf',recursive=True)][0]
def mono(s): return ImageFont.truetype(MONO,s)
def wrap(d,text,font,maxw):
    out,cur=[],''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
os.makedirs('out',exist_ok=True)
start=datetime.date(2026,11,16)
cal=[]
for i,(slug,head,rows,total,title,desc,alt,topics) in enumerate(P):
    acc=ACC[i%4]
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    for x in range(0,W,50): d.line([(x,0),(x,H)],fill=(28,60,88),width=1)
    for y in range(0,H,50): d.line([(0,y),(W,y)],fill=(28,60,88),width=1)
    d.rectangle([0,0,W,14],fill=acc)
    # eyebrow
    ef=f('Inter-Bold.otf',30); et='FREE CALCULATOR  ·  NO SIGN-UP'
    tw=d.textlength(et,font=ef); d.rounded_rectangle([70,80,70+tw+48,80+62],8,outline=acc,width=3); d.text((94,94),et,font=ef,fill=acc)
    # headline
    size=118
    while True:
        hf=f('InterDisplay-Black.otf',size); lines=wrap(d,head.upper(),hf,W-140)
        if len(lines)<=4 or size<=80: break
        size-=6
    y=190
    for ln in lines:
        d.text((70,y),ln,font=hf,fill=CHALK); y+=int(size*1.04)
    y+=40
    # receipt card
    ch=150+len(rows)*78+150
    d.rounded_rectangle([70,y,W-70,y+ch],14,fill=CHALK)
    d.text((110,y+38),'EXAMPLE',font=mono(30),fill=SOFT)
    yy=y+100
    lf=f('Inter-Medium.otf',36); vf=mono(33)
    for a,b in rows:
        d.text((110,yy),a,font=lf,fill=GRAPH)
        bw=d.textlength(b,font=vf)
        if bw>W-220-d.textlength(a,font=lf)-30:
            vf2=mono(26); bw=d.textlength(b,font=vf2); d.text((W-110-bw,yy+6),b,font=vf2,fill=GRAPH)
        else: d.text((W-110-bw,yy+2),b,font=vf,fill=GRAPH)
        d.line([(110,yy+60),(W-110,yy+60)],fill=(215,212,200),width=2)
        yy+=78
    d.line([(110,yy+6),(W-110,yy+6)],fill=GRAPH,width=4)
    d.text((110,yy+34),total[0].upper(),font=f('Inter-Bold.otf',34),fill=SOFT)
    ts=66
    while True:
        tf=f('InterDisplay-Black.otf',ts)
        if d.textlength(total[1],font=tf)<=W-220 or ts<=40: break
        ts-=4
    d.text((110,yy+78),total[1],font=tf,fill=NAVY)
    # footer
    by=H-250
    bf=f('Inter-ExtraBold.otf',44); bt='TRY IT FREE  →'
    d.rounded_rectangle([70,by,W-70,by+104],12,fill=acc); bw=d.textlength(bt,font=bf); d.text(((W-bw)/2,by+26),bt,font=bf,fill=DEEP if acc!=(228,87,46) else (255,255,255))
    uf=f('InterDisplay-Black.otf',54); ut='calcproject.org'; uw=d.textlength(ut,font=uf); d.text(((W-uw)/2,by+128),ut,font=uf,fill=CHALK)
    im.save(f'out/{i+1:02d}-{slug}.png',optimize=True)
    day=start+datetime.timedelta(days=i)
    cal.append(dict(day=i+1,date=day.isoformat(),image=f'{i+1:02d}-{slug}.png',title=title,description=desc,link=f'https://calcproject.org/{slug}.html',alt=alt,topics=topics))
json.dump(cal,open('out/calendar.json','w'),indent=1)
with open('out/calendar.md','w') as m:
    m.write('# CalcProject Pinterest calendar: 1 pin a day, 30 days\n\nPost time: 7:00 PM Central. Board: the CalcProject / DIY calculators board.\n\n')
    for c in cal:
        m.write(f"## Day {c['day']} - {c['date']}\n- Image: {c['image']}\n- Title: {c['title']}\n- Description: {c['description']}\n- Link: {c['link']}\n- Alt text: {c['alt']}\n- Topics: {', '.join(c['topics'])}\n\n")
# contact sheet
th=[Image.open(f'out/{c["image"]}').resize((200,300)) for c in cal]
sheet=Image.new('RGB',(6*210+10,5*310+10),(240,240,240))
for i,t in enumerate(th): sheet.paste(t,(10+(i%6)*210,10+(i//6)*310))
sheet.save('out/contact-sheet.png')
print(len(cal),max(len(c['title']) for c in cal),max(len(c['description']) for c in cal))
