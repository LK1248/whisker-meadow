"""v60: the open shop listens for money changes. Buy/upgrade buttons enable or disable live
(e.g. coins arriving while the shop is open make the guided kibble buyable) without re-rendering."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function openShop(guide){ guide=guide||rainGuide();",
"""function shopCan(it){ const avail=it.avail?it.avail():true, max=it.max?it.max():Infinity, have=it.id==='helper'?helpers.length:it.max?countItems(it.id):0, need=it.need?it.need():0, hn=it.homes?it.homes():0;
  return avail&&have<max&&W.money>=it.cost()&&W.stars>=need&&W.homes.length>=hn; }
function upCan(k){ const n=W.tier[k]+1; return n<=TIERS[k].length&&W.stars>=starsFor(n)&&W.money>=upCost(k,n); }
// live refresh while the shop is open: money (or stars) changed -> toggle buttons in place
function shopRefresh(){ if($('#modal').hidden)return; const bs=document.querySelectorAll('#modal [data-buy],#modal [data-up]'); if(!bs.length)return;
  for(const b of bs){ let can; if(b.dataset.buy){ const it=SHOP.find(x=>x.id===b.dataset.buy); if(!it)continue; can=shopCan(it); } else can=upCan(b.dataset.up);
    if(b.disabled===can){ b.disabled=!can; if(can){ b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); } } } }
function openShop(guide){ guide=guide||rainGuide();""")
rep("const hn=it.homes?it.homes():0, hOk=W.homes.length>=hn; const can=avail&&have<max&&W.money>=cost&&starOk&&hOk;",
    "const hn=it.homes?it.homes():0, hOk=W.homes.length>=hn; const can=shopCan(it);")
rep("$('#hRib').textContent=W.ribbons; $('#hStars').textContent=W.stars; }",
    "$('#hRib').textContent=W.ribbons; $('#hStars').textContent=W.stars; shopRefresh(); }")
# little pop when a button becomes available
rep("</style>", "#modal button.pop{animation:btnPop .35s ease-out}@keyframes btnPop{40%{transform:scale(1.15)}}\n</style>")
rep("window.__wm={Snd,", "window.__wm={Snd,shopRefresh,openShop,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
