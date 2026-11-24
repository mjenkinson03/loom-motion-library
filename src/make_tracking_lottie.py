# Tracking: like a hand-held camera — the logo moves (quickly) down-left, stops; up, stops; down-right, stops; back to centre.
# The ring never changes size; the legs tuck in while it travels and grow out (tiny overshoot) once it is back at centre. 2.5s pause at centre.
from emit import emit
FPS=60
CW,CH=680,460; CX,CY=CW/2,CH/2
EASE={"i":{"x":[0.15],"y":[1]},"o":{"x":[0.3],"y":[0]}}
HOLD=2.5; MOVE=0.32; PAUSE=0.45
WP={"C":(0,0),"L":(-50,24),"U":(0,-44),"R":(50,24)}
seq=[("C",0.0,100),("C",HOLD,100),("L",HOLD+MOVE,86),("L",HOLD+MOVE+PAUSE,86),("U",HOLD+2*MOVE+PAUSE,86),("U",HOLD+2*MOVE+2*PAUSE,86),
     ("R",HOLD+3*MOVE+2*PAUSE,86),("R",HOLD+3*MOVE+3*PAUSE,86),("C",HOLD+4*MOVE+3*PAUSE,86)]
GROW=HOLD+4*MOVE+3*PAUSE
seq+=[("C",GROW+0.45,105),("C",GROW+0.8,100)]
KEYS=[(t,WP[w][0],WP[w][1],r,w) for w,t,r in seq]
LOOP=round(KEYS[-1][0],2)
def kf(vals,tang=None):
    k=[]
    for i,(t,v) in enumerate(vals):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
        if i<len(vals)-1:
            d.update(EASE)
            if tang: d["to"],d["ti"]=tang[i]
        k.append(d)
    return {"a":1,"k":k}
order=["C","L","U","R"]; m={}
for j,w in enumerate(order):
    pv=WP[order[(j-1)%4]]; nx=WP[order[(j+1)%4]]; m[w]=((nx[0]-pv[0])/2,(nx[1]-pv[1])/2)
P=[(CX+K[1],CY+K[2]) for K in KEYS]; tang=[]; Z=[0,0,0]
for i in range(len(KEYS)-1):
    a_,b_=KEYS[i],KEYS[i+1]
    if (a_[1],a_[2])==(b_[1],b_[2]) or (a_[4]=="C" and b_[4]=="C"): tang.append((Z,Z)); continue
    mo=m[a_[4]]; mi=m[b_[4]]
    tang.append(([round(mo[0]/3,3),round(mo[1]/3,3),0],[round(-mi[0]/3,3),round(-mi[1]/3,3),0]))
pos=kf([(K[0],[P[i][0],P[i][1],0]) for i,K in enumerate(KEYS)],tang)
size=kf([(K[0],[24,K[3]-40]) for K in KEYS]); lpos=kf([(K[0],[0,-(40+K[3])/2]) for K in KEYS])
tr=lambda rot=0:{"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":rot},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}
W_={"a":0,"k":[1,1,1,1]}
shapes=[{"ty":"gr","nm":f"Leg {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":lpos,"r":{"a":0,"k":0}},{"ty":"fl","c":W_,"o":{"a":0,"k":100},"r":1},tr(i*30)]} for i in range(12)]
shapes.append({"ty":"gr","nm":"Ring","it":[{"ty":"el","d":1,"s":{"a":0,"k":[78,78]},"p":{"a":0,"k":[0,0]}},{"ty":"st","c":W_,"o":{"a":0,"k":100},"w":{"a":0,"k":10},"lc":1,"lj":1},tr()]})
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":CW,"h":CH,"nm":"Tracking","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Logo","sr":1,"ks":{"o":{"a":0,"k":100},"r":{"a":0,"k":0},"p":pos,"a":{"a":0,"k":[0,0,0]},"s":{"a":0,"k":[100,100,100]}},"ao":0,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}]}
emit("tracking",lot,"tracking")
