"""v127: the camera stays the player's during lessons and tips, and each lesson frames its cats.
- Pan (drag the meadow) and pinch/wheel zoom work while a lesson, tip or forced step is running; only taps on the
  wrong things stay ignored (a tap on empty ground does nothing during a lesson).
- When a lesson/tip/forced step starts, the camera glides to frame the cats (and family) involved: centred on them,
  as close as possible while all of them fit with a margin (never closer than a comfortable single-cat view).
  If a framed cat wanders off screen it re-frames. Any pan/zoom by the player pauses all lesson camera moves for 3s.
- When the step ends, the zoom goes back to what it was (unless the player zoomed meanwhile)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# --- player camera input is remembered; lesson camera moves wait for it
rep("function zoomBy(f){ cam.want=clamp(cam.want*f,3.2,LV().zoom*1.3); }",
    "function zoomBy(f){ cam.want=clamp(cam.want*f,3.2,LV().zoom*1.3); cam.userT=W.time; }\n"
    "function camUser(){ return W.time-(cam.userT??-99)<3; } // the player moved the camera just now: lessons don't steer it")
rep("else if(P.mode==='pan'){ const p=groundAt(e,tmp); if(p&&P.moved){ cam.target.x+=P.grab.x-p.x;",
    "else if(P.mode==='pan'){ const p=groundAt(e,tmp); if(p&&P.moved){ cam.userT=W.time; cam.target.x+=P.grab.x-p.x;")
# --- pinch and pan allowed during locks
rep("  if(P.pointers.size===2&&tutLock()){ P.mode='none'; return; }\n", "")
rep("P.start={x:e.clientX,y:e.clientY}; P.last={...P.start}; P.t0=performance.now(); P.moved=false; handPos(e); P.down=true;",
    "P.start={x:e.clientX,y:e.clientY}; P.last={...P.start}; P.t0=performance.now(); P.moved=false; P.lockPan=false; handPos(e); P.down=true;")
rep("if(!hit||W.tool==='wand'||W.tool==='laser'){ P.mode='none'; handVis(); return; }",
    "if(!hit||W.tool==='wand'||W.tool==='laser'){ P.mode='pan'; P.lockPan=true; groundAt(e,P.grab); handVis(); return; }")
rep("else if(P.mode==='pan'&&!P.moved){ if(W.collarPick)", "else if(P.mode==='pan'&&!P.moved&&P.lockPan){ /* a tap that a lesson doesn't use: nothing happens */ }\n  else if(P.mode==='pan'&&!P.moved){ if(W.collarPick)")
# --- existing lesson cameras step aside while the player steers
rep("cam.want=lerp(intro.w0,3.5,ee); cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*(0.6+2.4*ee)));",
    "if(!camUser()){ cam.want=lerp(intro.w0,3.5,ee); cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*(0.6+2.4*ee))); }")
rep("  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));\n  if(c.state!=='idle')setState(c,'idle',3);",
    "  const p=c.g.position; if(!camUser())cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));\n  if(c.state!=='idle')setState(c,'idle',3);")
rep("  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));\n",
    "  const p=c.g.position; if(!camUser())cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));\n")
rep("const mid=pa.clone().add(pb).multiplyScalar(0.5); cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));\n  { const vh=",
    "const mid=pa.clone().add(pb).multiplyScalar(0.5); if(!camUser())cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));\n  if(!camUser()){ const vh=")
rep("if(on){ if(cam.fa==null){ cam.fa=cam.want; leaveClose(false); tag.c=null; hideHint(); } cam.focus=f.cat; cam.focusT=0.3;",
    "if(on){ if(cam.fa==null){ cam.fa=cam.want; leaveClose(false); tag.c=null; hideHint(); } if(!camUser()){ cam.focus=f.cat; cam.focusT=0.3; }")
rep("function updateCamera(dt){\n  if(cam.focusT>0&&cam.focus&&!cam.meet){",
    "function updateCamera(dt){ lessonFrame(dt);\n  if(cam.focusT>0&&cam.focus&&!cam.meet&&!camUser()){")
# --- framing for steps that had none (tips, fair, first adoption) and the first moment of every lesson
FRAME = r"""
// ---- lesson framing: centre the cats a step is about, as close as fits them all ----
const LF={key:'',pts:null,glide:0,want0:null,user0:-99};
function lessonPts(){ const ok=c=>c&&c.away<=0&&!c.outside&&!c.leaving;
  if(intro.c||!W.started)return null; // the petting lesson frames itself
  if(bt.c)return ['blink',[bt.c]]; if(pl.a)return ['pair',[pl.a,pl.b]]; if(br.c)return ['brush',[br.c]];
  if(firstAdopt()&&W.family){ const f=W.family, m=(f.members||[]).filter(x=>x&&x.g).map(x=>x.g.position); const cs=W.pickHome?W.cats.filter(c=>ok(c)&&readyHome(c)).slice(0,3):f.cat?[f.cat]:[]; if(cs.length)return ['adopt',cs,m]; return null; }
  if(tips.cur&&ok(tips.cur.c))return ['tip'+tips.cur.kind,[tips.cur.c]];
  if(fairForce()==='show'){ const cs=W.cats.filter(c=>ok(c)&&showReady(c)).sort((a,b)=>dist2(a.g.position,cam.target)-dist2(b.g.position,cam.target)).slice(0,1); if(cs.length)return ['fair',cs]; }
  return null; }
