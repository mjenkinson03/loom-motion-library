# Outro 3 (Cartwheel): the shutter plays all the way through as the bar fills. Then the logo spins up very quickly (while drifting left like a
# run-up) and cartwheels back across, one full turn with a little hop. On the way the two bottom beams click into a check and the other ten
# shrink away; it lands upright as the check (with a small squash), holds, dissolves, then the beams spring back open.
import math
from emit import emit
from holefix import wrap,R_HOLE
FPS=60; LOOP=5.7
CX,CY=350,124          # wide comp (700) so the cartwheel has room
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "click":((0.34,1.56),(0.64,1)),"io":((0.45,0),(0.55,1)),"out":((0.22,1),(0.36,1)),"in":((0.55,0),(1,0.45)),"lin":((0,0),(1,1))}
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
# timeline (seconds)
T_SPIN0,T_SPIN1,T_HOP,T_LAND,T_DONE=2.4,2.75,2.9,3.07,3.17
T_M0,T_M1=2.8,3.02
T_OUT,T_FADE,T_OPEN,T_SET,T_REST=4.3,4.7,4.9,5.35,5.6
RUN=-110           # how far left the logo drifts during the spin (the run-up)
def beam(r): return [24,r-40],[0,-(40+r)/2]
def arm(p0,p1):
    L=math.dist(p0,p1); c=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2); u=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L)
    return L,c,math.degrees(math.atan2(u[0],-u[1]))
def local(c,th):
    t=math.radians(th); return [c[0]*math.cos(t)+c[1]*math.sin(t), -c[0]*math.sin(t)+c[1]*math.cos(t)]
V=(-16,38); U2=(70,-76); n=math.hypot(*U2)
ARMS={7:arm((-52,2),V),5:arm((V[0]-12*U2[0]/n,V[1]-12*U2[1]/n),(54,-38))}   # beams 7 / 5 = lower left / lower right of centre
# shutter, played through: (time, outer radius, easing)
SHUT=[(0,100,"hold"),(1.3,100,"gentle"),(1.5,104,"snapin"),(1.68,46,"hold"),(1.76,46,"snapout"),(2.1,108,"settle"),(2.4,100,"hold")]
def beam_keys(i):
    base=i*30; size=[];pos=[];rot=[]
    def add(t,sz,ps,r,e): size.append((t,sz,e)); pos.append((t,ps,e)); rot.append((t,[r],e))
    for t,r,e in SHUT: sz,ps=beam(r); add(t,sz,ps,base,e)
    sz,ps=beam(100); add(T_M0,sz,ps,base,"click" if i in ARMS else "snapin")
    if i in ARMS:
        L,c,th=ARMS[i]; th=min((th+180*k for k in range(-3,4)),key=lambda x:abs(x-base))
        add(T_M1,[24,L],local(c,th),th,"H"); add(T_FADE,[24,L],local(c,th),th,"H")
    else:
        sz,ps=beam(40); add(T_M1,sz,ps,base,"H"); add(T_FADE,sz,ps,base,"H")
    sz,ps=beam(40); add(T_OPEN,sz,ps,base,"snapout")
    for t,r,e in [(T_SET,108,"settle"),(T_REST,100,"hold"),(LOOP,100,"hold")]:
        sz,ps=beam(r); add(t,sz,ps,base,e)
    return kf(size),kf(pos),kf(rot)
# the gymnast: spin up fast while running left, then one full cartwheel back to the centre with a hop, landing upright as the check
def kf1(vals): return kf([(t,[v],e) for t,v,e in vals])
px=kf1([(0,CX,"hold"),(T_SPIN0,CX,"io"),(T_SPIN1,CX+RUN,"H"),(T_SPIN1+0.001,CX+RUN,"out"),(T_LAND,CX,"hold"),(LOOP,CX,"hold")])
py=kf1([(0,CY,"hold"),(T_SPIN1,CY,"out"),(T_HOP,CY-34,"in"),(T_LAND,CY,"hold"),(LOOP,CY,"hold")])
pos={"a":1,"s":True,"x":px,"y":py,"z":S(0)}
lrot=kf1([(0,0,"hold"),(T_SPIN0,0,"in"),(T_SPIN1,360,"lin"),(T_LAND,720,"hold"),(T_FADE,720,"H"),(T_OPEN,0,"hold"),(LOOP,0,"hold")])
scl=kf([(0,[100,100,100],"hold"),(1.3,[100,100,100],"gentle"),(1.5,[103,103,100],"snapin"),(1.68,[96,96,100],"hold"),(1.76,[96,96,100],"snapout"),(2.1,[102,102,100],"settle"),(2.4,[100,100,100],"hold"),
        (T_LAND-0.02,[100,100,100],"out"),(T_LAND+0.05,[108,92,100],"io"),(T_DONE,[100,100,100],"hold"),
        (T_OUT,[100,100,100],"io"),(T_FADE,[104,104,100],"H"),(T_OPEN,[96,96,100],"snapout"),(T_SET,[102,102,100],"settle"),(T_REST,[100,100,100],"hold"),(LOOP,[100,100,100],"hold")])
opa=kf([(0,[100],"hold"),(T_OUT,[100],"io"),(T_FADE,[0],"H"),(T_OPEN,[100],"H"),(LOOP,[100],"hold")])
tr=lambda rot:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot,"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[]
for i in range(12):
    size,ps,rot=beam_keys(i)
    legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":ps,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(rot)]})
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":opa,"r":lrot,"p":pos,"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":700,"h":248,"nm":"Outro: cartwheel check","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
lot=wrap(lot,[(0,R_HOLE),(T_M0,R_HOLE),(T_M0+0.08,0),(T_FADE,0),(T_FADE+0.01,R_HOLE),(LOOP,R_HOLE)])
emit("outro-cartwheel",lot,"outro-cartwheel")
