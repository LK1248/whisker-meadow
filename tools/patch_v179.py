"""v179: a low-love cat (love under 50, same line as over-petting) that dislikes butt taps scratches after the second
unwanted tap (hiss, claw on the hand, "Ouch!", counts toward the Band-Aid Club badge), then walks away.
Cats with more love still just walk off."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.buttNo>=2){ c.buttNo=0; walkAway(c,false); c.leaveT=1.2; }",
    "if(c.buttNo>=2){ c.buttNo=0; if(s.aff<50){ c.snap=0.4; c.bat=0.5; s.aff=Math.max(0,s.aff-3); handScratch(c); setTimeout(()=>{ walkAway(c,false); c.leaveT=1.2; },300); } else { walkAway(c,false); c.leaveT=1.2; } } /* low love: a scratch first */")
open(P, 'w', encoding='utf-8').write(s)
print('v179 applied')
