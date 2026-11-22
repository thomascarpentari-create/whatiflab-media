import json,sys,difflib,subprocess
cfg,oldw,neww,audio,name=sys.argv[1:6]
C=json.load(open(cfg)); O=json.load(open(oldw)); N=json.load(open(neww))
ow=[w for w,_ in O]; nw=[w for w,_ in N]
m=difflib.SequenceMatcher(None,ow,nw,autojunk=False); mp={}
for a,b,n in m.get_matching_blocks():
    for i in range(n): mp[a+i]=b+i
def new_idx(i):
    if i in mp: return mp[i],True
    j=i
    while j>=0 and j not in mp: j-=1
    return (min(len(N)-1,mp[j]+(i-j)) if j>=0 else 0),False
bad=0; last=-1
for s in C['shots']:
    i=next((k for k,(w,t) in enumerate(O) if t>=s['t']-0.13),len(O)-1) if s['t']>0 else 0
    j,ok=new_idx(i); bad+=not ok
    t=max(0.0,round(N[j][1]-0.08,2)) if s['t']>0 else 0.0
    if t<=last: t=round(last+0.3,2)
    s['t']=t; last=t
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',audio]))
C['end']=round(dur+0.7,2); C['audio']=audio; C['name']=name; C['label']='Satire · AI-generated images and voice'
json.dump(C,open(name+'.json','w')); print(name,'words old/new',len(O),len(N),'ratio %.3f'%m.ratio(),'unmatched shots',bad,'end',C['end'])
