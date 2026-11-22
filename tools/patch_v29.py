"""v29: continuous petting. The pet meter fills only while your hand moves over the cat, at a comfortable pace
(~0.7 strokes/s at most); too fast = hourglass (no progress), frantic = overstimulation (scratch/leave as before).
Hold still for 6s and the cat gets bored and wanders off. Slipping off the cat's outline (e.g. circling the face)
no longer resets the stroke."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# onStroke can be told the stroke was on-beat
rep("function onStroke(c,zone,frantic){", "function onStroke(c,zone,frantic,good){")
rep("  const rating=frantic||iv<(brush?0.55:1.0)*slow?'fast':", "  const rating=good?'good':frantic||iv<(brush?0.55:1.0)*slow?'fast':")

# strokeMove: hand tool = continuous meter; brief slips off the outline keep the stroke alive
rep("""  if(!h||!h.cat){ if(S.cat)finishStroke(); S.cat=null; return; }
  if(h.cat!==S.cat){ if(S.cat)finishStroke(); if(W.tool==='hand'&&!petReact(h.cat)){ S.cat=null; return; } beginStroke(h.cat,now); }
  const len=Math.hypot(dx,dy); if(len<0.5)return; const ux=dx/len, uy=dy/len;""",
"""  const len0=Math.hypot(dx,dy), dtm=Math.max(0.008,(now-(S.tm||now-16))/1000); S.tm=now; const inst=len0/dtm; S.v=S.v==null?inst:lerp(S.v,inst,0.35);
  if(!h||!h.cat){ if(W.tool==='hand'&&S.cat)return; if(S.cat)finishStroke(); S.cat=null; return; }
  if(h.cat!==S.cat){ if(S.cat)finishStroke(); if(W.tool==='hand'&&!petReact(h.cat)){ S.cat=null; return; } beginStroke(h.cat,now); }
  const len=len0; if(len<0.5)return; const ux=dx/len, uy=dy/len;
  if(W.tool==='hand'){ S.last=now; S.zones[h.zone]=(S.zones[h.zone]||0)+len; petMove(S.cat,len,h.zone); S.cat.petT=Math.max(S.cat.petT,1.5); return; }""")
rep("function finishStroke(){ if(S.cat&&S.len>=40&&W.tool!=='brush'){", "function finishStroke(){ if(S.cat&&S.len>=40&&W.tool!=='brush'&&W.tool!=='hand'){")
rep("  if(P.mode==='stroke'&&S.cat&&S.len>=40&&performance.now()-S.last>260){", "  updatePetIdle(dt);\n  if(W.tool!=='hand'&&P.mode==='stroke'&&S.cat&&S.len>=40&&performance.now()-S.last>260){")

rep("function beginStroke(c,now){", r"""// ---- continuous petting ----
function petMove(c,len,zone){
  if(c.state==='hiding'){ foundCat(c); return; }
  if(c.away>0||c.carried||c.leaveT>0||c.outside||c.leaving||['boop','path','greet','bye'].includes(c.state))return;
  c.petT=3; tagFor(c,3); if(!['flop','sleep','pet','eat','litter','perch','shelter'].includes(c.state))setState(c,'pet');
  if(c.state==='sleep'){ setState(c,'pet'); c.slowBlink=1.9; c.purr=Math.max(c.purr,0.4); }
  if(zone==='tail'){ c.over+=len/260; c.flick=0.6; if(c.over>=1.5)showIcon(c,'angry',1.2); return; }
  const D=2.5*Math.max(60,Math.min(400,catScreenH(c))), vMax=D*0.7*(c.trait==='shy'?0.87:1), v=S.v||0, now=W.time;
  let gain=0;
  if(v>vMax*4.5){ c.over+=len/D*0.9; if(now>(c.hgT||0)){ c.hgT=now+0.9; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),true); slowNag.n++; } }
  else if(v>vMax*2.2){ c.over+=len/D*0.2; if(now>(c.hgT||0)){ c.hgT=now+1.1; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),false); slowNag.n++; } }
  else gain=len/D*Math.min(1,vMax/Math.max(1,v));
  if(slowNag.n>=4&&now>slowNag.next){ slowNag.n=0; slowNag.next=now+40; showSlow(); }
  if(gain>0){ c.petProg=(c.petProg||0)+gain; c.petIdle=0; c.purr=Math.max(c.purr,0.15);
    if(c.petProg>=1){ c.petProg=0; let z='back',best=0; for(const k in S.zones)if(S.zones[k]>best){best=S.zones[k];z=k;} S.zones={}; onStroke(c,z,false,true); } } }
// hand resting still on a cat: 6s of patience, then it wanders off, bored
function updatePetIdle(dt){ if(W.tool!=='hand'||P.mode!=='stroke'||!S.cat)return; const c=S.cat;
  if(performance.now()-(S.last||0)>120){ S.v=(S.v||0)*Math.pow(0.02,dt); c.petIdle=(c.petIdle||0)+dt; }
  if(c.petIdle>6&&!intro.c&&!bt.c&&!pl.a&&!br.c&&!['flop','sleep'].includes(c.state)){ c.petIdle=0; c.petProg=0; showIcon(c,'bored',1.6); walkAway(c,false); c.leaveT=1.2; S.cat=null; P.mode='none'; } }
function beginStroke(c,now){""")

# the ring shows the pet meter (movement), not elapsed time
rep("  const slow=c.trait==='shy'?1.15:1, g0=(W.tool==='brush'?0.8:1.55)*slow, t=W.time-c.lastStroke, p=t>7?1:clamp(t/g0,0,1);",
    "  const fresh=W.time-c.lastStroke<0.45, p=fresh?1:clamp(c.petProg||0,0,1);")
rep("let gOp=0; if(c.petT>0&&handOn(c)&&!c.carried&&W.tool!=='brush'){ const el=W.time-c.lastStroke, g0=(W.tool==='brush'?0.8:1.55)*(c.trait==='shy'?1.15:1); gOp=el<g0?0.05+0.2*(el/g0):el<=7?0.6+0.15*Math.sin(t*6):0.25; }",
    "let gOp=0; if(c.petT>0&&handOn(c)&&!c.carried&&W.tool!=='brush'){ gOp=W.time-c.lastStroke<0.45?0.75:0.08+0.4*clamp(c.petProg||0,0,1); }")
# wording
rep("label:'Stroke, then wait for ✓'", "label:'Stroke gently'")
rep("""A ring by your hand fills in about 1.5 seconds (longer for shy cats). Stroke again when it turns <b>green with a ✓</b>.</li><li>"Purr!" = perfect. An hourglass = slow down (a shaking one = way too fast).</li>""",
    """Keep stroking slowly: the ring by your hand fills while your hand moves over the cat, and every full ring is a happy purr. Holding still doesn't fill it, and after a few seconds of stillness the cat gets bored and wanders off.</li><li>An hourglass = slow down (a shaking one = way too fast; too much of that and the cat has had enough).</li>""")
rep("window.__wm={animateCat,", "window.__wm={animateCat,petMove,S,")
rep('function beginStroke(c,now){ S.cat=c;','function beginStroke(c,now){ S.v=null; S.tm=null; S.cat=c;')
open(P, 'w', encoding='utf-8').write(s); print('ok')
