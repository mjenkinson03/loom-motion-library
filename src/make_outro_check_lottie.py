# Outro 1 (Shutter -> check): the shutter's last beat. As the loading bar completes, the legs wind up and snap in; ten of them shrink
# away into the centre while two of them (the beams at 3 and 8 o'clock-ish) swing round and turn into the two arms of a check mark, drawn
# with the beam's own 24-unit width. The check holds, dissolves, and the beams spring back open for the next loop. Beams only: no ring.
import math
from emit import emit
FPS=60; LOOP=5.9
CX,CY=130.5,124
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),
     "morph":((0.45,0),(0.15,1)),"io":((0.45,0),(0.55,1))}
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
T_WIND,T_SNAP,T_M,T_OUT,T_FADE,T_OPEN,T_SET,T_REST=2.2,2.45,2.85,3.9,4.4,4.7,5.15,5.45
# beams as (length-from-radius-40 [outer radius r]) : size [24, r-40], centre y -(40+r)/2
def beam(r): return [24,r-40],[0,-(40+r)/2]
# the check: two arms from the beams at index 8 (lower left) and 3 (right); rect centre c, length L, rotation th (clockwise degrees)
def arm(p0,p1):
    L=math.dist(p0,p1); c=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2); u=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L)
    th=math.degrees(math.atan2(u[0],-u[1]))                    # axis of a vertical rect rotated clockwise by th is (sin th, -cos th)
    return L,c,th
def local(c,th):                                                # rect centre in the rotated frame
    t=math.radians(th); return [c[0]*math.cos(t)+c[1]*math.sin(t), -c[0]*math.sin(t)+c[1]*math.cos(t)]
V=(-16,38); U2=(70,-76); n=math.hypot(*U2)
short=arm((-52,2),V)                                            # to the vertex
long_=arm((V[0]-12*U2[0]/n,V[1]-12*U2[1]/n),(54,-38))          # starts 12 behind the vertex so the corner is filled
ARMS={8:short,3:long_}
def beam_keys(i):
    base=i*30; size=[];pos=[];rot=[]
    def add(t,sz,ps,r,e): size.append((t,sz,e)); pos.append((t,ps,e)); rot.append((t,[r],e))
    for t,r,e in [(0,100,"hold"),(2.0,100,"gentle"),(T_WIND,104,"snapin" if i not in ARMS else "morph")]:
        sz,ps=beam(r); add(t,sz,ps,base,e)
    if i in ARMS:
        L,c,th=ARMS[i]
        if th-base>180: th-=360
        if th-base<-180: th+=360
        add(T_M,[24,L],local(c,th),th,"H")                  # arm state; held until it is collapsed (while invisible)
        add(T_FADE,[24,L],local(c,th),th,"H")
    else:
        sz,ps=beam(40); add(T_SNAP,sz,ps,base,"H"); add(T_FADE,sz,ps,base,"H")
    sz,ps=beam(40); add(T_OPEN,sz,ps,base,"snapout")
    for t,r,e in [(T_SET,108,"settle"),(T_REST,100,"hold"),(LOOP,100,"hold")]:
        sz,ps=beam(r); add(t,sz,ps,base,e)
    return kf(size),kf(pos),kf(rot)
# logo scale: wind-up, snap, a little pop as the check forms, then reopen
scl=kf([(0,[100,100,100],"hold"),(2.0,[100,100,100],"gentle"),(T_WIND,[103,103,100],"snapin"),(T_SNAP,[96,96,100],"settle"),(T_M+0.1,[106,106,100],"io"),(T_M+0.4,[100,100,100],"hold"),
        (T_OUT,[100,100,100],"io"),(T_FADE,[104,104,100],"H"),(T_OPEN,[96,96,100],"snapout"),(T_SET,[102,102,100],"settle"),(T_REST,[100,100,100],"hold"),(LOOP,[100,100,100],"hold")])
opa=kf([(0,[100],"hold"),(T_OUT,[100],"io"),(T_FADE,[0],"H"),(T_OPEN,[100],"H"),(LOOP,[100],"hold")])
tr=lambda rot:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":rot,"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[]
for i in range(12):
    size,pos,rot=beam_keys(i)
    legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":pos,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(rot)]})
logo={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":opa,"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Outro: shutter to check","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[logo]}
emit("outro-check",lot,"outro-check")
