"""v192: events wait for petting to finish. While the player is petting, carrying or butt-tapping (and for 4 s after),
no stray is dropped off (the person kneels at the gate with the box until then), and no new-cat card, card, postcard,
tip, family visit or runaway starts.
Butt taps: after the first tap of a round, taps give less and less: 20 of them add 3 love in total, then nothing more
until 10 s pass with no taps."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# --- petting in progress (or just ended)
rep("let uiOffT=-99, uiWas=false; const UI_GAP=4;\n",
    "let uiOffT=-99, uiWas=false; const UI_GAP=4, PET_GAP=4;\n"
    "function petRecent(){ if(['stroke','catPending','carry'].includes(P.mode))return true; const t=W.time-PET_GAP; return W.cats.some(c=>(c.lastStroke??-99)>t||(c.buttAnimT??-99)>t||c.carried); } // petting, carrying or butt taps in the last 4 s\n")
# meet cards
rep("&&!lessonBusy()&&!tutAny()&&uiGapOk())nextMeet(); }", "&&!lessonBusy()&&!tutAny()&&uiGapOk()&&!petRecent())nextMeet(); }")
rep("&&!lessonBusy()&&!tutAny()&&gapOk)nextMeet();", "&&!lessonBusy()&&!tutAny()&&gapOk&&!petRecent())nextMeet();")
# cards and postcards
rep("function showCard(fn){ if(!$('#modal').hidden||cam.meet||cardQ.length||!uiGapOk()){",
    "function showCard(fn){ if(!$('#modal').hidden||cam.meet||cardQ.length||!uiGapOk()||petRecent()){")
rep("if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused&&uiGapOk()){",
    "if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused&&uiGapOk()&&!petRecent()){")
rep("&&!W.paused&&!tutQuiet()&&uiGapOk()){", "&&!W.paused&&!tutQuiet()&&uiGapOk()&&!petRecent()){")
# tips
rep("if(!tips.cur){ if(busy||!W.stat.brushTut||curHint||hintGap>0||!uiGapOk())return;",
    "if(!tips.cur){ if(busy||!W.stat.brushTut||curHint||hintGap>0||!uiGapOk()||petRecent())return;")
# events: stray drop-off, family visit, runaway
rep("function calmHold(){ return cardUp()||playerBusy()||", "function calmHold(){ return cardUp()||playerBusy()||petRecent()||")
rep("function famHold(){ return !uiGapOk()||", "function famHold(){ return !uiGapOk()||petRecent()||")
rep("if(!((firstAdopt()||lessonOn())&&!D.done))D.t+=dt;", "if(!((firstAdopt()||lessonOn()||(!D.gift&&petRecent()))&&!D.done))D.t+=dt; /* the stray waits at the gate until petting ends */")

# --- butt taps: diminishing love
rep("if(c.buttLike){ const fresh=W.time-(c.buttT??-99)>8; c.buttT=W.time;",
    "if(c.buttLike){ const fresh=W.time-(c.buttT??-99)>((c.buttN||0)>=BUTT_N?10:8); c.buttT=W.time; if(fresh)c.buttN=0; else c.buttN=(c.buttN||0)+1;")
rep("else s.aff=Math.min(100,s.aff+0.4); }",
    "else if(c.buttN<=BUTT_N)s.aff=Math.min(100,s.aff+BUTT_A*BUTT_R**(c.buttN-1)); }")
rep("const SH_D=0.95, BUTT_HOLD=2.5;",
    "const BUTT_N=20, BUTT_R=0.88, BUTT_A=3*(1-BUTT_R)/(1-BUTT_R**BUTT_N); // 20 follow-up taps add 3 love in all, each less than the last; then none until 10 s without taps\n"
    "const SH_D=0.95, BUTT_HOLD=2.5;")
open(P, 'w', encoding='utf-8').write(s)
print('v192 applied')
