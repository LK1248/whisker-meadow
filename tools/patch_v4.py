"""One-off patch: v3 -> v4 fixes (boop spacing, family stuck/expansion, helper wages, runaway hunt)."""
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old); assert n==cnt,(n,old[:90]); s=s.replace(old,new)
def rx(pat,new):
    global s
    s2,n=re.subn(pat,lambda m:new,s,count=1,flags=re.S); assert n==1,('RX',pat[:90]); s=s2

# 1. nose boop / lick spacing (heads no longer intersect)
rep("want=0.95*(c.g.scale.x+o.g.scale.x)/2;","want=(c.boopKind==='lick'?1.32:1.56)*(c.g.scale.x+o.g.scale.x)/2;")

# 2. family: petting/tapping can no longer hijack a cat on its way to the gate
rep("if(c.away>0||c.carried||c.leaveT>0||c.outside||c.leaving||c.state==='boop')return;","if(c.away>0||c.carried||c.leaveT>0||c.outside||c.leaving||['boop','path','greet','bye'].includes(c.state))return;")
rep("function buttTap(c){ if(c.away>0||c.carried||c.outside||c.leaving)return;","function buttTap(c){ if(c.away>0||c.carried||c.outside||c.leaving||['path','greet','bye'].includes(c.state))return;")
rx(r"function renderFamily\(msg\)\{.*?\nfunction pickForHome",r'''function renderFamily(msg,noX){ const f=W.family, el=$('#family'); if(!f){ el.hidden=true; return; } el.hidden=false;
  const x=noX?'':'<button class="fx" id="fX" aria-label="Send them off">&times;</button>';
  if(msg) el.innerHTML=`${x}<div class="fam">${FAM_SVG}<div class="want">${msg}</div></div>`;
  else if(W.pickHome){ el.innerHTML=`${x}<div class="fam">${FAM_SVG}<div><div class="want">Tap a cat</div><div class="sub">one with a little house</div></div></div><div class="fb"><button id="fCancel">Back</button></div>`; $('#fCancel').onclick=()=>{ W.pickHome=false; renderFamily(); }; }
  else { el.innerHTML=`${x}<div class="fam">${FAM_SVG}<div><div class="sub">The ${f.name} family would love</div><div class="want">${tsvg(f.want)} a ${f.want} cat</div></div></div><div class="fb"><button id="fNo">Not now</button><button class="go" id="fPick">Pick a cat</button></div>`;
    $('#fPick').onclick=()=>{ if(!W.cats.some(readyHome)){ renderFamily('No one is ready yet'); setTimeout(()=>{ if(W.family&&W.family.state!=='leaving')renderFamily(); },1800); return; } W.pickHome=true; renderFamily(); }; $('#fNo').onclick=()=>familyLeave("We'll come back!"); }
  const bx=$('#fX'); if(bx)bx.onclick=()=>familyLeave('Maybe another day!'); }
function pickForHome''')
rep("function familyLeave(msg){ const f=W.family; if(!f||f.state==='leaving'||f.state==='bye')return; W.pickHome=false; renderFamily(msg);","function familyLeave(msg){ const f=W.family; if(!f||f.state==='leaving'||f.state==='bye')return; W.pickHome=false; renderFamily(msg,true);")
rep("""renderFamily(f.cats.length>1?`Welcome home, ${c.name} &amp; ${fr.name}!`:`Welcome home, ${c.name}!`);""","""renderFamily(f.cats.length>1?`Welcome home, ${c.name} &amp; ${fr.name}!`:`Welcome home, ${c.name}!`,true);""")
rep("  else { f.t+=dt;\n","  else { f.t+=dt;\n    if(f.state==='walking'&&f.cat&&f.cat.state!=='path'){ f.state='wait'; f.cat=null; renderFamily(); }\n    if(W.pickHome&&!W.cats.some(readyHome)){ W.pickHome=false; renderFamily(); }\n    if(!['bye','leaving'].includes(f.state)&&f.t>150)familyLeave(\"We'll come back!\");\n")
rep("#family .fb .go{background:var(--leaf);color:#fff}","#family .fb .go{background:var(--leaf);color:#fff}\n#family .fx{position:absolute;right:8px;top:8px;width:32px;height:32px;border-radius:50%;background:#f3e7d6;font:700 18px/1 var(--display)}\n#family .fam{padding-right:26px}")

# 2b. expanding the meadow while a family (or runaway) is at the gate
rep("function expand(){ W.level++; buildEnclosure();","function expand(){ const oh=LV().half; W.level++; shiftOutside(oh-LV().half); buildEnclosure();")
rep("function readyHome(c){",r'''function shiftOutside(dz){
  const f=W.family; if(f){ for(const m of f.members){ m.g.position.z+=dz; m.target.z+=dz; } }
  for(const c of W.cats){ if(c.outside&&W.runaway&&W.runaway.c===c)continue; if(c.leaving||['path','greet','bye'].includes(c.state)){ c.g.position.z+=dz; if(c.path)c.path.forEach(v=>v.z+=dz); } }
  if(W.runaway){ const c=W.runaway.c; clearTrail(); c.outside=false; c.path=null; c.pathEnd=null; c.g.position.set(0,0,-LV().half+2); setState(c,'idle',2); W.runaway=null; $('#missing').hidden=true; floatWorld(c.g.position.clone().setY(1.2),'Home safe'); }
}
function readyHome(c){''')

