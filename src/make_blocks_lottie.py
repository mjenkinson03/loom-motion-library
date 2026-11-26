# Stitchable building blocks for the recommendation sequences, written to lottie/blocks/. All use the same canvas (261 x 1500, logo centred at
# 130.5, 750) and the same logo, so they can be placed one after another:
#   shutter-cycle.json  1.5s   the 1.0s shutter, then a 0.5s rest on the full white logo. Starts and ends on the full logo: just set it to loop
#   gray.json           3.3s   white -> light gray -> dark gray -> light gray -> white, with markers: gray-in (0-0.8s), gray-pulse (0.8-2.8s, loop this one),
#                              gray-out (2.8-3.3s)
#   check-outro.json    0.95s  a white full logo fades in (0.15s) over whatever is on screen, then it nudges, drops and the check rises and settles.
#                              Layer it over the loader at the moment loading ends and remove the loader: it works from any point.
# Slow load: shutter-cycle x N -> gray (play gray-in, loop gray-pulse, play gray-out) -> check-outro.   Fast load: shutter-cycle x N -> check-outro.
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
def extend(o,secs):
    """Hold the last state for `secs` more seconds (a rest)."""
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                y=copy.deepcopy(v[-1]); y["t"]=round(v[-1]["t"]+secs*fps,3); y.pop("o",None); y.pop("i",None); v.append(y)
            else: extend(v,secs)
    elif isinstance(o,list):
        for x in o: extend(x,secs)
b=copy.deepcopy(cut); window(b,0,1.0); extend(b,0.5); finish(b,"shutter-cycle",1.5)
# still logo for the gray block
still=copy.deepcopy(cut); window(still,0,0.0); freeze(still)
b=copy.deepcopy(still); colour(b,[(0,W),(0.8,L),(1.8,D),(2.8,L),(3.3,W)])
b["markers"]=[{"tm":round(t*fps,3),"cm":n,"dr":round(d*fps,3)} for n,t,d in [("gray-in",0,0.8),("gray-pulse",0.8,2.0),("gray-out",2.8,0.5)]]
finish(b,"gray",3.3)
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
