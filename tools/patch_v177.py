"""v177: quieter butt taps.
- A cat enjoying butt taps no longer head-bumps (with its chirp) during the taps and for 3 s after; it just purrs.
- A cat that dislikes them meows at most once every 6 s (not on every tap), and the overstimulation grumble meow doesn't
  stack on top of it."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.petT>0&&!c.carried&&s.aff>=45&&c.hbCD<=0&&W.time-c.lastStroke>0.8&&handOn(c)&&Math.random()<dt*1.8){",
    "if(c.petT>0&&!c.carried&&s.aff>=45&&c.hbCD<=0&&W.time-c.lastStroke>0.8&&W.time-(c.buttAnimT??-99)>3&&handOn(c)&&Math.random()<dt*1.8){ /* no head bumps (chirps) during butt taps */")
rep("if(c.buttNo<=2)Snd.meow(c.buttNo>1?0.8:0.88,0.6);",
    "if(W.time-(c.buttMeowT??-99)>6){ c.buttMeowT=W.time; Snd.meow(0.88,0.6); } c.grumbleT=Math.max(c.grumbleT||0,W.time+2.5); /* one meow per sequence, no grumble on top */")
open(P, 'w', encoding='utf-8').write(s)
print('v177 applied')
