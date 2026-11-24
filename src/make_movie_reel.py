# Movie reel = the paid Jitter export of the product loader, plus a soft loop: it fades out over the last ~0.25s and fades in from 0%
# at the start, so the loop point is no longer a hard chop. The original file in Downloads is not touched.
# (Known: around 1.2-1.5s the original export has moments where the logo is half cut off or blank, in lottie-web too.)
import json
from emit import emit
d=json.load(open("/Users/mjenkinson/Downloads/loader (paid).json"))
FADE=14
LIN={"i":{"x":[1],"y":[1]},"o":{"x":[0],"y":[0]}}
for l in d["layers"]:
    if l.get("refId")=="1619":
        l["ks"]["o"]={"a":1,"k":[{"t":0,"s":[0],**LIN},{"t":FADE,"s":[100],"h":1},{"t":90,"s":[0],"h":1},{"t":168,"s":[0]}]}
    if l.get("refId")=="810":
        l["ks"]["o"]={"a":1,"k":[{"t":0,"s":[0],"h":1},{"t":90,"s":[100],"h":1},{"t":168-FADE,"s":[100],**LIN},{"t":168,"s":[0]}]}
def r(o):
    if isinstance(o,float): return round(o,3)
    if isinstance(o,list): return [r(x) for x in o]
    if isinstance(o,dict): return {k:r(v) for k,v in o.items()}
    return o
emit("movie-reel",r(d),"movie-reel")
