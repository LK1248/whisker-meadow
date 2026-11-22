"""v35: the brush lesson keeps the tool dock live (and lit) so the player can actually pick the brush."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("body.intro .dock,body.intro #hud,body.intro .top{opacity:.25;pointer-events:none}",
    "body.intro .dock,body.intro #hud,body.intro .top{opacity:.25;pointer-events:none}body.intro.tools .dock{opacity:1;pointer-events:auto;z-index:7}")
rep("hintDone.add('brush2'); tag.c=null;\n  document.body.classList.add('intro');",
    "hintDone.add('brush2'); tag.c=null;\n  document.body.classList.add('intro','tools');")
rep("W.stat.brushTut=1; cam.want=Math.max(br.want||0,LV().zoom*0.75); document.body.classList.remove('intro');",
    "W.stat.brushTut=1; cam.want=Math.max(br.want||0,LV().zoom*0.75); document.body.classList.remove('intro','tools');")
open(P, 'w', encoding='utf-8').write(s); print('ok')
