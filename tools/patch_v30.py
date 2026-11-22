"""v30: owls perch on treetops at night (blink, turn heads, puff up when they hoot, sometimes answer each other); some helpers are women (skirt, longer hair)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- owls ----------
rep("function outsideDecor(grp,h){", """const owls=[]; let owlEyeMat=null;
function owlMesh(){ const g=new THREE.Group(), body=new THREE.Group(); g.add(body); const br=0x8a6a4a, lt=0xe8d6b4, dk=0x6e5238;
  if(!owlEyeMat)owlEyeMat=new THREE.MeshBasicMaterial({color:0xffcf3a});
  body.add(mesh(G.sph,br,{p:[0,0.22,0],s:[0.2,0.25,0.18]})); body.add(mesh(G.sph,lt,{p:[0,0.19,0.08],s:[0.14,0.18,0.12],cast:false}));
  for(const sx of [1,-1]){ body.add(mesh(G.sph,dk,{p:[0.17*sx,0.22,-0.01],s:[0.07,0.18,0.14]})); body.add(mesh(G.sphLo,0xe0a030,{p:[0.06*sx,0.01,0.08],s:[0.04,0.025,0.05],cast:false})); }
  const head=new THREE.Group(); head.position.y=0.53; body.add(head);
  head.add(mesh(G.sph,br,{s:[0.18,0.15,0.16]})); head.add(mesh(G.sph,lt,{p:[0,-0.01,0.085],s:[0.14,0.105,0.08],cast:false}));
  for(const sx of [1,-1])head.add(mesh(G.cone,br,{p:[0.11*sx,0.14,0],s:[0.045,0.11,0.045],r:[0,0,-0.35*sx]}));
  const eyes=[1,-1].map(sx=>{ const e=new THREE.Group(); e.position.set(0.058*sx,0.012,0.15); head.add(e);
    e.add(mesh(G.sph,owlEyeMat,{s:[0.048,0.048,0.02],cast:false})); e.add(mesh(G.sph,0x1a1410,{p:[0,0,0.013],s:[0.024,0.024,0.012],cast:false})); return e; });
  head.add(mesh(G.cone,0xe0a030,{p:[0,-0.045,0.165],s:[0.022,0.05,0.022],r:[Math.PI,0,0],cast:false}));
  return {g,body,head,eyes}; }
function owlHoot(){ const vis=owls.filter(o=>o.k>0.9); if(!vis.length)return; const o=pick(vis); o.hoot=1.4;
  // now and then a second owl answers from another tree
  if(vis.length>1&&Math.random()<0.5){ const o2=pick(vis.filter(x=>x!==o)); setTimeout(()=>{ if(o2.k>0.9&&(W.night||0)>0.5){ o2.hoot=1.4; Snd.owl((W.night||0)*0.75); } },rand(1800,2800)); } }
function updateOwls(dt){ const on=(W.night||0)>0.45&&!weather.raining;
  for(const o of owls){ o.k=clamp(o.k+(on?dt:-dt)*0.5,0,1); o.g.visible=o.k>0.01; if(!o.g.visible)continue;
    o.g.scale.setScalar(o.inv*(1-Math.pow(1-o.k,3)));
    o.blink-=dt; if(o.blink<=0){ o.blink=rand(2,6); o.bl=0.16; } o.bl=Math.max(0,o.bl-dt); for(const e of o.eyes)e.scale.y=o.bl>0?0.12:1;
    o.turnT-=dt; if(o.turnT<=0){ o.turnT=rand(2,5); o.yaw=Math.random()<0.15?rand(-2.4,2.4):rand(-0.8,0.8); }
    o.head.rotation.y=lerp(o.head.rotation.y,o.yaw,Math.min(1,dt*(Math.abs(o.yaw-o.head.rotation.y)>1.2?7:2)));
    if(o.hoot>0){ o.hoot-=dt; const p=Math.max(0,Math.sin((1.4-o.hoot)*Math.PI*2.2)); o.body.scale.set(1+0.13*p,1+0.06*p,1+0.13*p); o.head.rotation.x=-0.28*p; }
    else { o.body.scale.setScalar(1); o.head.rotation.x=0; } } }
