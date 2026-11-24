# Tunnel: the beams are a tunnel, the circle is its far end. A huge circle hides everything; it shrinks and settles into the middle,
# revealing the beams at their normal size. The beams then spin clockwise (half a turn, strong ease in/out), and the circle opens back out. Shapes only.
from emit import emit
FPS=60
CW,CH=1400,880; CX,CY=CW/2,CH*0.42
CURVES={"io":(0.45,0,0.55,1),"out":(0.2,0.9,0.35,1),"flat":(0.5,0,0.5,1),"spin":(0.65,0,0.35,1)}
flip=lambda c:(1-c[2],1-c[3],1-c[0],1-c[1])
T_IN=1.9; HOLD_END=T_IN+2.0; EXIT_SCALE=0.9; LOOP=round(HOLD_END+T_IN*EXIT_SCALE+0.3,2)
def full_keys(kin):
    keys=[(t,v,e) for t,v,e in kin]; keys.append((HOLD_END,kin[-1][1],"flat"))
    for j in range(len(kin)-1,0,-1):
        t,v,_=kin[j]; pe=kin[j-1][2]; keys.append((HOLD_END+(T_IN-t)*EXIT_SCALE,v,("rev",pe)))
    keys.append((LOOP,kin[0][1],"flat")); return keys
def bez(e):
    c=flip(CURVES[e[1]]) if isinstance(e,tuple) else CURVES[e]
    return {"o":{"x":[c[0]],"y":[c[1]]},"i":{"x":[c[2]],"y":[c[3]]}}
def kf(keys,wrap=lambda v:[v]):
    k=[]
    for i,(t,v,e) in enumerate(keys):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in wrap(v)]}
        if i<len(keys)-1: d.update(bez(e))
        k.append(d)
    return {"a":1,"k":k}
S=lambda v:{"a":0,"k":v}
tr=lambda rot=None,op=None:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot or S(0),"o":op or S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
circ=full_keys([(0,1900,"flat"),(0.30,1900,"io"),(0.55,206,"io"),(T_IN,68,"out")])
matte=[{"ty":"gr","it":[{"ty":"el","d":1,"s":kf(circ,lambda r:[r,r]),"p":S([0,0])},{"ty":"fl","c":W,"o":S(100),"r":1},tr()]}]
beams=[{"ty":"gr","it":[{"ty":"rc","d":1,"s":S([24,200]),"p":S([0,0]),"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(S(i*30))]} for i in range(6)]
def layer(ind,nm,shapes,ks=None,**extra):
    k={"o":S(100),"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":S([100,100,100])}
    if ks: k.update(ks)
    d={"ddd":0,"ind":ind,"ty":4,"nm":nm,"sr":1,"ks":k,"ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}; d.update(extra); return d
SPIN_START,SPIN_END=T_IN+0.2,T_IN+1.5
spin=kf([(0,0,"flat"),(SPIN_START,0,"spin"),(SPIN_END,180,"flat"),(LOOP,180,"flat")])
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":CW,"h":CH,"nm":"Tunnel","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[layer(1,"Tunnel end (matte)",matte,td=1),layer(2,"Beams",beams,{"r":spin},tt=2)]}
emit("tunnel",lot,"tunnel")
