# Assemble: the 12 legs spin in from far out and bounce into place, the centre hole opens to lock them, the logo holds, then the legs
# fling outward clockwise. Built only from the logo's rectangles (no stroked circle anywhere): the hole is a matte.
from emit import emit
FPS=60
CW,CH=1400,880; CX,CY=CW/2,CH*0.42
LOOP=4.9
C={"in":(0.5,0,0.85,0.45),"out":(0.15,0.8,0.35,1),"io":(0.45,0,0.55,1),"lin":(0.5,0.5,0.5,0.5),"flat":(0.5,0,0.5,1),"fast":(0.2,0,0.1,1)}
def kf(keys,wrap=lambda v:[v]):
    k=[]
    for i,(t,v,e) in enumerate(keys):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in wrap(v)]}
        if i<len(keys)-1:
            c=C[e]; d.update({"o":{"x":[c[0]],"y":[c[1]]},"i":{"x":[c[2]],"y":[c[3]]}})
        k.append(d)
    return {"a":1,"k":k}
S=lambda v:{"a":0,"k":v}
W=S([1,1,1,1])
tr=lambda rot=None,p=None,a=None,s=None,o=None:{"ty":"tr","p":p or S([0,0]),"a":a or S([0,0]),"s":s or S([100,100]),"r":rot or S(0),"o":o or S(100),"sk":S(0),"sa":S(0)}
ORDER=[0,7,3,10,5,1,8,4,11,6,2,9]
SPIN=[-50,42,-36,58,-44,34,-60,38,-46,52,-32,48]
FLY_ORDER=list(range(12))
BREAK=3.5
legs=[]
for i in range(12):
    t0=0.15+ORDER.index(i)*0.045; land=t0+0.55
    off=kf([(0,175,"flat"),(t0,175,"in"),(land,-9,"out"),(land+0.16,3,"io"),(land+0.30,0,"flat"),
            (BREAK+FLY_ORDER.index(i)*0.03,0,"io"),(BREAK+FLY_ORDER.index(i)*0.03+0.12,-7,"in"),(BREAK+FLY_ORDER.index(i)*0.03+0.65,230,"flat"),(LOOP,230,"flat")],lambda d:[0,-60-d,0])
    rot=kf([(0,SPIN[i],"flat"),(t0,SPIN[i],"in"),(land,0,"flat"),
            (BREAK+FLY_ORDER.index(i)*0.03,0,"in"),(BREAK+FLY_ORDER.index(i)*0.03+0.65,-SPIN[i]*2,"flat"),(LOOP,-SPIN[i]*2,"flat")])
    ob=BREAK+FLY_ORDER.index(i)*0.03
    op=kf([(0,0,"flat"),(t0,0,"io"),(t0+0.22,100,"flat"),(ob+0.3,100,"io"),(ob+0.65,0,"flat"),(LOOP,0,"flat")])
    inner={"ty":"gr","nm":f"Leg {i+1} piece","it":[{"ty":"rc","d":1,"s":S([24,80]),"p":S([0,-60]),"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},
           tr(rot=rot,p=off,a=S([0,-60,0]),o=op)]}
    legs.append({"ty":"gr","nm":f"Leg {i+1}","it":[inner,tr(rot=S(i*30))]})
T_HOLE=0.15+11*0.045+0.55+0.05
hole=kf([(0,0,"flat"),(T_HOLE,0,"out"),(T_HOLE+0.25,78,"io"),(T_HOLE+0.45,66,"io"),(T_HOLE+0.6,68,"flat"),(LOOP,68,"flat")],lambda d:[d,d])
matte=[{"ty":"gr","it":[{"ty":"el","d":1,"s":hole,"p":S([0,0])},{"ty":"fl","c":W,"o":S(100),"r":1},tr()]}]
base={"o":S(100),"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":S([100,100,100])}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":CW,"h":CH,"nm":"Assemble","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Centre hole (matte)","sr":1,"ks":base,"ao":0,"shapes":matte,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0,"td":1},
           {"ddd":0,"ind":2,"ty":4,"nm":"Legs","sr":1,"ks":base,"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0,"tt":2}]}
emit("assemble",lot,"assemble")
