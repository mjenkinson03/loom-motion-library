# Icon carousel (Atlassian): one rounded dark tile at a time (Loom logo, film frame, cursor click, camera). Each tile zooms in, holds,
# then it zooms out as the next one zooms in. Built only from shapes: no images, no effects.
# Icon geometry is measured from the Figma design (tile 52px; Loom glyph 32px; film/cursor 27x28; camera 31x27), authored in those
# 52px units and scaled up by K.
import math
from emit import emit
FPS=60
MOVE,HOLD=0.65,1.5; STEP=MOVE+HOLD; N=4; LOOP=N*STEP
W,H=530,347; CX,CY=265,173.5; T=52; K=1        # the design is 743x486; cropping the canvas to 530x347 shows the same 52px tile about 40% larger
S=lambda v:{"a":0,"k":v}
WH=S([1,1,1,1])
EASE={"o":{"x":[0.7],"y":[0]},"i":{"x":[0.25],"y":[1]}}      # strong ease in and out
LIN={"o":{"x":[0.5],"y":[0.5]},"i":{"x":[0.5],"y":[0.5]}}
def tr(r=None,s=100,p=(0,0),a=(0,0)): return {"ty":"tr","p":S(list(p)),"a":S(list(a)),"s":S([s,s]),"r":r if isinstance(r,dict) else S(r or 0),"o":S(100),"sk":S(0),"sa":S(0)}
def stroke(w,cap=2,join=2): return {"ty":"st","c":WH,"o":S(100),"w":S(w),"lc":cap,"lj":join,"ml":4}
fill={"ty":"fl","c":WH,"o":S(100),"r":1}
def path(pts,closed=False): return {"ty":"sh","ks":S({"i":[[0,0]]*len(pts),"o":[[0,0]]*len(pts),"v":[[round(x,3),round(y,3)] for x,y in pts],"c":closed})}
def grp(items,nm="g"): return {"ty":"gr","nm":nm,"it":items+[tr()]}
def rect(w,h,r=0,p=(0,0)): return {"ty":"rc","d":1,"s":S([w,h]),"p":S(list(p)),"r":S(r)}
# ---- icons: the exact vector paths exported from the Figma design (src/figma/*.svg), converted to Lottie bezier paths ----
import re,os
HERE=os.path.dirname(os.path.abspath(__file__))
def svg_paths(fn):
    """Return (size, [subpath...]) where a subpath = (closed, [(x,y,inDx,inDy,outDx,outDy)...]) from an SVG with one absolute-coordinate path."""
    t=open(os.path.join(HERE,"figma",fn)).read()
    size=float(re.search(r'viewBox="0 0 ([\d.]+)',t).group(1)); d=re.search(r' d="([^"]+)"',t).group(1)
    tok=re.findall(r"[MLHVCZ]|-?\d*\.?\d+",d); i=0; cmd=None; cur=(0,0); subs=[]; pts=None
    def num():
        nonlocal i; v=float(tok[i]); i+=1; return v
    while i<len(tok):
        if tok[i] in "MLHVCZ": cmd=tok[i]; i+=1
        if cmd=="M":
            cur=(num(),num()); pts=[[cur[0],cur[1],0,0,0,0]]; subs.append([False,pts]); cmd="L"
        elif cmd=="L": cur=(num(),num()); pts.append([cur[0],cur[1],0,0,0,0])
        elif cmd=="H": cur=(num(),cur[1]); pts.append([cur[0],cur[1],0,0,0,0])
        elif cmd=="V": cur=(cur[0],num()); pts.append([cur[0],cur[1],0,0,0,0])
        elif cmd=="C":
            c1=(num(),num()); c2=(num(),num()); e=(num(),num())
            pts[-1][4:6]=[c1[0]-cur[0],c1[1]-cur[1]]; pts.append([e[0],e[1],c2[0]-e[0],c2[1]-e[1],0,0]); cur=e
        elif cmd=="Z":
            subs[-1][0]=True
            if len(pts)>1 and abs(pts[-1][0]-pts[0][0])<1e-6 and abs(pts[-1][1]-pts[0][1])<1e-6:      # explicit return to the start: merge
                pts[0][2:4]=pts[-1][2:4]; pts.pop()
            cur=(pts[0][0],pts[0][1])
    return size,subs
