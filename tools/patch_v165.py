"""v165: no more slow-blink hint, only the slow-blink lesson.
The small floating hint (eyes + heart over a cat that blinked) is gone: a slow blink is easy to miss while cats bustle
about. The slow-blink lesson, which stops everything and walks the player through it, is unchanged."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  {id:'blink',when:()=>W.cats.some(c=>c.blinkBackT>0.5&&c.away<=0),at:()=>headOf(W.cats.find(c=>c.blinkBackT>0)),g:'tap',label:()=>H_EYES+hIco(H_HEART,24),done:()=>W.stat.blinkBack>0,auto:9,again:true},\n", "")
open(P, 'w', encoding='utf-8').write(s)
print('v165 applied')
