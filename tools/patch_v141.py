"""v141: fewer dead presses.
- Families only visit when a cat is ready to adopt (no more "would love a cat" visits when nobody is ready); one
  comes as soon as a cat is ready if the visit timer has run out.
- Tapping an item with no tap action (bed, post, perch...) squishes it with a soft pop; a fancy ball spins.
- When a lesson or step only allows certain cats (fair step, adoption pick, brush and flea lessons...), a tap
  that just misses an allowed cat counts as a tap on it instead of being ignored. (Not for the butt-tap tip,
  where the exact spot matters.)"""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function spawnFamily(){ const ready=W.cats.filter(readyHome); if(!ready.length&&!W.homes.length)return;",
    "function spawnFamily(){ const ready=W.cats.filter(readyHome); if(!ready.length)return;")
rep("  else if(it.kind==='ball'){ it.vel.set(rand(-3,3),0,rand(-3,3)); Snd.jingle(); }\n}",
    "  else if(it.kind==='ball'&&!(it.tier>1)){ it.vel.set(rand(-3,3),0,rand(-3,3)); Snd.jingle(); }\n"
    "  else { if(it.kind==='ball'){ it.spin=4; Snd.jingle(); } else Snd.pop(); it.boing=1; }\n}")
rep("  for(const it of items){ if(it.kind==='ball'&&it.tier>1&&it.orb){",
    "  for(const it of items){ if(it.boing>0){ it.boing=Math.max(0,it.boing-dt*2.5); const k=Math.sin((1-it.boing)*Math.PI*3)*it.boing*0.14; it.mesh.scale.set(1+k*0.6,1-k,1+k*0.6); }\n    if(it.kind==='ball'&&it.tier>1&&it.orb){")
rep("{ const L=tutLock(); if(L&&!(L.wandOk&&W.tool==='wand')){ if(hit&&(!hit.cat||!L.cats.includes(hit.cat)))hit=null;",
    "{ const L=tutLock(); if(L&&!(L.wandOk&&W.tool==='wand')){ if(!(hit&&hit.cat&&L.cats.includes(hit.cat))&&!(tips.cur&&tips.cur.kind==='butt')){ const nc=L.cats.find(c=>nearPet(c,e)); if(nc)hit={cat:nc,zone:'back'}; } if(hit&&(!hit.cat||!L.cats.includes(hit.cat)))hit=null;")
open(P, 'w', encoding='utf-8').write(s)
print('v141 applied')
