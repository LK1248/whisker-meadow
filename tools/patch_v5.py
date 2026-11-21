"""One-off patch: v4 -> v5. Road behind the cottage; families and rescuers arrive by car."""
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old); assert n==cnt,(n,old[:90]); s=s.replace(old,new)
def rx(pat,new):
    global s
    s2,n=re.subn(pat,lambda m:new,s,count=1,flags=re.S); assert n==1,('RX',pat[:90]); s=s2

# --- keep trees/bushes off the road strip ---
rep("if(Math.abs(x)<4.5&&z<-h&&z>-h-8)continue;\n    const t=treeMesh","if(Math.abs(x)<4.5&&z<-h&&z>-h-8)continue; if(Math.abs(z-(-h-9.5))<2)continue;\n    const t=treeMesh")
rep("if(Math.abs(x)<4.5&&z<-h)continue; decorGroup.add(mesh(G.sphLo","if(Math.abs(x)<4.5&&z<-h)continue; if(Math.abs(z-(-h-9.5))<1.8)continue; decorGroup.add(mesh(G.sphLo")

# --- move the tire-swing tree off the road and update its hiding spot ---
rep("const bt=treeMesh(1.7); bt.position.set(-2.5,0,-h-9); grp.add(bt); grp.add(mesh(G.cyl,0xd9c3a3,{p:[-1.6,1.6,-h-9],s:[0.015,1.6,0.015],cast:false})); grp.add(mesh(new THREE.TorusGeometry(0.28,0.1,8,18),0x3d3532,{p:[-1.6,0.75,-h-9],r:[0,1.2,0]}));",
    "const bt=treeMesh(1.7); bt.position.set(-6.4,0,-h-7.2); grp.add(bt); grp.add(mesh(G.cyl,0xd9c3a3,{p:[-5.5,1.6,-h-7.2],s:[0.015,1.6,0.015],cast:false})); grp.add(mesh(new THREE.TorusGeometry(0.28,0.1,8,18),0x3d3532,{p:[-5.5,0.75,-h-7.2],r:[0,1.2,0]}));")
rep("{via:[[-3,-h-2.4],[-3.2,-h-8]],p:[-1.6,-h-9.5]}","{via:[[-3,-h-2.4],[-4.4,-h-6.6]],p:[-5.6,-h-7.8]}")

# --- road, driveway, roadside details ---
rep("  // farther props: crates",r'''  // road behind the cottage + driveway to the gate
  const rz=-h-9.5;
  grp.add(mesh(G.box,0x8f949a,{p:[0,0.012,rz],s:[90,0.02,2.3],cast:false,recv:true}));
  for(const e of [-1.2,1.2])grp.add(mesh(G.box,0xd8d2c4,{p:[0,0.02,rz+e],s:[90,0.03,0.12],cast:false}));
  for(let x=-44;x<44;x+=2.4)grp.add(mesh(G.box,0xf6d34a,{p:[x,0.026,rz],s:[1.2,0.01,0.1],cast:false}));
  grp.add(mesh(G.box,0xe0cfa8,{p:[-3.6,0.011,(rz+1.2+(-h-2.6))/2],s:[1.3,0.02,Math.abs(rz+1.2-(-h-2.6))],cast:false,recv:true}));
  grp.add(mesh(G.box,0xe0cfa8,{p:[-1.8,0.011,-h-2.2],s:[3.6,0.02,1.1],cast:false,recv:true}));
  for(const x of [-14,-8,8,15,22,-22]){ const lp=new THREE.Group(); lp.position.set(x,0,rz-1.6); lp.add(mesh(G.cyl,0x4a4f55,{p:[0,1.1,0],s:[0.05,2.2,0.05]})); lp.add(mesh(G.sph,0xfff3c4,{p:[0,2.25,0],s:[0.16,0.12,0.16],cast:false})); grp.add(lp); }
  const sg=new THREE.Group(); sg.position.set(-5.2,0,rz+1.7); sg.add(mesh(G.cyl,0x8a5a3b,{p:[0,0.5,0],s:[0.05,1,0.05]})); sg.add(mesh(G.box,0xff7aa2,{p:[0,1.05,0.03],s:[0.7,0.32,0.05]})); grp.add(sg);
  // farther props: crates''')

