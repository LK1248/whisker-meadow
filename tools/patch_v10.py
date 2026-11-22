"""v10: exotic breeds (Bengal, Savannah, Maine Coon, Siamese, Ragdoll, Scottish Fold) arrive as special rescues later in the game."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# coat colours for the breeds (all count as rare)
rep("golden:{body:0xe9c157,belly:0xfff0c0,stripe:0xc6902a,rare:1}};",
"""golden:{body:0xe9c157,belly:0xfff0c0,stripe:0xc6902a,rare:1},
  bengal:{body:0xe3a352,belly:0xfbe8cc,stripe:0x5a3a22,rare:1},savannah:{body:0xe8cc92,belly:0xfaf1de,stripe:0x2a2220,rare:1},mainecoon:{body:0x8c6a4c,belly:0xeadac4,stripe:0x4e3826,rare:1},
  siamese:{body:0xf1e4cf,belly:0xfbf5ea,stripe:0x4a3426,rare:1},ragdoll:{body:0xf4ede4,belly:0xffffff,stripe:0x8b7d74,rare:1},fold:{body:0xa3abb6,belly:0xe0e4ea,stripe:0x6e7782,rare:1}};
// body plans: len = body length, leg = leg length, size = overall, ear = ear size
const BREEDS={
  bengal:{name:'Bengal',pattern:'solid',eye:0x8fd14f,len:1.1,leg:1.06,size:1.02,ear:0.95,rosettes:15},
  savannah:{name:'Savannah',pattern:'solid',eye:0xd9a441,len:1.24,leg:1.34,size:1.04,ear:1.55,spots:22,tailLen:0.8},
  mainecoon:{name:'Maine Coon',pattern:'tabby',eye:0xd9a441,len:1.12,leg:1.06,size:1.2,ear:1.18,ruff:1,tufts:1,bushy:1.6},
  siamese:{name:'Siamese',pattern:'solid',eye:0x5fb8f2,len:1.08,leg:1.12,size:0.96,ear:1.3,points:1},
  ragdoll:{name:'Ragdoll',pattern:'socks',eye:0x4f9ff0,len:1.05,leg:1.0,size:1.12,ear:1.0,points:1,ruff:1,bushy:1.35},
  fold:{name:'Scottish Fold',pattern:'solid',eye:0xe08a2a,len:0.94,leg:0.92,size:1.0,ear:0.75,fold:1,round:1.12}};
