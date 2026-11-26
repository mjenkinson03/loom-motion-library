# Outro 2 (Bounce check): the shutter plays all the way through (wind up, snap, spring open) as the bar fills. Then the logo lifts a little
# (winding up a shot) and drops like a basketball, right off the bottom of the screen. Then a check mark bounces back up into place: the two bottom beams
# slide up into the check while the other ten beams shrink away. The check settles with a little dribble, holds, dissolves, then the beams spring back open.
# (v2: the logo now drops right off the bottom of the screen first; while it is out of sight it becomes the check, which bounces back up into place.)
import math
from emit import emit
from holefix import wrap,R_HOLE
FPS=60; LOOP=5.15
CX,CY=130.5,750        # tall comp (1500) so the logo can fall completely out of sight before the check rises
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "click":((0.34,1.56),(0.64,1)),"io":((0.45,0),(0.55,1)),"out":((0.22,1),(0.36,1)),"in":((0.55,0),(1,0.45))}
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
T_LIFT0,T_LIFT1,T_GONE,T_RISE,T_APEX,T_LAND,T_UP2,T_DONE=2.4,2.7,2.9,2.92,3.2,3.38,3.48,3.58
T_OUT,T_FADE,T_OPEN,T_SET,T_REST=3.75,4.1,4.25,4.7,4.95
OFF=140            # the floor: the logo's bottom lands just above the blue loading bar (fading to 0% on the way down, back to 100% on the way up)
def beam(r): return [24,r-40],[0,-(40+r)/2]
def arm(p0,p1):
    L=math.dist(p0,p1); c=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2); u=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L)
    return L,c,math.degrees(math.atan2(u[0],-u[1]))
def local(c,th):
    t=math.radians(th); return [c[0]*math.cos(t)+c[1]*math.sin(t), -c[0]*math.sin(t)+c[1]*math.cos(t)]
V=(-16,38); U2=(70,-76); n=math.hypot(*U2)
ARMS={7:arm((-52,2),V),5:arm((V[0]-12*U2[0]/n,V[1]-12*U2[1]/n),(54,-38))}   # beams 7 / 5 = lower left / lower right of centre
# shutter, played through: (time, outer radius, easing)
SHUT=[(0,100,"hold"),(1.3,100,"gentle"),(1.5,104,"snapin"),(1.68,40,"hold"),(1.76,40,"snapout"),(2.1,108,"settle"),(2.4,100,"hold")]
def beam_keys(i):
    base=i*30; size=[];pos=[];rot=[]
    def add(t,sz,ps,r,e): size.append((t,sz,e)); pos.append((t,ps,e)); rot.append((t,[r],e))
    for t,r,e in SHUT: sz,ps=beam(r); add(t,sz,ps,base,e)
    sz,ps=beam(100); add(T_GONE,sz,ps,base,"H")                           # full logo falls away; the change to a check happens while it is out of sight
    if i in ARMS:
        L,c,th=ARMS[i]; th=min((th+180*k for k in range(-3,4)),key=lambda x:abs(x-base))
        add(T_GONE+0.02,[24,L],local(c,th),th,"H"); add(T_FADE,[24,L],local(c,th),th,"H")
    else:
        sz,ps=beam(40); add(T_GONE+0.02,sz,ps,base,"H"); add(T_FADE,sz,ps,base,"H")
    sz,ps=beam(40); add(T_OPEN,sz,ps,base,"snapout")
    for t,r,e in [(T_SET,108,"settle"),(T_REST,100,"hold"),(LOOP,100,"hold")]:
        sz,ps=beam(r); add(t,sz,ps,base,e)
    return kf(size),kf(pos),kf(rot)
# the ball: lift, drop, squash on the floor, rise as the check, dribble to rest
Y=lambda y:[CX,CY+y,0]
pos=kf([(0,Y(0),"hold"),(T_LIFT0,Y(0),"out"),(T_LIFT1,Y(-26),"in"),(T_GONE,Y(OFF),"H"),(T_RISE,Y(OFF),"out"),(T_APEX,Y(-14),"in"),(T_LAND,Y(0),"out"),(T_UP2,Y(-4),"in"),(T_DONE,Y(0),"hold"),(LOOP,Y(0),"hold")])
scl=kf([(0,[100,100,100],"hold"),(1.3,[100,100,100],"gentle"),(1.5,[103,103,100],"snapin"),(1.68,[96,96,100],"hold"),(1.76,[96,96,100],"snapout"),(2.1,[102,102,100],"settle"),(2.4,[100,100,100],"hold"),
        (T_LIFT1,[100,100,100],"in"),(T_GONE,[100,100,100],"H"),(T_RISE,[100,100,100],"out"),(T_APEX,[100,100,100],"hold"),(T_LAND-0.02,[100,100,100],"out"),(T_LAND+0.04,[100,100,100],"io"),(T_UP2,[100,100,100],"hold"),
        (T_OUT,[100,100,100],"io"),(T_FADE,[104,104,100],"H"),(T_OPEN,[96,96,100],"snapout"),(T_SET,[102,102,100],"settle"),(T_REST,[100,100,100],"hold"),(LOOP,[100,100,100],"hold")])
opa=kf([(0,[100],"hold"),(T_LIFT1,[100],"in"),(T_GONE,[0],"hold"),(T_RISE,[0],"out"),(T_RISE+0.2,[100],"hold"),(T_OUT,[100],"io"),(T_FADE,[0],"H"),(T_OPEN,[100],"H"),(LOOP,[100],"hold")])
tr=lambda rot:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot,"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[]
for i in range(12):
    size,ps,rot=beam_keys(i)
    legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":ps,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(rot)]})
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":opa,"r":S(0),"p":pos,"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":1500,"nm":"Outro: bounce check","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
lot=wrap(lot,[(0,R_HOLE),(T_LIFT1,R_HOLE),(T_GONE,0),(T_FADE,0),(T_FADE+0.01,R_HOLE),(LOOP,R_HOLE)])
emit("outro-bounce",lot,"outro-bounce")
