"""v19: funnier, varied postcards from adopting families (selfie, belly-up, dresser mischief, windowsill guardian,
box, laundry, laptop, pillow, sunbeam; pairs play on the carpet). Thank-you cards for the first adoptions,
a postcard collection achievement, and grumpy/smelly adoptees sometimes don't write."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("// ---- saving ----", r"""// ---- postcards from new homes: little staged photos ----
const CARD_SCENES={
  selfie:{line:(n)=>`${n} figured out the phone camera.`},
  belly:{line:(n)=>`Sunday mornings at our place. ${n} has no shame.`},
  dresser:{line:(n)=>`${n} keeps staring at the mug. We hold on to it now.`},
  window:{line:(n)=>`${n} loves the windowsill. We have a guardian now.`},
  box:{line:(n)=>`We bought ${n} a fancy bed. ${n} prefers the box.`},
  laundry:{line:(n)=>`Found ${n} in the clean laundry. Again.`},
  laptop:{line:(n)=>`${n} helps me work from home. Every. Single. Day.`},
  pillow:{line:(n)=>`${n} sleeps on our pillow. We don't mind.`},
  sunny:{line:(n)=>`${n} found the sunniest spot in the house.`},
  carpet:{line:(n,m)=>`${n} and ${m} haven't stopped playing since they got here.`}};
