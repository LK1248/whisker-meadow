"""v56: everyday snapshots, live from the sanctuary.
Candid photos are taken automatically when something worth a picture happens: zoomies, a pounce at its peak,
a herd following the wand or laser, a nap pile, a boop, a belly flop, a cat up the cat tree, a kitten with a grown-up,
cats sheltering from rain, a shared meal, pond watching, a night-time cuddle, a big group. Some achievements also
take a photo of their moment.
- Framing is between staged and honest: the camera aims at the cats in the moment, sizes the frame to fit them,
  tries 16 angles, and scores each on faces toward the lens, things in the way, light direction and lead room.
  It then adds a little handheld tilt on action shots. Jumps are caught at the top of the leap.
- Each kind of moment is one card in a 13-card album, so the collection shows what has been seen. A later,
  better moment of the same kind (more cats, or tied to an achievement) can replace an old photo now and then.
- Photos are pinned on the corkboard with the adoption postcards, and listed in the card wall under the postcards,
  with empty slots for the moments still to come. Each new photo plays a shutter sound and shows a small polaroid toast.
- Quiet during tutorials and the first goodbye; at most one photo every ~2.5 min.
- New achievement: Photo Album (3/7/11 moments).
- Groomed sheen a little more visible (still soft, no wet highlight)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- sheen: a touch stronger ----------
rep("' reflectedLight.directDiffuse += directLight.color*tint*(pow(nh,8.0)*0.1+rim*nl*0.16);'",
    "' reflectedLight.directDiffuse += directLight.color*tint*(pow(nh,8.0)*0.17+rim*nl*0.26);'")

# ---------- CSS ----------
rep(".toast.badge{background:linear-gradient(#ffe48a,#f6c443);color:#5a3d00}",
    ".toast.badge{background:linear-gradient(#ffe48a,#f6c443);color:#5a3d00}\n"
    ".toast.snap{background:#fff;padding:6px 6px 14px;border-radius:4px;transform:rotate(-3deg);box-shadow:0 6px 18px rgba(0,0,0,.3);animation:snapIn .5s ease-out}\n"
    ".toast.snap img{display:block;width:132px;height:99px;object-fit:cover;border-radius:2px}\n"
    "@keyframes snapIn{0%{transform:translateY(-30px) rotate(8deg) scale(.6);opacity:0}100%{transform:rotate(-3deg);opacity:1}}\n"
    "#snapFlash{position:fixed;inset:0;background:#fff;pointer-events:none;z-index:6;opacity:0;transition:opacity .45s}\n"
    ".albumH{display:flex;align-items:center;gap:8px;margin:16px 0 8px;font:700 19px var(--display)}\n"
    ".pc.snap img{aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:4px;display:block}\n"
    ".pc.snap .k{position:absolute;right:8px;bottom:8px;font-size:20px;line-height:1;filter:drop-shadow(0 1px 2px rgba(0,0,0,.4))}\n"
    ".pc.empty{background:rgba(255,255,255,.18);border:2px dashed rgba(255,255,255,.6);box-shadow:none;display:flex;align-items:center;justify-content:center;aspect-ratio:4/3.4;font-size:30px;opacity:.75;cursor:default}\n"
    ".snapBig{background:#fff;padding:10px 10px 18px;border-radius:6px;box-shadow:0 6px 20px rgba(74,52,38,.25);transform:rotate(-1deg);text-align:center}\n"
    ".snapBig img{width:100%;display:block;border-radius:3px}.snapBig .k{font-size:26px;margin-top:8px;display:block}")

# ---------- the snapshot system (placed before the card wall code) ----------
rep("// ---- adoption card wall: thank-you postcards pinned on a corkboard by the house ----",
r"""// ---- everyday snapshots: candid photos of the live sanctuary, pinned with the postcards ----
const SNAP_KEY='wm_snaps';
const SNAP_KINDS={zoomies:'💨',pounce:'⚡',herd:'🐾',nap:'💤',boop:'😽',flop:'🙃',perch:'🌳',kittens:'🍼',rain:'☔',feast:'🍽️',pond:'🐟',night:'🌙',crowd:'📸'};
// camera elevation range per moment (radians) and whether it's an action shot (low, a little handheld tilt, three-quarter view)
const SNAP_EL={pounce:[0.1,0.22,1],zoomies:[0.14,0.28,1],herd:[0.5,0.65,0],nap:[0.6,0.85,0],night:[0.45,0.6,0],boop:[0.12,0.24,0],flop:[0.75,0.95,0],perch:[0.12,0.25,0],kittens:[0.25,0.4,0],rain:[0.3,0.42,0],feast:[0.4,0.55,0],pond:[0.22,0.35,0],crowd:[0.5,0.62,0]};
let SNAPS=store.get(SNAP_KEY)||[], snapCD=60, snapScanT=1, snapPend=null, snapWant=null;
const snapCam=new THREE.PerspectiveCamera(40,4/3,0.1,300), snapRay=new THREE.Raycaster();
function snapSave(){ let L=SNAPS.slice(); for(let i=0;i<4;i++){ try{ localStorage.setItem(SNAP_KEY,JSON.stringify(L)); return; }catch(e){ L=L.slice(0,-1); } } }
function snapHave(k){ return SNAPS.find(s=>s.k===k); }
function snapOk(){ return W.started&&!W.paused&&$('#modal').hidden&&!tutQuiet()&&!firstBye()&&!intro.c; }
const snapFree=c=>c.g.visible&&!c.outside&&!c.leaving&&!c.carried&&!(c.away>0);
function snapNear(c,list,r){ return list.filter(o=>o!==c&&dist2(o.g.position,c.g.position)<r); }
// what's worth a photo right now: [{k, cats, score, wait}]
function snapMoments(){ const A=W.cats.filter(snapFree), out=[], by=st=>A.filter(c=>c.state===st);
  for(const c of A)if(c.hopT>0&&(c.lunge>0||['pounce','chase','laser'].includes(c.state))){ const w=snapNear(c,A,2.2).filter(o=>['chase','laser','watch','idle','stalk'].includes(o.state)).slice(0,2); out.push({k:'pounce',cats:[c,...w],score:3,wait:()=>!(c.hopT>0)||c.hopT<=c.hopDur*0.55}); break; }
  const romp=by('romp'); if(romp.length>=2){ const a=romp[0], b=a.rompP&&romp.includes(a.rompP)?a.rompP:romp[1]; out.push({k:'zoomies',cats:[a,b],score:3,wait:()=>a.hopT>0||b.hopT>0}); }
  const sleepy=A.filter(c=>c.state==='sleep'||(c.state==='idle'&&c.sit&&W.night>0.5)); for(const c of sleepy){ const g=[c,...snapNear(c,sleepy,1.6)]; if(g.length>=2){ out.push({k:W.night>0.5?'night':'nap',cats:g.slice(0,4),score:2+g.length*0.3}); break; } }
  const fl=by('flop'); if(fl.length){ const c=fl[0]; out.push({k:'flop',cats:[c,...snapNear(c,A,1.6).slice(0,1)],score:1.5}); }
  const pe=by('perch'); if(pe.length)out.push({k:'perch',cats:[pe[0]],score:1.6,perch:true});
  for(const c of A)if(c.age<1){ const big=snapNear(c,A,1.4).filter(o=>o.age>=1); if(big.length){ const m=big.find(o=>o===c.mother)||big[0]; out.push({k:'kittens',cats:[c,m],score:2}); break; } }
  if(weather.raining){ const sh=by('shelter'); if(sh.length)out.push({k:'rain',cats:sh.slice(0,4),score:2+sh.length*0.2}); }
  const eat=by('eat'); if(eat.length>=2)out.push({k:'feast',cats:eat.slice(0,4),score:1.5+eat.length*0.3});
  const pw=by('pondwatch'); if(pw.length)out.push({k:'pond',cats:pw.slice(0,2),score:1.5});
  if(A.length>=6){ let best=null; for(const c of A){ const g=[c,...snapNear(c,A,2.4)]; if(!best||g.length>best.length)best=g; } if(best&&best.length>=4)out.push({k:'crowd',cats:best.slice(0,6),score:1+best.length*0.15}); }
  return out; }
