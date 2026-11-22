import sherpa_onnx, json, sys, wave, re, numpy as np
from scipy.signal import resample_poly
K='/home/claude/models/kokoro-multi-lang-v1_0'
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=K+'/model.onnx',voices=K+'/voices.bin',tokens=K+'/tokens.txt',data_dir=K+'/espeak-ng-data',dict_dir=K+'/dict',lexicon=K+'/lexicon-us-en.txt,'+K+'/lexicon-zh.txt'),num_threads=4)))
def wr(p,x,sr):
    w=wave.open(p,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(np.array(x),-1,1)*32767).astype('<i2').tobytes()); w.close()
def speak(text,sid,speed,pitch):
    out=[]; sr=24000
    for part in re.split(r'(\|+|/+)',text):
        if not part.strip(): continue
        if part.startswith('/'): out.append(np.zeros(int(sr*0.75*len(part)))); continue
        if part.startswith('|'): out.append(np.zeros(int(sr*0.24*len(part)))); continue
        p=part.strip(); sp=speed; pt=pitch
        if p.startswith('^'): p=p[1:].strip(); sp=speed*1.05; pt=pitch*1.06
        if p.startswith('~'): p=p[1:].strip(); sp=speed*0.9; pt=pitch*0.93
        a=tts.generate(p,sid=sid,speed=sp/pt); sr=a.sample_rate; x=np.array(a.samples)
        x=resample_poly(x,1000,int(round(1000*pt))) if abs(pt-1.0)>0.004 else x
        out.append(x)
    return np.concatenate(out),sr
