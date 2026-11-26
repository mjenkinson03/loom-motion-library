# Outro 1 (Morph): the shutter's last beat, snappy. As the loading bar completes the beams wind up, then ALL twelve gather clockwise, spiralling
# in together, and become a check mark: two of them (the lower left / lower right of centre) become its arms, the rest wind into the arms and
# disappear. The check, drawn with the beam's own 24-unit width, hops up a touch and drops back as if it had been hit, holds, dissolves,
# and the beams spring back open for the next loop. Beams only: no ring.
import math
from emit import emit
from holefix import wrap,R_HOLE
FPS=60; LOOP=4.65
CX,CY=130.5,124
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "click":((0.34,1.56),(0.64,1)),"out":((0.2,0.9),(0.3,1)),"in":((0.55,0),(1,0.45)),"io":((0.45,0),(0.55,1))}
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
T_WIND,T_GATHER,T_ARR=2.1,0.30,2.46          # wind-up starts, how long each beam takes to gather, when the check has formed
STAG=0.012                                    # clockwise stagger between beams
T_OUT,T_FADE,T_OPEN,T_SET,T_REST=3.2,3.5,3.65,4.05,4.3
def beam(r): return [24,r-40],[0,-(40+r)/2]
def arm(p0,p1):
    L=math.dist(p0,p1); c=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2); u=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L)
    return L,c,math.degrees(math.atan2(u[0],-u[1]))
def local(c,th):
    t=math.radians(th); return [c[0]*math.cos(t)+c[1]*math.sin(t), -c[0]*math.sin(t)+c[1]*math.cos(t)]
V=(-16,38); U2=(70,-76); n=math.hypot(*U2)
SHORT=arm((-52,2),V); LONG=arm((V[0]-12*U2[0]/n,V[1]-12*U2[1]/n),(54,-38))   # the check's two arms
ARMS={7:SHORT,5:LONG}                          # beams 7 / 5 = lower left / lower right of centre become the arms
def target(i):
    """Which arm beam i gathers into: the two arm beams take their own; the others split between the arms, nearest first."""
    if i in ARMS: return ARMS[i],True
    return (SHORT if i in (6,8,9,10,11) else LONG),False
def clockwise(th,base,min_turn=60):
    """equivalent angle of a (symmetric) beam, reached by turning clockwise by at least min_turn degrees."""
    while th<=base+min_turn: th+=180
    while th>base+min_turn+180: th-=180
    return th
def beam_keys(i):
    base=i*30; size=[];pos=[];rot=[]
    def add(t,sz,ps,r,e): size.append((t,sz,e)); pos.append((t,ps,e)); rot.append((t,[r],e))
    sz,ps=beam(100); add(0,sz,ps,base,"hold"); add(T_WIND-0.1,sz,ps,base,"gentle")
    t0=T_WIND+i*STAG; t1=t0+T_GATHER
    sz,ps=beam(104); add(t0,sz,ps,base,"click" if i in ARMS else "out")             # wound up; then all gather clockwise
    (L,c,th),is_arm=target(i)
    th=th if is_arm and False else clockwise(th,base)
    add(t1,[24,L if i in ARMS else 0],local(c,th),th,"H"); add(T_FADE,[24,L if i in ARMS else 0],local(c,th),th,"H")
    sz,ps=beam(40); add(T_OPEN,sz,ps,base,"snapout")
    for t,r,e in [(T_SET,108,"settle"),(T_REST,100,"hold"),(LOOP,100,"hold")]:
        sz,ps=beam(r); add(t,sz,ps,base,e)
    return kf(size),kf(pos),kf(rot)
H=14                                           # the hop: up a touch, then back down, as if hit
scl=kf([(0,[100,100,100],"hold"),(2.0,[100,100,100],"gentle"),(T_WIND,[103,103,100],"snapin"),(T_WIND+0.2,[98,98,100],"out"),(T_ARR,[100,100,100],"hold"),
        (T_ARR+0.09,[96,106,100],"in"),(T_ARR+0.2,[106,94,100],"io"),(T_ARR+0.3,[100,100,100],"hold"),
        (T_OUT,[100,100,100],"io"),(T_FADE,[104,104,100],"H"),(T_OPEN,[96,96,100],"snapout"),(T_SET,[102,102,100],"settle"),(T_REST,[100,100,100],"hold"),(LOOP,[100,100,100],"hold")])
pos=kf([(0,[CX,CY,0],"hold"),(T_ARR,[CX,CY,0],"out"),(T_ARR+0.09,[CX,CY-H,0],"in"),(T_ARR+0.2,[CX,CY,0],"hold"),(LOOP,[CX,CY,0],"hold")])
opa=kf([(0,[100],"hold"),(T_OUT,[100],"io"),(T_FADE,[0],"H"),(T_OPEN,[100],"H"),(LOOP,[100],"hold")])
tr=lambda rot:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot,"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[]
for i in range(12):
    size,ps,r=beam_keys(i)
    legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":ps,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(r)]})
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":opa,"r":S(0),"p":pos,"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Outro: morph","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
lot=wrap(lot,[(0,R_HOLE),(T_WIND,R_HOLE),(T_WIND+0.08,0),(T_FADE,0),(T_FADE+0.01,R_HOLE),(LOOP,R_HOLE)])
emit("outro-check",lot,"outro-check")
