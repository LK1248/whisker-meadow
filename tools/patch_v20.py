"""v20: a cat that has been offered to a family can't be sent to the fair."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function showReady(c){ const s=c.s; return c.away<=0&&", "function showReady(c){ const s=c.s; return !(W.family&&W.family.cat===c)&&c.away<=0&&")
rep("$('#tShow').onclick=()=>{ if(tag.c)enterShow(tag.c); };", "$('#tShow').onclick=()=>{ if(tag.c&&!(W.family&&W.family.cat===tag.c))enterShow(tag.c); };")
open(P, 'w', encoding='utf-8').write(s); print('ok')
