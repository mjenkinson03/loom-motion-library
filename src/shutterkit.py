# The simple-structure shutter used by the stitchable block AND by the Recommendation cards' loading phase.
# 12 beams share one set of size/position keys and each has a fixed rotation (the same structure as the Shutter card), which lottie-web loops and
# renders reliably. A cycle is the 1.0s shutter followed by an optional rest on the full logo; during a rest a ripple (each beam dips a touch,
# clockwise from the top) can run. fill_keys (optional) animates the beams' colour over the whole timeline (used for the gray dips on the 15s card).
from holefix import wrap,R_HOLE
FPS=60
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),"io":((0.45,0),(0.55,1))}
RIP_DIP,RIP_STAG,RIP_DOWN,RIP_UP=75,0.02,0.07,0.12
SH=[(0,100,100,"gentle"),(0.182,104,103,"snapin"),(0.345,40,96,"hold"),(0.418,40,96,"snapout"),(0.727,108,102,"settle"),(1.0,100,100,"hold")]   # (t, outer radius, scale, easing)
S=lambda v:{"a":0,"k":v}
def kf(vals,fps=FPS):
    k=[]
    for i,(t,v,e) in enumerate(vals):
        d={"t":round(t*fps,3),"s":[round(x,3) for x in v]}
        if i<len(vals)-1:
            (ox,oy),(ix,iy)=BEZ[e]; d.update({"o":{"x":[ox],"y":[oy]},"i":{"x":[ix],"y":[iy]}})
        k.append(d)
    return {"a":1,"k":k}
def build(pauses,total=None,ripple=True,fill_keys=None,aid="hole_logo",w=261,h=1500,cx=130.5,cy=750,name="shutter"):
    """pauses = rest after each cycle in seconds (0 = none). Returns a lot (with the round hole punched). total = length in seconds (hold the full logo to it)."""
    keys=[]; rests=[]; t0=0.0
    for p in pauses:
        for t,r,s,e in SH: keys.append((t0+t,r,s,e))
        if p>0: rests.append(t0+1.0); keys.append((t0+1.0+p,100,100,"hold"))
        t0+=1.0+p
    end=total if total else t0
    if end>t0+1e-6: keys.append((end,100,100,"hold"))
    dd=[]                                                   # drop keys that land on the same time as the next cycle's first key
    for k in keys:
        if dd and abs(dd[-1][0]-k[0])<1e-6: dd[-1]=k
        else: dd.append(k)
    keys=dd
    size=kf([(t,[24,r-40],e) for t,r,s,e in keys]); pos=kf([(t,[0,-(40+r)/2],e) for t,r,s,e in keys]); scl=kf([(t,[s,s,100],e) for t,r,s,e in keys])
    legs=[]
    for i in range(12):
        if ripple and rests:
            ok=[(0,[100])]
            for r0 in rests:
                s0=r0+i*RIP_STAG; ok+=[(s0,[100]),(s0+RIP_DOWN,[RIP_DIP]),(s0+RIP_DOWN+RIP_UP,[100])]
            ok.append((end,[100])); o=kf([(t,v,"io") for t,v in ok])
        else: o=S(100)
        tr={"ty":"tr","p":S([0,0]),"a":S([0,0]),"s":S([100,100]),"r":S(i*30),"o":o,"sk":S(0),"sa":S(0)}
        fillc=S([1,1,1,1])
        if fill_keys:
            fillc={"a":1,"k":[dict(k) for k in fill_keys]}
        legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":pos,"r":S(0)},{"ty":"fl","c":fillc,"o":S(100),"r":1},tr]})
    op=round(end*FPS)
    layer={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":S(100),"r":S(0),"p":S([cx,cy,0]),"a":S([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":op,"st":0,"bm":0}
    lot={"v":"5.7.4","fr":FPS,"ip":0,"op":op,"w":w,"h":h,"nm":name,"ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[layer]}
    return wrap(lot,[(0,R_HOLE),(end,R_HOLE)],aid=aid)