# 3. helper wages
rep("{id:'helper',name:()=>'Helper',desc:'Feeds, scoops, pets',","{id:'fire',name:()=>'Fewer helpers',desc:'Saves wages',cost:()=>0,buy(){ const hp=helpers.pop(); if(hp){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; scene.remove(hp.g); } }},\n  {id:'helper',name:()=>'Helper',desc:'Feeds, scoops, pets \\u00b7 $6/min wage',")
rep("  const cards=SHOP.map(it=>{ const avail","  const cards=SHOP.filter(it=>it.id!=='fire'||helpers.length).map(it=>{ const avail")
rep(":!starOk?`★${need} needed`:`$${cost}`;",":!starOk?`★${need} needed`:it.id==='fire'?'Let one go':`$${cost}`;")
rep("  helper:'<circle","  fire:'<circle cx=\"12\" cy=\"7\" r=\"4\" fill=\"#f6d2b4\"/><path d=\"M5 21c0-5 3-8 7-8s7 3 7 8z\" fill=\"#c9b8a6\"/>',\n  helper:'<circle")
rep("function updateHelper(hp,dt,t){\n  const p=hp.g.position; hp.t-=dt;","function updateHelper(hp,dt,t){\n  const p=hp.g.position; hp.t-=dt;\n  if(W.unpaid&&hp.state!=='idle'){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; hp.task=null; hp.state='idle'; }\n  if(W.unpaid)hp.t=Math.max(hp.t,1);")
rep("  updateBoops(dt);\n","  updateBoops(dt);\n  W.payT=(W.payT??30)-dt; if(W.payT<=0){ W.payT=30; const cost=helpers.length*3; if(cost){ if(W.money>=cost){ W.money-=cost; if(W.unpaid)toast('Helpers back to work'); W.unpaid=false; floatAt(70,62,'-$'+cost+' wages'); hud(); } else { if(!W.unpaid)toast('Not enough for wages: helpers are resting'); W.unpaid=true; } } else W.unpaid=false; }\n")

# 4. runaway hunt: farther hiding spots, delayed notice, early catch
rep("coatsMax:0,butt:0}};","coatsMax:0,butt:0,quick:0}};")
rep("['found','Welcome Home','Runaways found',()=>W.stat.found,[1,3,8]],","['found','Welcome Home','Runaways found',()=>W.stat.found,[1,3,8]],['quick','Quick Paws','Caught a runaway at the gate',()=>W.stat.quick||0,[1,3,6]],")
rep("  for(let i=0;i<5;i++)grp.add(mesh(G.cyl,0xcfc6b8,",r'''  // farther props: crates, wheelbarrow, big tree with a tire swing, bushes behind the meadow
  const cr=new THREE.Group(); cr.position.set(h+6,0,-h-6); grp.add(cr); cr.add(mesh(G.box,0xc99a6b,{p:[0,0.3,0],s:[0.6,0.6,0.6]})); cr.add(mesh(G.box,0xb58b63,{p:[0.65,0.25,0.1],s:[0.5,0.5,0.5],r:[0,0.3,0]})); cr.add(mesh(G.box,0xd9b48a,{p:[0.2,0.82,0],s:[0.45,0.45,0.45],r:[0,0.6,0]}));
  const wb=new THREE.Group(); wb.position.set(-h-7,0,-h-5); wb.rotation.y=0.8; grp.add(wb); wb.add(mesh(G.box,0x7fb2e5,{p:[0,0.42,0],s:[0.7,0.25,0.5]})); wb.add(mesh(new THREE.TorusGeometry(0.16,0.05,8,16),0x3d3532,{p:[0.42,0.18,0],r:[0,0,0]})); for(const sz of [-0.2,0.2])wb.add(mesh(G.cyl,0x9b6b43,{p:[-0.55,0.4,sz],s:[0.03,0.6,0.03],r:[0,0,1.2]}));
  const bt=treeMesh(1.7); bt.position.set(-2.5,0,-h-9); grp.add(bt); grp.add(mesh(G.cyl,0xd9c3a3,{p:[-1.6,1.6,-h-9],s:[0.015,1.6,0.015],cast:false})); grp.add(mesh(new THREE.TorusGeometry(0.28,0.1,8,18),0x3d3532,{p:[-1.6,0.75,-h-9],r:[0,1.2,0]}));
  for(let i=0;i<3;i++)grp.add(mesh(G.sphLo,pick([0x6db657,0x7fc463]),{p:[h*0.5-0.6+i*0.6,0.3,h+4+(i%2)*0.3],s:[0.6,0.5,0.55]}));
  W.hideSpots=[{via:[[h+1.6,-h-1.4]],p:[h+5.8,h*0.3+0.6]},{via:[[-h-1.4,-h-1.4]],p:[-h-5.2,-h-1.5]},{via:[[-h-1.6,-h-1.4]],p:[-h-4.9,h*0.4+1.7]},{via:[[h+1.4,-h-1.4]],p:[h+3.6,-h-3.0]},
    {via:[[h+1.4,-h-1.4]],p:[h+6.7,-h-6.7]},{via:[[-h-1.4,-h-1.4]],p:[-h-7.6,-h-4.2]},{via:[[-3,-h-2.4],[-3.2,-h-8]],p:[-1.6,-h-9.5]},{via:[[h+1.6,-h-1.4],[h+1.8,h+2]],p:[h*0.5,h+3.4]}];
  for(let i=0;i<5;i++)grp.add(mesh(G.cyl,0xcfc6b8,''')
