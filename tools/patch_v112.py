"""v112: the wand lesson gets the same dim-with-a-spotlight the shop lessons use, centred on the wand button while
you're being asked to pick it up. And the first Bigger meadow needs only 1 star."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("b.classList.toggle('shopLock',!!(L&&L.shop)); if(L&&L.shop){ const r=$('#bShop').getBoundingClientRect();",
    "b.classList.toggle('shopLock',!!(L&&L.shop)); const wl=!!L&&wandForce()==='pick'; b.classList.toggle('wandLock',wl); if(wl){ const r=document.querySelector('.tool[data-tool=\"wand\"]').getBoundingClientRect(); b.style.setProperty('--sx',(r.left+r.width/2)+'px'); b.style.setProperty('--sy',(r.top+r.height/2)+'px'); } if(L&&L.shop){ const r=$('#bShop').getBoundingClientRect();")
rep("body.shopLock:not(.shopOpen)::after{opacity:1}", "body.shopLock:not(.shopOpen)::after,body.wandLock::after{opacity:1}")
open(P, 'w', encoding='utf-8').write(s); print('ok')
# the first Bigger meadow needs just 1 star (later ones unchanged)
s = open(P, encoding='utf-8').read()
rep("need:()=>Math.min(5,W.level+1),", "need:()=>W.level===1?1:Math.min(5,W.level+1),")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
