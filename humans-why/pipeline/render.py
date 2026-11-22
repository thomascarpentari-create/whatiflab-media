import json, math, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
BG=(14,14,17); YE=(255,212,0); WH=(245,245,245); GR=(150,150,160)
AN='/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
import glob
PL=(glob.glob('/usr/share/fonts/truetype/google-fonts/**/IBMPlexSans-SemiBold.ttf',recursive=True) or glob.glob('/usr/share/fonts/truetype/**/DejaVuSans-Bold.ttf',recursive=True))[0]
F=lambda s: ImageFont.truetype(AN,s); P=lambda s: ImageFont.truetype(PL,s)
PAD=0.45
CFG=json.load(open(sys.argv[1])); dur=json.load(open(sys.argv[1].replace('.json','.dur.json'))); SC=CFG['sc']; NAME=CFG['name']; DATE=CFG['date']; LABEL=CFG.get('label','Nur zur Ansicht')
random.seed(4)
STARS=[(random.randint(0,W),random.randint(300,1500),random.choice([1,2,2,3])) for _ in range(90)]
FLK=[(random.randint(0,W),random.random(),random.randint(4,9),random.uniform(60,140)) for _ in range(60)]
ease=lambda x: 1-(1-max(0,min(1,x)))**3
def header(d):
    d.rectangle((0,0,W,150),fill=YE)
    d.text((60,28),CFG.get("brand","WELT TÄGLICH"),font=F(84),fill=(14,14,17))
    t=DATE; d.text((W-60-d.textlength(t,font=P(34)),40),t,font=P(34),fill=(14,14,17))
    t2=CFG.get("sub","SATIRE · KI-KOMMENTAR"); d.text((W-60-d.textlength(t2,font=P(24)),92),t2,font=P(24),fill=(60,50,0))
