# Arrival: dust drifts in from the left and forms the Loom logo (entrance = the exit mirrored and played backwards), a sharp vector logo takes over
# once whole, it sways left/right with pauses, then it breaks apart left-to-right and drifts away. The dust is ~700 small squares kept inside the
# logo's edges, so the whole thing stays a real, light Lottie file. usage: python3 make_arrival_lottie.py [particle_count]
import json,math,random,sys
from emit import emit
N=int(sys.argv[1]) if len(sys.argv)>1 else 800
FPS=60; FORM,HOLD,DISSOLVE,REST=2.1,3.0,2.1,0.3; LOOP=FORM+HOLD+DISSOLVE+REST
T1,T2=FORM,FORM+HOLD
CW,CH=1040,650
CX,CY=CW/2,CH*0.42; SC=1.2308
rnd=random.Random(7).random
cl=lambda x:min(1,max(0,x)); ss=lambda a,b,x:(lambda v:v*v*(3-2*v))(cl((x-a)/(b-a)))
ei=lambda x:cl(x)**2.2
WIND=math.atan2(-0.28,1)
def inside(x,y):
    r=math.hypot(x,y)
    if 34<=r<=44: return True
    a=math.atan2(y,x)+math.pi/2
    for i in range(12):
        t=a-i*math.pi/6; t=(t+math.pi)%(2*math.pi)-math.pi
        u=r*math.sin(t); v=r*math.cos(t)
        if abs(u)<=12 and 40<=v<=100: return True
    return False
cell=math.sqrt(19700/N); SZ=cell*0.72; hh=SZ/2; pts=[]
def inside_sq(x,y): return all(inside(x+dx,y+dy) for dx,dy in ((0,0),(hh,hh),(-hh,hh),(hh,-hh),(-hh,-hh)))
gx=-104
while gx<104:
    gy=-104
    while gy<104:
        for _ in range(6):
            x=gx+rnd()*cell; y=gy+rnd()*cell
            if inside_sq(x,y): pts.append((x,y)); break
        gy+=cell
    gx+=cell
P=[]
for (tx,ty) in pts:
    z=0.35+rnd()*0.65; frac=(tx+104)/208
    P.append(dict(tx=tx,ty=ty,z=z,dG=0.55*frac*0.75+0.3*rnd(),dD=0.55*(1-frac)*0.75+0.3*rnd(),ang=WIND+(rnd()-.5)*1.3,dr=80+rnd()*420,cu=(rnd()-.5)*70))
def state(p,t):
    if t<T2:
        qi=cl((t-p['dG'])/1.35); q=1-qi; an=math.pi-p['ang']; a=qi**1.5
    else:
        q=cl((t-T2-p['dD'])/1.35); qi=1-q; an=p['ang']; a=(1-q)**1.5
    e=ei(q); s=math.sin(q*3.1)
    dx=math.cos(an)*p['dr']*e*p['z']-math.sin(an)*p['cu']*s*e
    dy=math.sin(an)*p['dr']*e*p['z']+math.cos(an)*p['cu']*s*e
    return (CX+p['tx']+dx/SC, CY+p['ty']+dy/SC), a*(0.55+0.45*p['z'])*100
DT=0.15
tpos=sorted(set([round(i*DT,3) for i in range(int(FORM/DT)+1)]+[FORM,T2]+[round(T2+i*DT,3) for i in range(int(DISSOLVE/DT)+2) if T2+i*DT<=T2+DISSOLVE+0.001]+[T2+DISSOLVE,LOOP]))
LIN={"i":{"x":[1],"y":[1]},"o":{"x":[0],"y":[0]}}
def kf(times,vals,scalar=False):
    k=[]
    for i,(t,v) in enumerate(zip(times,vals)):
        d={"t":round(t*FPS,2),"s":[round(x,2) for x in (v if not scalar else [v])]}
        if i<len(times)-1: d.update(LIN)
        k.append(d)
    return {"a":1,"k":k}
def prune(times,vals):
    keep=[0]
    for i in range(1,len(times)-1):
        if vals[i]!=vals[i-1] or vals[i]!=vals[i+1]: keep.append(i)
    keep.append(len(times)-1)
    return [times[i] for i in keep],[vals[i] for i in keep]
