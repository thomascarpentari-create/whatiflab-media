import sherpa_onnx, json, sys, wave, re, numpy as np
import os
K=os.environ.get('KOKORO','/home/claude/models/kokoro-en-v0_19')
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=K+'/model.onnx',voices=K+'/voices.bin',tokens=K+'/tokens.txt',data_dir=K+'/espeak-ng-data'),num_threads=4)))
def wr(p,x,sr):
    w=wave.open(p,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(np.array(x),-1,1)*32767).astype('<i2').tobytes()); w.close()
def speak(text,sid,speed,pitch):
    out=[]; sr=24000
    for part in re.split(r'(\|+|/+)',text):
        if not part.strip(): continue
        if part.startswith('/'): out.append(np.zeros(int(sr*0.75*len(part)))); continue
        if part.startswith('|'): out.append(np.zeros(int(sr*0.24*len(part)))); continue
        p=part.strip(); sp=speed; pt=pitch
        if p.startswith('^'): p=p[1:].strip(); sp=speed*1.05; pt=pitch*1.075
        if p.startswith('~'): p=p[1:].strip(); sp=speed*0.88; pt=pitch*0.915
        a=tts.generate(p,sid=sid,speed=sp/pt); sr=a.sample_rate; x=np.array(a.samples)
        from scipy.signal import resample_poly
        x=resample_poly(x,1000,int(round(1000*pt))) if abs(pt-1.0)>0.004 else x
        out.append(x)
    return np.concatenate(out),sr
if __name__=='__main__':
    C=json.load(open(sys.argv[1])); d=[]
    for i,s in enumerate(C['sc']):
        x,sr=speak(s['say'],C.get('sid',6),C.get('speed',1.04),C.get('pitch',1.07)); wr(f"{C['name']}_{i}.wav",x,sr); d.append(len(x)/sr)
    json.dump(d,open(sys.argv[1].replace('.json','.dur.json'),'w')); print(d,sum(d))
