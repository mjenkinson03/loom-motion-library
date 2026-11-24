# Surfacing: the logo steps forward into the light. It is already there, nearly invisible in shadow; a soft diagonal shadow edge
# leaves it from top-left to bottom-right (that is the whole entrance) while it rises/grows a little. Once fully lit, the legs ripple
# (dip to ~80% one after another, clockwise from the top). Then it holds and steps back into shadow.
import math
from emit import emit
FPS=60; LOOP=5.4
CX,CY=130.5,124
C={"io":(0.45,0,0.55,1),"out":(0.2,0.9,0.35,1),"in":(0.6,0,0.8,0.3),"flat":(0.5,0,0.5,1)}
def kf(keys,wrap=lambda v:[v]):
    k=[]
    for i,(t,v,e) in enumerate(keys):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in wrap(v)]}
        if i<len(keys)-1:
            c=C[e]; d.update({"o":{"x":[c[0]],"y":[c[1]]},"i":{"x":[c[2]],"y":[c[3]]}})
        k.append(d)
    return {"a":1,"k":k}
S=lambda v:{"a":0,"k":v}
def pt(a,u,v):
    d=(math.sin(a),-math.cos(a)); c=(math.cos(a),math.sin(a)); return [u*c[0]+v*d[0],u*c[1]+v*d[1]]
V=[]
for i in range(12):
    a=math.radians(i*30)
    V+=[pt(a,-12,100),pt(a,12,100),[46.36*math.sin(a+math.radians(15)),-46.36*math.cos(a+math.radians(15))]]
V=[[round(x,3),round(y,3)] for x,y in V]
star={"ty":"sh","nm":"Logo outline","ks":S({"i":[[0,0]]*len(V),"o":[[0,0]]*len(V),"v":V,"c":True})}
hole={"ty":"el","nm":"Hole","d":2,"s":S([68,68]),"p":S([0,0])}
tr=lambda:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":S(0),"o":S(100),"sk":S(0),"sa":S(0)}
T_GROW0,T_GROW1,T_HOLD,T_REC1,T_END=0.6,2.0,3.5,5.0,5.2
SOFT=90
fr=kf([(0,-250,"flat"),(T_GROW0,-250,"io"),(T_GROW1,120,"flat"),(T_HOLD,120,"io"),(T_REC1,-250,"flat"),(LOOP,-250,"flat")],lambda f:[f,f])
fr2=kf([(0,-250+SOFT,"flat"),(T_GROW0,-250+SOFT,"io"),(T_GROW1,120+SOFT,"flat"),(T_HOLD,120+SOFT,"io"),(T_REC1,-250+SOFT,"flat"),(LOOP,-250+SOFT,"flat")],lambda f:[f,f])
shadowgrp={"ty":"gr","nm":"Shadow","it":[{"ty":"rc","d":1,"s":S([420,420]),"p":S([0,0]),"r":S(0)},
   {"ty":"gf","o":S(100),"r":1,"t":1,"s":fr,"e":fr2,"g":{"p":2,"k":S([0,0.043,0.043,0.047, 1,0.043,0.043,0.047, 0,0, 1,0.95])}},tr()]}
overlays=[]
for i in range(12):
    s=T_GROW1+0.05+i*0.07
    dip=kf([(0,0,"flat"),(s,0,"io"),(s+0.12,20,"io"),(s+0.32,0,"flat"),(LOOP,0,"flat")])
    overlays.append({"ty":"gr","nm":f"Ripple {i+1}","it":[{"ty":"rc","d":1,"s":S([24,54]),"p":S([0,-73.2]),"r":S(0)},
        {"ty":"fl","c":S([0.043,0.043,0.047,1]),"o":S(100),"r":1},
        {"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":S(i*30),"o":dip,"sk":S(0),"sa":S(0)}]})
bodygrp={"ty":"gr","nm":"Body","it":[star,hole,{"ty":"fl","c":S([1,1,1,1]),"o":S(100),"r":2},tr()]}
RISE=5
scale=kf([(0,[94,94,100],"flat"),(T_GROW0,[94,94,100],"io"),(T_GROW1,[104,104,100],"flat"),(T_HOLD,[105,105,100],"io"),(T_REC1,[94,94,100],"flat"),(LOOP,[94,94,100],"flat")],lambda v:v)
pos=kf([(0,[CX,CY+RISE,0],"flat"),(T_GROW0,[CX,CY+RISE,0],"io"),(T_GROW1,[CX,CY,0],"flat"),(T_HOLD,[CX,CY,0],"io"),(T_REC1,[CX,CY+RISE,0],"flat"),(LOOP,[CX,CY+RISE,0],"flat")],lambda v:v)
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Surfacing","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Logo","sr":1,"ks":{"o":S(100),"r":S(0),"p":pos,"a":S([0,0,0]),"s":scale},"ao":0,"shapes":[shadowgrp]+overlays+[bodygrp],"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}]}
emit("surfacing",lot,"surfacing")
