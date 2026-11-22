"""One-off patch: v5 -> v6. Rectangular meadow wings with ponds (levels 5-8, gated by homes found),
badge cash rewards, special collars unlocked by gold badges."""
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old); assert n==cnt,(n,old[:90]); s=s.replace(old,new)
def rx(pat,new):
    global s
    s2,n=re.subn(pat,lambda m:new,s,count=1,flags=re.S); assert n==1,('RX',pat[:90]); s=s2

# ---------- levels + bounds helpers ----------
rep("const LEVELS=[null,{half:3.2,cap:4,cost:0,zoom:8.5},{half:5,cap:8,cost:120,zoom:12.5},{half:7.5,cap:14,cost:300,zoom:17.5},{half:11,cap:24,cost:700,zoom:25}];",
r'''const LEVELS=[null,{half:3.2,cap:4,cost:0,zoom:8.5},{half:5,cap:8,cost:120,zoom:12.5},{half:7.5,cap:14,cost:300,zoom:17.5},{half:11,cap:24,cost:700,zoom:25},
  {half:11,x0:-11,x1:21,z1:11,cap:30,cost:1100,zoom:31,homes:3,name:'East wing',ponds:[[12,1.5,3.2]]},
  {half:11,x0:-21,x1:21,z1:11,cap:36,cost:1600,zoom:35,homes:6,name:'West wing',ponds:[[12,1.5,3.2],[-14,-2.5,2.4]]},
  {half:11,x0:-21,x1:21,z1:23,cap:44,cost:2300,zoom:40,homes:10,name:'North meadow',ponds:[[12,1.5,3.2],[-14,-2.5,2.4],[2,15,4.2]]},
  {half:11,x0:-27,x1:28,z1:27,cap:52,cost:3200,zoom:46,homes:16,name:'Grand sanctuary',ponds:[[12,1.5,3.2],[-14,-2.5,2.4],[2,15,4.2],[-20,18,2.8],[22,19,3]]}];
function bnd(){ const L=LEVELS[W.level]; return {x0:L.x0??-L.half,x1:L.x1??L.half,z0:-L.half,z1:L.z1??L.half}; }
function ponds(){ return LEVELS[W.level].ponds||[]; }
function inPond(x,z,m=0){ return ponds().some(([px,pz,r])=>Math.hypot(x-px,z-pz)<r+m); }
function inB(x,z,m=0){ const B=bnd(); return x>B.x0+m&&x<B.x1-m&&z>B.z0+m&&z<B.z1-m; }
function rIn(m=0){ const B=bnd(); for(let k=0;k<40;k++){ const x=rand(B.x0+m,B.x1-m), z=rand(B.z0+m,B.z1-m); if(!inPond(x,z,0.4))return {x,z}; } return {x:0,z:B.z0+2}; }
function area(){ const B=bnd(); return (B.x1-B.x0)*(B.z1-B.z0); }
function clampX(x,m){ const B=bnd(); return clamp(x,B.x0+m,B.x1-m); }
function clampZ(z,m){ const B=bnd(); return clamp(z,B.z0+m,B.z1-m); }
function ext(){ const B=bnd(); return Math.max(-B.x0,B.x1,-B.z0,B.z1); }
function outPt(d){ const B=bnd(), s=Math.floor(Math.random()*4); if(s===0)return {x:rand(B.x0-d,B.x1+d),z:B.z0-d}; if(s===1)return {x:B.x1+d,z:rand(B.z0-d,B.z1+d)}; if(s===2)return {x:rand(B.x0-d,B.x1+d),z:B.z1+d}; return {x:B.x0-d,z:rand(B.z0-d,B.z1+d)}; }
function fencePt(){ const B=bnd(), s=Math.floor(Math.random()*4); if(s===0){ let x=rand(B.x0+0.8,B.x1-0.8); if(Math.abs(x)<1)x=B.x1*0.6; return [x,B.z0]; } if(s===1)return [B.x1,rand(B.z0+0.8,B.z1-0.8)]; if(s===2)return [rand(B.x0+0.8,B.x1-0.8),B.z1]; return [B.x0,rand(B.z0+0.8,B.z1-0.8)]; }''')
rep("function setShadowBounds(){ const h=LV().half+6,","function setShadowBounds(){ const h=ext()+6,")

