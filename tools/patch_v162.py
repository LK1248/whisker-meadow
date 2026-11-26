"""v162: fleas are a little contagious, and a cat with fleas can't go to the fair.
- When two cats start playing (a romp) and one has fleas, the other catches them half the time if its groom is
  below 60. Caught fleas don't lower groom, and they don't vanish on their own as the coat improves: they stay until
  they're brushed off.
- Any cat with fleas can't enter a fair (no fair star or button) until its fleas are brushed off."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function startRomp(a,b){ ",
    "function startRomp(a,b){ for(const [x,y] of [[a,b],[b,a]])if(x.fleas&&!y.fleas&&y.s.groom<60&&Math.random()<0.5){ y.fleas=3+Math.floor(rand(0,3)); y.fleaCaught=true; } // fleas can hop over while playing\n  ")
rep("  if(c.fleas&&s.groom>=40)c.fleas=0;\n",
    "  if(c.fleas&&s.groom>=40&&!c.fleaCaught)c.fleas=0; if(!c.fleas)c.fleaCaught=false; // caught fleas stay until brushed off\n")
rep("&&s.groom>=GROOM_FAIR; }", "&&s.groom>=GROOM_FAIR&&!c.fleas; }")
open(P, 'w', encoding='utf-8').write(s)
print('v162 applied')
