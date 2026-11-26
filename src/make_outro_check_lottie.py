# Outro 1 (Shutter + check): the shutter's last beat. As the loading bar completes, the legs wind up and blink in ALL the way (legs and ring
# collapse to nothing), a check mark - drawn with the same 24-unit stroke as the logo's beams - bounces in from the centre, holds, then
# dissolves; the logo then springs back open for the next loop.
from emit import emit
FPS=60; LOOP=5.9
CX,CY=130.5,124
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),"bounce":((0.2,0.8),(0.3,1)),"io":((0.45,0),(0.55,1))}
def kf(vals):
    k=[]
    for i,(t,v,e) in enumerate(vals):
        d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
        if i<len(vals)-1:
            (ox,oy),(ix,iy)=BEZ[e]; d.update({"o":{"x":[ox],"y":[oy]},"i":{"x":[ix],"y":[iy]}})
        k.append(d)
    return {"a":1,"k":k}
S=lambda v:{"a":0,"k":v}
# (time, leg outer radius, logo scale, easing to next). r=40 means the legs have zero length.
T_WIND,T_SNAP,T_OPEN,T_SET=2.2,2.42,4.7,5.15
KEYS=[(0,100,100,"hold"),(2.0,100,100,"gentle"),(T_WIND,104,103,"snapin"),(T_SNAP,40,96,"hold"),(T_OPEN,40,96,"snapout"),(T_SET,108,102,"settle"),(5.45,100,100,"hold"),(LOOP,100,100,"hold")]
size=kf([(t,[24,r-40],e) for t,r,s,e in KEYS]); pos=kf([(t,[0,-(40+r)/2],e) for t,r,s,e in KEYS]); scl=kf([(t,[s,s,100],e) for t,r,s,e in KEYS])
ring_s=kf([(0,[100,100],"hold"),(T_WIND,[100,100],"snapin"),(T_SNAP,[0,0],"hold"),(T_OPEN,[0,0],"snapout"),(T_SET,[104,104],"settle"),(5.45,[100,100],"hold"),(LOOP,[100,100],"hold")])
tr=lambda rot=0,s=None:{"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":s or S([100,100]),"r":S(rot),"o":S(100),"sk":S(0),"sa":S(0)}
W=S([1,1,1,1])
legs=[{"ty":"gr","nm":f"Leg {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":pos,"r":S(0)},{"ty":"fl","c":W,"o":S(100),"r":1},tr(i*30)]} for i in range(12)]
ring={"ty":"gr","nm":"Ring","it":[{"ty":"el","d":1,"s":S([78,78]),"p":S([0,0])},{"ty":"st","c":W,"o":S(100),"w":S(10),"lc":1,"lj":1},tr(0,ring_s)]}
logo={"ddd":0,"ind":2,"ty":4,"nm":"Logo","sr":1,"ks":{"o":S(100),"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs+[ring],"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
# check mark: same stroke width as a beam (24), flat ends like the beams
T_IN=T_SNAP; T_OUT=3.9
chk_s=kf([(0,[0,0,100],"hold"),(T_IN,[0,0,100],"bounce"),(T_IN+0.33,[118,118,100],"io"),(T_IN+0.53,[94,94,100],"io"),(T_IN+0.70,[102,102,100],"io"),(T_IN+0.83,[100,100,100],"hold"),(T_OUT,[100,100,100],"io"),(T_OUT+0.5,[108,108,100],"hold"),(LOOP,[0,0,100],"hold")])
chk_o=kf([(0,[0],"hold"),(T_IN,[100],"hold"),(T_OUT,[100],"io"),(T_OUT+0.5,[0],"hold"),(LOOP,[0],"hold")])
check_path={"ty":"sh","ks":S({"i":[[0,0]]*3,"o":[[0,0]]*3,"v":[[-52,2],[-16,38],[54,-38]],"c":False})}
check={"ddd":0,"ind":1,"ty":4,"nm":"Check","sr":1,"ks":{"o":chk_o,"r":S(0),"p":S([CX,CY,0]),"a":S([0,0,0]),"s":chk_s},"ao":0,
 "shapes":[{"ty":"gr","nm":"Check","it":[check_path,{"ty":"st","c":W,"o":S(100),"w":S(24),"lc":1,"lj":1,"ml":4},tr()]}],"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":261,"h":248,"nm":"Outro: shutter + check","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[check,logo]}
emit("outro-check",lot,"outro-check")