# ---------- fence for any rectangle + ponds inside ----------
rx(r"function buildEnclosure\(\)\{.*?\n  // gate with arch sign\n",r'''function buildEnclosure(){
  const h=LV().half, B=bnd(); if(fenceGroup)scene.remove(fenceGroup); fenceGroup=new THREE.Group();
  const W2=B.x1-B.x0, D2=B.z1-B.z0, cx=(B.x0+B.x1)/2, cz=(B.z0+B.z1)/2;
  fenceGroup.add(mesh(new THREE.PlaneGeometry(W2,D2),0x97d06d,{r:[-Math.PI/2,0,0],p:[cx,0.006,cz],cast:false,recv:true}));
  const sides=[[[B.x0,B.z0],[B.x1,B.z0]],[[B.x1,B.z0],[B.x1,B.z1]],[[B.x1,B.z1],[B.x0,B.z1]],[[B.x0,B.z1],[B.x0,B.z0]]];
  sides.forEach(([a,b],side)=>{ const L=Math.hypot(b[0]-a[0],b[1]-a[1]), n=Math.ceil(L/1.1);
    for(let i=0;i<n;i++){ const f=i/n, x=a[0]+(b[0]-a[0])*f, z=a[1]+(b[1]-a[1])*f; if(side===0&&Math.abs(x)<0.75)continue;
      fenceGroup.add(mesh(G.box,0xc99a6b,{p:[x,0.42,z],s:[0.14,0.84,0.14]})); fenceGroup.add(mesh(G.cone,0xc99a6b,{p:[x,0.9,z],s:[0.1,0.14,0.1]})); }
    for(const y of [0.36,0.68]){
      if(side===0){ for(const [xa,xb] of [[B.x0,-0.62],[0.62,B.x1]]){ const seg=xb-xa; fenceGroup.add(mesh(G.box,0xe3bd90,{p:[(xa+xb)/2,y,B.z0],s:[seg,0.09,0.06]})); } continue; }
      const horiz=side===2; fenceGroup.add(mesh(G.box,0xe3bd90,{p:[(a[0]+b[0])/2,y,(a[1]+b[1])/2],s:horiz?[L,0.09,0.06]:[0.06,0.09,L]})); } });
  for(const [px,pz,r] of ponds()){ const pg=new THREE.Group(); pg.position.set(px,0,pz); fenceGroup.add(pg);
    pg.add(mesh(new THREE.CircleGeometry(r,32),0x7fc4e8,{r:[-Math.PI/2,0,0],p:[0,0.025,0],cast:false,recv:true}));
    pg.add(mesh(new THREE.CircleGeometry(r*0.55,24),0x6ab6de,{r:[-Math.PI/2,0,0],p:[0,0.03,0],cast:false}));
    const n=Math.round(r*7); for(let i=0;i<n;i++){ const a=i/n*6.28; pg.add(mesh(G.sphLo,0xb9b2a6,{p:[Math.cos(a)*(r+0.12),0.06,Math.sin(a)*(r+0.12)],s:[rand(.15,.26),rand(.08,.14),rand(.15,.24)]})); }
    for(let i=0;i<Math.round(r*2);i++)pg.add(mesh(new THREE.CircleGeometry(0.22,12),0x6db657,{r:[-Math.PI/2,0,rand(0,6)],p:[rand(-r*0.6,r*0.6),0.035,rand(-r*0.6,r*0.6)],cast:false}));
    for(let i=0;i<Math.round(r*4);i++){ const a=rand(0,6.28); pg.add(mesh(G.cone,0x5e9e48,{p:[Math.cos(a)*(r-0.2),0.3,Math.sin(a)*(r-0.2)],s:[0.03,rand(.5,.8),0.03]})); } }
  // gate with arch sign
''')

