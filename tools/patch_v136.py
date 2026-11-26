"""v136: the stray (meet) window no longer interrupts the slow-blink, pair or brush lessons. No new stray is
dropped off while one of them runs, and a stray that arrives anyway (car already on its way) waits: its window
opens once the lesson ends."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function strayHold(){ return calmHold()||", "function lessonBusy(){ return !!(bt.c||pl.a||br.c); }\nfunction strayHold(){ return calmHold()||lessonBusy()||")
rep("meetQ.push({c,origin,parents}); if(!cam.meet&&!playerBusy()&&!cardUp())nextMeet(); }",
    "meetQ.push({c,origin,parents}); if(!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy())nextMeet(); }")
rep("if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp())nextMeet();",
    "if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy())nextMeet();")
open(P, 'w', encoding='utf-8').write(s)
print('v136 applied')
