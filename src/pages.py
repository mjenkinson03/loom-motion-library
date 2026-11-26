# Writes the small per-animation pages in items/ (each plays one Lottie file, or is a self-contained canvas/WebGL page).
BAR=".bar{position:absolute;left:50%;top:73.5%;width:58vh;height:2vh;min-height:3px;transform:translateX(-50%);background:#1e1e20;overflow:hidden}.bar i{display:block;height:100%;width:0;background:#1b6ae0;@@}"
LOOPBAR="animation:load 5s linear infinite}@keyframes load{from{width:0}to{width:100%}"
CSS={
 "std":"#a{position:absolute;inset:0 0 auto 0;height:84%;display:grid;place-items:center}#a svg{height:36%!important;width:auto!important;overflow:visible!important}",
 "wide":"#a{position:absolute;inset:0 0 auto 0;height:84%;display:grid;place-items:center}#a svg{height:66%!important;width:auto!important;overflow:visible!important}",
 "reel":"#a{position:absolute;inset:0 0 auto 0;height:84%;display:grid;place-items:center}#a svg{height:58%!important;width:auto!important;overflow:visible!important}",
 "full":"#a{position:absolute;inset:0}#a svg{width:100%!important;height:100%!important}",
}
LOAD='''const FIX=new URLSearchParams(location.search).get('t');
new Response(new Blob([Uint8Array.from(atob(window.LOADER_GZ),c=>c.charCodeAt(0))]).stream().pipeThrough(new DecompressionStream('gzip'))).json()
 .then(data=>{const a=lottie.loadAnimation({container:document.getElementById('a'),renderer:'svg',loop:true,autoplay:FIX===null,animationData:data});@@
   if(FIX!==null)a.addEventListener('DOMLoaded',()=>a.goToAndStop(+FIX*1000,false));});'''
def page(name,title,kind,player="lottie_light.min.js"):
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>html,body{{margin:0;height:100%;background:#0b0b0c;overflow:hidden}}{CSS[kind]}
{BAR.replace('@@',LOOPBAR)}</style></head>
<body><div id="a"></div><div class="bar"><i></i></div>
<script src="{player}"></script><script src="{name}.gz.js"></script>
<script>
{LOAD.replace('@@','')}
</script></body></html>'''
def outro(name,title,bar_full):
    """Like page(), but the blue bar is driven by the animation: it fills as the logo loads and is full when the success beat starts."""
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>html,body{{margin:0;height:100%;background:#0b0b0c;overflow:hidden}}{CSS["std"]}
{BAR.replace('@@','')}</style></head>
<body><div id="a"></div><div class="bar"><i></i></div>
<script src="lottie_light.min.js"></script><script src="{name}.gz.js"></script>
<script>
const BAR_FULL={bar_full};
const setBar=s=>document.querySelector('.bar i').style.width=(Math.min(1,s/BAR_FULL)*100)+'%';
{LOAD.replace('@@',"a.addEventListener('enterFrame',e=>setBar(e.currentTime/60));")}
</script></body></html>'''
def arrival():
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>Arrival</title>
<style>html,body{{margin:0;height:100%;background:#0a0a0c;overflow:hidden}}#a{{position:absolute;inset:0;transform:scale(.75);transform-origin:50% 42%}}#a svg{{width:100%!important;height:100%!important}}
.vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 42%,rgba(0,0,0,0) 35%,rgba(0,0,0,.55) 100%)}}
{BAR.replace('@@','')}</style></head>
<body><div id="a"></div><div class="vig"></div><div class="bar"><i></i></div>
<script src="lottie_light.min.js"></script><script src="arrival.gz.js"></script>
<script>
const BAR_FULL=5.4;                       // the blue bar is driven by the animation: it starts with the entrance and is ~94% full when the exit begins (5.1s)
const setBar=s=>document.querySelector('.bar i').style.width=(Math.min(1,s/BAR_FULL)*100)+'%';
{LOAD.replace('@@',"a.addEventListener('enterFrame',e=>setBar(e.currentTime/60));")}
</script></body></html>'''
PAGES={
 "movie-reel":page("movie-reel","Movie reel","reel"),
 "shutter":page("shutter","Shutter","std"),
 "tracking":page("tracking","Tracking","wide"),
 "arrival":arrival(),
 "dof":page("dof","Depth of field","wide","lottie.min.js"),     # blur effect needs the full player
 "surfacing":page("surfacing","Surfacing","std"),
 "unfold":page("unfold","Unfold","std"),
 "tunnel":page("tunnel","Tunnel","full"),
 "assemble":page("assemble","Assemble","full"),
 "outro-bounce":outro("outro-bounce","Bounce check",2.4).replace("</style>","#a{display:block}#a svg{position:absolute;left:50%;top:50%;translate:-50% -50%;height:218%!important;width:auto!important}</style>"),   # comp is 1500 tall (logo falls off screen): same on-screen scale as the 248-tall comps
 "outro-cartwheel":outro("outro-cartwheel","Cartwheel",2.4),
 "outro-check":outro("outro-check","Morph",2.1),
 "carousel":page("carousel","Icon carousel","full").replace("</style>","#a{transform:translateY(-9%)}.bar{top:64.5%}</style>"),   # small tile: tile + bar centred as a pair
}
if __name__=="__main__":
    for k,v in PAGES.items(): open(f"items/{k}.html","w").write(v)
    print("wrote",len(PAGES),"pages")
