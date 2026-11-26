"""v152: the bonding lesson only continues when the carried cat is put down right next to the other cat.
dist2() returns a plain distance (not squared), so the check `dist2(...) < 1.9*1.9` accepted drops up to 3.6 m
away. Now it is < 1.9 m (about a cat's length plus a little); farther drops start the pointing hand over."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){ pl.stage='watch';",
    "if(o&&dist2(o.g.position,d.g.position)<1.9){ pl.stage='watch';")
open(P, 'w', encoding='utf-8').write(s)
print('v152 applied')
