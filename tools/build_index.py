"""Build index.html (a standalone page for GitHub Pages) from whisker-meadow.html.

whisker-meadow.html is authored as an artifact body (no doctype/head skeleton),
so this wraps it with the doctype and viewport tag a plain browser needs.
"""
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "whisker-meadow.html").read_text(encoding="utf-8")
if body.startswith('<meta charset="utf-8">'):
    body = body[len('<meta charset="utf-8">'):].lstrip("\n")
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
    + body + "\n</html>\n"
)
(root / "index.html").write_text(page, encoding="utf-8")
print("index.html written")
