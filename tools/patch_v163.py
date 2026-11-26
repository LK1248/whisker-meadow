"""v163: the slow-blink lesson is modal.
Before, during the lesson the cat could still be stroked or picked up (picking it up quietly ended the lesson), and
only the boop moved it on. Now the lesson cat only takes taps (the boop that answers its blink): dragging on it does
nothing and holding it doesn't lift it. Other cats, tools and buttons were already locked; panning still works and
the camera glides back as in the other lessons."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  if(bt.c)return {cats:[bt.c],tools:[]};", "  if(bt.c)return {cats:[bt.c],tools:[],tapOnly:true,noCarry:true};")
rep("  if(P.mode==='catPending'&&!P.moved&&(W.tool==='hand'||W.tool==='brush')){ const e=",
    "  if(P.mode==='catPending'&&!P.moved&&(W.tool==='hand'||W.tool==='brush')&&!(tutLock()||{}).noCarry){ const e=")
open(P, 'w', encoding='utf-8').write(s)
print('v163 applied')
