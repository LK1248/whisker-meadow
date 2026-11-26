"""v138: the brush touches the world exactly like the hand; only swiping on a cat differs (pet vs brush).
- Press and hold a cat with the brush: the pick-up ring fills and the cat is picked up, as with the hand.
- Holding the brush no longer counts as "busy" for strays, families and meet windows (as with the hand)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(P.mode==='catPending'&&!P.moved&&W.tool==='hand'){ const e=performance.now()-P.t0, r=$('#ring');",
    "if(P.mode==='catPending'&&!P.moved&&(W.tool==='hand'||W.tool==='brush')){ const e=performance.now()-P.t0, r=$('#ring');")
rep("function playerBusy(){ if(W.time-(W.lastInput||-99)>=6)return false; return W.tool!=='hand'||",
    "function playerBusy(){ if(W.time-(W.lastInput||-99)>=6)return false; return (W.tool!=='hand'&&W.tool!=='brush')||")
open(P, 'w', encoding='utf-8').write(s)
print('v138 applied')
