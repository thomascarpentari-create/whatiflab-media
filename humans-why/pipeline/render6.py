# Timeline renderer, news look: one audio file, one shot per statement.
import json, sys, subprocess, os, glob
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
BG=(14,14,17); YE=(255,212,0); WH=(245,245,245); RED=(225,40,40)
AN='/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
PL=(glob.glob('/usr/share/fonts/truetype/google-fonts/**/IBMPlexSans-SemiBold.ttf',recursive=True) or glob.glob('/usr/share/fonts/truetype/**/DejaVuSans-Bold.ttf',recursive=True))[0]
_f={}
def F(s):
    if ('a',s) not in _f: _f[('a',s)]=ImageFont.truetype(AN,s)
    return _f[('a',s)]
def P(s):
    if ('p',s) not in _f: _f[('p',s)]=ImageFont.truetype(PL,s)
    return _f[('p',s)]
C=json.load(open(sys.argv[1])); SH=C['shots']; END=C['end']; NAME=C['name']
ease=lambda x: 1-(1-max(0.0,min(1.0,x)))**3
# image runs: consecutive shots with the same image share one camera move
runs=[]
for i,s in enumerate(SH):
    t1=SH[i+1]['t'] if i+1<len(SH) else END
    if runs and runs[-1][2]==s['img']: runs[-1][1]=t1
    else: runs.append([s['t'],t1,s['img'],len(runs)])
tag=None
for s in SH:
    tag=s.get('tag',tag); s['_tag']=tag
def grad():
    g=Image.new('L',(1,H))
    for y in range(H):
        a=0
        if y<520: a=int(170*min(1,(520-y)/370))
        if y>1250: a=max(a,int(235*min(1,(y-1250)/330)))
        g.putpixel((0,y),a)
    return g.resize((W,H))
GM=grad(); BLK=Image.new('RGB',(W,H),(8,8,10)); BGC={}
def bg(path,t,T,k):
    if path not in BGC: BGC[path]=Image.open(path).convert('RGB').resize((1296,2304),Image.LANCZOS)
    b=BGC[path]; p=t/max(T,0.1)
    z=(1.0+0.12*p) if k%2==0 else (1.12-0.12*p)      # alternate push-in / pull-out
    z*=1.0+0.05*(1-ease(t/0.22))                     # small punch on every cut
    cw,ch=1296/1.2*1.0/z*1.2/1.0*(1080/1296)*1.2/1.2, 0
    cw=1080*1.2/z/1.0*(1296/1296)/1.0; cw=min(cw,1296); ch=cw*H/W
    dx=(1296-cw)*(0.5+0.25*(p-0.5)*(1 if k%3 else -1)); dy=(2304-ch)/2
    im=b.resize((W,H),Image.BILINEAR,box=(dx,dy,dx+cw,dy+ch))
    return Image.composite(BLK,im,GM)
TICK='   ·   '.join(C['ticker'])+'   ·   '
_tw=None
def frame(t):
    global _tw
    r=[x for x in runs if x[0]<=t][-1]; i=max(k for k,s in enumerate(SH) if s['t']<=t); s=SH[i]
    img=bg(r[2],t-r[0],r[1]-r[0],r[3]); d=ImageDraw.Draw(img)
    # header
    d.rectangle((0,0,W,132),fill=YE); d.text((48,20),C['brand'],font=F(78),fill=BG)
    x=W-48-d.textlength(C['date'],font=P(30)); d.text((x,30),C['date'],font=P(30),fill=BG)
    x=W-48-d.textlength(C['sub'],font=P(22)); d.text((x,78),C['sub'],font=P(22),fill=(60,50,0))
    # big words (hook, answer, end card)
    if s.get('big'):
        y=250; a=ease((t-s['t'])/0.3)
        for k,l in enumerate(s['big']):
            f=F(150)
            while d.textlength(l,font=f)>W-110: f=F(f.size-4)
            d.text((54-int(50*(1-a)),y),l,font=f,fill=YE if k==0 else WH,stroke_width=6,stroke_fill=(8,8,10)); y+=f.size+14
    # lower third: tag chip + caption
    c=s['cap']; f=P(54); lines=[c]
    if d.textlength(c,font=f)>W-170:
        ws=c.split(' '); best=None
        for k in range(1,len(ws)):
            a_,b_=' '.join(ws[:k]),' '.join(ws[k:]); m=max(d.textlength(a_,font=f),d.textlength(b_,font=f))
            if best is None or m<best[0]: best=(m,[a_,b_])
        lines=best[1]
        while max(d.textlength(l,font=f) for l in lines)>W-170: f=P(f.size-2)
    tw=max(d.textlength(l,font=f) for l in lines); lh=f.size+12; bh=lh*len(lines)+34
    y0=1470-(lh if len(lines)>1 else 0); a=ease((t-s['t'])/0.16)
    tg=s['_tag']
    if tg:
        col=RED if tg.startswith('BREAKING') else YE; fc=WH if col==RED else BG
        w=d.textlength(tg,font=P(30))+36; d.rectangle((48,y0-58,48+w,y0-8),fill=col); d.text((66,y0-52),tg,font=P(30),fill=fc)
    d.rounded_rectangle((48,y0,48+tw+64,y0+bh),radius=10,fill=WH)
    for k,l in enumerate(lines): d.text((80,y0+15+k*lh+int(10*(1-a))),l,font=f,fill=BG)
    # ticker
    d.rectangle((0,1640,W,1702),fill=(12,12,16)); d.rectangle((0,1640,150,1702),fill=RED); 
    if _tw is None: _tw=d.textlength(TICK,font=P(30))
    off=int(t*95)%int(_tw); x=150-off
    tl=Image.new('RGB',(W-150,62),(12,12,16)); td=ImageDraw.Draw(tl)
    xx=-off
    while xx<W: td.text((xx,12),TICK,font=P(30),fill=(230,230,235)); xx+=_tw
    img.paste(tl,(150,1640)); d.text((30,1652),'LIVE',font=P(30),fill=WH) if int(t*1.2)%2==0 else d.text((30,1652),'LIVE',font=P(30),fill=(255,190,190))
    d.text((48,1722),C['label'],font=P(24),fill=(190,190,200))
    if s.get('handle'): d.text((54,760),s['handle'],font=P(44),fill=WH,stroke_width=4,stroke_fill=(8,8,10))
    return img
if '--stills' in sys.argv:
    ts=[float(x) for x in sys.argv[sys.argv.index('--stills')+1].split(',')]
    sh=Image.new('RGB',(len(ts)*270,480))
    for k,t in enumerate(ts): sh.paste(frame(t).resize((270,480)),(k*270,0))
    sh.save(NAME+'_stills.jpg'); frame(ts[0]).save(NAME+'_full.jpg',quality=88); sys.exit()
n=int(END*FPS); out=NAME+'.tmp.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',C['audio'],'-af',f'apad=whole_dur={END:.3f}','-c:v','libx264','-crf','23','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{n/FPS:.3f}','-movflags','+faststart',out],stdin=subprocess.PIPE)
for k in range(n): p.stdin.write(frame(k/FPS).tobytes())
p.stdin.close(); assert p.wait()==0; os.replace(out,NAME+'.mp4'); print('DONE',NAME)