// a moment handed in by the game itself (a boop, a herd): taken shortly after if nothing is in the way
function snapHint(k,cats,delay=0.3){ if(snapPend||!snapOk())return; const fresh=!snapHave(k); if(snapCD>0&&!(fresh&&snapCD<40)&&!(snapWant&&snapWant.k===k))return; snapPend={k,cats:cats.filter(snapFree),t:W.time+delay,ach:snapWant&&snapWant.k===k?snapWant.ach:null}; }
const SNAP_ACH={herd:'herd',zoomies:'pounce',belly:'flop',kittens:'kittens',family:'crowd',rescues:'crowd'};
function snapAch(id){ if(SNAP_ACH[id])snapWant={k:SNAP_ACH[id],ach:id,until:W.time+25}; }
function snapTick(dt){ snapCD-=dt; if(snapWant&&W.time>snapWant.until)snapWant=null;
  if(snapPend){ const p=snapPend; if(!snapOk()||p.cats.length===0||!p.cats.every(snapFree)){ snapPend=null; return; }
    if(W.time>=p.t&&(!p.wait||p.wait()||W.time>p.t+0.9)){ snapPend=null; snapTake(p.k,p.cats,p.ach); } return; }
  snapScanT-=dt; if(snapScanT>0||!snapOk())return; snapScanT=0.5;
  const want=snapWant&&snapWant.k; if(snapCD>0&&!want)return;
  let best=null; for(const m of snapMoments()){ const had=snapHave(m.k); let sc=m.score+(had?0:4)+(m.k===want?20:0);
    if(had&&m.k!==want){ if(W.time-had.at<480||m.cats.length<=(had.n||1)&&Math.random()<0.7)continue; }
    if(snapCD>0&&m.k!==want)continue; sc+=Math.random(); if(!best||sc>best.sc)best={...m,sc}; }
  if(!best)return; snapPend={k:best.k,cats:best.cats,t:W.time,wait:best.wait,ach:best.k===want?snapWant.ach:null,perch:best.perch}; if(best.k===want)snapWant=null; }