# ---------- decor uses bounds ----------
rep("  const h=LV().half; if(decorGroup)scene.remove(decorGroup); decorGroup=new THREE.Group();","  const h=LV().half, B=bnd(); if(decorGroup)scene.remove(decorGroup); decorGroup=new THREE.Group();")
rep("for(let i=0;i<Math.round(h*h*1.4);i++){ const g=new THREE.Group(); g.position.set(rand(-h+.3,h-.3),0,rand(-h+.3,h-.3));","for(let i=0;i<Math.round(Math.min(area()*0.35,900));i++){ const g=new THREE.Group(); const q=rIn(0.3); g.position.set(q.x,0,q.z);")
rep("for(let i=0;i<Math.round(h*h*2);i++){ const g=new THREE.Group(); g.position.set(rand(-h,h),0,rand(-h,h));","for(let i=0;i<Math.round(Math.min(area()*0.5,1300));i++){ const g=new THREE.Group(); const q=rIn(0); g.position.set(q.x,0,q.z);")
rep("  const R=h+11; let placed=0;\n  for(let k=0;k<500&&placed<Math.round(12+h*3);k++){ const x=rand(-R,R),z=rand(-R,R); if(Math.abs(x)<h+1.6&&Math.abs(z)<h+1.6)continue;",
    "  let placed=0;\n  for(let k=0;k<900&&placed<Math.round(12+(B.x1-B.x0+B.z1-B.z0)*0.75);k++){ const x=rand(B.x0-11,B.x1+11),z=rand(B.z0-11,B.z1+11); if(inB(x,z,-1.6))continue;")
rep("const a=rand(0,6.28); const x=Math.cos(a)*(h+rand(1.2,4)), z=Math.sin(a)*(h+rand(1.2,4));\n    if(Math.abs(x)<h+1&&Math.abs(z)<h+1)continue;","const q=outPt(rand(1.2,4)), x=q.x, z=q.z;\n    ")
# outside props follow the rectangle
rep("function outsideDecor(grp,h){","function outsideDecor(grp,h){ const BB=bnd(), X0=BB.x0, X1=BB.x1, Z1=BB.z1;")
rep("pond.position.set(h+4.2,0,h*0.3)","pond.position.set(X1+4.2,0,h*0.3)")
rep("shed.position.set(-h-4.2,0,-h-0.6)","shed.position.set(X0-4.2,0,-h-0.6)")
rep("veg.position.set(-h-3.6,0,h*0.4)","veg.position.set(X0-3.6,0,h*0.4)")
rep("{p:[h+2.6,0.22,-h-2.4]","{p:[X1+2.6,0.22,-h-2.4]")
rep("const a=rand(0,6.28), r=h+rand(1.6,6); grp.add(mesh(G.sphLo,0xb9b2a6,{p:[Math.cos(a)*r,0.08,Math.sin(a)*r]","const q=outPt(rand(1.6,6)); grp.add(mesh(G.sphLo,0xb9b2a6,{p:[q.x,0.08,q.z]")
rep("const a=rand(0,6.28), r=h+rand(0.6,8); const x=Math.cos(a)*r, z=Math.sin(a)*r; if(Math.abs(x)<h+0.3&&Math.abs(z)<h+0.3)continue;","const q=outPt(rand(0.6,8)), x=q.x, z=q.z; if(Math.abs(z-(-h-9.5))<1.4)continue;")
rep("cr.position.set(h+6,0,-h-6)","cr.position.set(X1+6,0,-h-6)")
rep("wb.position.set(-h-7,0,-h-5)","wb.position.set(X0-7,0,-h-5)")
rep("{p:[h*0.5-0.6+i*0.6,0.3,h+4+(i%2)*0.3]","{p:[h*0.5-0.6+i*0.6,0.3,Z1+4+(i%2)*0.3]")
rx(r"  W\.hideSpots=\[.*?\];\n",r'''  W.hideSpots=[{via:[[X1+1.6,-h-1.4]],p:[X1+5.8,h*0.3+0.6]},{via:[[X0-1.4,-h-1.4]],p:[X0-5.2,-h-1.5]},{via:[[X0-1.6,-h-1.4]],p:[X0-4.9,h*0.4+1.7]},{via:[[X1+1.4,-h-1.4]],p:[X1+3.6,-h-3.0]},
    {via:[[X1+1.4,-h-1.4]],p:[X1+6.7,-h-6.7]},{via:[[X0-1.4,-h-1.4]],p:[X0-7.6,-h-4.2]},{via:[[-3,-h-2.4],[-4.4,-h-6.6]],p:[-5.6,-h-7.8]},{via:[[X1+1.6,-h-1.4],[X1+1.8,Z1+2]],p:[h*0.5,Z1+3.4]}];
''')