def icon(img,kind,t,T):
    d=ImageDraw.Draw(img); cx,cy=540,1080
    if kind=="globe":
        r=190; d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=YE,width=8)
        for k in (-0.5,0,0.5): d.arc((cx-r,cy-r+ k*r*1.2 - 60,cx+r,cy+r+k*r*1.2-(-60)),0,180,fill=YE,width=4) if False else None
        for k in range(-2,3):
            yy=cy+k*70; hw=int((r*r-(k*70)**2)**0.5); d.line((cx-hw,yy,cx+hw,yy),fill=YE,width=4)
        ph=t*0.6
        for k in range(4):
            a=abs(math.cos(ph+k*math.pi/4)); w=int(r*a); d.ellipse((cx-w,cy-r,cx+w,cy+r),outline=YE,width=4)
    if kind=="probe":
        for x,y,s in STARS: d.ellipse((x,y,x+s,y+s),fill=(200,200,210))
        ex,ey=150,1300; d.ellipse((ex-26,ey-26,ex+26,ey+26),fill=(70,140,255)); d.text((ex-34,ey+36),("EARTH" if CFG.get("lang")=="en" else "ERDE"),font=P(26),fill=GR)
        px=int(300+520*ease(t/T*1.1)); py=int(1210-330*ease(t/T*1.1))
        for i in range(0,40):
            f=i/40; x=ex+(px-ex)*f; y=ey+(py-ey)*f
            if i%2==0: d.ellipse((x-3,y-3,x+3,y+3),fill=YE)
        d.polygon([(px-10,py-10),(px+70,py-55),(px+85,py-25),(px+5,py+20)],fill=WH)
        d.ellipse((px+40,py-95,px+130,py-5),outline=WH,width=8); d.line((px+85,py-50,px+150,py-110),fill=WH,width=6)
        d.line((px-10,py+5,px-90,py+60),fill=WH,width=6)
        d.text((330,1380),"16 BILLION MILES" if CFG.get("lang")=="en" else "25,9 Mrd. km",font=F(64),fill=YE)
    if kind=="ufo":
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); l=ImageDraw.Draw(lay)
        ox=int(40*math.sin(t*9)); oy=int(22*math.sin(t*13+1)); x,y=cx+ox,cy-60+oy
        l.polygon([(x-60,y+30),(x+60,y+30),(x+200,y+420),(x-200,y+420)],fill=(255,212,0,70))
        l.ellipse((x-210,y-40,x+210,y+50),fill=(230,230,235,255)); l.ellipse((x-95,y-110,x+95,y+10),fill=(150,200,255,255))
        for k in range(-2,3): l.ellipse((x+k*75-10,y+2,x+k*75+10,y+22),fill=(255,212,0,255))
        lay=lay.filter(ImageFilter.GaussianBlur(9)); img.paste(lay,(0,0),lay)
        d.rectangle((120,820,960,1420),outline=(110,110,120),width=3)
        d.text((140,836),"REC ●  UNSCHARF",font=P(28),fill=(255,90,90))
        if t>T*0.72:
            st=Image.new('RGBA',(520,150),(0,0,0,0)); s2=ImageDraw.Draw(st); s2.rectangle((4,4,515,145),outline=(255,70,70,255),width=8); s2.text((40,28),"AMTLICH",font=F(88),fill=(255,70,70,255))
            st=st.rotate(-12,expand=True,resample=Image.BICUBIC); img.paste(st,(400,1240),st)
    if kind=="snow":
        for x,ph,s,v in FLK:
            y=780+((ph*760+t*v)%760); xx=x+18*math.sin(t*1.5+ph*9); d.ellipse((xx-s,y-s,xx+s,y+s),fill=WH)
        tx=540; d.rounded_rectangle((tx-34,860,tx+34,1300),radius=34,outline=WH,width=8); d.ellipse((tx-70,1260,tx+70,1400),fill=(70,140,255),outline=WH,width=8)
        lvl=int(1250-(300*(1-ease(t/T*1.4)))); d.rectangle((tx-14,max(lvl,900)+200 if False else 1100+int(120*ease(t/T*1.4)),tx+14,1290),fill=(70,140,255))

    if kind=="pad":
        d.rounded_rectangle((cx-260,cy-110,cx+260,cy+120),radius=110,outline=WH,width=10)
        d.rectangle((cx-190,cy-18,cx-90,cy+18),fill=WH); d.rectangle((cx-158,cy-50,cx-122,cy+50),fill=WH)
        for (ox,oy,c) in ((120,-30,YE),(180,10,(255,90,90)),(120,50,(70,140,255)),(60,10,(95,224,160))): d.ellipse((cx+ox-24,cy+oy-24,cx+ox+24,cy+oy+24),fill=c)
        z=int(8*math.sin(t*10)); d.text((cx-250,cy+170+z),"AUSSER BETRIEB: ALLE",font=F(56),fill=YE)
    if kind=="chart":
        d.line((180,820,180,1380),fill=GR,width=5); d.line((180,1380,900,1380),fill=GR,width=5)
        pts=[(180,900),(300,860),(420,930),(520,900),(620,1040),(720,1010),(800,1230),(880,1330)]
        n=max(2,int(len(pts)*ease(t/T*1.6))+1); d.line(pts[:n],fill=(255,80,80),width=10,joint="curve")
        x,y=pts[min(n,len(pts))-1]; d.ellipse((x-14,y-14,x+14,y+14),fill=(255,80,80))
    if kind=="bulb":
        on=int(t*3)%2==0; col=YE if on else (90,90,100)
        d.ellipse((cx-150,cy-200,cx+150,cy+100),outline=col,width=10, fill=(60,50,0) if on else None)
        d.rectangle((cx-60,cy+100,cx+60,cy+170),outline=col,width=10); d.line((cx-40,cy+200,cx+40,cy+200),fill=col,width=10)
        if on:
            for k in range(8):
                a=k*math.pi/4; d.line((cx+230*math.cos(a),cy-50+230*math.sin(a),cx+300*math.cos(a),cy-50+300*math.sin(a)),fill=YE,width=8)
    if kind=="ice":
        d.polygon([(cx-200,cy-120),(cx+120,cy-120),(cx+120,cy+200),(cx-200,cy+200)],outline=(150,210,255))
        d.rectangle((cx-200,cy-120,cx+120,cy+200),outline=(150,210,255),width=8); d.line((cx-200,cy-120,cx-110,cy-210,cx+210,cy-210,cx+120,cy-120),fill=(150,210,255),width=8); d.line((cx+210,cy-210,cx+210,cy+110,cx+120,cy+200),fill=(150,210,255),width=8)
        for k in range(5):
            y=int(760+((t*520+k*170)%760)); x=cx-150+k*70; d.line((x,y-40,x+12,y),fill=YE,width=5); d.ellipse((x+6,y-6,x+18,y+6),fill=YE)
    if kind=="heat":
        d.ellipse((760,820,940,1000),fill=YE)
        tx=440; d.rounded_rectangle((tx-34,860,tx+34,1300),radius=34,outline=WH,width=8); d.ellipse((tx-70,1260,tx+70,1400),fill=(255,80,80),outline=WH,width=8)
        d.rectangle((tx-14,int(1250-330*ease(t/T*1.3)),tx+14,1290),fill=(255,80,80))
        d.text((560,1180),"REKORD",font=F(80),fill=(255,80,80))
    if kind=="book":
        d.polygon([(cx-280,cy-140),(cx,cy-90),(cx,cy+190),(cx-280,cy+140)],outline=WH); d.line((cx-280,cy-140,cx,cy-90,cx,cy+190,cx-280,cy+140,cx-280,cy-140),fill=WH,width=8)
        d.line((cx+280,cy-140,cx,cy-90),fill=WH,width=8); d.line((cx+280,cy-140,cx+280,cy+140,cx,cy+190),fill=WH,width=8)
        for k in range(4): d.line((cx-240,cy-80+k*50,cx-40,cy-45+k*50),fill=GR,width=5); d.line((cx+40,cy-45+k*50,cx+240,cy-80+k*50),fill=GR,width=5)
