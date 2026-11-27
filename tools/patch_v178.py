"""v178: a cat that dislikes butt taps complains on every tap.
Each tap gets one meow, pitched a little differently each time; if you keep going the complaints get louder and lower
(over a 5 s streak), then the cat walks off as before. The overstimulation grumble doesn't double up on the same tap.
A cat that likes butt taps stays quiet and purrs (v177)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(W.time-(c.buttMeowT??-99)>6){ c.buttMeowT=W.time; Snd.meow(0.88,0.6); }",
    "{ const n=Math.min(4,c.buttAng=(W.time-(c.buttMeowT??-99)<5?(c.buttAng||0)+1:0)); c.buttMeowT=W.time; Snd.meow(0.92-0.045*n+rand(-0.04,0.04),0.55+0.11*n); } /* complains every tap, louder and lower if you keep going */")
open(P, 'w', encoding='utf-8').write(s)
print('v178 applied')
