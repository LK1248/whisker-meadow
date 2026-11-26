"""v170: shorter nights.
The day clock now runs faster the darker it is (up to 2.5x at full night), so night is about half as long as before
(dark part ~124 s -> ~62 s, dusk to dawn ~162 s -> ~91 s). Daytime is unchanged (~258 s), so a day is now roughly
three times as long as a night. The whole cycle is ~5.8 min instead of 7."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function applySky(dt){ if(W.dayOn&&!tutQuiet())dayT=(dayT+dt)%DAYLEN;",
    "function applySky(dt){ if(W.dayOn&&!tutQuiet())dayT=(dayT+dt*(1+Math.min(1,(W.night||0)*1.5)))%DAYLEN; /* nights pass quicker */")
open(P, 'w', encoding='utf-8').write(s)
print('v170 applied')
