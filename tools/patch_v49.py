"""v49: trees no longer block the view. A tree that stands between the camera and what it looks at, or that
fills a big part of the screen from up close, fades to see-through (and back when the camera moves on)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const matCache={};", "const matCache={}, TREES=[];")
rep("g.add(mesh(G.sph,fc,{p:[-0.55,1.85,-0.2],s:[0.65,0.6,0.65]})); return g; }",
    "g.add(mesh(G.sph,fc,{p:[-0.55,1.85,-0.2],s:[0.65,0.6,0.65]})); g.userData.parts=g.children.slice(); g.userData.fade=1; TREES.push(g); return g; }")

rep("  camera.lookAt(t);\n}", """  camera.lookAt(t);
  fadeTrees(dt);
}
// trees between the camera and its target (or looming large right in front of it) fade out of the way
const _tw=new V3(), _tv=new V3(), _tc=new V3(); let treePrune=0;
function treeInScene(g){ let o=g; while(o.parent)o=o.parent; return o===scene; }
function fadeTrees(dt){ if(!TREES.length)return; treePrune-=dt; if(treePrune<=0){ treePrune=3; for(let i=TREES.length-1;i>=0;i--)if(!treeInScene(TREES[i]))TREES.splice(i,1); }
  const cp=camera.position, tg=cam.target, seg=_tv.copy(tg).sub(cp), L=seg.length(), tanH=Math.tan(camera.fov*Math.PI/360), k=Math.min(1,dt*5||1);
  for(const g of TREES){ const u=g.userData; if(!u.wp){ g.updateWorldMatrix(true,false); u.wp=g.localToWorld(new V3(0,1.95,0)); u.R=1.15*g.getWorldScale(_tw).x; }
    const c=u.wp; let want=1;
    const along=_tc.copy(c).sub(cp).dot(seg)/(L*L);
    if(along>0&&along<1){ const d=_tw.copy(cp).addScaledVector(seg,along).distanceTo(c), dc=c.distanceTo(cp), dt2=tg.distanceTo(cp);
      if(dc<dt2-0.4){ const ndc=_tw.copy(c).project(camera), r=u.R/(dc*tanH);
        if(d<u.R+0.25||(r>0.35&&Math.abs(ndc.x)<0.75+r/camera.aspect&&Math.abs(ndc.y)<0.75+r))want=0.22; } }
    if(Math.abs(u.fade-want)<0.01&&!(u.fading))continue;
    u.fade+= (want-u.fade)*k; if(Math.abs(u.fade-want)<0.01)u.fade=want;
    if(!u.own){ u.own=true; u.parts.forEach(m=>{ m.material=m.material.clone(); m.material.transparent=true; }); }
    u.parts.forEach(m=>{ m.material.opacity=u.fade; m.material.depthWrite=u.fade>0.98; }); u.fading=u.fade!==want; } }""")
rep("window.__wm={Snd,", "window.__wm={Snd,TREES,fadeTrees,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
