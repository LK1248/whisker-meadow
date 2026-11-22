"""v24: pond life. Notched lily pads with a few blossoms, koi gliding under them; pond-watching cats swipe at fish that come close and always miss."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  for(const [px,pz,r] of ponds()){ const pg=new THREE.Group(); pg.position.set(px,0,pz); fenceGroup.add(pg);",
    "  pondFish.length=0;\n  for(const [px,pz,r] of ponds()){ const pg=new THREE.Group(); pg.position.set(px,0,pz); fenceGroup.add(pg);")
# lily pads: notched, a few with blossoms (sit above the fish)
rep("    for(let i=0;i<Math.round(r*2);i++)pg.add(mesh(new THREE.CircleGeometry(0.22,12),0x6db657,{r:[-Math.PI/2,0,rand(0,6)],p:[rand(-r*0.6,r*0.6),0.035,rand(-r*0.6,r*0.6)],cast:false}));",
    """    for(let i=0;i<Math.round(r*2.6);i++){ const a=rand(0,6.28), d=rand(0.15,0.72)*r, lx=Math.cos(a)*d, lz=Math.sin(a)*d, sz=rand(0.17,0.27);
      pg.add(mesh(new THREE.CircleGeometry(sz,16,0.35,5.6),i%2?0x6db657:0x5fa84c,{r:[-Math.PI/2,0,rand(0,6.28)],p:[lx,0.042,lz],cast:false}));
      if(i%3===0){ const fl=new THREE.Group(); fl.position.set(lx+rand(-.05,.05),0.05,lz+rand(-.05,.05)); pg.add(fl);
        for(let k=0;k<6;k++){ const pa=k/6*6.28; fl.add(mesh(G.sph,k%2?0xffb3cf:0xff9fc2,{p:[Math.cos(pa)*0.045,0.02,Math.sin(pa)*0.045],s:[0.04,0.022,0.018],r:[0,-pa,0.5],cast:false})); }
        fl.add(mesh(G.sph,0xffe27a,{p:[0,0.03,0],s:[0.022,0.02,0.022],cast:false})); } }
    // koi gliding under the pads
    for(let i=0;i<Math.max(2,Math.round(r*1.3));i++){ const col=pick([0xff8a3d,0xff7a2e,0xffffff,0xffb347]); const fg=new THREE.Group(); pg.add(fg);
      const mat=new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:0.82,depthWrite:false});
      const body=new THREE.Mesh(G.sphLo,mat); body.scale.set(0.045,0.012,0.12); fg.add(body);
      const tail=new THREE.Mesh(G.cone,mat); tail.scale.set(0.05,0.08,0.012); tail.rotation.x=Math.PI/2; tail.position.z=-0.15; fg.add(tail);
      if(col===0xffffff){ const sp=new THREE.Mesh(G.sphLo,new THREE.MeshBasicMaterial({color:0xff6a2e,transparent:true,opacity:0.85,depthWrite:false})); sp.scale.set(0.03,0.013,0.05); sp.position.z=0.03; fg.add(sp); }
      const a=rand(0,6.28), d=rand(0.2,0.6)*r; fg.position.set(Math.cos(a)*d,0.034,Math.sin(a)*d);
      pondFish.push({g:fg,tail,px,pz,r,h:rand(0,6.28),sp:0.25,tgt:null,flee:0,tease:0,ph:rand(0,6)}); }""")
rep("function buildEnclosure(){", """const pondFish=[];
function updateFish(dt){ for(const f of pondFish){ const p=f.g.position;
    if(!f.tgt||Math.hypot(f.tgt.x-p.x,f.tgt.z-p.z)<0.08){ const a=rand(0,6.28), d=rand(0.1,0.7)*f.r; f.tgt={x:Math.cos(a)*d,z:Math.sin(a)*d}; f.tease=0; }
    f.flee=Math.max(0,f.flee-dt); f.tease=Math.max(0,f.tease-dt);
    const want=Math.atan2(f.tgt.x-p.x,f.tgt.z-p.z); f.h=angLerp(f.h,want,dt*(f.flee>0?9:2.2)); const sp=f.flee>0?1.4:f.tease>0?0.35:0.22;
    p.x+=Math.sin(f.h)*sp*dt; p.z+=Math.cos(f.h)*sp*dt; const d=Math.hypot(p.x,p.z), lim=f.r*0.82; if(d>lim){ p.x*=lim/d; p.z*=lim/d; }
    f.g.rotation.y=f.h; f.ph+=dt*(f.flee>0?22:7); f.tail.rotation.y=Math.sin(f.ph)*0.5; } }
