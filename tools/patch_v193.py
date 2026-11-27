"""v193: the slow zoom-in on a petted cat keeps going when the finger lifts between strokes, as long as the next
stroke comes within the petting window (2 strokes at the cat's tempo after the finger lifts, at least 1.5 s). Lifting no longer restarts
the 3 s wait before the zoom begins."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function petZoom(dt){ if(!dt||W.paused)return; const c=P.mode==='stroke'&&W.tool==='hand'?S.cat:petGrace(PG.c)?PG.c:null;\n"
    "  if(!c||c!==PZ.c){ PZ.c=c; PZ.t=0; return; } PZ.t+=dt;\n"
    "  if(PZ.t<3||P.mode!=='stroke'||camUser()||lessonOn()||cam.meet||cam.close)return;",
    "function petWin(c){ return !!c&&W.tool==='hand'&&!c.carried&&!c.leaving&&!c.outside&&!(c.away>0)&&W.time-(PZ.touch??-99)<Math.max(1.5,2*strokeT(c)); } // finger up, but still in the petting rhythm\n"
    "function petZoom(dt){ if(!dt||W.paused)return; const up=!P.mode||P.mode==='none';\n"
    "  const c=P.mode==='stroke'&&W.tool==='hand'?S.cat:(up||(P.mode==='catPending'&&P.cat===PZ.c))&&petWin(PZ.c)?PZ.c:petGrace(PG.c)?PG.c:null;\n"
    "  if(P.mode==='stroke')PZ.touch=W.time; if(!c||c!==PZ.c){ PZ.c=c; PZ.t=0; return; } PZ.t+=dt;\n"
    "  if(PZ.t<3||!(P.mode==='stroke'||up||P.mode==='catPending')||camUser()||lessonOn()||cam.meet||cam.close)return;")
open(P, 'w', encoding='utf-8').write(s)
print('v193 applied')
