# Recommendation row: the same sequence at three total lengths (6s, 3s, 1s). It is the Bounce outro (shutter plays through to start, the
# bounce closes) built once by make_outro_bounce_lottie.py, then every keyframe time is scaled uniformly so the whole loop lasts 6, 3 or 1 second.
import sys,types,copy,runpy,os
import emit as real
captured={}
fake=types.ModuleType("emit"); fake.emit=lambda name,lot,export: captured.update(lot=lot); sys.modules["emit"]=fake
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),"make_outro_bounce_lottie.py"))
sys.modules["emit"]=real
base=captured["lot"]; MASTER=base["op"]/base["fr"]          # seconds in the master timeline
def scale(o,K):
    if isinstance(o,dict):
        if "t" in o and "s" in o and isinstance(o["t"],(int,float)): o["t"]=round(o["t"]*K,3)
        for k,v in o.items():
            if k in ("op","ip","st") and isinstance(v,(int,float)): o[k]=round(v*K,3)
            else: scale(v,K)
    elif isinstance(o,list):
        for x in o: scale(x,K)
def cut_start(o,T,fps):
    """Drop the first T seconds (the loading hold) of every animated property and shift everything else earlier: the shutter then starts at 0 at its natural speed."""
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                keep=[dict(x) for x in v if x["t"]>=T*fps-1e-6]
                for x in keep: x["t"]=round(x["t"]-T*fps,3)
                if keep[0]["t"]>0: keep.insert(0,{**keep[0],"t":0})
                o[k]=keep
            elif k in ("op",) and isinstance(v,(int,float)): o[k]=round(v-T*fps,3)
            else: cut_start(v,T,fps)
    elif isinstance(o,list):
        for x in o: cut_start(x,T,fps)
def retime(o,delta,t0,fps):
    """Shift every keyframe at or after t0 (seconds) by delta seconds (positive = a longer loading hold before the shutter)."""
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                for x in v:
                    if x["t"]>=t0*fps-1e-6: x["t"]=round(x["t"]+delta*fps,3)
            elif k=="op" and isinstance(v,(int,float)): o[k]=round(v+delta*fps,3)
            else: retime(v,delta,t0,fps)
    elif isinstance(o,list):
        for x in o: retime(x,delta,t0,fps)
# Even it out: in this row the shutter lasts exactly 1.0s (it is 1.1s in the master) and the outro (nudge, drop, check, fade) exactly 1.0s (1.7s
# in the master). The loop reset after the check (beams opening again, 1.05s) keeps its normal speed. Done by warping the master timeline piecewise.
def warp_t(t):
    if t<=1.3: return t
    if t<=2.4: return 1.3+(t-1.3)*(1.0/1.1)          # shutter 1.1s -> 1.0s
    if t<=4.1: return 2.3+(t-2.4)*(1.0/1.7)          # outro 1.7s -> 1.0s
    return 3.3+(t-4.1)                                  # reset unchanged
def warp(o,fps):
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                for x in v: x["t"]=round(warp_t(x["t"]/fps)*fps,3)
            elif k=="op" and isinstance(v,(int,float)): o[k]=round(warp_t(v/fps)*fps,3)
            else: warp(v,fps)
    elif isinstance(o,list):
        for x in o: warp(x,fps)
warp(base,base["fr"])
# The number in each card is how long the blue bar takes to load. The shutter plays at the END of the loading (it lasts 1.1s: 1.3s-2.4s in the master
# timeline) and the bounce outro follows at its normal speed. Nothing is sped up: only the loading hold before the shutter is longer or shorter.
SHUTTER_START,SHUTTER_LEN=1.3,1.0
def repeat_shutter(o,n,L,pause,D,fps):
    """The shutter (the first L seconds of every animated property) plays n times, each followed by a pause; the rest (the outro) starts at D."""
    C=L+pause; shift=D-L
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="k" and isinstance(v,list) and v and isinstance(v[0],dict) and "t" in v[0] and "s" in v[0]:
                pre=[x for x in v if x["t"]<L*fps-1e-6]; post=[x for x in v if x["t"]>=L*fps-1e-6]
                out=[]
                for c in range(n):
                    for x in pre: y=copy.deepcopy(x); y["t"]=round(x["t"]+c*C*fps,3); out.append(y)
                    if pause>0:                                    # hold the resting state through the pause
                        y=copy.deepcopy(pre[0]); y["t"]=round((c*C+L)*fps,3); out.append(y)
                for x in post: y=copy.deepcopy(x); y["t"]=round(x["t"]+shift*fps,3); out.append(y)
                o[k]=out
            elif k=="op" and isinstance(v,(int,float)): o[k]=round(v+shift*fps,3)
            else: repeat_shutter(v,n,L,pause,D,fps)
    elif isinstance(o,list):
        for x in o: repeat_shutter(x,n,L,pause,D,fps)
# Loading is filled with the shutter: it keeps cycling (1.0s shutter + 0.5s pause per cycle) until the bar is full, then the 1.0s outro runs. 6s = 4 cycles, 3s = 2, 1s = 1.
cut=copy.deepcopy(base); cut_start(cut,SHUTTER_START,base["fr"])
for secs in (6,3,1):
    pause=0.5 if secs>1 else 0.0                          # half a second between shutter cycles (the 1s card is a single shutter, no pause)
    n=round(secs/(SHUTTER_LEN+pause))
    lot=copy.deepcopy(cut); repeat_shutter(lot,n,SHUTTER_LEN,pause,secs,base["fr"])
    lot["nm"]=f"Recommendation {secs}s loading"
    real.emit(f"rec-{secs}",lot,f"recommendation-{secs}s")

# ---- 15 seconds ("error"): the shutter cycles for the first 8s, then stops: the logo fades to a subtle gray and slowly pulses between light gray and white
# until the 15s load finishes, then it warms back to white as the 1s check outro plays.
DARK=[0.24,0.24,0.26,1]; LIGHT=[0.50,0.50,0.53,1]; WHITE=[1,1,1,1]       # the logo never goes back to white while it waits: dark gray <-> light gray
def colour_keys(fps):
    half=6/5                                               # 9s -> 15s is 5 half-pulses of 1.2s each (slower), so it ends on the light gray
    pts=[(0,WHITE),(8.0,WHITE),(9.0,DARK)]+[(9.0+half*(k+1),LIGHT if k%2==0 else DARK) for k in range(5)]+[(15.5,WHITE),(40,WHITE)]
    ks=[]
    for i,(t,c) in enumerate(pts):
        d={"t":round(t*fps,3),"s":c}
        if i<len(pts)-1: d.update({"o":{"x":[0.45],"y":[0]},"i":{"x":[0.55],"y":[1]}})
        ks.append(d)
    return {"a":1,"k":ks}
def recolour(o,fps):
    if isinstance(o,dict):
        if o.get("td"): return                              # leave the hole's matte layer alone (it only supplies a shape)
        if o.get("ty")=="fl": o["c"]=colour_keys(fps)
        for v in o.values(): recolour(v,fps)
    elif isinstance(o,list):
        for x in o: recolour(x,fps)
lot=copy.deepcopy(cut); repeat_shutter(lot,5,SHUTTER_LEN,0.5,15,base["fr"])     # 5 shutter cycles = 7.5s, then it holds still
recolour(lot,base["fr"]); lot["nm"]="Recommendation 15s (error)"
real.emit("rec-15",lot,"recommendation-15s")
