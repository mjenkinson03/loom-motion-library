# The beams-only logo's centre hole is formed by the flat inner ends of 12 rectangles, so its edge is a ridged 12-gon.
# wrap() puts the logo layer inside a precomp and punches a perfect circle through it (inverted-alpha matte), so the hole is round.
# hole = [(seconds, radius), ...]: the radius of the circle over time (linear between keys; use radius 0 where the beams must reach the middle).
import copy
R_HOLE=41.8                 # just outside the beams' inner corners (sqrt(40^2+12^2)), so every inner end is trimmed to the same arc
def wrap(lot,hole,fps=60):
    d=lot; layer=d["layers"][0]; W,H=d["w"],d["h"]
    cx,cy=layer["ks"]["p"]["k"][:2] if not layer["ks"]["p"]["a"] else (None,None)
    if cx is None:                                   # animated position: the centre is wherever the generator's CX,CY put it (first key)
        p=layer["ks"]["p"]; k=p["k"] if "k" in p and isinstance(p["k"],list) else None
        if k: cx,cy=k[0]["s"][0],k[0]["s"][1]
        else: cx,cy=p["x"]["k"][0]["s"][0],p["y"]["k"][0]["s"][0]
    keys=[]
    for i,(t,r) in enumerate(hole):
        k={"t":round(t*fps,2),"s":[round(2*r,3)]*2}
        if i<len(hole)-1: k.update({"o":{"x":[0.5],"y":[0.5]},"i":{"x":[0.5],"y":[0.5]}})
        keys.append(k)
    matte={"ddd":0,"ind":2,"ty":4,"nm":"Hole","td":1,"sr":1,"ks":{"o":{"a":0,"k":100},"r":{"a":0,"k":0},"p":{"a":0,"k":[cx,cy,0]},"a":{"a":0,"k":[0,0,0]},"s":{"a":0,"k":[100,100,100]}},
           "ao":0,"shapes":[{"ty":"gr","it":[{"ty":"el","d":1,"s":{"a":1,"k":keys},"p":{"a":0,"k":[0,0]}},{"ty":"fl","c":{"a":0,"k":[1,1,1,1]},"o":{"a":0,"k":100},"r":1},
             {"ty":"tr","p":{"a":0,"k":[0,0]},"a":{"a":0,"k":[0,0]},"s":{"a":0,"k":[100,100]},"r":{"a":0,"k":0},"o":{"a":0,"k":100},"sk":{"a":0,"k":0},"sa":{"a":0,"k":0}}]}],
           "ip":0,"op":d["op"],"st":0,"bm":0}
    inner=copy.deepcopy(layer); inner["ind"]=1; inner["tt"]=2
    inner["ks"]={"o":{"a":0,"k":100},"r":{"a":0,"k":0},"p":{"a":0,"k":[cx,cy,0]},"a":{"a":0,"k":[0,0,0]},"s":{"a":0,"k":[100,100,100]}}
    outer={"ddd":0,"ind":1,"ty":0,"nm":layer.get("nm","Logo"),"refId":"hole_logo","sr":1,"ks":copy.deepcopy(layer["ks"]),"ao":0,"w":W,"h":H,"ip":0,"op":d["op"],"st":0,"bm":0}
    outer["ks"]["a"]={"a":0,"k":[cx,cy,0]}
    d["assets"]=d.get("assets",[])+[{"id":"hole_logo","layers":[matte,inner]}]
    d["layers"]=[outer]
    return d
