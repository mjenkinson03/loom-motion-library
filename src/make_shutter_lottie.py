# Shutter: the logo's 12 legs wind up, snap shut like a shutter, then spring back open. Long hold at full, with a clockwise ripple round the legs.
from emit import emit
FPS=60; LOOP=3.4; T_RIPPLE=2.5; STAGGER=0.05
CX,CY=130.5,124
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1))}
KEYS=[(0.00,100,100,"hold"),(1.30,100,100,"gentle"),(1.50,104,103,"snapin"),(1.68,46,96,"hold"),(1.76,46,96,"snapout"),(2.10,108,102,"settle"),(2.40,100,100,"hold"),(LOOP,100,100,"hold")]
def kf(vals):
    k=[]
    for i,(t,v,e) in enumerate(vals):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
        if i<len(vals)-1:
            (ox,oy),(ix,iy)=BEZ[e]; d.update({"o":{"x":[ox],"y":[oy]},"i":{"x":[ix],"y":[iy]}})
        k.append(d)
    return {"a":1,"k":k}
size=kf([(t,[24,r-40],e) for t,r,s,e in KEYS]); pos=kf([(t,[0,-(40+r)/2],e) for t,r,s,e in KEYS]); scl=kf([(t,[s,s,100],e) for t,r,s,e in KEYS])
def dip(i):
    # once fully open and settled, a ripple runs clockwise round the legs (each dips to 80% and back), well before the next wind-up
    s=T_RIPPLE+i*STAGGER
    ks=[(0,100),(s,100),(s+0.12,80),(s+0.32,100),(LOOP,100)]
    k=[{"t":round(t*FPS,2),"s":[v],"o":{"x":[0.45],"y":[0]},"i":{"x":[0.55],"y":[1]}} for t,v in ks[:-1]]+[{"t":round(ks[-1][0]*FPS,2),"s":[ks[-1][1]]}]
    return {"a":1,"k":k}
tr=lambda rot=0,o=None:{"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":rot},"o":o or {"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}
W={"a":0,"k":[1,1,1,1]}
shapes=[{"ty":"gr","nm":f"Leg {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":pos,"r":{"a":0,"k":0}},{"ty":"fl","c":W,"o":{"a":0,"k":100},"r":1},tr(i*30,dip(i))]} for i in range(12)]
# (no centre ring: just the beams)
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Shutter","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Logo","sr":1,"ks":{"o":{"a":0,"k":100},"r":{"a":0,"k":0},"p":{"a":0,"k":[CX,CY,0]},"a":{"a":0,"k":[0,0,0]},"s":scl},"ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}]}
emit("shutter",lot,"shutter")