function outsideDecor(grp,h){""")
rep("""  for(let k=0,n=0;k<300&&n<Math.round(8+h);k++){ const q=outPt(rand(4.5,10)); if(clear(q.x,q.z))continue; const t=treeMesh(rand(0.7,1.2)); t.position.set(q.x,0,q.z); t.rotation.y=rand(0,6); grp.add(t); n++; }""",
"""  const trs=[]; owls.length=0;
  for(let k=0,n=0;k<300&&n<Math.round(8+h);k++){ const d=rand(4.5,10), q=outPt(d); if(clear(q.x,q.z))continue; const sc=rand(0.7,1.2), t=treeMesh(sc); t.position.set(q.x,0,q.z); t.rotation.y=rand(0,6); grp.add(t); trs.push({t,d,sc}); n++; }
  // owls perch on a few of the nearer treetops; they only show up after dark
  trs.sort((a,b)=>a.d-b.d); const perch=trs.slice(0,Math.max(3,Math.ceil(trs.length*0.6)));
  for(let i=0;i<Math.min(perch.length,2+Math.floor((W.level||1)/2),5);i++){ const j=Math.floor(Math.random()*perch.length), P0=perch.splice(j,1)[0], t=P0.t, ow=owlMesh();
    ow.g.position.set(0,2.92,0); ow.g.rotation.y=rand(-0.5,0.5)-t.rotation.y; ow.g.visible=false; t.add(ow.g);
    owls.push(Object.assign(ow,{inv:1/P0.sc,k:0,blink:rand(1,4),bl:0,turnT:rand(1,3),yaw:0,hoot:0})); }""")
rep("if(n>0.6)Snd.owl(n); } } }", "if(n>0.6){ Snd.owl(n); owlHoot(); } } } }")
rep("updateMice(dt); updateFish(dt);", "updateMice(dt); updateOwls(dt); updateFish(dt);")

# ---------- women helpers ----------
rep("""  hips.add(mesh(G.cyl,shirt,{p:[0,0.3,0],s:[0.22,0.6,0.17]})); hips.add(mesh(G.sph,shirt,{p:[0,0.6,0],s:[0.23,0.12,0.18]}));
  const head=new THREE.Group(); head.position.y=0.86; hips.add(head);
  head.add(mesh(G.sph,skin,{s:[0.19,0.2,0.19]})); head.add(mesh(G.sph,hair,{p:[0,0.06,-0.03],s:[0.205,0.18,0.2]}));""",
"""  hips.add(mesh(G.cyl,shirt,{p:[0,0.3,0],s:[0.22,0.6,0.17]})); hips.add(mesh(G.sph,shirt,{p:[0,0.6,0],s:[0.23,0.12,0.18]}));
  if(o.woman){ if(!G.skirt)G.skirt=new THREE.CylinderGeometry(0.55,1,1,18);
    hips.add(mesh(G.skirt,o.skirt||pick([0xd9637a,0x4f6fb0,0x7a5aa8,0x3f8a6a,0xe08a3c,0x8a4a5a]),{p:[0,-0.1,0],s:[0.3,0.38,0.25]})); }
  const head=new THREE.Group(); head.position.y=0.86; hips.add(head);
  head.add(mesh(G.sph,skin,{s:[0.19,0.2,0.19]})); head.add(mesh(G.sph,hair,{p:[0,0.06,-0.03],s:[0.205,0.18,0.2]}));
  if(o.woman){ const st=o.hairStyle??Math.floor(Math.random()*3);
    if(st===0){ head.add(mesh(G.sph,hair,{p:[0,-0.07,-0.08],s:[0.2,0.2,0.13]})); }   // shoulder-length
    else if(st===1){ head.add(mesh(G.sph,hair,{p:[0,0.02,-0.2],s:[0.07,0.07,0.07]})); head.add(mesh(G.sph,hair,{p:[0,-0.12,-0.22],s:[0.06,0.13,0.06]})); }   // ponytail
    else { head.add(mesh(G.sph,hair,{p:[0,0.2,-0.07],s:[0.1,0.09,0.1]})); }   // bun
  }""")
rep("function makeHelper(){ const m=personMesh(); const h=LV().half;",
    "function makeHelper(){ const last=helpers[helpers.length-1], m=personMesh({woman:last?!last.woman:Math.random()<0.5}); const h=LV().half;")
rep("const hp=Object.assign(m,{state:'idle',", "const hp=Object.assign(m,{woman:m.woman,state:'idle',")
rep("  return {g,hips,legs,arms,head};\n}", "  return {g,hips,legs,arms,head,woman:!!o.woman};\n}")
rep("window.__wm={animateCat,", "window.__wm={animateCat,cam,makeHelper,owls,owlHoot,helpers,personMesh,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
