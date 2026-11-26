"""v139:
- The stray (meet) window keeps its Hello! button always visible: the window is a column, only the cat list in
  the middle scrolls, and the name stays at the top and the button at the bottom.
- Butterflies glow less at night: their (unlit) wing colour dims with the night amount, down to about 55%."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#meet .sheet{background:var(--cream);border-radius:26px;width:min(540px,100%);max-height:50vh;overflow:auto;",
    "#meet .sheet{background:var(--cream);border-radius:26px;width:min(540px,100%);max-height:50vh;overflow:hidden;display:flex;flex-direction:column;box-sizing:border-box;")
rep("#meet .big{margin-top:12px}",
    "#meet .big{margin-top:12px;flex:none}#meet .nm,#meet .org{flex:none}#meet .roster{flex:0 1 auto;min-height:0;overflow:auto;overscroll-behavior:contain}")
rep("const b={g,lp,rp,ph:rand(0,6),tgt:new V3(),spd:0.9};", "const b={g,lp,rp,wm,col:new THREE.Color(col),ph:rand(0,6),tgt:new V3(),spd:0.9};")
rep("function updateButterflies(dt,t){ for(const b of butterflies){ const p=b.g.position;",
    "function updateButterflies(dt,t){ const dim=1-0.45*(W.night||0); for(const b of butterflies){ b.wm.color.copy(b.col).multiplyScalar(dim); const p=b.g.position;")
open(P, 'w', encoding='utf-8').write(s)
print('v139 applied')
