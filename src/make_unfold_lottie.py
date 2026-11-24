# Unfold: one beam wipes in (slight angle), spins in place while the other beams appear, the centre circle grows (a hole punched by a matte),
# it becomes the Loom logo, a clockwise flutter ripples round it, then it reverses on exit. Per-segment easing; the exit plays the curves backwards.
from emit import emit
FPS=60
CX,CY=130.5,124
CURVES={"io":(0.45,0,0.55,1),"spin":(0.65,0,0.35,1),"wipe":(0.4,0,0.2,1),"out":(0.25,0.9,0.4,1),"flat":(0.5,0,0.5,1)}
flip=lambda c:(1-c[2],1-c[3],1-c[0],1-c[1])
ease=lambda x:4*x*x*x if x<.5 else 1-pow(-2*x+2,3)/2
WIPE=(0.10,0.60); SPIN=(0.65,1.55); CIRC=(1.45,1.95); T_IN=1.95
START_ANGLE,END_ANGLE=-12,150
BEAM_ANGLES=[0,30,60,90,120]
HOLD_END=T_IN+2.4; EXIT_SCALE=0.9
FLUTTER_START=T_IN+0.7; STAGGER=0.09
LOOP=round(HOLD_END+T_IN*EXIT_SCALE+0.2,2)
def full_keys(kin):
    keys=[(t,v,e) for t,v,e in kin]
    keys.append((HOLD_END,kin[-1][1],"flat"))
    for j in range(len(kin)-1,0,-1):
        t,v,_=kin[j]; pe=kin[j-1][2]
        keys.append((HOLD_END+(T_IN-t)*EXIT_SCALE,v,("rev",pe)))
    keys.append((LOOP,kin[0][1],"flat"))
    return keys
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
def add_dips(keys,i):
    s=FLUTTER_START+i*STAGGER
    keys=list(keys)+[(s,100,"io"),(s+0.12,80,"io"),(s+0.32,100,"flat")]
    out=[]
    for k in sorted(keys,key=lambda k:k[0]):
        if not out or k[0]>out[-1][0]+1e-6: out.append(k)
    return out
def static(v): return {"a":0,"k":v}
tr=lambda rot=None,op=None:{"ty":"tr","p":static([0,0]),"a":static([0,0]),"s":static([100,100]),"r":rot or static(0),"o":op or static(100),"sk":static(0),"sa":static(0)}
SOFT=70
front=full_keys([(0,-100-SOFT,"flat"),(WIPE[0],-100-SOFT,"wipe"),(WIPE[1],100,"flat"),(T_IN,100,"flat")])
lead_rot=full_keys([(0,START_ANGLE,"flat"),(SPIN[0],START_ANGLE,"spin"),(SPIN[1],END_ANGLE,"flat"),(T_IN,END_ANGLE,"flat")])
grad={"ty":"gf","o":static(100),"r":1,"t":1,"s":kf(front,lambda f:[0,f]),"e":kf(front,lambda f:[0,f+SOFT]),"g":{"p":2,"k":static([0,1,1,1, 1,1,1,1, 0,1, 1,0])}}
def bar(rot=None,fill=None,op=None):
    return {"ty":"gr","it":[{"ty":"rc","d":1,"s":static([24,200]),"p":static([0,0]),"r":static(0)},fill or {"ty":"fl","c":static([1,1,1,1]),"o":static(100),"r":1},tr(rot,op)]}
shapes=[]
for a in BEAM_ANGLES:
    target=(a-START_ANGLE)/(END_ANGLE-START_ANGLE); lo,hi=0,1
    for _ in range(40):
        mid=(lo+hi)/2
        if ease(mid)<target: lo=mid
        else: hi=mid
    ta=SPIN[0]+lo*(SPIN[1]-SPIN[0])-0.05
    op=full_keys([(0,0,"flat"),(ta,0,"io"),(ta+0.16,100,"flat"),(T_IN,100,"flat")])
    op=add_dips(op,1+BEAM_ANGLES.index(a))
    shapes.append(bar(static(a),None,kf(op)))
lead_op=add_dips([(0,100,"flat"),(LOOP,100,"flat")],0)
shapes.append(bar(kf(lead_rot),grad,kf(lead_op)))
circ=full_keys([(0,0,"flat"),(CIRC[0],0,"out"),(CIRC[1]-0.10,72,"io"),(T_IN,68,"flat")])
matte=[{"ty":"gr","it":[{"ty":"el","d":1,"s":kf(circ,lambda r:[r,r]),"p":static([0,0])},{"ty":"fl","c":static([1,1,1,1]),"o":static(100),"r":1},tr()]}]
def layer(ind,nm,shapes,**extra):
    d={"ddd":0,"ind":ind,"ty":4,"nm":nm,"sr":1,"ks":{"o":static(100),"r":static(0),"p":static([CX,CY,0]),"a":static([0,0,0]),"s":static([100,100,100])},"ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
    d.update(extra); return d
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Unfold","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[layer(1,"Centre circle (matte)",matte,td=1),layer(2,"Beams",shapes,tt=2)]}
emit("unfold",lot,"unfold")
