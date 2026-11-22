"""v21: tapping a runaway on its way out always brings it back; pressing on a cat holds it still until the tap/stroke/carry is decided."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
# runaway: catchable any time it's still walking out, even after the "slipped out" notice
rep("else if(W.runaway&&W.runaway.c===c&&!W.runaway.notified&&c.pathEnd==='hide')caughtEarly(c);",
    "else if(W.runaway&&W.runaway.c===c&&c.pathEnd==='hide')caughtEarly(c);")
rep("function caughtEarly(c){ W.stat.quick=(W.stat.quick||0)+1;", "function caughtEarly(c){ if(W.runaway&&W.runaway.notified){ W.stat.found++; c.s.trust=Math.min(100,c.s.trust+4); } else W.stat.quick=(W.stat.quick||0)+1;")
# hold still while a finger is on it
rep("if(hit&&hit.cat){ P.mode='catPending'; P.cat=hit.cat;", "if(hit&&hit.cat){ P.mode='catPending'; P.cat=hit.cat; hit.cat.held=true;")
rep("  if(c.carried){ c.speed=0; c.holdT+=dt;", "  if(c.held&&!(P.mode==='catPending'&&P.cat===c))c.held=false;\n  if(c.held&&!c.carried){ c.speed=0; return; }\n  if(c.carried){ c.speed=0; c.holdT+=dt;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
