"""v70: the whole petting icon pulses with the beat (ring + disc), not just the inner disc."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("pu.style.transform=`scale(${(0.5+0.5*k).toFixed(3)})`; pu.style.fillOpacity=(0.35+0.65*k).toFixed(2); }",
    "pu.style.transform=`scale(${(0.5+0.5*k).toFixed(3)})`; pu.style.fillOpacity=(0.35+0.65*k).toFixed(2);"
    " el.querySelector('svg').style.transform=W.stat.metroOff?'':`scale(${(0.9+0.16*k).toFixed(3)})`; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
