"""Build index.html (a standalone page for GitHub Pages) from whisker-meadow.html.

whisker-meadow.html is authored as an artifact body (no doctype/head skeleton),
so this wraps it with the doctype and viewport tag a plain browser needs.
"""
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "whisker-meadow.html").read_text(encoding="utf-8")
if body.startswith('<meta charset="utf-8">'):
    body = body[len('<meta charset="utf-8">'):].lstrip("\n")
# installed app only: the OS splash closes at first paint (well under a second), so this one carries on in the same
# sky blue with a bigger icon, holds for about 1.8s from launch, then fades into the game.
SPLASH = (
    '<div id="wmSplash" style="position:fixed;inset:0;z-index:9999;background:#bfe8f7;display:none;align-items:center;justify-content:center;transition:opacity .45s">'
    '<img src="img/icon-512.png" alt="" style="width:min(46vmin,280px);height:auto;border-radius:22%;box-shadow:0 10px 30px rgba(40,90,120,.25);animation:wmPop .6s ease-out">'
    '</div><style>@keyframes wmPop{from{transform:scale(.82);opacity:.6}to{transform:none;opacity:1}}</style>'
    "<script>(function(){var s=document.getElementById('wmSplash'),st=matchMedia('(display-mode: standalone)').matches||navigator.standalone;"
    "if(!st){s.remove();return;}s.style.display='flex';var t0=performance.now(),done=false;"
    "function hide(){if(done)return;done=true;setTimeout(function(){s.style.opacity=0;setTimeout(function(){s.remove();},500);},Math.max(0,1800-(performance.now()-t0)));}"
    "addEventListener('load',hide);setTimeout(hide,5000);})();</script>\n"
)
page = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    # installable web app (GitHub Pages only; the artifact copy has no manifest or service worker)
    '<meta name="theme-color" content="#5fb35a">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-title" content="Whisker Meadow">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="icon" href="img/icon-192.png" type="image/png">\n'
    '<link rel="apple-touch-icon" href="img/icon-192.png">\n'
    "<script>if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'))"
    "addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>\n"
    + SPLASH + body + "\n</html>\n"
)
(root / "index.html").write_text(page, encoding="utf-8")
print("index.html written")
