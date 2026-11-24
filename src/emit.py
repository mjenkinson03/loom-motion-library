# Shared by every generator: writes the compressed copy the page plays (items/<name>.gz.js) and the plain Lottie JSON (../lottie/<export>.json).
import json,gzip,base64
def emit(name,lot,export,minify=True):
    b=json.dumps(lot,separators=(",",":")).encode()
    open(f"items/{name}.gz.js","w").write('window.LOADER_GZ="'+base64.b64encode(gzip.compress(b,9)).decode()+'";')
    open(f"../lottie/{export}.json","wb").write(b)
    print(f"{export}: {len(b)/1024:.1f} KB json, loop {lot['op']/lot['fr']:.2f}s")
