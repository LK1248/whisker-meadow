"""v62: tips (butt tap, belly, fleas) and guided hints (wand, brush, shop...) never show at the same time.
Each waits for the other to finish; a short gap follows a tip before the next hint."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("hintGap-=dt; if(hintGap>0||!W.hints||!W.started||W.paused)return;",
    "hintGap-=dt; if(hintGap>0||!W.hints||!W.started||W.paused||tips.cur)return;")
rep("if(!tips.cur){ if(busy||!W.stat.pairDone)return;",
    "if(!tips.cur){ if(busy||!W.stat.pairDone||curHint)return;")
rep("tips.cur=null; $('#tip').hidden=true; }",
    "tips.cur=null; $('#tip').hidden=true; hintGap=Math.max(hintGap,3); }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
