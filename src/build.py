# Builds ../index.html: index-src.html with every items/*.html inlined as srcdoc, one shared copy of each Lottie player.
import re,json,base64,os
h=open("index-src.html").read()
PLAYERS={}
def inline(p):
    t=open(p).read()
    def sub(m):
        name=m.group(1)
        if name.startswith("lottie"):
            PLAYERS[name]=open("items/"+name).read()
            return "<script>(function(){var s=document.createElement('script');s.textContent=parent.__PLAYER['"+name+"'];document.head.appendChild(s)})()</script>"
        return "<script>"+open("items/"+name).read().replace("</script","<\\/script")+"</script>"
    return re.sub(r'<script src="([^"]+)"></script>',sub,t)
srcs=re.findall(r"src:'(items/[^']+)'",h)
inl={s:inline(s) for s in srcs}
blob="var INLINE="+json.dumps(inl).replace("</","<\\/")+";\nvar __PLAYER="+json.dumps(PLAYERS).replace("</","<\\/")+";\n"
h=h.replace("var VW=1280",blob+"var VW=1280",1)
fav="data:image/svg+xml;base64,"+base64.b64encode(open("favicon-black.svg","rb").read()).decode()
h=h.replace("<title>Motion Library</title>",'<title>Motion Library</title>\n<link rel="icon" type="image/svg+xml" href="'+fav+'">',1)
h=h.replace("</body>",open("wave.html").read()+"\n</body>")
open("../index.html","w").write(h)
print("built ../index.html",os.path.getsize("../index.html")//1024,"KB")
