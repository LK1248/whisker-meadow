"""v135: tapping away from a cat you just petted ends the pet grace, so the stroke ring disappears at once
(before, it came back after the tap was lifted and lingered until the 1s grace ran out)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("&&nearPet(PG.c,e))hit={cat:PG.c,zone:'back'};\n",
    "&&nearPet(PG.c,e))hit={cat:PG.c,zone:'back'};\n  if(PG.c&&!(hit&&hit.cat===PG.c))PG.until=-1;\n")
open(P, 'w', encoding='utf-8').write(s)
print('v135 applied')