function cardPose(c,state,sit,rotY,extra){ c.state=state; c.sit=sit; c.stT=9; c.heading=0; c.g.rotation.y=rotY; for(let i=0;i<30;i++)animateCat(c,0.05,W.time+i*0.05); if(extra)extra(c); c.g.rotation.y=rotY; }
function postcard(cats){ try{
  if(!pRen){ pRen=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true}); pRen.setSize(320,240,false); pScene=new THREE.Scene(); pScene.add(new THREE.HemisphereLight(0xfffdf5,0xd9b48a,0.75)); const d=new THREE.DirectionalLight(0xfff0d0,0.7); d.position.set(2,4,3); pScene.add(d); pCam=new THREE.PerspectiveCamera(30,4/3,0.1,50); }
  const seen=new Set(W.stat.cards||[]), pool=Object.keys(CARD_SCENES).filter(k=>k!=='carpet'), fresh=pool.filter(k=>!seen.has(k));
  const scene=cats.length>1?'carpet':pick(fresh.length&&Math.random()<0.8?fresh:pool);
  const saved=cats.map(c=>({c,parent:c.g.parent,pos:c.g.position.clone(),rot:c.g.rotation.y,hd:c.heading,st:c.state,stT:c.stT,sit:c.sit,iv:c.icon.visible,go:c.glow.material.opacity}));
  const a=cats[0], sc=a.g.scale.x; for(const c of cats){ pScene.add(c.g); c.g.position.set(0,0,0); c.icon.visible=false; c.glow.material.opacity=0; }
  pCam.fov=30; pCam.rotation.set(0,0,0); let rect=[40,22,240,180];
  const camAt=(p,l)=>{ pCam.position.set(p[0]*sc,p[1]*sc,p[2]*sc); pCam.lookAt(l[0]*sc,l[1]*sc,l[2]*sc); };
  if(scene==='selfie'){ cardPose(a,'idle',true,0); a.g.updateMatrixWorld(true); const h=a.head.getWorldPosition(new V3()); pCam.fov=55; pCam.position.set(h.x+0.1*sc,h.y+0.12*sc,h.z+0.85*sc); pCam.lookAt(h.x,h.y-0.02*sc,h.z); pCam.rotateZ(0.16); rect=[0,0,320,240]; }
  else if(scene==='belly'){ cardPose(a,'flop',false,0.3); camAt([0.2,2.3,1.1],[0,0.25,0]); rect=[20,10,280,210]; }
  else if(scene==='dresser'){ cardPose(a,'idle',true,1.25,c=>{ c.bat=0.5; animateCat(c,0.02,W.time); }); camAt([0.3,0.9,2.8],[0,0.45,0]); rect=[40,30,200,150]; }
  else if(scene==='window'){ cardPose(a,'watch',true,Math.PI+0.55); camAt([0.9,0.9,2.6],[0,0.5,0]); rect=[90,40,200,150]; }
  else if(scene==='box'||scene==='laundry'){ cardPose(a,'idle',true,0.35); camAt([1.2,1.1,2.6],[0,0.5,0]); rect=[60,8,200,150]; }
  else if(scene==='laptop'){ cardPose(a,'flop',false,-0.4); camAt([0.4,1.4,2.4],[0,0.3,0]); rect=[40,20,240,180]; }
  else if(scene==='pillow'){ cardPose(a,'sleep',false,0.5); camAt([0.8,1.6,2.0],[0,0.25,0]); rect=[50,40,220,165]; }
  else if(scene==='carpet'){ const b=cats[1]; a.g.position.set(-0.4*sc,0,0); b.g.position.set(0.5*sc,0,0.15*sc); cardPose(a,'flop',false,0.2); cardPose(b,'idle',true,-1.6,c=>{ c.bat=0.5; animateCat(c,0.02,W.time); }); camAt([0.2,1.9,2.7],[0,0.3,0]); rect=[20,20,280,210]; }
  else { cardPose(a,'idle',true,0.6); camAt([1.5,1.0,2.5],[0,0.5,0]); }
  pCam.aspect=rect[2]/rect[3]; pCam.updateProjectionMatrix(); pRen.setSize(rect[2]*2,rect[3]*2,false); pRen.render(pScene,pCam);
  for(const v of saved){ const c=v.c; v.parent.add(c.g); c.g.position.copy(v.pos); c.g.rotation.y=v.rot; c.heading=v.hd; c.state=v.st; c.stT=v.stT; c.sit=v.sit; c.icon.visible=v.iv; c.glow.material.opacity=v.go; c.bat=0; }
  const cv=document.createElement('canvas'); cv.width=320; cv.height=240; const x=cv.getContext('2d'), R=(col,a,b,w,h)=>{ x.fillStyle=col; x.fillRect(a,b,w,h); }, E=(col,a,b,rx,ry)=>{ x.fillStyle=col; x.beginPath(); x.ellipse(a,b,rx,ry,0,0,7); x.fill(); };
  const wall=pick(['#f6e3c8','#e8eef6','#f3e0e6','#e6f0df']), rug=pick(['#e58fb5','#7fb2e5','#8ce99a','#ffb347']);
  // backgrounds
  if(scene==='selfie'){ R(wall,0,0,320,240); R('#fff',230,20,70,60); R('#bfe8f7',235,25,60,50); }
  else if(scene==='belly'||scene==='carpet'){ R('#c99a6a',0,0,320,240); for(let i=0;i<8;i++)R('rgba(0,0,0,.06)',0,i*32,320,2); E(rug,160,125,150,95); E('rgba(255,255,255,.25)',160,125,110,65); }
  else if(scene==='dresser'){ R(wall,0,0,320,240); R('#fff',30,18,70,90); R('#cfe9f5',36,24,58,78); R('#a0714a',40,120,200,120); R('#8a5e3b',40,120,200,10); for(const yy of [145,180,215]){ R('#b5845a',50,yy,180,28); E('#6b4a2d',140,yy+14,5,4); } }
  else if(scene==='window'){ R(wall,0,0,320,240); R('#fff',60,14,220,170); R('#bfe8f7',70,24,200,150); E('#8fd17d',170,170,140,40); R('#fff',167,24,6,150); E('#4a3426',110,70,6,4); E('#4a3426',225,56,6,4); x.strokeStyle='#4a3426'; x.lineWidth=2; for(const [bx,by] of [[110,70],[225,56]]){ x.beginPath(); x.moveTo(bx-9,by-4); x.quadraticCurveTo(bx-4,by-8,bx,by); x.quadraticCurveTo(bx+4,by-8,bx+9,by-4); x.stroke(); } R('#f4ede0',50,178,240,16); R('#d8c9b0',50,192,240,6); R('#d9b48a',0,198,320,42); }
  else if(scene==='box'||scene==='laundry'||scene==='laptop'||scene==='pillow'){ R(wall,0,0,320,240); R('#d9b48a',0,170,320,70); E(rug,160,205,120,24); if(scene==='pillow'){ E('#fff',160,180,130,40); E('#eef3fb',160,170,105,30); } }
  else { x.fillStyle=wall; x.fillRect(0,0,320,240); R('#fff',196,22,98,96); R('#bfe8f7',202,28,86,84); E('#ffe27a',262,50,12,12); R('#fff',243,28,4,84); R('#fff',202,68,86,4);
    x.fillStyle='rgba(255,236,170,.45)'; x.beginPath(); x.moveTo(202,112); x.lineTo(288,112); x.lineTo(250,205); x.lineTo(140,205); x.fill(); R('#d9b48a',0,170,320,70); E(rug,160,205,120,24); }
  x.drawImage(pRen.domElement,...rect); pRen.setSize(320,240,false);
  // foreground props
  if(scene==='dresser'){ R('#fff',206,96,24,26); x.strokeStyle='#fff'; x.lineWidth=4; x.beginPath(); x.arc(232,108,7,-1.4,1.4); x.stroke(); R('#7fc7e8',206,102,24,4); R('#5fb35a',58,100,8,20); E('#e8a0b5',62,98,10,8); }
  if(scene==='box'){ R('#c8955a',55,130,210,90); R('#b07d45',55,130,210,10); x.fillStyle='#d9a96a'; x.beginPath(); x.moveTo(55,130); x.lineTo(20,110); x.lineTo(60,104); x.fill(); x.beginPath(); x.moveTo(265,130); x.lineTo(300,108); x.lineTo(262,104); x.fill(); R('rgba(0,0,0,.15)',150,150,30,4); }
  if(scene==='laundry'){ E('#fff',100,138,40,14); E('#bfe0ff',220,136,44,14); E('#ffd6e2',160,132,40,12); x.fillStyle='#e9d3a8'; x.beginPath(); x.moveTo(52,140); x.lineTo(268,140); x.lineTo(250,224); x.lineTo(70,224); x.fill(); x.strokeStyle='#c9a86e'; x.lineWidth=3; for(let i=0;i<6;i++){ x.beginPath(); x.moveTo(60+i*40,146); x.lineTo(78+i*34,220); x.stroke(); } }
  if(scene==='laptop'){ x.fillStyle='#8d97a6'; x.beginPath(); x.moveTo(190,200); x.lineTo(300,200); x.lineTo(310,222); x.lineTo(180,222); x.fill(); R('#5b6573',200,140,90,62); R('#9fd3ff',206,146,78,50); }
  const n=W.homes.length, first=n<3, grumpy=!first&&cats.every(c=>c.s.clean<35||c.s.aff<30)&&Math.random()<0.5;
  const nm=cats.map(c=>c.name), line=CARD_SCENES[scene].line(nm[0],nm[1]);
  return {img:cv.toDataURL('image/jpeg',0.8),scene,line,thanks:first,noCard:grumpy}; }catch(e){ console.warn(e); return null; } }
