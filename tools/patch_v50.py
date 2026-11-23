"""v50: a cleaner tutorial stage.
- The quiet tutorial stage now runs until the brush lesson (the last one) is over, not just until the pair lesson.
  Before, the ~45s gap between the pair and brush lessons let families, strays, runaways, rain, hints and tips start,
  which then delayed or cut into the brush lesson. The gap is shorter now (25s) and stays quiet. Safety cap: 8 minutes.
- The cat fair is closed during the tutorial stage: no fair button on the cat tag, no fair star icon, no fair hint.
- Daytime holds during the tutorial stage, so night doesn't fall in the middle of a lesson.
- Badge, goal and sanctuary-star toasts wait while a lesson is on screen and pop once it ends."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# quiet until the brush lesson is done (it is the last opening lesson)
rep("// quiet while a lesson runs, and until the three opening lessons are through\nfunction tutQuiet(){ return !!(W.started&&(lessonOn()||(!W.stat.pairDone&&W.time<360))); }",
    "// quiet while a lesson runs, and until the opening lessons (pet, blink, pair, brush) are through\nfunction tutQuiet(){ return !!(W.started&&(lessonOn()||(!W.stat.brushTut&&W.time<480))); }")
# shorter breather between the pair and brush lessons
rep("W.time>(W.stat.pairDoneT!=null?W.stat.pairDoneT+45:200)", "W.time>(W.stat.pairDoneT!=null?W.stat.pairDoneT+25:200)")
# no fair during the tutorial stage
rep("function showReady(c){ const s=c.s; return !(W.family", "function showReady(c){ const s=c.s; return !tutQuiet()&&!(W.family")
# keep it daytime through the tutorial
rep("function applySky(dt){ if(W.dayOn)dayT=", "function applySky(dt){ if(W.dayOn&&!tutQuiet())dayT=")
# reward toasts wait for the lesson to end
rep("checkCollection(); updateStars(); updateAch(); updateGoals(); hud(); }",
    "checkCollection(); if(!lessonOn()){ updateStars(); updateAch(); updateGoals(); } hud(); }")
rep("window.__wm={Snd,", "window.__wm={Snd,showReady,updateTag,lessonOn,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