topc=sorted(set([round(i*0.15,2) for i in range(int(LOOP/0.15)+1)]+[LOOP]))
mask=lambda t:ss(T1-0.05,T1+0.3,t)*(1-ss(T2-0.15,T2,t))        # dust hidden while the sharp logo is up
groups=[]
for p in P:
    pos=[tuple(round(c,1) for c in state(p,t)[0]) for t in tpos]
    tp,vp=prune(tpos,pos)
    op=[round(state(p,t)[1]*(1-mask(t))) for t in topc]
    to,vo=prune(topc,op)
    groups.append({"ty":"gr","it":[
        {"ty":"rc","d":1,"s":{"a":0,"k":[SZ,SZ]},"p":{"a":0,"k":[0,0]},"r":{"a":0,"k":0}},
        {"ty":"fl","c":{"a":0,"k":[1,1,1,1]},"o":{"a":0,"k":100},"r":1},
        {"ty":"tr","p":kf(tp,vp),"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":0},"o":kf(to,vo,True),"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}]})
def layer(name,shapes,ind,op_keys=None):
    return {"ddd":0,"ind":ind,"ty":4,"nm":name,"sr":1,"ks":{"o":op_keys or {"a":0,"k":100},"r":{"a":0,"k":0},"p":{"a":0,"k":[CX,CY,0]},"a":{"a":0,"k":[0,0,0]},"s":{"a":0,"k":[100,100,100]}},"ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
ST=sorted(set([0,T1-0.55,T1-0.05,T2,T2+0.35,LOOP])); SV=[100*ss(T1-0.55,T1-0.05,t)*(1-ss(T2,T2+0.35,t)) for t in ST]
solid=[]
for i in range(12):
    solid.append({"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[24,60]},"p":{"a":0,"k":[0,-70]},"r":{"a":0,"k":0}},
        {"ty":"fl","c":{"a":0,"k":[1,1,1,1]},"o":{"a":0,"k":100},"r":1},
        {"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":i*30},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}]})
solid.append({"ty":"gr","it":[{"ty":"el","d":1,"s":{"a":0,"k":[78,78]},"p":{"a":0,"k":[0,0]}},
    {"ty":"st","c":{"a":0,"k":[1,1,1,1]},"o":{"a":0,"k":100},"w":{"a":0,"k":10},"lc":1,"lj":1},
    {"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":0},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}]})
glow=[{"ty":"gr","it":[{"ty":"el","d":1,"s":{"a":0,"k":[230,230]},"p":{"a":0,"k":[0,0]}},
    {"ty":"gf","o":{"a":0,"k":100},"r":1,"t":2,"s":{"a":0,"k":[0,0]},"e":{"a":0,"k":[115,0]},"g":{"p":2,"k":{"a":0,"k":[0,1,1,1, 1,1,1,1, 0,0.35, 1,0]}}},
    {"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":0},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}]}]
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":CW,"h":CH,"nm":"Arrival","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[layer("Solid logo",solid,1,kf(ST,SV,True)), {**layer("Dust",groups,2),"ks":{"o":{"a":0,"k":100},"r":{"a":0,"k":0},"p":{"a":0,"k":[0,0,0]},"a":{"a":0,"k":[0,0,0]},"s":{"a":0,"k":[100,100,100]}}}, layer("Glow",glow,3,kf(ST,[v*0.10 for v in SV],True))]}
# once whole, the logo (and its glow) sways: left · pause · right · pause · back to middle · pause
DRIFT=18
def drift_keys():
    pts=[(T1,0),(T1+0.55,-DRIFT),(T1+0.90,-DRIFT),(T1+1.65,DRIFT),(T1+2.00,DRIFT),(T1+2.50,0),(T2,0)]
    ks=[]
    for i,(tt,dx) in enumerate(pts):
        k={"t":round(tt*FPS,2),"s":[CX+dx,CY,0]}
        if i<len(pts)-1: k.update({"i":{"x":[0.55],"y":[1]},"o":{"x":[0.45],"y":[0]}})
        ks.append(k)
    return {"a":1,"k":ks}
for L in (lot["layers"][0],lot["layers"][2]): L["ks"]["p"]=drift_keys()
print("particles",len(P))
emit("arrival",lot,"arrival")