BGC={}
def grad():
    g=Image.new('L',(1,H))
    for y in range(H):
        a=0
        if y<820: a=int(215*min(1,(820-y)/420))
        if y>1380: a=max(a,int(225*min(1,(y-1380)/260)))
        g.putpixel((0,y),a)
    return g.resize((W,H))
GM=grad(); BLK=Image.new('RGB',(W,H),(8,8,10))
def bgimg(path,t,T):
    if path not in BGC: BGC[path]=Image.open(path).convert('RGB').resize((1210,2168),Image.LANCZOS).crop((11,9,1199,2121))
    b=BGC[path]; z=1.0+0.10*(t/T); cw,ch=1188/ (1.1/ z) if False else 1080*1.1/z, 1920*1.1/z
    x=(1188-cw)/2; y=(2112-ch)/2
    im=b.resize((W,H),Image.BILINEAR,box=(x,y,x+cw,y+ch))
    return Image.composite(BLK,im,GM)
def frame(sc,t,T):
    if sc.get('imgs'):
        cs=sc['_cuts']; k=max(i for i,c in enumerate(cs) if t/T>=c)
        t0=cs[k]*T; t1=(cs[k+1] if k+1<len(cs) else 1.0)*T
        img=bgimg(sc['imgs'][k],t-t0,max(t1-t0,0.1))
    elif sc.get('img'): img=bgimg(sc['img'],t,T)
    else:
        img=Image.new('RGB',(W,H),BG); icon(img,sc['icon'],t,T)
    d=ImageDraw.Draw(img); header(d)
    a=ease(t/0.35)
    d.rectangle((60,210,60+int((d.textlength(sc['tag'],font=P(34))+40)*a),270),fill=WH)
    if a>0.6: d.text((80,220),sc['tag'],font=P(34),fill=BG)
    y=310
    for i,l in enumerate(sc['head']):
        b=ease((t-0.12*i)/0.4); f=F(118)
        while d.textlength(l,font=f)>W-120: f=F(f.size-4)
        d.text((60-int(60*(1-b)),y),l,font=f,fill=WH if i else YE) if b>0 else None
        y+=f.size+18
    # captions
    n=len(sc['cap']); tot=sum(len(c) for c in sc['cap']); acc=0; cur=0
    for i,c in enumerate(sc['cap']):
        if t>=(T-PAD)*acc/tot: cur=i
        acc+=len(c)
    c=sc['cap'][cur]; f=P(50)
    while d.textlength(c,font=f)>W-160: f=P(f.size-2)
    tw=d.textlength(c,font=f); d.rounded_rectangle(((W-tw)/2-32,1560,(W+tw)/2+32,1560+f.size+44),radius=18,fill=(245,245,245)); d.text(((W-tw)/2,1578),c,font=f,fill=BG)
    if sc['src']: d.text((60,1700),sc['src'],font=P(28),fill=(210,210,220))
    d.text((60,1760),LABEL,font=P(26),fill=(190,190,200))
    return img
if '--stills' in sys.argv:
    sh=Image.new('RGB',(len(SC)*270,480))
    for i,sc in enumerate(SC):
        T=dur[i]+PAD; frame(sc,T*0.8,T).resize((270,480)).save(f'st{i}.jpg'); sh.paste(frame(sc,T*0.8,T).resize((270,480)),(i*270,0))
    sh.save('stills.jpg'); sh.save(NAME+'_stills.jpg'); sys.exit()
files=[]
for i,sc in enumerate(SC):
    T=dur[i]+PAD; n=int(T*FPS); out=f'{NAME}_c{i}.tmp.mp4'
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',f'{NAME}_{i}.wav','-af',f'apad=whole_dur={T:.3f}','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{n/FPS:.3f}',out],stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frame(sc,k/FPS,T).tobytes())
    p.stdin.close(); assert p.wait()==0
    import os; os.replace(out,f'{NAME}_c{i}.mp4'); files.append(f'{NAME}_c{i}.mp4')
open(f'{NAME}.txt','w').write(''.join(f"file '{f}'\n" for f in files))
subprocess.check_call(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{NAME}.txt','-c','copy','-movflags','+faststart',f'{NAME}.mp4'])
