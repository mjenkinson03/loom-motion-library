# Stitchable building blocks for the recommendation sequences, written to lottie/blocks/. All use the same canvas (261 x 1500, logo centred at
# 130.5, 750) and the same logo, so they can be placed one after another:
#   shutter-cycle.json  1.5s   the 1.0s shutter, then a 0.5s rest on the full white logo with a little ripple (each beam dips a touch, clockwise from the top). Starts and ends on the full logo: just set it to loop
#   gray.json           2.0s   one gray cycle: white -> dark gray -> white (1.0s down, 1.0s up). Starts and ends on the full white logo: just set it to loop.
#   check-outro.json    0.95s  a white full logo fades in (0.15s) over whatever is on screen, then it nudges, drops and the check rises and settles.
#                              Layer it over the loader at the moment loading ends and remove the loader: it works from any point.
# Slow load: shutter-cycle x N -> gray (looping) -> check-outro.   Fast load: shutter-cycle x N -> check-outro.
import copy,json,os
import make_rec_lottie as R               # builds the recommendation files and gives us the master timeline: R.cut = shutter 0-1.0s, outro 1.0-2.0s, reset 2.0-3.05s
cut=R.cut; fps=cut["fr"]
def window(o,t0,t1):
    """Keep only the keyframes between t0 and t1 (seconds), shifted to start at 0. Where a property has no key exactly at t0 the value in force there is copied in."""
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                a,b=t0*fps,t1*fps; before=[x for x in v if x["t"]<a-1e-6]; inside=[x for x in v if a-1e-6<=x["t"]<=b+1e-6]
                if (not inside or inside[0]["t"]>a+1e-6) and before:
                    y=copy.deepcopy(before[-1]); y["t"]=a; inside.insert(0,y)
                if not inside: inside=[copy.deepcopy(v[-1])]; inside[0]["t"]=a
                if inside[-1]["t"]<b-1e-6:
                    y=copy.deepcopy(inside[-1]); y["t"]=b; y.pop("o",None); y.pop("i",None); inside.append(y)
                for x in inside: x["t"]=round(x["t"]-a,3)
                inside[-1].pop("o",None); inside[-1].pop("i",None)
                o[k]=inside
            elif k in ("op",) and isinstance(v,(int,float)): o[k]=round((t1-t0)*fps,3)
            else: window(v,t0,t1)
    elif isinstance(o,list):
        for x in o: window(x,t0,t1)
def freeze(o):
    """Turn every animated property into its first value (a still logo)."""
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                s=v[0]["s"]; o[k]=s[0] if len(s)==1 else s; o["a"]=0
            else: freeze(v)
    elif isinstance(o,list):
        for x in o: freeze(x)
def colour(lot,keys):
    def go(o):
        if isinstance(o,dict):
            if o.get("td"): return
            if o.get("ty")=="fl":
                ks=[]
                for i,(t,c) in enumerate(keys):
                    d={"t":round(t*fps,3),"s":c}
                    if i<len(keys)-1: d.update({"o":{"x":[0.45],"y":[0]},"i":{"x":[0.55],"y":[1]}})
                    ks.append(d)
                o["c"]={"a":1,"k":ks}
            for v in o.values(): go(v)
        elif isinstance(o,list):
            for x in o: go(x)
    go(lot)
W,L,D=R.WHITE,R.LIGHT,R.DARK
from emit import emit
def finish(lot,name,secs):
    lot["op"]=round(secs*fps,3); lot["nm"]=name
    for l in lot["layers"]: l["op"]=lot["op"]
    for a in lot.get("assets",[]):
        for l in a.get("layers",[]): l["op"]=lot["op"]
    os.makedirs("../lottie/blocks",exist_ok=True)
    emit(f"blk-{name}",lot,f"blocks/{name}")        # also writes the small copy the page's previews play