# --- cars, people stepping along routes, rescuer drop-offs ---
rep("function readyHome(c){",r'''const cars=[];
const CAR_COLS=[0xff7aa2,0x5b9be6,0xf6c443,0x6cbf8a,0xb48cff,0xf2a35e,0xffffff];
function makeCar(){ const g=new THREE.Group(), col=pick(CAR_COLS);
  g.add(mesh(G.box,col,{p:[0,0.38,0],s:[0.9,0.38,1.9]})); g.add(mesh(G.box,col,{p:[0,0.72,-0.1],s:[0.82,0.34,1.1]}));
  g.add(mesh(G.box,0xbfe8f7,{p:[0,0.74,0.46],s:[0.74,0.24,0.04],cast:false})); g.add(mesh(G.box,0xbfe8f7,{p:[0,0.74,-0.66],s:[0.74,0.24,0.04],cast:false}));
  for(const sx of [-0.42,0.42])g.add(mesh(G.box,0xbfe8f7,{p:[sx,0.74,-0.1],s:[0.02,0.22,0.9],cast:false}));
  const wheels=[]; for(const sx of [-0.46,0.46])for(const sz of [-0.62,0.62]){ const w=mesh(G.cyl,0x2a2421,{p:[sx,0.2,sz],s:[0.2,0.12,0.2],r:[0,0,Math.PI/2]}); g.add(w); wheels.push(w); }
  for(const sx of [-0.3,0.3])g.add(mesh(G.sph,0xfff3c4,{p:[sx,0.42,0.96],s:[0.08,0.06,0.03],cast:false}));
  return {g,wheels}; }
function carVisit(onPark){ const h=LV().half, c=makeCar(); c.g.position.set(-30,0,-h-9.1); c.g.rotation.y=Math.PI/2; scene.add(c.g);
  const car=Object.assign(c,{state:'in',stopX:-3.6,onPark,speed:7}); cars.push(car); return car; }
function carLeave(car){ if(car)car.state='out'; }
function updateCars(dt){ for(let i=cars.length-1;i>=0;i--){ const c=cars[i], p=c.g.position;
  if(c.state==='in'){ const d=c.stopX-p.x; c.speed=Math.min(7,Math.max(0.4,d*1.6)); p.x+=c.speed*dt; if(d<0.03){ p.x=c.stopX; c.state='park'; c.speed=0; if(c.onPark)c.onPark(); } }
  else if(c.state==='out'){ c.speed=Math.min(8,c.speed+dt*4); p.x+=c.speed*dt; if(p.x>34){ scene.remove(c.g); cars.splice(i,1); continue; } }
  for(const w of c.wheels)w.rotation.x+=c.speed*dt*4; } }
function stepPerson(m,dt,t,wave){
  if(m.route&&m.route.length){ m.target.copy(m.route[0]); if(dist2(m.g.position,m.target)<0.15)m.route.shift(); }
  const p=m.g.position, dx=m.target.x-p.x, dz=m.target.z-p.z, d=Math.hypot(dx,dz);
  if(d>0.05){ m.heading=angLerp(m.heading,Math.atan2(dx,dz),dt*6); const sp=Math.min(0.95,d*2+((m.route&&m.route.length)?0.6:0)); p.x+=Math.sin(m.heading)*sp*dt; p.z+=Math.cos(m.heading)*sp*dt; m.speed=sp; } else { m.speed=0; m.heading=angLerp(m.heading,m.face??0,dt*3); }
  m.phase=(m.phase||0)+dt*m.speed*7; const sw=Math.sin(m.phase)*0.55*Math.min(1,m.speed), kk=Math.min(1,dt*6);
  m.hips.position.y=lerp(m.hips.position.y,m.kneel?0.32:0.62,kk); m.legs[0].rotation.x=m.kneel?lerp(m.legs[0].rotation.x,-1.5,kk):sw; m.legs[1].rotation.x=m.kneel?lerp(m.legs[1].rotation.x,-0.2,kk):-sw;
  const wv=wave&&!m.kneel&&m.speed<0.05; m.arms[0].rotation.x=m.kneel?lerp(m.arms[0].rotation.x,-1.1,kk):wv?-2.6:m.carry?-0.9:-sw*0.8; m.arms[0].rotation.z=wv?Math.sin(t*6)*0.4:0; m.arms[1].rotation.x=m.carry?-0.9:sw*0.8; m.g.rotation.y=m.heading; }
function arrived(m){ return (!m.route||!m.route.length)&&dist2(m.g.position,m.target)<0.2; }
function routeIn(h,i,n){ const gx=(i-(n-1)/2)*0.65; return [new V3(-3.6+gx*0.5,0,-h-8.3),new V3(-3.6,0,-h-2.9),new V3(gx,0,-h-1.05)]; }
function routeOut(h,i){ return [new V3(-3.6,0,-h-2.9),new V3(-3.6+i*0.3-0.3,0,-h-8.3)]; }
function startDropoff(){ if(W.dropoff||W.cats.length>=LV().cap)return; const h=LV().half;
  const per=personMesh(); per.g.visible=false; per.g.position.set(-3.6,0,-h-8.3); per.heading=0; per.target=per.g.position.clone(); per.route=[]; per.carry=true; per.face=Math.PI; scene.add(per.g);
  const box=new THREE.Group(); box.position.set(0,0.2,0.3); box.add(mesh(G.box,0x7fb2e5,{s:[0.42,0.3,0.3]})); box.add(mesh(G.box,0x3d3532,{p:[0,0,0.155],s:[0.26,0.18,0.01],cast:false})); per.hips.add(box); per.box=box;
  const car=carVisit(()=>{ per.g.visible=true; per.route=routeIn(h,1,3).map((v,i)=>i===2?new V3(0.45,0,-h-1.05):v); });
  W.dropoff={p:per,car,stage:'walkin',t:0}; }
function updateDropoff(dt){ const D=W.dropoff; if(!D)return; const h=LV().half;
  if(D.stage==='walkin'&&D.p.g.visible&&arrived(D.p)){ D.stage='drop'; D.t=0; D.p.kneel=true; D.p.face=Math.PI; }
  else if(D.stage==='drop'){ D.t+=dt; if(D.t>1.0&&!D.done){ D.done=true; D.p.box.visible=false; D.p.carry=false; arriveStray(); } if(D.t>2.2){ D.p.kneel=false; D.stage='walkout'; D.p.route=routeOut(h,1); } }
  else if(D.stage==='walkout'&&arrived(D.p)){ scene.remove(D.p.g); carLeave(D.car); W.dropoff=null; } }
function readyHome(c){''')

