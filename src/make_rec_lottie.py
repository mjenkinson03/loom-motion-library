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
for secs in (6,3,1):
    lot=copy.deepcopy(base)
    start=max(0.0,secs-SHUTTER_LEN)                                   # when the shutter begins in the new timeline
    if start>=SHUTTER_START: retime(lot,start-SHUTTER_START,SHUTTER_START,base["fr"])
    else: cut_start(lot,SHUTTER_START-start,base["fr"])               # loading shorter than the master hold: cut the hold (the 1s card starts on the shutter)
    lot["nm"]=f"Recommendation {secs}s loading"
    real.emit(f"rec-{secs}",lot,f"recommendation-{secs}s")
