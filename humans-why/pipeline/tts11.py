import json,sys,subprocess,wave,os
from tts10 import speak,wr
FX="highpass=f=120,aecho=0.8:0.6:14:0.22,chorus=0.8:0.9:18:0.25:0.15:1,treble=g=3:f=5000,acompressor=threshold=-18dB:ratio=3,volume=1.5"
C=json.load(open(sys.argv[1])); d=[]
for i,s in enumerate(C['sc']):
    t=s['say'].replace('^','').replace('~','')
    x,sr=speak(t,C.get('sid',3),C.get('speed',0.96),1.0); wr('_t.wav',x,sr)
    out=f"{C['name']}_{i}.wav"
    subprocess.check_call(['ffmpeg','-v','error','-y','-i','_t.wav','-filter_complex',FX,'-ar',str(sr),'-ac','1',out])
    w=wave.open(out); d.append(w.getnframes()/w.getframerate()); w.close()
json.dump(d,open(sys.argv[1].replace('.json','.dur.json'),'w')); print(d,sum(d))
