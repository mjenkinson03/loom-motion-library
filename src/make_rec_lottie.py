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
for secs in (6,3):                                    # 6s and 3s: the whole sequence stretched / squeezed in time
    lot=copy.deepcopy(base); K=secs/MASTER; scale(lot,K); lot["nm"]=f"Recommendation {secs}s"
    real.emit(f"rec-{secs}",lot,f"recommendation-{secs}s")
# 1s: loading is just the 1.1s shutter. Nothing is sped up; the bounce outro is tagged on after it at its normal speed (about 3.9s in all).
lot=copy.deepcopy(base); cut_start(lot,1.3,base["fr"]); lot["nm"]="Recommendation 1s (shutter, then outro)"
real.emit("rec-1",lot,"recommendation-1s")
