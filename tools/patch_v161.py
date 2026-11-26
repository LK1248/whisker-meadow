"""v161: the flea tip only comes back for a player who hasn't been brushing fleas.
A repeat now needs both: one cat has had fleas for over a minute, and no flea has been brushed off any cat in the
last 2 minutes. A player who knows about fleas and is brushing them (or chooses to leave a cat for later) isn't
nagged; the repeat is also spaced at least 2 minutes apart (was 90 s)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.fleas){ c.fleas=Math.max(0,c.fleas-2);", "if(c.fleas){ c.fleas=Math.max(0,c.fleas-2); W.stat.fleaBrushT=W.time;")
rep("(!W.stat.fleaTip||(c.fleaT>60&&W.time>(W.stat.fleaAgain||0)))",
    "(!W.stat.fleaTip||(c.fleaT>60&&W.time>(W.stat.fleaAgain||0)&&W.time-(W.stat.fleaBrushT??-999)>120))")
rep("W.stat.fleaAgain=W.time+90;", "W.stat.fleaAgain=W.time+120;")
open(P, 'w', encoding='utf-8').write(s)
print('v161 applied')
