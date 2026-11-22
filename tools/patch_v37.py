"""v37: forgiving presses. If a press misses every cat, grab the nearest cat within a finger's width on screen
(small, moving cats - e.g. runaways walking home outside the fence - are otherwise easy to miss and the press turns into a pan)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function toScreen(v){", """function nearCat(e,touch){ const lim=touch?46:26; let best=null, bd=lim;
  for(const c of W.cats){ if(c.away>0||c.carried||!c.g.visible)continue; const q=toScreen(c.g.position.clone().setY(0.35*c.g.scale.y)); if(!q.ok)continue;
    const d=Math.hypot(q.x-e.clientX,q.y-e.clientY)-(c===(W.runaway&&W.runaway.c)?14:0); if(d<bd){ bd=d; best=c; } }
  return best?{cat:best,zone:'back'}:null; }
function toScreen(v){""")
rep("  const hit=pickAt(e);\n  if(hit&&hit.item&&hit.item.kind!=='shelter'){ P.mode='item';",
    "  let hit=pickAt(e); if(!(hit&&(hit.cat||(hit.item&&hit.item.kind!=='shelter')))&&(W.tool==='hand'||W.tool==='brush')){ const nc=nearCat(e,e.pointerType!=='mouse'); if(nc)hit=nc; }\n  if(hit&&hit.item&&hit.item.kind!=='shelter'){ P.mode='item';")
open(P, 'w', encoding='utf-8').write(s); print('ok')