def figma_icon(fn,off):          # centred on the 52px tile centre; off = where the SVG's own centre sits relative to the tile centre
    size,subs=svg_paths(fn); h=size/2; items=[]
    for closed,pts in subs:
        items.append({"ty":"sh","ks":S({"c":closed,"v":[[round(p[0]-h,3),round(p[1]-h,3)] for p in pts],
            "i":[[round(p[2],3),round(p[3],3)] for p in pts],"o":[[round(p[4],3),round(p[5],3)] for p in pts]})})
    return [{"ty":"gr","nm":fn,"it":items+[{"ty":"fl","c":WH,"o":S(100),"r":2},tr()]}],off       # r:2 = even-odd (cut-outs)
def loom(): return figma_icon("loom.svg",(0,0))
def film(): return figma_icon("film.svg",(0.5,0))
def cursor(): return figma_icon("cursor.svg",(0.5,0))
def camera(): return figma_icon("camera.svg",(0.5,0))
ICONS=[("Loom",loom),("Film",film),("Cursor",cursor),("Camera",camera)]
X_IN,X_OUT=-130,130; SC=60                             # hidden: slid 130px (2.5 tiles) to the left/right of centre, at 60% size
def key(t,v,e=EASE,hold=False):
    d={"t":round(t*FPS,2),"s":[round(x,3) for x in v]}
    d.update({"h":1} if hold else e); return d
def clean(L,end):
    L.sort(key=lambda d:d["t"]); out=[]
    for d in L:
        if out and abs(out[-1]["t"]-d["t"])<1e-6: out[-1]=d
        else: out.append(d)
    out[-1].pop("o",None); out[-1].pop("i",None); return out
def tile_layer(i):
    nm,fn=ICONS[i]
    te0=i*STEP; te1=te0+MOVE; ex0=(i+1)*STEP; ex1=ex0+MOVE
    HID_L=([CX+X_IN,CY,0],[0],[SC,SC,100]); HID_R=([CX+X_OUT,CY,0],[0],[SC,SC,100]); SHOW=([CX,CY,0],[100],[100,100,100])
    pk=[];ok=[];sk=[]
    def add(t,st,e=EASE,hold=False):
        pk.append(key(t,st[0],e,hold)); ok.append(key(t,st[1],e,hold)); sk.append(key(t,st[2],e,hold))
    wrap=ex1>LOOP                                          # last tile: its zoom-out wraps round to the start of the loop
    if wrap:
        add(0,SHOW); add(ex1-LOOP,HID_R,hold=True) ; add(te0-0.001,HID_R,hold=True)
        # (hidden-right holds until just before its zoom-in; then it is placed at the left)
        add(te0,HID_L); add(te1,SHOW); add(LOOP,SHOW)
        # hold full size through the wiggle, up to the loop end
        pk[:]=[d for d in pk]
    else:
        add(0,HID_L,hold=True); add(te0,HID_L); add(te1,SHOW); add(ex0,SHOW); add(ex1,HID_R,hold=True)
        add(LOOP,HID_L if i>0 else HID_L)
    # the exit of the last tile begins at 0 (state SHOW) and eases to HID_R; the others begin hidden at the left
    pk=clean(pk,LOOP); ok=clean(ok,LOOP); sk=clean(sk,LOOP)
    icon_items,off=fn()
    icon={"ty":"gr","nm":"Icon","it":icon_items+[tr(p=off)]}
    tile=grp([rect(T-1,T-1,11.5),{**stroke(1,1,1),"c":S([0.231,0.239,0.259,1])},{"ty":"fl","c":S([0.188,0.192,0.204,1]),"o":S(100),"r":1}],"Tile")   # #303134 with a 1px #3b3d42 border, radius 12
    return {"ddd":0,"ind":i+1,"ty":4,"nm":nm,"sr":1,"ks":{"o":{"a":1,"k":ok},"r":S(0),"p":{"a":1,"k":pk},"a":S([0,0,0]),"s":{"a":1,"k":sk}},
            "ao":0,"shapes":[icon,tile],"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":W,"h":H,"nm":"Icon carousel","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
     "layers":[tile_layer(i) for i in range(N)]}
emit("carousel",lot,"carousel")