# ---------- clamps & movement ----------
rx(r"function placeSpot\(minD=1\.4,edge=0\.9\)\{[^\n]*\n","function placeSpot(minD=1.4,edge=0.9){ for(let k=0;k<160;k++){ const q=rIn(edge), x=q.x, z=q.z; if(Math.abs(x)<1&&z<-LV().half+1.2)continue; if(inPond(x,z,1))continue; if(items.every(it=>Math.hypot(it.pos.x-x,it.pos.z-z)>(it.kind==='shelter'?Math.max(minD,2):minD))) return new V3(x,0,z);} const q=rIn(edge); return new V3(q.x,0,q.z); }\n")
rep("function goTo(c,x,z,after,data){ const h=LV().half-0.4; c.target.set(clamp(x,-h,h),0,clamp(z,-h,h));",
    "function goTo(c,x,z,after,data){ let tx=clampX(x,0.4), tz=clampZ(z,0.4); for(const [px,pz,r] of ponds()){ const d=Math.hypot(tx-px,tz-pz); if(d<r+0.5){ const n=d||1; tx=px+(tx-px)/n*(r+0.6); tz=pz+(tz-pz)/n*(r+0.6); } } c.target.set(tx,0,tz);")
rep("    const h=LV().half-0.6; goTo(c,clamp(p.x+rand(-3,3),-h,h),clamp(p.z+rand(-3,3),-h,h),null); return; }",
    "    if(ponds().length&&Math.random()<0.18){ const [px,pz,pr]=pick(ponds()); const a=rand(0,6.28); goTo(c,px+Math.cos(a)*(pr+0.55),pz+Math.sin(a)*(pr+0.55),'pond',{px,pz}); return; }\n    goTo(c,p.x+rand(-3,3),p.z+rand(-3,3),null); return; }")
rep("  if(a==='shelter'){ setState(c,'shelter',rand(5,9)); return; }","  if(a==='shelter'){ setState(c,'shelter',rand(5,9)); return; }\n  if(a==='pond'&&it){ setState(c,'pondwatch',rand(5,10)); c.heading=Math.atan2(it.px-c.g.position.x,it.pz-c.g.position.z); return; }")
rep("    case 'watch': {","    case 'pondwatch': s.fun=Math.min(100,s.fun+dt*0.8); if(Math.random()<dt*0.35){ const a=c.heading+rand(-0.4,0.4); spawnFx('spark',new V3(c.g.position.x+Math.sin(a)*1.2,0.15,c.g.position.z+Math.cos(a)*1.2),2,.15); c.earTw=0.3; } if(c.stT<=0)setState(c,'idle',1); break;\n    case 'watch': {")
rep("if((st==='idle'&&c.sit||st==='watch')&&!moving){","if((st==='idle'&&c.sit||st==='watch'||st==='pondwatch')&&!moving){")
rep("  const cs=active().filter(solid); const h=LV().half-0.35;","  const cs=active().filter(solid);")
rep("      for(const hp of helpers){ const hpp=hp.g.position; for(const cc of catCircles(c)){","      for(const [px,pz,r] of ponds())for(const cc of catCircles(c)){ const dx=cc[0]-px,dz=cc[1]-pz,d=Math.hypot(dx,dz)||0.001,m=cc[2]+r; if(d<m){ c.g.position.x+=dx/d*(m-d); c.g.position.z+=dz/d*(m-d); } }\n      for(const hp of helpers){ const hpp=hp.g.position; for(const cc of catCircles(c)){")
rep("  for(const c of cs){ const p=c.g.position; p.x=clamp(p.x,-h,h); p.z=clamp(p.z,-h,h); }","  for(const c of cs){ const p=c.g.position; p.x=clampX(p.x,0.35); p.z=clampZ(p.z,0.35); }")
rep("  const h=LV().half-0.8; hp.target.set(rand(-h,h),0,rand(-h,h)); hp.task=null;","  const q=rIn(0.8); hp.target.set(q.x,0,q.z); hp.task=null;")
rep("  const h=LV().half-0.2; if(Math.abs(tip.x)>h){ tip.x=Math.sign(tip.x)*h; wand.tipV.x*=-0.5; } if(Math.abs(tip.z)>h){ tip.z=Math.sign(tip.z)*h; wand.tipV.z*=-0.5; }",
    "  { const nx=clampX(tip.x,0.2), nz=clampZ(tip.z,0.2); if(nx!==tip.x){ tip.x=nx; wand.tipV.x*=-0.5; } if(nz!==tip.z){ tip.z=nz; wand.tipV.z*=-0.5; } }")
