# Icon carousel (Atlassian): one rounded dark tile at a time (Loom logo, film frame, cursor click, camera). Each tile zooms in, holds,
# its icon gives a little wiggle, then it zooms out as the next one zooms in. Built only from shapes: no images, no effects.
# Icon geometry is measured from the Figma design (tile 52px; Loom glyph 32px; film/cursor 27x28; camera 31x27), authored in those
# 52px units and scaled up by K.
import math
from emit import emit
FPS=60
MOVE,HOLD,WIG=0.65,1.3,0.6; STEP=MOVE+HOLD+WIG; N=4; LOOP=N*STEP
W,H=400,260; CX,CY=200,130; T=130; K=T/52
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
# ---- icons, in Figma's 52px tile units, centred on the tile centre (0,0) ----
def loom():                      # 32px glyph: 12 thin legs round a ring with a dark hole
    legs=[{"ty":"gr","it":[rect(2.3,9.6,0,(0,-11.2)),fill,tr(i*30)]} for i in range(12)]
    ring={"ty":"gr","it":[{"ty":"el","d":1,"s":S([11.2,11.2]),"p":S([0,0])},stroke(2.4,1,1),tr()]}
    return legs+[ring],(0,0)
def film():                      # 27.5 x 27.5 frame, sprocket holes down both sides, a bar across the middle
    it=[grp([rect(25.6,25.6,3.6),stroke(2.1)],"Frame"),
        grp([path([(-6.6,-12.8),(-6.6,12.8)]),stroke(1.7,1)],"L"),grp([path([(6.6,-12.8),(6.6,12.8)]),stroke(1.7,1)],"R"),
        grp([path([(-6.6,1.2),(6.6,1.2)]),stroke(1.7,1)],"Bar")]
    for y in (-9.6,-3.2,3.2,9.6):
        for x in (-10,10): it.append(grp([rect(2.6,2.4,0.5,(x,y)),fill],"Hole"))
    return it,(0.8,0)
def cursor():                    # navigation arrow with a small click arc at its top left
    arrow=[(-6.6,-7.2),(13.6,0.7),(0.6,13.7),(-0.8,3.6)]
    arc=[(-6.8+6.6*math.cos(math.radians(a)),-4.8+6.6*math.sin(math.radians(a))) for a in range(160,331,10)]
    return [grp([path(arrow,True),stroke(2.1,2,2)],"Arrow"),grp([path(arc),stroke(2.1,1,1)],"Click")],(0.5,0.2)
def camera():                    # 31 x 27: body, raised top, lens ring
    return [grp([path([(-15,-8),(-15,-4),(-15,10.5)]),stroke(0.01)],"x") if False else grp([rect(30,20,4.5,(0,3.7)),stroke(2.1)],"Body"),
            grp([path([(-8,-6.2),(-5.7,-10.8),(5.7,-10.8),(8,-6.2)]),stroke(2.1)],"Top"),
            grp([{"ty":"el","d":1,"s":S([10.4,10.4]),"p":S([0,3])},stroke(2.1)],"Lens")],(0,1.5)
ICONS=[("Loom",loom),("Film",film),("Cursor",cursor),("Camera",camera)]
X_IN,X_OUT=-70,70; SC=60                               # hidden: slid 70px to the left/right of centre, at 60% size
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
    te0=i*STEP; te1=te0+MOVE; wg0=te1+HOLD; wg1=wg0+WIG; ex0=(i+1)*STEP; ex1=ex0+MOVE
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
    rk=[key(0,[0],LIN),key(wg0,[0])]
    for dt,a in [(0.07,-11),(0.18,9),(0.29,-6),(0.4,3.5),(0.5,-1.5),(WIG,0)]: rk.append(key(wg0+dt,[a]))
    rk.append(key(LOOP,[0]))
    rk=clean(rk,LOOP)
    icon_items,off=fn()
    icon={"ty":"gr","nm":"Icon","it":icon_items+[tr(r={"a":1,"k":rk},s=K*100,p=(off[0]*K,off[1]*K),a=(off[0],off[1]))]}
    tile=grp([rect(T,T,12*K),{"ty":"fl","c":S([0.188,0.192,0.204,1]),"o":S(100),"r":1}],"Tile")
    return {"ddd":0,"ind":i+1,"ty":4,"nm":nm,"sr":1,"ks":{"o":{"a":1,"k":ok},"r":S(0),"p":{"a":1,"k":pk},"a":S([0,0,0]),"s":{"a":1,"k":sk}},
            "ao":0,"shapes":[icon,tile],"ip":0,"op":round(LOOP*FPS),"st":0,"bm":0}
lot={"v":"5.7.4","fr":FPS,"ip":0,"op":round(LOOP*FPS),"w":W,"h":H,"nm":"Icon carousel","ddd":0,"assets":[],"meta":{"g":"hand-built generator"},
     "layers":[tile_layer(i) for i in range(N)]}
emit("carousel",lot,"carousel")