# families come and go by car
rx(r"function spawnFamily\(\)\{.*?\n  W\.family=\{members,want,tries:0,t:0,name:pick\(FAM_NAMES\),state:'arrive'\}; Snd\.chime\(\); renderFamily\(\); \}",
r'''function spawnFamily(){ const ready=W.cats.filter(readyHome); if(!ready.length)return; const h=LV().half;
  const want=Math.random()<0.7?pick(ready).trait:pick(TRAITS); const n=Math.random()<0.5?2:3; const members=[];
  for(let i=0;i<n;i++){ const kid=i===2||(n===2&&i===1&&Math.random()<0.4); const m=personMesh({scale:kid?0.68:1}); m.g.visible=false; m.g.position.set(-3.6+i*0.3,0,-h-8.3); m.target=m.g.position.clone(); m.route=[]; m.heading=0; m.face=Math.PI; m.speed=0; m.phase=0; scene.add(m.g); members.push(m); }
  const car=carVisit(()=>{ members.forEach((m,i)=>{ m.g.visible=true; m.route=routeIn(h,i,n); }); });
  W.family={members,want,tries:0,t:0,name:pick(FAM_NAMES),state:'arrive',car}; Snd.chime(); renderFamily(); }''')
rep("  for(const m of f.members){ m.kneel=false; m.target.set(-8,0,-h-2.2); } if(f.cat&&!f.cat.leaving&&['path','greet'].includes(f.cat.state))backFromGate(f.cat); }",
    "  f.members.forEach((m,i)=>{ m.kneel=false; m.g.visible=true; m.route=routeOut(h,i); }); if(f.cat&&!f.cat.leaving&&['path','greet'].includes(f.cat.state))backFromGate(f.cat); }")
