"""v119: butt taps no longer make the cat chirp on every single tap. Rapid tapping fired a chirp (or, for cats who
don't like it, an annoyed meow) per tap. Now a happy chirp sounds at most every 1.5s and an annoyed meow at most
every 2.5s; the purr, hearts and love gains are unchanged."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("c.buttT=W.time; c.purr=Math.max(c.purr,0.6); Snd.chirp();",
    "c.buttT=W.time; c.purr=Math.max(c.purr,0.6); if(W.time-(c.buttSndT??-99)>1.5){ c.buttSndT=W.time; Snd.chirp(); }")
rep("showIcon(c,'angry',1.5); Snd.meow(0.85,0.7);",
    "showIcon(c,'angry',1.5); if(W.time-(c.buttSndT??-99)>2.5){ c.buttSndT=W.time; Snd.meow(0.85,0.7); }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
