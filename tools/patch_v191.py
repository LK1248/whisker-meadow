"""v191: butt taps give a bit more love and the chest dips less; cards, meet cards, tips, lessons and hints
never come back to back: each waits until 4 s after the last one closed."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# --- butt taps: +2.5 love for a fresh round (was +1), +0.4 for each further tap
rep("if(fresh){ s.aff=Math.min(100,s.aff+1); spawnFx('h',c.g.position.clone().setY(.9),1); W.stat.butt++; } }",
    "if(fresh){ s.aff=Math.min(100,s.aff+2.5); spawnFx('h',c.g.position.clone().setY(.9),1); W.stat.butt++; } else s.aff=Math.min(100,s.aff+0.4); }")
# --- softer pose: less forward pitch, shoulders lower only a little
rep("rx=lerp(rx,0.44,k); coreY=lerp(coreY,0.41,k); hx=lerp(hx,0.08,k); legA=legA.map((v,i)=>lerp(v,i<2?-0.78:-0.46,k));",
    "rx=lerp(rx,0.2,k); coreY=lerp(coreY,0.44,k); hx=lerp(hx,0.05,k); legA=legA.map((v,i)=>lerp(v,i<2?-0.5:-0.4,k));")

# --- 4 s gap between cards / tutorials (real seconds; sampled every frame, even while the game is paused)
rep("requestAnimationFrame(frame); const dt=Math.min(0.05,(now-last)/1000);", "requestAnimationFrame(frame); uiGapOk(); const dt=Math.min(0.05,(now-last)/1000);")
rep("function playerBusy(){",
    "let uiOffT=-99, uiWas=false; const UI_GAP=4;\n"
    "function uiUp(){ return !$('#modal').hidden||!!cam.meet||!$('#meet').hidden||lessonOn()||!!tips.cur||!!curHint; }\n"
    "function uiGapOk(){ const up=uiUp(), now=performance.now()/1000; if(uiWas&&!up)uiOffT=now; uiWas=up; return !up&&now-uiOffT>=UI_GAP; } // nothing up, and the last one closed 4 s ago\n"
    "function playerBusy(){")
# meet cards
rep("meetQ.push({c,origin,parents,kits}); if(!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny())nextMeet(); }",
    "meetQ.push({c,origin,parents,kits}); if(!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny()&&uiGapOk())nextMeet(); }")
rep("function updateHints(dt){ tutLockTick(); needTick(dt); calmTick(); if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny())nextMeet();",
    "function updateHints(dt){ tutLockTick(); needTick(dt); calmTick(); const gapOk=uiGapOk(); if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny()&&gapOk)nextMeet();")
rep("$('#mOk').onclick=nextMeet;", "$('#mOk').onclick=()=>{ const q=meetQ.splice(0); nextMeet(); meetQ.push(...q); }; // close; any queued meet waits for the gap")
# modal cards and postcards
rep("function showCard(fn){ if(!$('#modal').hidden||cam.meet||cardQ.length){",
    "function showCard(fn){ if(!$('#modal').hidden||cam.meet||cardQ.length||!uiGapOk()){")
rep("if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused){",
    "if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused&&uiGapOk()){")
rep("if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!cardQ.length&&!W.paused&&!tutQuiet()){",
    "if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!cardQ.length&&!W.paused&&!tutQuiet()&&uiGapOk()){")
# tips (flea, butt) and hints; hints also let queued cards go first
rep("if(!tips.cur){ if(busy||!W.stat.brushTut||curHint||hintGap>0)return;",
    "if(!tips.cur){ if(busy||!W.stat.brushTut||curHint||hintGap>0||!uiGapOk())return;")
rep("hintGap-=dt; if(hintGap>0||!W.hints||!W.started||W.paused||tips.cur)return;",
    "hintGap-=dt; if(hintGap>0||!W.hints||!W.started||W.paused||tips.cur||!gapOk||meetQ.length||cardQ.length)return;")
# lessons
rep("if(brushReady())startBrushTut();", "if(brushReady()&&uiGapOk())startBrushTut();")
rep("if(pairReady())startPairTut();", "if(pairReady()&&uiGapOk())startPairTut();")
rep("function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tutLock()||evBusy()||tips.cur)return;",
    "function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tutLock()||evBusy()||tips.cur||!uiGapOk())return;")
# family arrivals wait too
rep("function famHold(){ return cardUp()||", "function famHold(){ return !uiGapOk()||cardUp()||")
open(P, 'w', encoding='utf-8').write(s)
print('v191 applied')
