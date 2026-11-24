"""v103: tips (butt tap, fleas, belly) no longer barge into chained lessons. They wait out the short gap between one
hint and the next (e.g. 'pick the wand' -> 'sway the wand'), and the butt-tap tip only starts while the hand is the
current tool, so it never snatches the wand or brush away mid-play."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("if(!tips.cur){ if(busy||!W.stat.pairDone||curHint)return;", "if(!tips.cur){ if(busy||!W.stat.pairDone||curHint||hintGap>0)return;")
rep("if(!W.stat.buttTip&&W.time>240&&!W.stat.butt){", "if(!W.stat.buttTip&&W.time>240&&!W.stat.butt&&W.tool==='hand'){")
open(P, 'w', encoding='utf-8').write(s); print('ok')
