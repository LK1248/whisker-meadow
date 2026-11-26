"""v129: petting zoom, double-tap-drag zoom, clearer pair lesson.
14 after 3s of petting the same cat the camera slowly zooms in (about 8%/s, down to a close view), zooming about the
   finger so the cat stays under it; any pan/zoom by the player (camUser) or a lesson stops it.
15 touch: tap the ground, then tap again and hold within 0.35s and drag: down zooms in, up zooms out.
17 pair lesson: either cat may be the one carried; a drop next to the other always gives the single boop heart first
   (states are cleared so the boop can't be refused); a drop that's too far restarts the pointing hand."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# 14 petting zoom
rep("function updateCamera(dt){ lessonFrame(dt);",
    """const PZ={c:null,t:0}, PZ_PLANE=new THREE.Plane(new V3(0,1,0),-0.3), PZ_V=new V3();
function petZoom(dt){ if(!dt||W.paused)return; const c=P.mode==='stroke'&&W.tool==='hand'?S.cat:petGrace(PG.c)?PG.c:null;
  if(!c||c!==PZ.c){ PZ.c=c; PZ.t=0; return; } PZ.t+=dt;
  if(PZ.t<3||P.mode!=='stroke'||camUser()||lessonOn()||cam.meet||cam.close)return;
  const goal=4.4; if(cam.want<=goal)return; const nw=Math.max(goal,cam.want*(1-0.08*dt)), k=1-nw/cam.want;
  setRay({clientX:P.hx,clientY:P.hy}); const gp=ray.ray.intersectPlane(PZ_PLANE,PZ_V); if(gp){ cam.target.x+=(gp.x-cam.target.x)*k; cam.target.z+=(gp.z-cam.target.z)*k; clampTarget(); }
  cam.want=nw; cam.dist=Math.min(cam.dist,cam.want+0.05); }
function updateCamera(dt){ lessonFrame(dt); petZoom(dt);""")
# 15 double-tap-hold-drag zoom (touch, from the ground)
rep("  if(petGrace(PG.c)&&(!hit||(hit.cat&&hit.cat!==PG.c))&&nearPet(PG.c,e))hit={cat:PG.c,zone:'back'};",
    "  if(petGrace(PG.c)&&(!hit||(hit.cat&&hit.cat!==PG.c))&&nearPet(PG.c,e))hit={cat:PG.c,zone:'back'};\n  if(e.pointerType!=='mouse'&&!hit&&performance.now()-(P.tapT??-1e9)<350&&Math.hypot(e.clientX-P.tapX,e.clientY-P.tapY)<50){ P.tapT=-1e9; P.mode='dzoom'; P.dz0=e.clientY; P.dzW=cam.want; rec('dzoom',''); return; }")
rep("  if(P.mode==='pinch'){ if(P.pointers.size<2)return; const [a,b]=[...P.pointers.values()];",
    "  if(P.mode==='dzoom'){ cam.want=clamp(P.dzW*Math.exp((P.dz0-e.clientY)*0.006),3.2,LV().zoom*1.3); cam.userT=W.time; return; }\n  if(P.mode==='pinch'){ if(P.pointers.size<2)return; const [a,b]=[...P.pointers.values()];")
rep("  if(P.mode==='pinch'){ if(P.pointers.size===0)P.mode=null; handVis(); return; }\n",
    "  if(P.mode==='pinch'){ if(P.pointers.size===0)P.mode=null; handVis(); return; }\n  if(P.mode==='pan'&&!P.moved&&e.pointerType!=='mouse'){ P.tapT=performance.now(); P.tapX=e.clientX; P.tapY=e.clientY; }\n")
# 17 pair lesson
rep("    const o=d===a?b:null;\n    if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){ pl.stage='watch'; pl.t=0; $('#ghost').hidden=true; if(d.state!=='boop'&&canBoop(d)&&canBoop(o)){ d.boopCD=o.boopCD=0; boop(d,o); } updatePairTut(0); return; } }",
    "    const o=d===a?b:d===b?a:null;\n    if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){ pl.stage='watch'; pl.t=0; $('#ghost').hidden=true; if(d.state!=='boop'&&o.state!=='boop'&&!o.carried){ d.boopCD=o.boopCD=0; d.petT=o.petT=0; boop(d,o); } updatePairTut(0); return; }\n    pl.t=0; /* dropped too far (or another cat): the pointing hand starts over */ }")
open(P, 'w', encoding='utf-8').write(s)
print('v129 applied')
