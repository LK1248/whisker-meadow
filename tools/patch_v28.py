"""v28: the 'slipped out' notice waits until the cat is past the fence (5s the first time, 5-30s after that);
livelier countryside outside the fence (well, more trees, bushes, flower patches) and field mice that runaways chase and never catch."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- notice timing ----
rep("    if(!R.notified&&c.pathEnd==='hide'&&(R.t>7||dist2(c.g.position,new V3(0,0,-LV().half))>4.5)){ R.notified=true; renderMissing(); toast(c.name+' slipped out!'); Snd.meow(0.95,0.6); }",
    """    if(!R.notified){ if(R.delay==null){ R.delay=(W.stat.runNotes||0)===0?5:rand(5,30); R.outT=0; }
      if(!inB(c.g.position.x,c.g.position.z,0))R.outT+=dt;
      if(R.outT>=R.delay&&(c.pathEnd==='hide'||c.state==='hiding')){ R.notified=true; W.stat.runNotes=(W.stat.runNotes||0)+1; renderMissing(); toast(c.name+' slipped out!'); Snd.meow(0.95,0.6); } }""")
rep("{id:'find',when:()=>W.runaway&&W.runaway.c.state==='hiding',", "{id:'find',when:()=>W.runaway&&W.runaway.notified&&W.runaway.c.state==='hiding',")

# ---- countryside ----
rep("  W.hideSpots=[{via:[[X1+1.6,-h-1.4]],p:[X1+5.8,h*0.3+0.6]},", r"""  // a stone well with a little roof and a bucket
  { const wl=new THREE.Group(); wl.position.set(X0-3.6,0,Z1+2.4); wl.rotation.y=0.4; grp.add(wl);
    for(let i=0;i<12;i++){ const a=i/12*6.28; wl.add(mesh(G.box,i%2?0xb9b2a6:0xa8a196,{p:[Math.cos(a)*0.5,0.28,Math.sin(a)*0.5],s:[0.28,0.56,0.16],r:[0,-a,0]})); }
    wl.add(mesh(new THREE.CircleGeometry(0.44,20),0x3f6f8a,{r:[-Math.PI/2,0,0],p:[0,0.4,0],cast:false}));
    for(const sx of [-1,1])wl.add(mesh(G.cyl,0x9b6b43,{p:[sx*0.48,0.95,0],s:[0.05,1.0,0.05]}));
    wl.add(mesh(G.cyl,0x9b6b43,{p:[0,1.25,0],s:[0.035,1.0,0.035],r:[0,0,Math.PI/2]}));
    for(const sz of [-1,1])wl.add(mesh(G.box,0xc8553d,{p:[0,1.56,sz*0.26],s:[1.25,0.05,0.62],r:[sz*0.62,0,0]}));
    wl.add(mesh(G.cyl,0x8a8f99,{p:[0.15,0.78,0],s:[0.13,0.16,0.13]})); wl.add(mesh(G.cyl,0xd9c3a3,{p:[0.15,1.02,0],s:[0.01,0.44,0.01],cast:false})); }
  // more trees, bushes and wildflower patches scattered around the meadow
  const clear=(x,z)=>inB(x,z,-1.4)||(Math.abs(x)<4.5&&z<-h&&z>-h-9)||Math.abs(z-(-h-9.5))<2||Math.hypot(x-(X1+4.2),z-h*0.3)<3||Math.hypot(x-(X0-3.6),z-(Z1+2.4))<1.4;
  for(let k=0,n=0;k<300&&n<Math.round(8+h);k++){ const q=outPt(rand(4.5,10)); if(clear(q.x,q.z))continue; const t=treeMesh(rand(0.7,1.2)); t.position.set(q.x,0,q.z); t.rotation.y=rand(0,6); grp.add(t); n++; }
  for(let k=0,n=0;k<300&&n<Math.round(14+h*2);k++){ const q=outPt(rand(1.4,6)); if(clear(q.x,q.z))continue; const b=new THREE.Group(); b.position.set(q.x,0,q.z); grp.add(b);
    for(let j=0;j<3;j++)b.add(mesh(G.sphLo,pick([0x6db657,0x7fc463,0x5fa84c]),{p:[rand(-.3,.3),rand(.18,.3),rand(-.3,.3)],s:[rand(.3,.5),rand(.28,.4),rand(.3,.5)]}));
    if(Math.random()<0.4)for(let j=0;j<5;j++)b.add(mesh(G.sphLo,pick([0xff9ec7,0xffffff,0xffd84d]),{p:[rand(-.4,.4),rand(.35,.55),rand(-.4,.4)],s:[0.05,0.05,0.05],cast:false})); n++; }
  const fcol=[0xffffff,0xffd84d,0xff9ec7,0xb89cff,0xff8a65,0x8ecbff];
  for(let k=0,n=0;k<300&&n<Math.round(16+h*2);k++){ const q=outPt(rand(1,7)); if(clear(q.x,q.z))continue; const col=pick(fcol);
    for(let j=0;j<9;j++){ const f=new THREE.Group(); f.position.set(q.x+rand(-.7,.7),0,q.z+rand(-.7,.7)); f.add(mesh(G.cyl,0x5fa443,{p:[0,0.1,0],s:[0.012,0.2,0.012],cast:false})); f.add(mesh(G.sphLo,j%4?col:pick(fcol),{p:[0,0.21,0],s:[0.06,0.04,0.06],cast:false})); grp.add(f); } n++; }
  W.hideSpots=[{via:[[X1+1.6,-h-1.4]],p:[X1+5.8,h*0.3+0.6]},""")

# ---- field mice ----
rep("function updateDropoff(dt){", r"""const mice=[];
function mouseMesh(){ const g=new THREE.Group(), fur=pick([0x9a8f86,0xb3a593,0x8a7b6e]);
  g.add(mesh(G.sphLo,fur,{p:[0,0.06,0],s:[0.07,0.055,0.11]})); g.add(mesh(G.sphLo,fur,{p:[0,0.08,0.1],s:[0.045,0.04,0.05]}));
  for(const sx of [-1,1])g.add(mesh(G.sphLo,0xffb3c4,{p:[sx*0.035,0.12,0.09],s:[0.025,0.03,0.01],cast:false}));
  g.add(mesh(G.sphLo,0xff8fa8,{p:[0,0.08,0.15],s:[0.012,0.012,0.012],cast:false})); g.add(mesh(G.cyl,0xe0a8b0,{p:[0,0.05,-0.17],s:[0.008,0.14,0.008],r:[Math.PI/2-0.2,0,0],cast:false})); return g; }
function updateMice(dt){ const want=W.started?Math.min(10,3+W.level):0;
  while(mice.length<want){ const q=outPt(rand(1.5,6)); const g=mouseMesh(); g.position.set(q.x,0,q.z); scene.add(g); mice.push({g,tgt:null,wait:rand(0,2),flee:0,h:rand(0,6)}); }
  const R=W.runaway, rc=R&&R.c.outside&&R.c.state==='path'?R.c:null;
  for(const m of mice){ const p=m.g.position; m.flee=Math.max(0,m.flee-dt);
    if(rc&&!m.flee&&dist2(p,rc.g.position)<2.4&&(rc.chaseCD||0)<=W.time){ // a runaway spots a mouse: dash, pounce... miss
      rc.chaseCD=W.time+6; m.flee=1.6; const aw=Math.atan2(p.x-rc.g.position.x,p.z-rc.g.position.z)+rand(-0.5,0.5); m.h=aw; m.tgt={x:p.x+Math.sin(aw)*3,z:p.z+Math.cos(aw)*3};
      if(rc.path){ rc.path.unshift(p.clone()); rc.chaseLen=rc.path.length; rc.pathSpeed0=rc.pathSpeed; rc.pathSpeed=2.4; } }
    if(m.wait>0&&!m.flee){ m.wait-=dt; continue; }
    if(!m.tgt||Math.hypot(m.tgt.x-p.x,m.tgt.z-p.z)<0.1){ if(!m.flee){ m.wait=rand(0.8,3); const q=outPt(rand(1.2,6)); m.tgt={x:q.x,z:q.z}; } else m.tgt=null; continue; }
    const wanth=Math.atan2(m.tgt.x-p.x,m.tgt.z-p.z); m.h=angLerp(m.h,wanth,dt*(m.flee?14:6)); const sp=m.flee?3.2:1.1;
    p.x+=Math.sin(m.h)*sp*dt; p.z+=Math.cos(m.h)*sp*dt; if(inB(p.x,p.z,-0.4)){ p.x-=Math.sin(m.h)*sp*dt*2; p.z-=Math.cos(m.h)*sp*dt*2; m.tgt=null; }
    m.g.rotation.y=m.h; m.g.position.y=Math.abs(Math.sin(W.time*30))*0.012; }
  // the runaway reaches where the mouse was: a pounce on empty grass
  if(rc&&rc.chaseLen&&rc.path&&rc.path.length<rc.chaseLen){ rc.chaseLen=0; rc.pathSpeed=rc.pathSpeed0||1.3; hop(rc,0.32,0.4); spawnFx('spark',rc.g.position.clone().setY(0.2),3,0.2,0.1); if(Math.random()<0.5)showIcon(rc,'huff',1.2); } }
function updateDropoff(dt){""")
rep("  updateFirstAdopt(dt); updateCoats(dt);", "  updateFirstAdopt(dt); updateCoats(dt); updateMice(dt);")
rep("window.__wm={animateCat,", "window.__wm={animateCat,mice,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
