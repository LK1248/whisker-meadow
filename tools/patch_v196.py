"""v196: the slow zoom-in while petting also happens while brushing (same 3 s start, same lift window)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function petWin(c){ return !!c&&W.tool==='hand'&&", "function petWin(c){ return !!c&&(W.tool==='hand'||W.tool==='brush')&&")
rep("const c=P.mode==='stroke'&&W.tool==='hand'?S.cat:(up||", "const c=P.mode==='stroke'&&(W.tool==='hand'||W.tool==='brush')?S.cat:(up||")
open(P, 'w', encoding='utf-8').write(s)
print('v196 applied')
