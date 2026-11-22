"""v32: a runaway walking back home can be picked up (and carried straight into the meadow)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function startCarry(c){ $('#ring').hidden=true; if(c.away>0||",
    "function startCarry(c){ $('#ring').hidden=true; if(c.state==='path'&&c.pathEnd==='home'&&!c.leaving&&!c.away){ c.path=null; c.pathEnd=null; c.outside=false; setState(c,'idle',1); if(W.runaway&&W.runaway.c===c)W.runaway=null; } if(c.away>0||")
open(P, 'w', encoding='utf-8').write(s); print('ok')