function snapNow(){ const m=snapMoments(); const p=m.length?m[0]:{k:'crowd',cats:W.cats.filter(snapFree).slice(0,6)}; if(p.cats.length)snapTake(p.k,p.cats,null); }
// is anything (not one of the subjects) between the camera and this point?
function snapBlocked(from,to,skip){ const d=to.clone().sub(from), len=d.length(); snapRay.set(from,d.normalize()); snapRay.far=len-0.25; snapRay.camera=camera;
  for(const h of snapRay.intersectObjects(scene.children,true)){ let o=h.object, vis=true, sub=false; if(o.isSprite||o.isPoints||o.isLine)continue;
    const m=o.material; if(m&&(m.opacity<0.3||m.visible===false))continue;
    for(let q=o;q;q=q.parent){ if(!q.visible){ vis=false; break; } if(skip.has(q)){ sub=true; break; } }
    if(vis&&!sub)return true; }
  return false; }
// pick the camera: fit the cats in a 4:3 frame, try 16 angles, score faces / blockers / light / lead room
function snapFrame(cats,k,perch){ const pts=cats.map(c=>c.g.position.clone().setY((c.hopT>0||perch?c.g.position.y:0)+0.32*c.g.scale.y)), sc0=Math.max(...cats.map(c=>c.g.scale.x));
  const ctr=pts.reduce((a,p)=>a.add(p),new V3()).multiplyScalar(1/pts.length); let R=0.85*sc0; for(const p of pts)R=Math.max(R,p.distanceTo(ctr)+0.7*sc0);
  if(perch){ R=Math.max(R,ctr.y*0.55+0.3); ctr.y=ctr.y*0.62; }
  const e=SNAP_EL[k]||[0.25,0.45,0], el=rand(e[0],e[1]), act=!!e[2], hf=(cats.length>2?46:38)*Math.PI/180;
  const dist=Math.max(1.9, R/(Math.tan(hf/2)*0.75)*1.15), skip=new Set(cats.map(c=>c.g)), sunAz=Math.atan2(sun.position.x,sun.position.z);
  const heads=cats.slice(0,4).flatMap(c=>{ c.g.updateMatrixWorld(true); return [c.head.getWorldPosition(new V3()),c.g.position.clone().setY(c.g.position.y+0.22*c.g.scale.y),c.g.position.clone().setY(c.g.position.y+0.06)]; }); let best=null;
  for(let i=0;i<16;i++){ const az=i/16*Math.PI*2+rand(-0.08,0.08); const dir=new V3(Math.sin(az)*Math.cos(el),Math.sin(el),Math.cos(az)*Math.cos(el)); const pos=ctr.clone().addScaledVector(dir,dist); if(pos.y<0.25)pos.y=0.25;
    let s=0, wsum=0; cats.slice(0,6).forEach((c,j)=>{ const f=Math.sin(c.heading)*Math.sin(az)+Math.cos(c.heading)*Math.cos(az), wt=j===0?2:1; wsum+=wt; s+=wt*(act?1-Math.abs(f-0.45)*1.2:(f>0?f*1.3:f*0.5)); });
    s/=wsum; s+=0.35*Math.cos(az-sunAz); heads.forEach((h,j)=>{ if(snapBlocked(pos,h,skip))s-=j<3?[3,2,0.5][j]:[1.2,0.8,0.3][j%3]; });
    if(!inB(pos.x,pos.z,0.2))s-=1.2; s+=rand(0,0.25); if(!best||s>best.s)best={s,az,pos}; }
  // lead room: put space in front of the main cat
  const az=best.az, right=new V3(Math.cos(az),0,-Math.sin(az)), lead=cats[0], hv=new V3(Math.sin(lead.heading),0,Math.cos(lead.heading)), side=hv.dot(right);
  const at=ctr.clone().addScaledVector(right,side*0.2*dist*Math.tan(hf/2)); if(el>0.4)at.y-=0.05;
  return {pos:best.pos,at,hf,roll:act?rand(-0.06,0.06):rand(-0.015,0.015)}; }