// ---- saving ----""")

# take the postcard at the goodbye; pairs share one card
rep("for(const k of f.cats){ k.leaving=true; k.img=portrait(k); }", "{ const pc=postcard(f.cats); for(const k of f.cats){ k.leaving=true; k.img=pc?pc.img:portrait(k); k.card=pc; } if(pc&&f.cats[1])f.cats[1].cardDup=true; }")
rep("W.homes.push({name:c.name,coat:coatName(c.coat),img:c.img||null,fam:f?f.name:'',line:pick(LINES)(c.name)});",
    "const pc=c.card; W.homes.push({name:c.name,coat:coatName(c.coat),img:c.img||null,fam:f?f.name:'',line:pc?pc.line:pick(LINES)(c.name),scene:pc&&pc.scene,thanks:pc&&pc.thanks,noCard:!!(pc&&pc.noCard)||!!c.cardDup});")
rep("W.postQ.push({i:W.homes.length-1,t:W.time+35});", "if(!W.homes[W.homes.length-1].noCard)W.postQ.push({i:W.homes.length-1,t:W.time+35});")
# showing the card: thank-you header for the first ones; collection counts the scene
rep("""const pq=W.postQ.shift(), hm=W.homes[pq.i]; if(hm){ openModal(`<div class="postcard">${hm.img?`<img src="${hm.img}" alt="${hm.name} in a new home">`:''}<p>${hm.line}</p>""",
    """const pq=W.postQ.shift(), hm=W.homes[pq.i]; if(hm){ if(hm.scene)W.stat.cards=[...new Set([...(W.stat.cards||[]),hm.scene])]; openModal(`<div class="postcard">${hm.thanks?`<b class="ty">Thank you!</b>`:''}${hm.img?`<img src="${hm.img}" alt="${hm.name} in a new home">`:''}<p>${hm.thanks?`Thank you for ${hm.name}! `:''}${hm.line}</p>""")
rep(".postcard img{", ".postcard .ty{display:block;font:700 26px var(--display);color:#e0507a;text-align:center;margin:0 0 8px}\n.postcard img{")
rep("['rare','Rare Coat','Rare coats and breeds',", "['cards','Postcard Collector','Different postcards from new homes',()=>(W.stat.cards||[]).length,[3,6,10]],['rare','Rare Coat','Rare coats and breeds',")
rep("window.__wm={animateCat,", "window.__wm={animateCat,postcard,CARD_SCENES,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
