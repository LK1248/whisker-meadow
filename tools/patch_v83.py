"""v83: a cat that wriggles free of being held dashes away for about 2-3 s (runs 5-7 m) instead of a short hop away."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function walkAway(c,run=true){ const p=c.g.position; const away=Math.atan2(p.x-camera.position.x,p.z-camera.position.z)+rand(-1.2,1.2); goTo(c,p.x+Math.sin(away)*2.6,p.z+Math.cos(away)*2.6,null);",
    "function walkAway(c,run=true,dist=2.6){ const p=c.g.position; const away=Math.atan2(p.x-camera.position.x,p.z-camera.position.z)+rand(-1.2,1.2); goTo(c,p.x+Math.sin(away)*dist,p.z+Math.cos(away)*dist,null);")
rep("hop(c,0.3,0.45); showIcon(c,'huff',1.5); walkAway(c); W.stat.drops++;", "hop(c,0.3,0.45); showIcon(c,'huff',1.5); walkAway(c,true,rand(5,7)); W.stat.drops++;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("function walkAway(c,run=true,dist=2.6){ const p=c.g.position; const away=Math.atan2(p.x-camera.position.x,p.z-camera.position.z)+rand(-1.2,1.2);",
    "function walkAway(c,run=true,dist=2.6){ const p=c.g.position; let away=Math.atan2(p.x-camera.position.x,p.z-camera.position.z)+rand(-1.2,1.2);\n"
    "  if(dist>3){ let best=-1; for(let i=0;i<10;i++){ const a=away+(i-5)*0.55, tx=clampX(p.x+Math.sin(a)*dist,0.4), tz=clampZ(p.z+Math.cos(a)*dist,0.4), d=Math.hypot(tx-p.x,tz-p.z)-Math.abs(i-5)*0.15; if(d>best){ best=d; away=a; } } }")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
