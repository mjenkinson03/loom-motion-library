# Movie reel = the paid Jitter export of the product loader. The motion is untouched. Changes:
#  - The export clips every tile with a 191x191 track matte, which sliced the logo as it slid off to the right / in from the left.
#    The slide-out and slide-in now play with those mattes (and precomp clips) switched off, in an enlarged comp (261x248 -> 700x400,
#    content re-centred), so the logo travels in the open.
#  - The pulse (0-1.03s) keeps the ORIGINAL mattes: with them off, its translucent pieces overlap into a jagged, spiky ring.
#    So the first half exists twice: the original (frames 0-62, up to the moment the logo starts to slide) and an unclipped clone
#    (frame 62 on). At frame 62 the logo is sitting still and centred, so the hand-off is invisible.
#  - The pulse itself is smoothed: the original thins the spokes to hairline spikes and the centre circle changes. In its place the logo
#    holds its resting frame (Lottie time-remap, so the circle never changes) and just dims and brightens (frames 30-60).
#  - The slide-out fades to 0% quickly (frames 62-70) so you never see it slow down or stop; the slide-in fades in from 0%.
# The original export file is not modified.
import json,copy,os
from emit import emit
# the paid Jitter export of the product loader (set LOADER_JSON to point somewhere else)
d=json.load(open(os.environ.get("LOADER_JSON",os.path.expanduser("~/Downloads/loader (paid).json"))))
OLD_W,OLD_H=d["w"],d["h"]; NEW_W,NEW_H=700,400
dx,dy=(NEW_W-OLD_W)/2,(NEW_H-OLD_H)/2
d["w"],d["h"]=NEW_W,NEW_H
LIN={"i":{"x":[1],"y":[1]},"o":{"x":[0],"y":[0]}}
BIG=6000
A={a["id"]:a for a in d["assets"]}
def reach(root):
    seen=set(); stack=[root]
    while stack:
        i=stack.pop()
        if i in seen: continue
        seen.add(i)
        for l in A[i]["layers"]:
            if l["ty"]==0: stack.append(l["refId"])
    return seen
def unclip(layers):
    for l in layers:
        if l.get("ty")==0:
            l["w"]=max(l.get("w",0),BIG); l["h"]=max(l.get("h",0),BIG)      # precomp clip rectangle -> effectively none
        if l.get("td"): l["hd"]=True; l.pop("td")                             # hide the matte layer, stop using it
        if l.get("tt"): l.pop("tt")
first,second=reach("1619"),reach("810")
assert not (first&second)
# 1) second half (slide-in, settle, grow): unclipped
for i in second: unclip(A[i]["layers"])
# 2) first half: clone every asset (suffix x), unclip the clones, keep the originals (with mattes) for the pulse
clones=[]
for i in sorted(first):
    c=copy.deepcopy(A[i]); c["id"]=i+"x"
    for l in c["layers"]:
        if l["ty"]==0: l["refId"]=l["refId"]+"x"
    unclip(c["layers"]); clones.append(c)
d["assets"]+=clones
root={l["ind"]:l for l in d["layers"]}
orig_first=root[1621]; clone_first=copy.deepcopy(orig_first); clone_first["ind"]=1622; clone_first["refId"]="1619x"
clone_first["w"]=clone_first["h"]=BIG
d["layers"].insert(0,clone_first)
unclip(d["layers"])
for l in d["layers"]:
    if l["ind"]==0: l["ks"]["p"]={"a":0,"k":[dx,dy,0]}                      # re-centre everything in the bigger comp
import math
orig_first["ks"]["o"]={"a":1,"k":[{"t":0,"s":[100],"h":1},{"t":30,"s":[0],"h":1},{"t":168,"s":[0]}]}               # original, live: frames 0-30 (the settle)
pulse=copy.deepcopy(orig_first); pulse["ind"]=1623; pulse["tm"]={"a":0,"k":0.5}                                          # frozen at its resting frame (0.5s)
keys=[{"t":0,"s":[0],"h":1}]
for f in range(30,61,2):
    v=100-80*(0.5-0.5*math.cos(2*math.pi*(f-30)/30))                                                                    # smooth dip to 20% and back
    keys.append({"t":f,"s":[round(v,2)],**LIN})
keys[-1]={"t":60,"s":[100],"h":1}
keys+=[{"t":62,"s":[0],"h":1},{"t":168,"s":[0]}]
pulse["ks"]["o"]={"a":1,"k":keys}
d["layers"].insert(1,pulse)
clone_first["ks"]["o"]={"a":1,"k":[{"t":0,"s":[0],"h":1},{"t":62,"s":[100],**LIN},{"t":70,"s":[0],"h":1},{"t":168,"s":[0]}]}  # clone: slides out, fading fast
root[812]["ks"]["o"]={"a":1,"k":[{"t":0,"s":[0],"h":1},{"t":94,"s":[0],**LIN},{"t":112,"s":[100],"h":1},{"t":168,"s":[100]}]}  # slide-in fades in
def r(o):
    if isinstance(o,float): return round(o,3)
    if isinstance(o,list): return [r(x) for x in o]
    if isinstance(o,dict): return {k:r(v) for k,v in o.items()}
    return o
emit("movie-reel",r(d),"movie-reel")
