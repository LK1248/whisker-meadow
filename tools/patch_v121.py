"""v121: lessons don't wait for the fair result. The blink/bonding lessons may start as soon as the first cat has been
sent to the fair (as in v115); a cat whose fair ends during any lesson waits at the fair until the lesson is done
(kept from v120), so the award banner never interrupts a lesson."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function earlyDone(){ return ((W.stat.showsBack||0)>0||!!W.stat.fairSkip||W.time>600)&&!W.cats.some(c=>c.away>0); }",
    "function earlyDone(){ return (W.stat.shows||0)>0||!!W.stat.fairSkip||W.time>600; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
