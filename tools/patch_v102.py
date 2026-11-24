"""v102: shop lessons dim the screen like the other lessons, with a clear spotlight on the shop button, so it's obvious
what to tap. The dim lifts while the shop itself is open (the shop has its own guide arrow)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("#intro.off{opacity:0}",
    "#intro.off{opacity:0}\n"
    "body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:3;opacity:0;transition:opacity .6s;background:radial-gradient(circle at var(--sx,50%) var(--sy,50%),transparent 0,transparent 46px,rgba(30,20,45,.6) 160px)}\n"
    "body.shopLock:not(.shopOpen)::after{opacity:1}")
rep("b.classList.toggle('shopLock',!!(L&&L.shop));",
    "b.classList.toggle('shopLock',!!(L&&L.shop)); if(L&&L.shop){ const r=$('#bShop').getBoundingClientRect(); b.style.setProperty('--sx',(r.left+r.width/2)+'px'); b.style.setProperty('--sy',(r.top+r.height/2)+'px'); b.classList.toggle('shopOpen',!$('#modal').hidden); }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
