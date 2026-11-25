"""v122: petting grace. When a finger lifts off a cat mid-pet, that cat keeps the focus for half a second:
the purr stays at full volume, the ring stays up and its progress keeps creeping (slowly), and a new touch
near where the finger lifted goes back to the same cat. So players who stroke one way, lift and stroke again
get one continuous pet."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
# grace state + helper, next to handOn; the purr counts as hand-on during grace
rep("function handOn(c){ return (P.mode==='stroke'&&S.cat===c)||",
    "const PG={c:null,until:-1,x:0,y:0}, PG_T=0.5; // pet grace: focus outlives a lifted finger by half a second\n"
    "function petGrace(c){ return !!c&&PG.c===c&&!P.mode&&W.time<PG.until&&W.tool==='hand'&&!c.carried&&!c.leaving&&!c.outside&&!(c.away>0)&&!(c.leaveT>0); }\n"
    "function handOn(c){ return petGrace(c)||(P.mode==='stroke'&&S.cat===c)||")
# lifting the finger mid-pet starts the grace
rep("function endPointer(e){ S.lock=null;",
    "function endPointer(e){ S.lock=null; const petC=P.mode==='stroke'&&W.tool==='hand'?S.cat:null;")
rep("  else if(P.mode==='wand')wandUp(e);\n  S.cat=null; P.mode=null; handVis();",
    "  else if(P.mode==='wand')wandUp(e);\n  if(petC){ PG.c=petC; PG.until=W.time+PG_T; PG.x=P.hx; PG.y=P.hy; }\n  S.cat=null; P.mode=null; handVis();")
# a new touch during the grace, near where the finger lifted, goes back to the same cat
rep("  if(pl.a&&pl.stage==='carry'&&hit&&hit.cat!==pl.a)hit=null;",
    "  if(petGrace(PG.c)&&(!hit||(hit.cat&&hit.cat!==PG.c))&&Math.hypot(e.clientX-PG.x,e.clientY-PG.y)<(e.pointerType==='mouse'?90:140))hit={cat:PG.c,zone:'back'};\n"
    "  if(pl.a&&pl.stage==='carry'&&hit&&hit.cat!==pl.a)hit=null;")
# during the grace the ring progress creeps on slowly (never completes a stroke by itself)
rep("function updatePetIdle(dt){ if(W.tool!=='hand'||P.mode!=='stroke'||!S.cat)return; const c=S.cat;",
    "function updatePetIdle(dt){ if(petGrace(PG.c)){ const g=PG.c; if(g.petProg>0)g.petProg=Math.min(0.97,g.petProg+dt*PET_RATE*0.15); g.petLast=W.time; g.petT=Math.max(g.petT,1); }\n"
    "  if(W.tool!=='hand'||P.mode!=='stroke'||!S.cat)return; const c=S.cat;")
# the ring stays on the graced cat
rep("if(P.mode==='stroke'&&S.cat)c=S.cat; else if(P.mode==='catPending')c=P.cat; else if(",
    "if(P.mode==='stroke'&&S.cat)c=S.cat; else if(P.mode==='catPending')c=P.cat; else if(petGrace(PG.c))c=PG.c; else if(")
open(P, 'w', encoding='utf-8').write(s); print('ok')
