"""v169: the newborn family heart floats higher.
It used to sit on the top edge of the welcome card. Now it is centred in the space between the top of the card and
the top of the screen."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#mFam{flex:none;margin-bottom:-14px;z-index:1;pointer-events:none}",
    "#mFam{flex:none;z-index:1;pointer-events:none}#meet.fam{top:0;justify-content:flex-end;pointer-events:none}#meet.fam .sheet{pointer-events:auto}"
    "#meet.fam #mFam{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}")
rep("fe.hidden=!im; if(im)", "fe.hidden=!im; $('#meet').classList.toggle('fam',!!im); if(im)")
# a long origin line (parents + coat + trait) wraps as whole pieces, centred, instead of squeezing each piece
rep("#meet .org{display:flex;justify-content:center;align-items:center;gap:6px;", "#meet .org{display:flex;flex-wrap:wrap;text-align:center;justify-content:center;align-items:center;gap:2px 6px;")
open(P, 'w', encoding='utf-8').write(s)
print('v169 applied')
