"""v81: on touch screens the hand hides while dragging the meadow (pan) or rotating; it is only there when touching
something. With a mouse the hand stays, since it is the cursor."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("P.mode!=='carry'&&P.mode!=='pinch'&&(P.type==='mouse'?P.over:P.down);",
    "P.mode!=='carry'&&P.mode!=='pinch'&&(P.type==='mouse'?P.over:P.down&&P.mode!=='pan'&&P.mode!=='rotate');")
open(P, 'w', encoding='utf-8').write(s); print('ok')
