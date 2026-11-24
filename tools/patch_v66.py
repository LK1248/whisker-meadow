"""v66: new arrivals show their real coat from the first moment (the meet sheet pauses play, and coats only
updated while running). Matting/dull coat/gloss are applied on arrival, and a scruffy stray may bring fleas."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function meet(c,origin,parents){ meetQ.push({c,origin,parents});",
    "function coatNow(c){ if(!c||!c.core)return; ensureBurrs(c); updateScruff(c); updateSheen(c,0); updateFleas(c,0.05); }\n"
    "function meet(c,origin,parents){ if(origin==='stray'&&W.stat.pairDone&&c.s.groom<FLEA_AT&&!c.fleas&&Math.random()<0.4)c.fleas=5+Math.floor(rand(0,4)); coatNow(c); meetQ.push({c,origin,parents});")
rep("window.__wm={Snd,", "window.__wm={Snd,coatNow,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