rep("const h=LV().half; g.position.set(rand(-h,h),rand(.6,1.5),rand(-h,h)); scene.add(g);","const q=rIn(0); g.position.set(q.x,rand(.6,1.5),q.z); scene.add(g);")
rep("function newBfTarget(b){ const h=LV().half+0.5; b.tgt.set(rand(-h,h),rand(.35,1.6),rand(-h,h));","function newBfTarget(b){ const q=rIn(-0.5); b.tgt.set(q.x,rand(.35,1.6),q.z);")
rep("const R=LV().half+14, a=rand(0,6.28);","const R=ext()+14, a=rand(0,6.28);")
rx(r"function birdTarget\(b\)\{.*?\} \}\nfunction birdFlee\(b\)\{[^\n]*\n",r'''function birdTarget(b){ const r=Math.random(), E=ext();
  if(r<0.55){ b.land='ground'; const q=rIn(0.6); b.tgt.set(q.x,0.09,q.z); }
  else if(r<0.85){ b.land='fence'; const fp=fencePt(); b.tgt.set(fp[0],0.82,fp[1]); }
  else { b.land=null; const a=rand(0,6.28); b.tgt.set(Math.cos(a)*(E+16),7,Math.sin(a)*(E+16)); } }
function birdFlee(b){ if(b.state==='fly')return; b.state='fly'; Snd.tweet(); b.land=null; const a=rand(0,6.28), E=ext(); if(Math.random()<0.6){ b.land='fence'; const fp=fencePt(); b.tgt.set(fp[0],0.82,fp[1]); } else b.tgt.set(Math.cos(a)*(E+16),7,Math.sin(a)*(E+16)); }
''')
rep("const h=LV().half-0.5; p.x=clamp(p.x+Math.sin(b.heading)*0.18,-h,h); p.z=clamp(p.z+Math.cos(b.heading)*0.18,-h,h);","p.x=clampX(p.x+Math.sin(b.heading)*0.18,0.5); p.z=clampZ(p.z+Math.cos(b.heading)*0.18,0.5);")
rep("function seedRain(){ const R=LV().half+6;","function seedRain(){ const R=ext()+6;")
rep("function clampTarget(){ const h=LV().half; cam.target.x=clamp(cam.target.x,-h-9,h+9); cam.target.z=clamp(cam.target.z,-h-12,h+6); }","function clampTarget(){ const B=bnd(); cam.target.x=clamp(cam.target.x,B.x0-9,B.x1+9); cam.target.z=clamp(cam.target.z,B.z0-12,B.z1+6); }")
rep("function clampIn(p){ const h=LV().half-0.2; p.x=clamp(p.x,-h,h); p.z=clamp(p.z,-h,h); p.y=0; return p; }","function clampIn(p){ p.x=clampX(p.x,0.2); p.z=clampZ(p.z,0.2); p.y=0; return p; }")
rep("const h=LV().half-0.35; P.cat.g.position.x=clamp(p.x,-h,h); P.cat.g.position.z=clamp(p.z,-h,h);","P.cat.g.position.x=clampX(p.x,0.35); P.cat.g.position.z=clampZ(p.z,0.35);")
rep("it.vel.multiplyScalar(Math.max(0,1-dt*1.4)); const h=LV().half-0.2;\n    if(Math.abs(p.x)>h){ p.x=Math.sign(p.x)*h; it.vel.x*=-0.7; } if(Math.abs(p.z)>h){ p.z=Math.sign(p.z)*h; it.vel.z*=-0.7; }",
    "it.vel.multiplyScalar(Math.max(0,1-dt*1.4));\n    { const nx=clampX(p.x,0.2), nz=clampZ(p.z,0.2); if(nx!==p.x){ p.x=nx; it.vel.x*=-0.7; } if(nz!==p.z){ p.z=nz; it.vel.z*=-0.7; } for(const [px,pz,r] of ponds()){ const dx=p.x-px,dz=p.z-pz,d=Math.hypot(dx,dz)||0.01; if(d<r+0.15){ p.x=px+dx/d*(r+0.15); p.z=pz+dz/d*(r+0.15); it.vel.x*=-0.6; it.vel.z*=-0.6; } } }")
rep("cam.target.set(0,0.3,-1); cam.dist=cam.want=LV().zoom*1.15;","{ const B=bnd(); cam.target.set((B.x0+B.x1)/2,0.3,(B.z0+B.z1)/2-1); } cam.dist=cam.want=LV().zoom*1.15;")