function snapTake(k,cats,ach){ try{
  const f=snapFrame(cats,k,k==='perch'), cv0=renderer.domElement, W0=cv0.width, H0=cv0.height, cw=Math.min(W0,H0*4/3), ch=cw*0.75;
  const hfFull=2*Math.atan(Math.tan(f.hf/2)*W0/cw); snapCam.aspect=W0/H0; snapCam.fov=2*Math.atan(Math.tan(hfFull/2)/snapCam.aspect)*180/Math.PI; snapCam.updateProjectionMatrix();
  snapCam.position.copy(f.pos); snapCam.up.set(0,1,0); snapCam.lookAt(f.at); snapCam.rotateZ(f.roll);
  const ics=[...W.cats.map(c=>c.icon),...items.map(it=>it.icon)].filter(Boolean), iv=ics.map(o=>o.visible); ics.forEach(o=>o.visible=false);
  renderer.render(scene,snapCam); ics.forEach((o,i)=>o.visible=iv[i]);
  const out=document.createElement('canvas'); out.width=400; out.height=300; const x=out.getContext('2d'); x.filter=`saturate(1.08) contrast(1.04) brightness(${(1+0.45*W.night).toFixed(2)})`;
  x.drawImage(cv0,(W0-cw)/2,(H0-ch)/2,cw,ch,0,0,400,300); x.filter='none';
  const g=x.createRadialGradient(200,150,110,200,150,260); g.addColorStop(0,'rgba(40,20,10,0)'); g.addColorStop(1,'rgba(40,20,10,.32)'); x.fillStyle=g; x.fillRect(0,0,400,300);
  x.globalCompositeOperation='soft-light'; x.fillStyle='rgba(255,190,120,.16)'; x.fillRect(0,0,400,300); x.globalCompositeOperation='source-over';
  const img=out.toDataURL('image/jpeg',0.82), rec={k,img,at:W.time,n:cats.length,ach:ach||null,id:Date.now()};
  const i=SNAPS.findIndex(s=>s.k===k), fresh=i<0; if(i>=0)SNAPS.splice(i,1); SNAPS.unshift(rec); snapSave();
  snapCD=rand(130,170); Snd.shutter(); const fl=$('#snapFlash'); fl.style.transition='none'; fl.style.opacity=0.55; void fl.offsetWidth; fl.style.transition=''; fl.style.opacity=0;
  toast(`<img src="${img}" alt="">`,'snap',3200); boardPop(); W.stat.snaps=Math.max(W.stat.snaps||0,SNAPS.length);
  return rec; }catch(e){ console.error(e); return null; } }
