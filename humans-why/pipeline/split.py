import sys,json
d=open(sys.argv[1],'rb').read(); i=d.index(b'\n'); m=json.loads(d[:i]); p=i+1
for k,x in enumerate(m):
    open(f"{sys.argv[2]}/b{k+1:02d}.jpg",'wb').write(d[p:p+x['n']]); p+=x['n']
print(len(m),p,len(d))
