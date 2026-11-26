# Outro 4 (Fan): the shutter plays all the way through as the bar fills. Then the beams close like a hand fan, one after another, starting
# at the top left and going clockwise: each folds a notch clockwise onto its neighbour, shortening in towards the hinge at the centre, and fades
# away. Once the fan is shut and gone, the beams open again in the same clockwise order for the next loop. Beams only; no check.
from emit import emit
from holefix import wrap,R_HOLE
FPS=60; LOOP=5.5
CX,CY=130.5,124
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "io":((0.45,0),(0.55,1)),"in":((0.55,0),(1,0.45)),"out":((0.2,0.9),(0.3,1))}
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
SHUT=[(0,100,"hold"),(1.3,100,"gentle"),(1.5,104,"snapin"),(1.68,46,"hold"),(1.76,46,"snapout"),(2.1,108,"settle"),(2.4,100,"hold")]
T_CLOSE,CLOSE_STAG,CLOSE_DUR=2.5,0.06,0.38        # fan closes: first beam at 2.5s, one more every 60ms, 380ms each
T_OPEN,OPEN_STAG,OPEN_DUR=4.0,0.05,0.4
T_REST=4.0+11*0.05+0.4+0.2
FOLD=30                                            # each beam folds 30 degrees clockwise (onto its neighbour)
def beam_keys(i):
    base=i*30; k=(i-11)%12                           # k = order of closing: beam 11 (top left, 11 o'clock) first, then 12 o'clock, 1 o'clock ...
    size=[];pos=[];rot=[];opa=[]
    def add(t,sz,ps,r,o,e): size.append((t,sz,e)); pos.append((t,ps,e)); rot.append((t,[r],e)); opa.append((t,[o],e))
    for t,r,e in SHUT: sz,ps=beam(r); add(t,sz,ps,base,100,e)
    c0=T_CLOSE+k*CLOSE_STAG; c1=c0+CLOSE_DUR
    sz,ps=beam(100); add(c0,sz,ps,base,100,"in")                          # folds clockwise, shortening towards the hinge, fading out
    sz,ps=beam(40); add(c1,sz,ps,base+FOLD,0,"H")
    o0=T_OPEN+k*OPEN_STAG; o1=o0+OPEN_DUR
    sz,ps=beam(40); add(o0,sz,ps,base-FOLD,0,"out")                       # opens again in the same order, unfolding clockwise
    sz,ps=beam(100); add(o1,sz,ps,base,100,"hold")
    add(LOOP,sz,ps,base,100,"hold")
    return kf(size),kf(pos),kf(rot),kf(opa)
tr=lambda rot,o:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot,"o":o,"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[]
for i in range(12):
    size,ps,r,o=beam_keys(i)
    legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":ps,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(r,o)]})
scl=kf([(0,[100,100,100],"hold"),(1.3,[100,100,100],"gentle"),(1.5,[103,103,100],"snapin"),(1.68,[96,96,100],"hold"),(1.76,[96,96,100],"snapout"),(2.1,[102,102,100],"settle"),(2.4,[100,100,100],"hold"),(LOOP,[100,100,100],"hold")])
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":S(100),"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Outro: fan","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
lot=wrap(lot,[(0,R_HOLE),(LOOP,R_HOLE)])
emit("outro-fan",lot,"outro-fan")
