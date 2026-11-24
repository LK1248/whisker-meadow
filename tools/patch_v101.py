"""v101: no more overlap-then-snap after dropping a cat by another. If the dropped cat lands closer than nose-to-nose,
both cats ease back to the right spacing together over ~0.9s (each moves half, on a smooth curve) instead of staying
overlapped and then being shoved apart. The romp that follows still starts suddenly, as intended."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("  for(const o of active()){ if(o!==c&&dist2(o.g.position,c.g.position)<1.9){ addBond(c,o,6);",
    "  for(const o of active()){ if(o!==c&&dist2(o.g.position,c.g.position)<1.9){ { const p=c.g.position, op=o.g.position, want=1.56*(c.g.scale.x+o.g.scale.x)/2, d=dist2(p,op); /* too close: both ease back to nose-to-nose */\n"
    "      if(d<want-0.05){ const n=d>0.01?d:1, ux=d>0.01?(p.x-op.x)/n:Math.sin(c.heading+Math.PI), uz=d>0.01?(p.z-op.z)/n:Math.cos(c.heading+Math.PI), h=(want-d)/2;\n"
    "        c.landFrom=p.clone(); c.landTo=new V3(clampX(p.x+ux*h,0.35),0,clampZ(p.z+uz*h,0.35)); c.landK=0; o.landFrom=op.clone(); o.landTo=new V3(clampX(op.x-ux*h,0.35),0,clampZ(op.z-uz*h,0.35)); o.landK=0; } }\n"
    "      addBond(c,o,6);")
rep("function dropCat(c){", "function landGlide(c,dt){ if(!c.landTo)return; c.landK=Math.min(1,c.landK+dt/0.9); const k=c.landK*c.landK*(3-2*c.landK), p=c.g.position;\n"
    "  p.x=c.landFrom.x+(c.landTo.x-c.landFrom.x)*k; p.z=c.landFrom.z+(c.landTo.z-c.landFrom.z)*k; c.speed=0; if(c.landK>=1)c.landTo=null; }\nfunction dropCat(c){")
rep("  if(c.away>0){ c.away-=dt; if(c.away<=0)returnFromShow(c); return; }\n  const s=c.s, adult=c.age>=1,",
    "  if(c.away>0){ c.away-=dt; if(c.away<=0)returnFromShow(c); return; }\n  landGlide(c,dt);\n  const s=c.s, adult=c.age>=1,")
# while easing apart, the boop's own approach/back-off waits
rep("c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); if(d>want){",
    "c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); if(c.landTo||o.landTo){ c.stT=Math.max(c.stT,1); } else if(d>want){")
rep("window.__wm={Snd,", "window.__wm={Snd,dropCat,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
