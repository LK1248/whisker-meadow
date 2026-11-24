"""v77: the completed-stroke heart is bigger (26px -> 36px)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("#beat .bHeart{width:26px;height:26px;", "#beat .bHeart{width:36px;height:36px;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
