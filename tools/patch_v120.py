"""v120: the fair result no longer barges into a lesson. The blink/bonding lessons counted 'after the first fair' from
when the cat LEFT for the fair, so the bonding lesson could start while it was away and the award banner then popped
up over it. Now (1) those lessons wait until a fair result has been seen and no cat is still at the fair, and (2) a cat
whose fair ends while any lesson or forced step is running waits at the fair until it's over."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function earlyDone(){ return (W.stat.shows||0)>0||!!W.stat.fairSkip||W.time>600; }",
    "function earlyDone(){ return ((W.stat.showsBack||0)>0||!!W.stat.fairSkip||W.time>600)&&!W.cats.some(c=>c.away>0); }")
rep("if(c.away>0){ c.away-=dt; if(c.away<=0)returnFromShow(c); return; }",
    "if(c.away>0){ c.away-=dt; if(c.away<=0){ if(lessonOn()||tutLock())c.away=0.5; /* wait at the fair until the lesson is over */ else returnFromShow(c); } return; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