function exoticCoat(){ const owned=new Set(W.cats.map(c=>c.coat.base)), all=Object.keys(BREEDS), pool=all.filter(b=>!owned.has(b)); const b=pick(pool.length?pool:all); return {base:b,pattern:BREEDS[b].pattern,eye:BREEDS[b].eye}; }""")
rep("function coatName(c){ if(c.pattern==='calico')", "function coatName(c){ if(BREEDS[c.base])return BREEDS[c.base].name; if(c.pattern==='calico')")

# build: breed extras, applied before the mesh tagging pass
rep("  const icon=new THREE.Sprite(new THREE.SpriteMaterial({map:iconTexture('purr')", """  const B=BREEDS[cat.coat.base];
  if(B){ const ax=[0.36,0.33,0.58];
    if(B.rosettes) for(let i=0;i<B.rosettes;i++){ const d=[rand(-1,1),rand(0.05,1),rand(-0.95,0.95)]; cap(core,0x9a6a38,d,ax,'back',0.2); cap(core,dark,d,ax,'back',0.13); }
    if(B.spots){ for(let i=0;i<B.spots;i++)cap(core,dark,[rand(-1,1),rand(-0.1,1),rand(-0.95,0.95)],ax,'back',0.09); for(let i=0;i<4;i++)cap(head,dark,[rand(-0.8,0.8),rand(0.5,1),rand(-0.6,0.2)],[0.3,0.27,0.27],'head',0.07); }
    if(B.ruff){ add(core,G.sph,light,[0,0.12,0.4],[0.33,0.3,0.24],'chest'); add(head,G.sph,light,[0.17,-0.1,0.02],[0.14,0.13,0.12],'cheek'); add(head,G.sph,light,[-0.17,-0.1,0.02],[0.14,0.13,0.12],'cheek'); }
    if(B.points){ const pc=dark; head.traverse(o=>{ if(o.isMesh&&o.userData.zone==='chin')o.material=M(pc); }); add(head,G.sph,pc,[0,-0.06,0.2],[0.14,0.1,0.08],'chin');
      cat.ears.forEach(e=>{ e.children[0].material=M(pc); }); cat.tail.forEach((m,i)=>{ if(i>=2)m.material=M(pc); });
      if(B.pattern!=='socks')cat.legs.forEach(L=>L.children.forEach(m=>{ m.material=M(pc); })); }
    if(B.tufts)cat.ears.forEach(e=>add(e,G.cone,dark,[0,0.25,0],[0.03,0.1,0.025],'head'));
    cat.ears.forEach(e=>{ e.scale.setScalar(B.ear); if(B.fold){ e.scale.y=B.ear*0.55; e.rotation.x=0.95; e.position.y=0.17; } });
    if(B.bushy)cat.tail.forEach(m=>m.scale.multiplyScalar(B.bushy));
    // longer (or shorter) body: stretch the torso, push head, legs and tail out
    for(const m of core.children)if(m.isMesh){ m.position.z*=B.len; m.scale.z*=B.len; }
    head.position.z*=B.len; tail.position.z*=B.len; cat.legs.forEach(L=>{ L.position.z*=B.len; L.scale.y=B.leg; });
    cat.legLift=(B.leg-1)*0.34; cat.tailLen=B.tailLen||1; }
  const icon=new THREE.Sprite(new THREE.SpriteMaterial({map:iconTexture('purr')""")
rep("function applyAge(c){ const a=c.age; c.g.scale.setScalar(0.52+0.48*a); c.head.scale.setScalar(1+0.28*(1-a)); }",
    "function applyAge(c){ const a=c.age, B=BREEDS[c.coat.base]; c.g.scale.setScalar((0.52+0.48*a)*(B?B.size:1)); c.head.scale.setScalar((1+0.28*(1-a))*(B&&B.round||1)); }")
rep("  c.core.position.y=lerp(c.core.position.y,coreY+(moving", "  c.core.position.y=lerp(c.core.position.y,coreY+(c.legLift||0)*Math.max(0,Math.cos(legA[2]))+(moving")
rep("  const sp=0.075; let x=0,y=0,z=0;", "  const sp=0.075*(c.tailLen||1); let x=0,y=0,z=0;")

# arrivals: a guaranteed special rescue with each sanctuary expansion from level 3, and an occasional surprise later
rep("  else { const kit=Math.random()<0.35;", """  else if(W.exoticNext||(W.level>=3&&Math.random()<0.12)){ W.exoticNext=false; const coat=exoticCoat();
    const c=makeCat({coat,age:1,origin:'stray',fixed:true,x:rand(-0.3,0.3),z:-h+0.45,s:{trust:rand(15,25),aff:rand(15,25),full:rand(35,50),fun:40,groom:rand(20,35),health:rand(50,60),clean:70}});
    c.heading=0; goTo(c,rand(-1,1),-h+2.4,null); W.stat.rescues++; W.stat.breedSeen=[...new Set([...(W.stat.breedSeen||[]),coat.base])]; spawnFx('spark',c.g.position.clone().setY(0.8),14,0.7); Snd.chime(); meet(c,'stray'); }
  else { const kit=Math.random()<0.35;""")
rep("function expand(){ const oh=LV().half; W.level++;", "function expand(){ const oh=LV().half; W.level++; if(W.level>=3){ W.exoticNext=true; setTimeout(()=>startDropoff(),20000); }")
rep("['rare','Rare Coat','Lilac or golden cats',()=>W.stat.rare||0,[1,3,6]],", "['rare','Rare Coat','Rare coats and breeds',()=>W.stat.rare||0,[1,3,6]],['breeds','Exotic Friends','Different breeds rescued',()=>(W.stat.breedSeen||[]).length,[1,3,6]],")
rep("window.__wm={animateCat,", "window.__wm={animateCat,BREEDS,exoticCoat,makeCat,applyAge,arriveStray,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
