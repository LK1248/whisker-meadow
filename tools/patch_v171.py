"""v171: the newborn family heart is 6% bigger (the photo inside scales with it)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#mFam img{display:block;width:min(240px,56vw,30vh);", "#mFam img{display:block;width:min(254px,59.4vw,31.8vh);")
open(P, 'w', encoding='utf-8').write(s)
print('v171 applied')