// ---- adoption card wall: thank-you postcards pinned on a corkboard by the house ----""")
rep("<div id=\"toasts\"></div>", "<div id=\"toasts\"></div><div id=\"snapFlash\"></div>") if "<div id=\"toasts\"></div>" in s else None

# ---------- corkboard: postcards and snapshots together ----------
rep("function wallCards(){ return W.homes.map((hm,i)=>({hm,i})).filter(o=>cardOn(o.hm,o.i)).reverse(); }",
    "function wallCards(){ return W.homes.map((hm,i)=>({hm,i})).filter(o=>cardOn(o.hm,o.i)).reverse(); }\n"
    "// what's pinned on the board: postcards and snapshots, alternating, newest first\n"
    "function boardItems(){ const a=wallCards().map(o=>({i:o.i,img:o.hm.img,r:o.i*31+5})), b=SNAPS.map(s=>({i:'s'+s.id,img:s.img,r:(s.id%9973)+7})), L=[];\n"
    "  for(let k=0;k<Math.max(a.length,b.length);k++){ if(a[k])L.push(a[k]); if(b[k])L.push(b[k]); } return L; }")
rep("const L=wallCards().slice(0,12), n=L.length,", "const L=boardItems().slice(0,12), n=L.length,")
rep("const r2=boardRand(o.i*31+5),", "const r2=boardRand(o.r),")
rep("function boardSync(force){ const L=wallCards(); let wait=false;\n  for(const o of L.slice(0,12))if(!boardImgs[o.i]||boardImgs[o.i].src!==o.hm.img){ const im=new Image(); im.onload=()=>{ boardSig=''; }; im.src=o.hm.img; boardImgs[o.i]=im; wait=true; }",
    "function boardSync(force){ const L=boardItems(); let wait=false;\n  for(const o of L.slice(0,12))if(!boardImgs[o.i]||boardImgs[o.i].src!==o.img){ const im=new Image(); im.onload=()=>{ boardSig=''; }; im.src=o.img; boardImgs[o.i]=im; wait=true; }")

