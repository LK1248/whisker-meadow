"""v15: adopting families don't come by in the dead of night (dusk and early evening are fine)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "if(W.cats.some(readyHome)&&!W.runaway){ visitT-=dt; if(visitT<=0)spawnFamily(); }"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55){ visitT-=dt; if(visitT<=0)spawnFamily(); }")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
