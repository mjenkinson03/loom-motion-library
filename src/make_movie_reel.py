# Movie reel = the paid Jitter export of the product loader. The motion is untouched. Changes:
#  - The export clips every tile with a 191x191 track matte, which sliced the logo as it slid off to the right / in from the left.
#    The mattes (and precomp clip rectangles) are switched off and the comp is enlarged (261x248 -> 700x400, content re-centred), so the
#    logo can travel in the open.
#  - While it slides OFF to the right (~1.03-1.33s) it fades to 0% instead of being cut off; sliding IN from the left (~1.57-1.87s)
#    it fades in from 0%.
# The original file in Downloads is not touched.
import json
from emit import emit
d=json.load(open("/Users/mjenkinson/Downloads/loader (paid).json"))
OLD_W,OLD_H=d["w"],d["h"]; NEW_W,NEW_H=700,400
dx,dy=(NEW_W-OLD_W)/2,(NEW_H-OLD_H)/2
d["w"],d["h"]=NEW_W,NEW_H
LIN={"i":{"x":[1],"y":[1]},"o":{"x":[0],"y":[0]}}
BIG=6000
def unclip(layers):
    for l in layers:
        if l.get("ty")==0:
            l["w"]=max(l.get("w",0),BIG); l["h"]=max(l.get("h",0),BIG)     # precomp clip rectangle -> effectively none
        if l.get("td"): l["hd"]=True; l.pop("td")                            # hide the matte layer, stop using it
        if l.get("tt"): l.pop("tt")
unclip(d["layers"])
for a in d["assets"]: unclip(a.get("layers",[]))
for l in d["layers"]:
    if l["ind"]==0:                                # root null layer: re-centre everything in the bigger comp
        l["ks"]["p"]={"a":0,"k":[dx,dy,0]}
    if l.get("refId")=="1619":                     # first half (frames 0-90): fade out while it slides right (frames 62-80)
        l["ks"]["o"]={"a":1,"k":[{"t":0,"s":[100],"h":1},{"t":62,"s":[100],**LIN},{"t":80,"s":[0],"h":1},{"t":168,"s":[0]}]}
    if l.get("refId")=="810":                      # second half (frames 90-168): fade in while it slides in from the left (frames 94-112)
        l["ks"]["o"]={"a":1,"k":[{"t":0,"s":[0],"h":1},{"t":94,"s":[0],**LIN},{"t":112,"s":[100],"h":1},{"t":168,"s":[100]}]}
def r(o):
    if isinstance(o,float): return round(o,3)
    if isinstance(o,list): return [r(x) for x in o]
    if isinstance(o,dict): return {k:r(v) for k,v in o.items()}
    return o
emit("movie-reel",r(d),"movie-reel")