# shutter: the first second of the master (starts and ends on the full logo)
# shutter cycle: built the way the Shutter card is (12 beams sharing one set of size/position keys, a fixed rotation each), not cut from the master.
# The master turns every beam separately (so they can become a check); lottie-web mis-renders that structure when it loops and ignores the rest ripple.
from holefix import wrap,R_HOLE
BEZ={"hold":((0.33,0),(0.67,1)),"gentle":((0.33,0),(0.67,1)),"snapin":((0.75,0),(1,1)),"snapout":((0.1,0.9),(0.3,1)),"settle":((0.4,0),(0.6,1)),"io":((0.45,0),(0.55,1))}
def kf(vals):
    k=[]
    for i,(t,v,e) in enumerate(vals):
        d={"t":round(t*fps,3),"s":[round(x,3) for x in v]}
        if i<len(vals)-1:
            (ox,oy),(ix,iy)=BEZ[e]; d.update({"o":{"x":[ox],"y":[oy]},"i":{"x":[ix],"y":[iy]}})
        k.append(d)
    return {"a":1,"k":k}
Sx=lambda v:{"a":0,"k":v}
def shutter_cycle():
    CXs,CYs=130.5,750
    # (time, leg outer radius, logo scale, easing): the master's 1.1s shutter squeezed into 1.0s, then a 0.5s rest on the full logo
    KEYS=[(0,100,100,"gentle"),(0.182,104,103,"snapin"),(0.345,40,96,"hold"),(0.418,40,96,"snapout"),(0.727,108,102,"settle"),(1.0,100,100,"hold"),(1.5,100,100,"hold")]
    size=kf([(t,[24,r-40],e) for t,r,s,e in KEYS]); pos=kf([(t,[0,-(40+r)/2],e) for t,r,s,e in KEYS]); scl=kf([(t,[s,s,100],e) for t,r,s,e in KEYS])
    W3=Sx([1,1,1,1]); legs=[]
    for i in range(12):
        s0=1.0+i*R.RIP_STAG                                                    # the rest ripple: each beam dips a touch, one after another, clockwise from the top
        o=kf([(0,[100],"io"),(s0,[100],"io"),(s0+R.RIP_DOWN,[R.RIP_DIP],"io"),(s0+R.RIP_DOWN+R.RIP_UP,[100],"io"),(1.5,[100],"io")])
        tr={"ty":"tr","p":Sx([0,0]),"a":Sx([0,0]),"s":Sx([100,100]),"r":Sx(i*30),"o":o,"sk":Sx(0),"sa":Sx(0)}
        legs.append({"ty":"gr","nm":f"Beam {i+1}","it":[{"ty":"rc","d":1,"s":size,"p":pos,"r":Sx(0)},{"ty":"fl","c":W3,"o":Sx(100),"r":1},tr]})
    layer={"ddd":0,"ind":1,"ty":4,"nm":"Beams","sr":1,"ks":{"o":Sx(100),"r":Sx(0),"p":Sx([CXs,CYs,0]),"a":Sx([0,0,0]),"s":scl},"ao":0,"shapes":legs,"ip":0,"op":round(1.5*fps),"st":0,"bm":0}
    lot={"v":"5.7.4","fr":fps,"ip":0,"op":round(1.5*fps),"w":261,"h":1500,"nm":"shutter-cycle","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},"layers":[layer]}
    return wrap(lot,[(0,R_HOLE),(1.5,R_HOLE)])
finish(shutter_cycle(),"shutter-cycle",1.5)
# still logo for the gray block
still=copy.deepcopy(cut); window(still,0,0.0); freeze(still)
b=copy.deepcopy(still); colour(b,[(0,W),(1.0,D),(2.0,W)])
finish(b,"gray",2.0)
# check outro with a 0.15s lead-in: a white full logo fades in over whatever is under it (the loader can be stopped at any moment), then the outro plays
LEAD=0.15
def lead_in(o,secs):
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                for x in v: x["t"]=round(x["t"]+secs*fps,3)
                first=copy.deepcopy(v[0]); first["t"]=0; first.pop("h",None)
                v.insert(0,first)
            elif k=="op" and isinstance(v,(int,float)): o[k]=round(v+secs*fps,3)
            else: lead_in(v,secs)
    elif isinstance(o,list):
        for x in o: lead_in(x,secs)
b=copy.deepcopy(cut); window(b,1.0,1.8); lead_in(b,LEAD)
ok=b["layers"][0]["ks"]["o"]["k"]; ok[0]["s"]=[0]; ok[0].update({"o":{"x":[0.2],"y":[0.6]},"i":{"x":[0.4],"y":[1]}})
finish(b,"check-outro",round(0.8+LEAD,2))