function fitFor(cats,extra){ const P=cats.map(c=>c.g.position).concat(extra||[]); let x0=1e9,x1=-1e9,z0=1e9,z1=-1e9; for(const p of P){ x0=Math.min(x0,p.x); x1=Math.max(x1,p.x); z0=Math.min(z0,p.z); z1=Math.max(z1,p.z); }
  const cx=(x0+x1)/2, cz=(z0+z1)/2; let r=0; for(const p of P)r=Math.max(r,Math.hypot(p.x-cx,p.z-cz)); r+=1.0; // a cat's size plus a little room
  const vh=camera.fov*Math.PI/360, hh=Math.atan(Math.tan(vh)*camera.aspect), half=Math.min(vh,hh);
  return {t:new V3(cx,0.4,cz),d:clamp(r/Math.tan(half)*1.05,3.6,LV().zoom*1.6)}; }
function offScreen(cats){ return cats.some(c=>{ const s=toScreen(c.g.position.clone().setY(0.4)); return !s.ok||s.x<innerWidth*0.08||s.x>innerWidth*0.92||s.y<innerHeight*0.15||s.y>innerHeight*0.8; }); }
function lessonFrame(dt){ if(cam.meet)return; const L=lessonPts(), key=L?L[0]+':'+L[1].map(c=>c.name).join(','):'';
  if(key!==LF.key){ const was=LF.key; LF.key=key;
    if(was&&!key){ if(LF.want0!=null&&LF.user0===(cam.userT??-99))cam.want=Math.max(cam.want,LF.want0); LF.want0=null; LF.glide=0; return; }
    if(key){ if(!was){ LF.want0=cam.want; LF.user0=cam.userT??-99; } LF.glide=2.5; } }
  if(!L)return; if(camUser()){ LF.glide=0; return; }
  if(LF.glide<=0&&offScreen(L[1]))LF.glide=1.5; // a framed cat wandered out of view
  if(LF.glide<=0)return; LF.glide-=dt; const f=fitFor(L[1],L[2]), k=Math.min(1,dt*2.5);
  cam.target.lerp(f.t,k); if(!['blink','brush'].includes(L[0])||cam.want>f.d)cam.want=lerp(cam.want,f.d,k); }
"""
rep("function clampTarget(){", FRAME.lstrip('\n') + "function clampTarget(){")
# --- recorder: a lesson-ignored touch that became a camera pan
rep("${L&&P.mode==='none'?' BLOCKED':''}", "${L&&P.mode==='none'?' BLOCKED':''}${P.lockPan?' LOCKPAN':''}")
open(P, 'w', encoding='utf-8').write(s); print('ok')
