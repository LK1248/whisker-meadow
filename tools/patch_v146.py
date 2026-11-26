"""v146: a stray drop-off that arrives during a lesson (intro, slow blink, bonding/pair, brush) waits at the gate
with the box closed until the lesson is over, then lets the cat out and the usual stray flow starts."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("else if(D.stage==='drop'){ if(!(firstAdopt()&&!D.done))D.t+=dt;",
    "else if(D.stage==='drop'){ if(!((firstAdopt()||lessonOn())&&!D.done))D.t+=dt;")
open(P, 'w', encoding='utf-8').write(s)
print('v146 applied')
