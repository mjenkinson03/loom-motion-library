# Outro 5 (Drop): the shutter plays all the way through as the bar fills. Then the whole logo simply drops away, accelerating downward
# after a little nudge upward (stretching a touch as it picks up speed) along a curve: it eases out sideways while it accelerates down, tilting a little, and fades to 0%. Outro only: the loop restarts from the full logo.
from emit import emit
from holefix import wrap,R_HOLE
FPS=60; LOOP=3.05
CX,CY=130.5,750        # tall comp (1500) so the logo has room to fall without being clipped
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "fall":((0.6,0),(0.95,0.4)),"fade":((0.4,0),(0.8,0.6)),"arc":((0.15,0.55),(0.4,1)),"nudge":((0.2,0.9),(0.4,1))}
def kf(vals):
    k=[]
    for i,(t,v,e) in enumerate(vals):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
        if e=="H": d["h"]=1
        elif i<len(vals)-1:
            (ox,oy),(ix,iy)=BEZ[e]; d.update({"o":{"x":[ox],"y":[oy]},"i":{"x":[ix],"y":[iy]}})
        k.append(d)
    return {"a":1,"k":k}
S=lambda v:{"a":0,"k":v}
def beam(r): return [24,r-40],[0,-(40+r)/2]
SHUT=[(0,100,"hold"),(1.3,100,"gentle"),(1.5,104,"snapin"),(1.68,46,"hold"),(1.76,46,"snapout"),(2.1,108,"settle"),(2.4,100,"hold"),(LOOP,100,"hold")]
T_NUDGE,T_DROP,T_END=2.4,2.5,2.78      # nudged up for 0.1s, then the drop: 0.28s, quick
NUDGE=16                               # how far it is nudged up first
DROP=230; SIDE=46                                # how far it falls (units)
size=kf([(t,beam(r)[0],e) for t,r,e in SHUT]); ps=kf([(t,beam(r)[1],e) for t,r,e in SHUT])
tr=lambda rot:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":S(rot),"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[{"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":ps,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(i*30)]} for i in range(12)]
def kf1(v): return kf([(t,[x],e) for t,x,e in v])
pos={"a":1,"s":True,"x":kf1([(0,CX,"hold"),(T_DROP,CX,"arc"),(T_END,CX+SIDE,"H"),(LOOP,CX+SIDE,"hold")]),
     "y":kf1([(0,CY,"hold"),(T_NUDGE,CY,"nudge"),(T_DROP,CY-NUDGE,"fall"),(T_END,CY+DROP,"H"),(LOOP,CY+DROP,"hold")]),"z":S(0)}
rot=kf1([(0,0,"hold"),(T_DROP,0,"arc"),(T_END,14,"H"),(LOOP,14,"hold")])
opa=kf([(0,[100],"hold"),(T_DROP,[100],"fade"),(T_END,[0],"H"),(LOOP,[0],"hold")])
scl=kf([(0,[100,100,100],"hold"),(1.3,[100,100,100],"gentle"),(1.5,[103,103,100],"snapin"),(1.68,[96,96,100],"hold"),(1.76,[96,96,100],"snapout"),(2.1,[102,102,100],"settle"),(2.4,[100,100,100],"nudge"),
        (T_DROP,[98,104,100],"fall"),(T_END,[94,110,100],"H"),(LOOP,[94,110,100],"hold")])
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":opa,"r":rot,"p":pos,"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":1500,"nm":"Outro: drop","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
lot=wrap(lot,[(0,R_HOLE),(LOOP,R_HOLE)])
emit("outro-drop",lot,"outro-drop")