# ---------- card wall modal: snapshot album under the postcards ----------
rep("""  openModal(`<h3>Happy Tails<span class="cnt">♥ ${L.length}</span></h3><div class="wall">${L.length?`<div class="cards">${L.map(o=>`<button class="pc" data-hi="${o.i}"><img src="${o.hm.img}" alt="${o.hm.name} at home"><b>${o.hm.name}</b><span>with the ${o.hm.fam} family</span></button>`).join('')}</div>`:'<div class="wempty">\\u{1F48C}</div>'}</div>`);
  bindCards(openWall); }""",
"""  const kinds=Object.keys(SNAP_KINDS), got=kinds.filter(k=>snapHave(k)), miss=kinds.filter(k=>!snapHave(k));
  const album=`<div class="albumH">📷<span class="cnt">${got.length}/${kinds.length}</span></div><div class="wall"><div class="cards">${got.map(k=>{ const s=snapHave(k); return `<button class="pc snap" data-sk="${k}"><img src="${s.img}" alt=""><span class="k">${SNAP_KINDS[k]}</span></button>`; }).join('')}${miss.map(k=>`<div class="pc empty" aria-hidden="true">${SNAP_KINDS[k]}</div>`).join('')}</div></div>`;
  openModal(`<h3>Happy Tails<span class="cnt">♥ ${L.length}</span></h3><div class="wall">${L.length?`<div class="cards">${L.map(o=>`<button class="pc" data-hi="${o.i}"><img src="${o.hm.img}" alt="${o.hm.name} at home"><b>${o.hm.name}</b><span>with the ${o.hm.fam} family</span></button>`).join('')}</div>`:'<div class="wempty">\\u{1F48C}</div>'}</div>`+album);
  bindCards(openWall); document.querySelectorAll('#mbox [data-sk]').forEach(b=>b.onclick=()=>{ Snd.ding(); openSnap(b.dataset.sk); }); }
function openSnap(k){ const s=snapHave(k); if(!s)return; const a=s.ach&&ACH.find(x=>x[0]===s.ach);
  openModal(`<div class="snapBig"><img src="${s.img}" alt=""><span class="k">${SNAP_KINDS[k]}${a?' · ★':''}</span></div><button class="big" id="pcBack" aria-label="Back to the card wall">↩</button>`,true); $('#pcBack').onclick=openWall; }""")

# ---------- hooks ----------
rep("function boop(a,b){ const lick=getBond(a,b)>=40&&Math.random()<0.6;", "function boop(a,b){ const lick=getBond(a,b)>=40&&Math.random()<0.6; snapHint('boop',[a,b],0.5);")
rep("if(n>(W.stat.herd||0))W.stat.herd=n;", "if(n>(W.stat.herd||0))W.stat.herd=n;\n  if(n>=3&&n>herdShow)snapHint('herd',W.cats.filter(c=>c.herdFrom&&lure&&dist2(c.g.position,lure)<3).slice(0,8),0.2);")
rep("W.achT[id]=t; W.money+=rw;", "W.achT[id]=t; snapAch(id); W.money+=rw;")
rep("updateFirstAdopt(dt); updateCoats(dt);", "updateFirstAdopt(dt); snapTick(dt); updateCoats(dt);")
rep("['herd','Herding Cats','Cats led together with the wand or laser',()=>W.stat.herd||0,[3,6,10]]];",
    "['herd','Herding Cats','Cats led together with the wand or laser',()=>W.stat.herd||0,[3,6,10]],['album','Photo Album','Everyday moments caught on camera',()=>SNAPS.length,[3,7,11]]];")
rep("$('#bNew').onclick=()=>{ try{ localStorage.removeItem(SAVE); }catch(e){} begin(); };",
    "$('#bNew').onclick=()=>{ try{ localStorage.removeItem(SAVE); localStorage.removeItem(SNAP_KEY); }catch(e){} SNAPS=[]; boardSync(true); begin(); };")
rep("['Stray',()=>{ startDropoff(); }],", "['Stray',()=>{ startDropoff(); }],['Snap',()=>{ snapNow(); }],")
rep("window.__wm={Snd,", "window.__wm={Snd,tickAll:(dt)=>{ const t=performance.now()/1000; update(dt); for(const c of W.cats)animateCat(c,dt,t); updateWand(dt,t); updateLaser(t); updateFamilyMeshes(dt,t); updateFx(dt); },snapNow,snapTake,snapFrame,snapBlocked,snapRay,snapMoments,snapTick,openSnap,getSnaps:()=>SNAPS,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