# ---------- expansion: levels 5-8 need homes found ----------
rep("{id:'expand',name:()=>'Bigger meadow',desc:'',cost:()=>LEVELS[W.level+1]?.cost||0,avail:()=>W.level<4,need:()=>W.level+1,buy(){expand();}},",
    "{id:'expand',name:()=>LEVELS[W.level+1]?.name||'Bigger meadow',desc:'',cost:()=>LEVELS[W.level+1]?.cost||0,avail:()=>W.level<LEVELS.length-1,need:()=>Math.min(5,W.level+1),homes:()=>LEVELS[W.level+1]?.homes||0,buy(){expand();}},")
rep("const can=avail&&have<max&&W.money>=cost&&starOk; const lbl=!avail?(it.id==='laser'?'Owned':'Maxed'):have>=max?'Full':!starOk?`★${need} needed`:",
    "const hn=it.homes?it.homes():0, hOk=W.homes.length>=hn; const can=avail&&have<max&&W.money>=cost&&starOk&&hOk; const lbl=!avail?(it.id==='laser'?'Owned':'Maxed'):have>=max?'Full':!starOk?`★${need} needed`:!hOk?`${hn} homes needed`:")
rep("const desc=it.id==='expand'?(LEVELS[W.level+1]?`Room for ${LEVELS[W.level+1].cap} cats`:'Biggest already'):it.desc;",
    "const desc=it.id==='expand'?(LEVELS[W.level+1]?`Room for ${LEVELS[W.level+1].cap} cats${LEVELS[W.level+1].ponds?' \\u00b7 new pond':''}`:'Biggest already'):it.desc;")
rx(r"function expand\(\)\{ const oh=LV\(\)\.half; W\.level\+\+; shiftOutside\(oh-LV\(\)\.half\); buildEnclosure\(\); buildDecor\(\); cam\.want=LV\(\)\.zoom; cam\.target\.set\(0,0\.3,0\);",
   "function expand(){ const oh=LV().half; W.level++; shiftOutside(oh-LV().half); buildEnclosure(); buildDecor(); cam.want=LV().zoom; { const B=bnd(); cam.target.set((B.x0+B.x1)/2,0.3,(B.z0+B.z1)/2); } for(const c of W.cats){ const p=c.g.position; if(!c.outside&&!c.leaving&&inPond(p.x,p.z,0.4)){ const q=rIn(1); p.set(q.x,0,q.z); } } for(const it of items)if(inPond(it.pos.x,it.pos.z,0.8)){ const q=placeSpot(); it.pos.copy(q); }")
rep("toast('Bigger meadow!'); }","toast(LV().name?LV().name+' open!':'Bigger meadow!'); }")

# ---------- badges pay out ----------
rep("if(t>(W.achT[id]||0)){ W.achT[id]=t; Snd.chime(); toast(`★ ${n} · ${TIER_N[t]}`,'badge',3200); }",
    "if(t>(W.achT[id]||0)){ const rw=[0,10,25,60][t]-[0,10,25,60][W.achT[id]||0]; W.achT[id]=t; W.money+=rw; W.earned+=rw; hud(); Snd.chime(); toast(`★ ${n} · ${TIER_N[t]} +$${rw}`,'badge',3400); }")
rep("openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3>${tabs}${body}`);","openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3>${tabs}${tab==='badges'?`<p style=\"margin:-4px 0 10px;color:var(--muted);font:700 13px var(--body)\">Bronze +$10 \\u00b7 Silver +$25 \\u00b7 Gold +$60. Gold badges unlock special collars.</p>`:''}${body}`);")

