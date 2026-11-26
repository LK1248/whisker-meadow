"""v160: the flea tip comes back if a cat keeps its fleas.
If a cat has had fleas for over a minute (the player hasn't brushed them off), the flea tip (hand + brush glow on
that cat) shows again, at most once every 90 s. The tip stays up until the fleas are gone; once it closes, that cat's flea clock starts over."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  if(c.fleas&&s.groom>=40)c.fleas=0;\n",
    "  if(c.fleas&&s.groom>=40)c.fleas=0;\n  c.fleaT=c.fleas?(c.fleaT||0)+dt:0; // how long this cat has had fleas\n")
rep("const flea=!W.stat.fleaTip&&active().find(c=>c.fleas&&",
    "const flea=active().find(c=>c.fleas&&(!W.stat.fleaTip||(c.fleaT>60&&W.time>(W.stat.fleaAgain||0)))&&")
rep("showTip('flea',flea,FLEA_TIP,8,false); return; }",
    "flea.fleaT=0; W.stat.fleaAgain=W.time+90; showTip('flea',flea,FLEA_TIP,8,false); return; }")
# the flea clock also restarts when the tip goes away (it stays up while the fleas remain), so a repeat needs a full
# minute of fleas with no tip on screen
rep("if(tips.cur.kind==='flea')$('[data-tool=brush]').classList.remove('tutGlow','nudge');",
    "if(tips.cur.kind==='flea'){ $('[data-tool=brush]').classList.remove('tutGlow','nudge'); tips.cur.c.fleaT=0; }")
open(P, 'w', encoding='utf-8').write(s)
print('v160 applied')
