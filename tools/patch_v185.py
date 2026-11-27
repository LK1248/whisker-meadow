"""v185: fleas can lower health down to 40 (was 55). A cat with fleas can drop below the adoption line (55); families
already tend to turn away a cat with fleas for its grooming, so this plays out similarly.
Open question (not decided): whether fleas should block adoption outright, as they block fairs."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("FLEA_FLOOR=55;", "FLEA_FLOOR=40;")
rep("// fleas: a slow drain, never below the adoption line", "// fleas: a slow drain, down to a floor")
open(P, 'w', encoding='utf-8').write(s)
print('v185 applied')
