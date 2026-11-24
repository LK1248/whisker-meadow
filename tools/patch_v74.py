"""v74: top petting speed halved: the fast edge is now about 1.17x the cat's favourite speed (was 2.34x).
The gauge zooms in (full sweep = 3.3x either way instead of 11x) so the narrower band stays readable."""
import sys, math
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("const FAST_CAP=0.85; // loose top speed: about 2.3x the cat's favourite stroke speed",
    "const FAST_CAP=0.16; // top speed: about 1.17x the cat's favourite stroke speed")
rep("const A=68, m=v=>clamp(v/2.4,-1,1)*A,", "const A=68, m=v=>clamp(v/1.2,-1,1)*A,")
rep("const nx=st?TG.x:-2.4;", "const nx=st?TG.x:-1.2;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
