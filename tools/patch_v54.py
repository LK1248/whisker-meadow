"""v54: more strays, sooner.
- The gap between strays scales with how full the sanctuary is: about a minute when it's under half full,
  1.5 min when it's fuller, 2+ min near the cap.
- A stray that can't come right now (tutorial, a goodbye, another drop-off, low health, full) retries in a few
  seconds instead of waiting for the whole next gap, so the first one arrives right after the tutorial."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("strayT-=dt; if(strayT<=0&&firstBye())strayT=8; if(strayT<=0){ strayT=rand(110,170); const act=active(); const avgH=act.reduce((a,c)=>a+c.s.health,0)/Math.max(1,act.length); if(W.cats.length<LV().cap&&avgH>=50)startDropoff(); }",
    "strayT-=dt; if(strayT<=0){ const act=active(); const avgH=act.reduce((a,c)=>a+c.s.health,0)/Math.max(1,act.length);\n"
    "    if(!firstBye()&&W.cats.length<LV().cap&&avgH>=50)startDropoff(); strayT=W.dropoff&&!W.dropoff.gift?strayGap():rand(6,10); }")
rep("let strayT=rand(100,140);",
    "let strayT=rand(60,80);\n"
    "// time to the next stray: short while there's lots of room, longer as the sanctuary fills\n"
    "function strayGap(){ const f=W.cats.length/LV().cap; return f<0.5?rand(45,70):f<0.8?rand(75,110):rand(110,150); }")
rep("window.__wm={Snd,", "window.__wm={Snd,strayGap,getStrayT:()=>strayT,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
