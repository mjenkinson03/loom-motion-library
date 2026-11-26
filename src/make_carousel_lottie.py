# Icon carousel (Atlassian): a row of rounded dark tiles (Loom logo, film frame, cursor click, camera) turns left to right. Each tile that
# reaches the centre holds, gives a little wiggle, then the row moves on. Built only from shapes: no images, no effects.
import math
from emit import emit
FPS=60
HOLD,WIG,MOVE=1.3,0.55,0.55; STEP=HOLD+WIG+MOVE; N=4; LOOP=N*STEP
W,H=600,260; CX,CY=300,130; P=150; T=110
S=lambda v:{"a":0,"k":v}
WH=S([1,1,1,1])
EASE={"o":{"x":[0.55],"y":[0]},"i":{"x":[0.35],"y":[1]}}
LIN={"o":{"x":[0.5],"y":[0.5]},"i":{"x":[0.5],"y":[0.5]}}
tr=lambda r=0,s=100,p=(0,0):{"ty":"tr","p":S(list(p)),"a":S([0,0]),"s":S([s,s]),"r":S(r),"o":S(100),"sk":S(0),"sa":S(0)}
def stroke(w): return {"ty":"st","c":WH,"o":S(100),"w":S(w),"lc":2,"lj":2,"ml":4}
fill={"ty":"fl","c":WH,"o":S(100),"r":1}
def path(pts,closed=False):
    return {"ty":"sh","ks":S({"i":[[0,0]]*len(pts),"o":[[0,0]]*len(pts),"v":[list(p) for p in pts],"c":closed})}
def grp(items,nm): return {"ty":"gr","nm":nm,"it":items+[tr()]}
def rect(w,h,r=0,p=(0,0)): return {"ty":"rc","d":1,"s":S([w,h]),"p":S(list(p)),"r":S(r)}
# ---- the four icons, each roughly 60px, centred on 0,0 ----
def loom():
    legs=[{"ty":"gr","it":[rect(24,60,0,(0,-70)),fill,tr(i*30)]} for i in range(12)]
    ring={"ty":"gr","it":[{"ty":"el","d":1,"s":S([78,78]),"p":S([0,0])},{**stroke(10),"lc":1,"lj":1},tr()]}
    return [{"ty":"gr","nm":"Loom","it":legs+[ring,tr(0,36)]}]
def film():
    it=[grp([rect(62,74,10),stroke(6)],"Frame"),grp([path([(-15,-37),(-15,37)]),stroke(5)],"L"),grp([path([(15,-37),(15,37)]),stroke(5)],"R")]
    for y in (-24,0,24):
        for x in (-23,23): it.append(grp([rect(7,9,1.5,(x,y)),fill],"Hole"))
    return it
def cursor():
    arrow=[(-14,-28),(-14,20),(-2,9),(7,30),(15,26),(6,6),(22,6)]
    it=[grp([path(arrow,True),{**stroke(6),"lj":2}],"Arrow")]
    ticks=[((-27,-34),(-33,-40)),((-14,-40),(-14,-47)),((-3,-34),(3,-40))]
    for a,b in ticks: it.append(grp([path([a,b]),stroke(5)],"Tick"))
    return it
def camera():
    return [grp([rect(70,48,10,(0,6)),stroke(6)],"Body"),grp([path([(-14,-18),(-9,-28),(9,-28),(14,-18)]),stroke(6)],"Top"),
            grp([{"ty":"el","d":1,"s":S([26,26]),"p":S([0,6])},stroke(6)],"Lens")]
ICONS=[("Loom",loom),("Camera",camera),("Cursor",cursor),("Film",film)]
SLOT0=[0,1,2,-1]                                    # start slot of each tile: -1 left, 0 centre, 1 right, 2 hidden (right)
look={-2:(0,70),-1:(42,82),0:(100,100),1:(42,82),2:(0,70)}   # slot -> (opacity, scale)
def slot(i,k): return ((SLOT0[i]+k+1)%4)-1
def key(t,v,e=EASE,hold=False):
    d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
    if hold: d["h"]=1
    else: d.update(e)
    return d
def tile_layer(i):
    # build keyframes per step: stay, wiggle (centre only), move
    pk=[];ok=[];sk=[];rk=[]
    for k in range(N):
        t0=k*STEP; s=slot(i,k); s2=s+1 if s<2 else -1     # a tile at slot 2 re-enters from the left (slot -2 -> -1)
        tm=t0+HOLD+WIG; te=t0+STEP
        x0=CX+s*P; o0,s0=look[s]
        pk.append(key(t0,[x0,CY,0],LIN)); ok.append(key(t0,[o0],LIN)); sk.append(key(t0,[s0,s0,100],LIN))
        if s==2:                                           # hidden on the right: jump to hidden left at the start of the move
            pk.append(key(tm,[x0,CY,0],hold=True)); ok.append(key(tm,[0],hold=True)); sk.append(key(tm,[70,70,100],hold=True))
            pk.append(key(tm+1/FPS,[CX-2*P,CY,0])); ok.append(key(tm+1/FPS,[0])); sk.append(key(tm+1/FPS,[70,70,100]))
            x1=CX-P; o1,s1=look[-1]
        else:
            pk.append(key(tm,[x0,CY,0])); ok.append(key(tm,[o0])); sk.append(key(tm,[s0,s0,100]))
            x1=CX+(s+1)*P; o1,s1=look[s+1] if s+1<=2 else look[2]
        pk[-1]["o"]=EASE["o"]; pk[-1]["i"]=EASE["i"]
        pk.append(key(te,[x1,CY,0],LIN)); ok.append(key(te,[o1],LIN)); sk.append(key(te,[s1,s1,100],LIN))
        # wiggle: only the tile sitting in the centre
        r0=t0+HOLD
        if s==0:
            for j,(dt,a) in enumerate([(0,0),(0.08,-9),(0.2,8),(0.32,-5),(0.43,2.5),(WIG,0)]): rk.append(key(r0+dt,[a],EASE))
        else:
            rk.append(key(t0,[0],LIN))
    for L in (pk,ok,sk,rk):
        L.sort(key=lambda d:d["t"])
        # drop duplicate times (keep the later one) and the easing on the final key
        out=[]
        for d in L:
            if out and abs(out[-1]["t"]-d["t"])<1e-6: out[-1]=d
            else: out.append(d)
        L[:]=out
    # close the loop
    pk.append(key(LOOP,pk[0]["s"])); ok.append(key(LOOP,ok[0]["s"])); sk.append(key(LOOP,sk[0]["s"])); rk.append(key(LOOP,[0]))
    for L in (pk,ok,sk,rk): L[-1].pop("o",None); L[-1].pop("i",None)
    nm,fn=ICONS[i]
    shapes=fn()+[grp([rect(T,T,26),{"ty":"fl","c":S([0.176,0.176,0.188,1]),"o":S(100),"r":1}],"Tile")]     # first in the list = on top
    return {"ddd":0,"ind":i+1,"ty":4,"nm":nm,"sr":1,"ks":{"o":{"a":1,"k":ok},"r":{"a":1,"k":rk},"p":{"a":1,"k":pk},"a":S([0,0,0]),"s":{"a":1,"k":sk}},
            "ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":W,"h":H,"nm":"Icon carousel","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
     "layers":[tile_layer(i) for i in range(4)]}
emit("carousel",lot,"carousel")