// a pond-watching cat lures a fish to the edge, swipes... and misses. Every time.
function pondSwipe(c,dt){ const pd=c.pondAt; if(!pd)return; c.swipeT=(c.swipeT??rand(1.5,3))-dt; const cp=c.g.position;
  const mine=pondFish.filter(f=>f.px===pd.px&&f.pz===pd.pz); if(!mine.length)return;
  const lx=cp.x-pd.px, lz=cp.z-pd.pz, ld=Math.hypot(lx,lz)||1, edge={x:lx/ld*(pondFish[0]&&mine[0].r*0.78), z:lz/ld*(mine[0].r*0.78)};
  if(!c.lure||c.lure.flee>0){ c.lure=mine.sort((a,b)=>Math.hypot(a.g.position.x-edge.x,a.g.position.z-edge.z)-Math.hypot(b.g.position.x-edge.x,b.g.position.z-edge.z))[0]; }
  const f=c.lure; if(f.flee<=0&&c.swipeT<2.2){ f.tgt={x:edge.x,z:edge.z}; f.tease=2.5; }
  const fp=f.g.position; c.heading=angLerp(c.heading,Math.atan2(pd.px+fp.x-cp.x,pd.pz+fp.z-cp.z),dt*3); c.earTw=Math.max(c.earTw||0,0.1);
  if(c.swipeT<=0){ c.swipeT=rand(2.5,4.5); const near=Math.hypot(fp.x-edge.x,fp.z-edge.z)<0.7;
    if(near){ c.bat=0.5; hop(c,0.08,0.25); const wp=new V3(pd.px+fp.x,0.1,pd.pz+fp.z); spawnFx('spark',wp,5,0.15,0.1);
      f.flee=1.2; const away=Math.atan2(fp.x-edge.x,fp.z-edge.z)+rand(-0.6,0.6); f.h=away; f.tgt={x:fp.x+Math.sin(away)*f.r*0.6,z:fp.z+Math.cos(away)*f.r*0.6};
      c.s.fun=Math.min(100,c.s.fun+3); if(Math.random()<0.4)showIcon(c,'huff',1); if(Snd.ac){ const t=Snd.ac.currentTime; Snd.note(320,t,0.06,0.12,'sine'); Snd.note(190,t+0.05,0.05,0.15,'sine'); } c.lure=null; } } }
function buildEnclosure(){""")
rep("if(a==='pond'&&it){ setState(c,'pondwatch',rand(5,10));", "if(a==='pond'&&it){ c.pondAt=it; c.lure=null; c.swipeT=rand(1.5,3); setState(c,'pondwatch',rand(8,14));")
rep("    case 'pondwatch': s.fun=Math.min(100,s.fun+dt*0.8); if(Math.random()<dt*0.35){", "    case 'pondwatch': s.fun=Math.min(100,s.fun+dt*0.8); pondSwipe(c,dt); if(Math.random()<dt*0.2){")
rep("  updateFirstAdopt(dt); updateCoats(dt);", "  updateFirstAdopt(dt); updateCoats(dt); updateFish(dt);")
rep("window.__wm={animateCat,", "window.__wm={animateCat,pondFish,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