rx(r"function runaway\(c\)\{.*?\nfunction renderMissing",r'''function runaway(c){ const h=LV().half; const sp=pick(W.hideSpots||[{p:[1.6,-h-2.6]}]);
  const pts=[new V3(0,0,-h+0.5),new V3(0,0,-h-0.7)]; (sp.via||[]).forEach(v=>pts.push(new V3(v[0],0,v[1]))); pts.push(new V3(sp.p[0],0,sp.p[1]));
  c.outside=true; if(tag.c===c)tag.c=null; walkPath(c,pts.map(v=>v.clone()),'hide',1.3); c.flick=1;
  if(!pawMat)pawMat=new THREE.MeshBasicMaterial({map:iconTexture('paw'),transparent:true,depthWrite:false});
  const trail=[]; let i=0;
  for(let s=2;s<pts.length;s++){ const a=pts[s-1], b=pts[s], L=a.distanceTo(b), dir=b.clone().sub(a).normalize(), side=new V3(-dir.z,0,dir.x);
    for(let d=0.25;d<L-0.25;d+=0.4,i++){ const m=new THREE.Mesh(pawGeo,pawMat); m.rotation.x=-Math.PI/2; m.rotation.z=Math.PI-Math.atan2(dir.x,dir.z); const q=a.clone().addScaledVector(dir,d).addScaledVector(side,i%2?0.08:-0.08); m.position.set(q.x,0.015,q.z); scene.add(m); trail.push(m); } }
  W.runaway={c,t:0,trail,pts,trailMid:pts[1].clone().setY(0.1),looking:false,notified:false}; W.lastRun=W.time; }
function caughtEarly(c){ W.stat.quick=(W.stat.quick||0)+1; c.s.trust=Math.min(100,c.s.trust+2); spawnFx('h',c.g.position.clone().setY(0.9),3,.3); Snd.chirp(); floatWorld(c.g.position.clone().setY(1.2),'Got you!'); comeHome(c); }
function renderMissing''')
rx(r"function comeHome\(c\)\{.*?\n// ---- adoption ----",r'''function comeHome(c){ const R=W.runaway, h=LV().half; clearTrail(); $('#missing').hidden=true; let back=[];
  if(R&&R.pts){ const reached=R.pts.length-(c.pathEnd==='hide'&&c.path?c.path.length:0); back=R.pts.slice(0,Math.max(0,reached)).reverse().map(v=>v.clone()); }
  if(!back.length)back=[new V3(0,0,-h+0.6)]; back.push(new V3(rand(-1,1),0,-h+2)); walkPath(c,back,'home',1.0); }
// ---- adoption ----''')
rep("if(c.state==='hiding')foundCat(c); else if(W.pickHome)","if(c.state==='hiding')foundCat(c); else if(W.runaway&&W.runaway.c===c&&!W.runaway.notified&&c.pathEnd==='hide')caughtEarly(c); else if(W.pickHome)")
rep("    if(R.t>150&&c.state==='hiding')comeHome(c); }","    if(!R.notified&&c.pathEnd==='hide'&&(R.t>7||dist2(c.g.position,new V3(0,0,-LV().half))>4.5)){ R.notified=true; renderMissing(); toast(c.name+' slipped out!'); Snd.meow(0.95,0.6); }\n    if(R.t>180&&c.state==='hiding')comeHome(c); }")
rep("const d=dist2(cam.target,c.g.position); const vol=clamp(1-d/12,0.06,1);","const d=dist2(cam.target,c.g.position); const vol=clamp(1-d/14,0.05,1);")
rep("cam.target.x=clamp(cam.target.x,-h-6,h+6); cam.target.z=clamp(cam.target.z,-h-9,h+2);","cam.target.x=clamp(cam.target.x,-h-9,h+9); cam.target.z=clamp(cam.target.z,-h-12,h+6);")
open(p,'w',encoding='utf-8').write(s); print('v4 patch ok')