rep("function removeFamily(){ const f=W.family; if(!f)return; for(const m of f.members)scene.remove(m.g);","function removeFamily(){ const f=W.family; if(!f)return; for(const m of f.members)scene.remove(m.g); carLeave(f.car);")
rx(r"function updateFamilyMeshes\(dt,t\)\{.*?\}\); \}\n",r'''function updateFamilyMeshes(dt,t){ updateCars(dt); const f=W.family; if(f)f.members.forEach((m,i)=>stepPerson(m,dt,t,i===1&&(f.state==='arrive'||f.state==='bye'))); if(W.dropoff)stepPerson(W.dropoff.p,dt,t,false); }
''')
rep("for(const k of f.cats)walkPath(k,[new V3(rand(-.2,.2),0,-h-0.9),new V3(-7,0,-h-2.2+rand(-.3,.3))],'out',0.85); for(const m of f.members)m.target.set(-8,0,-h-2.2); }",
    "for(const k of f.cats)walkPath(k,[new V3(rand(-.2,.2),0,-h-0.9),new V3(-3.6,0,-h-2.9),new V3(-3.6,0,-h-8.2)],'out',0.85); f.members.forEach((m,i)=>m.route=routeOut(h,i)); }")
rep("if(f.walking&&!f.cats.some(k=>W.cats.includes(k))&&f.members.every(m=>dist2(m.g.position,m.target)<0.2))removeFamily(); }","if(f.walking&&!f.cats.some(k=>W.cats.includes(k))&&f.members.every(arrived))removeFamily(); }")
rep("if(f.msgT<=0)$('#family').hidden=true; if(f.members.every(m=>dist2(m.g.position,m.target)<0.2))removeFamily(); }","if(f.msgT<=0)$('#family').hidden=true; if(f.members.every(arrived))removeFamily(); }")
# strays now arrive with a rescuer's drop-off
rep("const act=active(); const avgH=act.reduce((a,c)=>a+c.s.health,0)/Math.max(1,act.length); if(W.cats.length<LV().cap&&avgH>=50)arriveStray(); }","const act=active(); const avgH=act.reduce((a,c)=>a+c.s.health,0)/Math.max(1,act.length); if(W.cats.length<LV().cap&&avgH>=50)startDropoff(); }")
rep("  updateBoops(dt);\n","  updateBoops(dt); updateDropoff(dt);\n")
# expansion shifts cars, routes and the drop-off person too
rep("  const f=W.family; if(f){ for(const m of f.members){ m.g.position.z+=dz; m.target.z+=dz; } }","  const f=W.family; if(f){ for(const m of f.members){ m.g.position.z+=dz; m.target.z+=dz; if(m.route)m.route.forEach(v=>v.z+=dz); } }\n  for(const car of cars)car.g.position.z+=dz; if(W.dropoff){ const q=W.dropoff.p; q.g.position.z+=dz; q.target.z+=dz; q.route.forEach(v=>v.z+=dz); }")
rep("window.__wm={W,items,cam,","window.__wm={W,items,cam,cars,startDropoff,")
open(p,'w',encoding='utf-8').write(s); print('v5 patch ok')
