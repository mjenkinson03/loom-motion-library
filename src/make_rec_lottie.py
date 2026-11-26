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
for secs in (6,3,1):
    lot=copy.deepcopy(base); K=secs/MASTER; scale(lot,K); lot["nm"]=f"Recommendation {secs}s"
    real.emit(f"rec-{secs}",lot,f"recommendation-{secs}s")
