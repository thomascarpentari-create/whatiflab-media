import sys,json,subprocess,wave,numpy as np,sherpa_onnx,glob
M='/home/claude/models/sherpa-onnx-zipformer-small-en-2023-06-26'
g=lambda p:[f for f in glob.glob(M+'/'+p) if 'int8' not in f][0]
r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=g('encoder*.onnx'),decoder=g('decoder*.onnx'),joiner=g('joiner*.onnx'),tokens=M+'/tokens.txt',num_threads=4)
src=sys.argv[1]; subprocess.check_call(['ffmpeg','-v','error','-y','-i',src,'-ar','16000','-ac','1','_asr.wav'])
w=wave.open('_asr.wav'); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768; sr=16000
# chunk on 25 s windows cut at quiet spots
out=[]; pos=0
while pos<len(x):
    end=min(len(x),pos+25*sr)
    if end<len(x):
        seg=np.abs(x[end-5*sr:end]); k=np.convolve(seg,np.ones(3200)/3200,'same'); end=end-5*sr+int(np.argmin(k))
    s=r.create_stream(); s.accept_waveform(sr,x[pos:end]); r.decode_stream(s); res=s.result
    word='';t0=None
    for tok,ts in zip(res.tokens,res.timestamps):
        if tok.startswith(' ') or tok.startswith('▁'):
            if word: out.append((word,round(t0,2)))
            word=tok.strip(' ▁'); t0=ts+pos/sr
        else:
            if t0 is None: t0=ts+pos/sr
            word+=tok
    if word: out.append((word,round(t0,2)))
    pos=end
json.dump(out,open(sys.argv[2],'w'))
print(' '.join(f"{w}@{t}" for w,t in out))
