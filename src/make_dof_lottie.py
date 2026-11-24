# Depth of field: the default logo floats a smooth triangle (lower-left, top, lower-right) and returns to centre.
# Off-centre it blurs, dims and shrinks a nudge. Uses Lottie's Gaussian Blur effect (needs the full lottie-web player).
from emit import emit
FPS=60; LOOP=4.3
CW,CH=680,460
CX,CY=CW/2,CH/2
# (time_s, dx, dy, blurriness, opacity, scale%)
KEYS=[(0.0,0,0,0,100,100),(0.5,0,0,0,100,100),(1.15,-50,24,20,42,88),(1.8,0,-44,20,42,88),(2.45,50,24,20,42,88),(3.1,0,0,0,100,100),(LOOP,0,0,0,100,100)]
EASE={"i":{"x":[0.55],"y":[1]},"o":{"x":[0.45],"y":[0]}}
def kf(vals):
    k=[]
    for i,(t,v) in enumerate(vals):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
        if i<len(vals)-1: d.update(EASE)
        k.append(d)
    return {"a":1,"k":k}
def kf_pos():
    P=[(CX+K[1],CY+K[2]) for K in KEYS]; n=len(P); ks=[]
    chain=list(range(1,n-1)); m={}
    for j,i in enumerate(chain):
        prev=P[chain[(j-1)%len(chain)]]; nxt=P[chain[(j+1)%len(chain)]]
        m[i]=((nxt[0]-prev[0])/2,(nxt[1]-prev[1])/2)
    for i,K in enumerate(KEYS):
        d={"t":round(K[0]*FPS,2),"s":[round(P[i][0],3),round(P[i][1],3),0]}
        if i<n-1:
            d.update(EASE)
            if P[i]==P[i+1]:                      # a hold: no curved path (this caused an end-of-loop wiggle once)
                d["to"]=[0,0,0]; d["ti"]=[0,0,0]
            else:
                mo=m.get(i,(0,0)); mi=m.get(i+1,(0,0))
                d["to"]=[round(mo[0]/3,3),round(mo[1]/3,3),0]; d["ti"]=[round(-mi[0]/3,3),round(-mi[1]/3,3),0]
        ks.append(d)
    return {"a":1,"k":ks}
pos=kf_pos()
op=kf([(K[0],[K[4]]) for K in KEYS]); scl=kf([(K[0],[K[5],K[5],100]) for K in KEYS]); blur=kf([(K[0],[K[3]]) for K in KEYS])
tr=lambda r=0:{"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":r},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}
W={"a":0,"k":[1,1,1,1]}
shapes=[{"ty":"gr","nm":f"Spoke {i+1}","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[24,60]},"p":{"a":0,"k":[0,-70]},"r":{"a":0,"k":0}},{"ty":"fl","c":W,"o":{"a":0,"k":100},"r":1},tr(i*30)]} for i in range(12)]
shapes.append({"ty":"gr","nm":"Ring","it":[{"ty":"el","d":1,"s":{"a":0,"k":[78,78]},"p":{"a":0,"k":[0,0]}},{"ty":"st","c":W,"o":{"a":0,"k":100},"w":{"a":0,"k":10},"lc":1,"lj":1},tr()]})
fx=[{"ty":29,"nm":"Gaussian Blur","np":5,"mn":"ADBE Gaussian Blur 2","ix":1,"en":1,"ef":[
  {"ty":0,"nm":"Blurriness","mn":"ADBE Gaussian Blur 2-0001","ix":1,"v":blur},
  {"ty":7,"nm":"Blur Dimensions","mn":"ADBE Gaussian Blur 2-0002","ix":2,"v":{"a":0,"k":1}},
  {"ty":7,"nm":"Repeat Edge Pixels","mn":"ADBE Gaussian Blur 2-0003","ix":3,"v":{"a":0,"k":0}}]}]
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":CW,"h":CH,"nm":"Depth of field","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
 "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Logo","sr":1,"ks":{"o":op,"r":{"a":0,"k":0},"p":pos,"a":{"a":0,"k":[0,0,0]},"s":scl},"ao":0,"ef":fx,"shapes":shapes,"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}]}
emit("dof",lot,"depth-of-field")