# ---------- special collars ----------
rep("function setCollar(c,col){ if(c.collarM){ c.core.remove(c.collarM); c.collarM=null; } c.collar=col||null; if(!col)return;\n  const g=new THREE.Group(); g.position.set(0,0.06,0.42); g.rotation.x=-Math.PI/2+0.35;\n  const ring=mesh(new THREE.TorusGeometry(0.245,0.036,8,28),col,{}); g.add(ring); g.add(mesh(G.sph,0xf6c443,{p:[0,-0.28,0.03],s:[0.05,0.05,0.05]}));",
r'''const SPECIAL=[{id:'rainbow',name:'Rainbow',gold:1,css:'conic-gradient(#ff6b6b,#ffa94d,#ffe066,#8ce99a,#74c0fc,#b197fc,#ff6b6b)'},{id:'starry',name:'Starry',gold:3,css:'radial-gradient(circle at 35% 35%,#ffe066 0 12%,#24305e 13%)'},{id:'blossom',name:'Blossom',gold:6,css:'radial-gradient(circle,#fff 0 22%,#ff9ec7 23%)'}];
function golds(){ return Object.values(W.achT).filter(t=>t>=3).length; }
function setCollar(c,col){ if(c.collarM){ c.core.remove(c.collarM); c.collarM=null; } c.collar=col||null; if(!col)return;
  const g=new THREE.Group(); g.position.set(0,0.06,0.42); g.rotation.x=-Math.PI/2+0.35;
  const base=col==='rainbow'?0xffffff:col==='starry'?0x24305e:col==='blossom'?0x8ce99a:col;
  const ring=mesh(new THREE.TorusGeometry(0.245,0.036,8,28),base,{}); g.add(ring); g.add(mesh(G.sph,col==='blossom'?0xff9ec7:0xf6c443,{p:[0,-0.28,0.03],s:[0.05,0.05,0.05]}));
  if(typeof col==='string'){ const beads=col==='rainbow'?[0xff6b6b,0xffa94d,0xffe066,0x8ce99a,0x74c0fc,0xb197fc]:col==='starry'?[0xffe066]:[0xff9ec7,0xffffff];
    for(let i=0;i<12;i++){ const a=i/12*6.28; g.add(mesh(G.sph,beads[i%beads.length],{p:[Math.cos(a)*0.245,Math.sin(a)*0.245,0.03],s:[0.032,0.032,0.032],cast:false})); } }''')
rep("function openCollars(){ openModal(`<h3>Choose a collar</h3><p style=\"margin:0 0 8px;color:var(--muted);font:700 14px var(--body)\">$15, then tap a cat to put it on.</p><div class=\"sw\">${COLLARS.map(col=>`<button data-col=\"${col}\" style=\"background:#${col.toString(16).padStart(6,'0')}\" aria-label=\"Collar color\"></button>`).join('')}</div>`);\n  document.querySelectorAll('[data-col]').forEach(b=>b.onclick=()=>{ if(W.money<15)return; W.money-=15; W.collarPick=+b.dataset.col; hud(); closeModal(); toast('Tap a cat to give it the collar'); }); }",
r'''function openCollars(){ const g=golds();
  openModal(`<h3>Choose a collar</h3><p style="margin:0 0 8px;color:var(--muted);font:700 14px var(--body)">$15, then tap a cat to put it on.</p><div class="sw">${COLLARS.map(col=>`<button data-col="${col}" style="background:#${col.toString(16).padStart(6,'0')}" aria-label="Collar color"></button>`).join('')}</div>
  <p style="margin:12px 0 6px;color:var(--muted);font:700 14px var(--body)">Special collars ($30), unlocked by gold badges (you have ${g}):</p><div class="sw">${SPECIAL.map(sp=>`<button data-sp="${sp.id}" ${g>=sp.gold?'':'disabled'} title="${sp.name}${g>=sp.gold?'':' · '+sp.gold+' gold'}" style="background:${sp.css};${g>=sp.gold?'':'opacity:.35;filter:grayscale(1)'}" aria-label="${sp.name} collar"></button>`).join('')}</div>`);
  const pickC=(col,price)=>{ if(W.money<price)return; W.money-=price; W.collarPick=col; W.collarPrice=price; hud(); closeModal(); toast('Tap a cat to give it the collar'); };
  document.querySelectorAll('[data-col]').forEach(b=>b.onclick=()=>pickC(+b.dataset.col,15));
  document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>pickC(b.dataset.sp,30)); }''')
rep("if(W.collarPick){ W.money+=15; W.collarPick=null; hud(); toast('Collar returned: $15 back'); }","if(W.collarPick){ const pr=W.collarPrice||15; W.money+=pr; W.collarPick=null; hud(); toast(`Collar returned: $${pr} back`); }")

# ---------- guide ----------
rep("Stars unlock bigger meadows and item upgrades (cat castle, fountain, sunroom...).</li><li>Badges have bronze, silver and gold.",
    "Stars unlock bigger meadows and item upgrades (cat castle, fountain, sunroom...).</li><li>At 5 stars the sanctuary keeps growing: new wings with ponds open as you find more cats homes (3, 6, 10, 16 homes).</li><li>Badges have bronze, silver and gold, and pay $10 / $25 / $60. Gold badges unlock special collars (rainbow, starry, blossom).")
open(p,'w',encoding='utf-8').write(s); print('v6 patch ok')
