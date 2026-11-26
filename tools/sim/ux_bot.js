// Whisker Meadow UX bot: plays the real game through pointer events on the canvas and clicks on the DOM, as one of
// many player personas, on a simulated clock, and records the game's own play log plus 'bot' intent lines.
// Runs inside tools/sim/ux.html (built by build_ux.py). URL: ux.html?seed=N&cfg=<json>&id=<name>
(function(){
const DT=1/30, Fr=s=>Math.max(1,Math.round(s/DT));
const q=new URLSearchParams(location.search);
const CFG=Object.assign({speed:1,oneDir:false,cam:1,follow:0.8,explore:0.2,distract:0.2,skip:0,react:1.2,mins:7},JSON.parse(q.get('cfg')||'{}'));
const RID=q.get('id')||'ux_test';
const R=()=>Math.random(), rnd=(a,b)=>a+(b-a)*R(), pick=a=>a[Math.floor(R()*a.length)];
const cv=canvas; cv.setPointerCapture=()=>{}; cv.releasePointerCapture=()=>{}; cv.hasPointerCapture=()=>false;
let pid=100;
const held=new Map();
function releaseAll(){ for(const [id,[x,y]] of [...held])pe('pointerup',x,y,id); }
function pe(type,x,y,id){ if(!isFinite(x)||!isFinite(y)){ const h=held.get(id); x=h?h[0]:innerWidth/2; y=h?h[1]:innerHeight/2; } if(type==='pointerup')held.delete(id); else held.set(id,[x,y]); cv.dispatchEvent(new PointerEvent(type,{pointerId:id,clientX:x,clientY:y,pointerType:'touch',button:0,buttons:type==='pointerup'?0:1,isPrimary:true,bubbles:true,cancelable:true})); }
const note=t=>rec('bot',t);
const vis=el=>!!el&&!el.hidden&&!el.disabled&&el.getClientRects().length>0&&getComputedStyle(el).visibility!=='hidden';
const TOP=70, BOT=110;
function scr(v){ if(!v)return null; const s=toScreen(v); return s.ok&&s.x>8&&s.x<innerWidth-8&&s.y>TOP&&s.y<innerHeight-BOT?s:null; }
const headW=c=>c.head.localToWorld(new V3(0,0.15,0.05)), midW=c=>c.core.localToWorld(new V3(0,0.2,0)), tailW=c=>c.core.localToWorld(new V3(0,0.22,-0.38));
const ok=c=>c&&!c.carried&&!c.outside&&!c.leaving&&c.away<=0;
function vP(c){ return 2.5*Math.max(60,Math.min(400,catScreenH(c)))*tempoOf(c); }
function* wait(s){ yield Fr(s); }
function* tapXY(x,y,why){ note(`${why} tap@${Math.round(x)},${Math.round(y)}`); const el=document.elementFromPoint(x,y);
  if(el&&el!==cv&&!cv.contains(el)){ const b=el.closest('button,.tool,summary,[data-buy]')||el; b.click(); yield Fr(0.3); return; }
  const id=++pid; pe('pointerdown',x,y,id); yield Fr(rnd(0.06,0.14)); pe('pointerup',x,y,id); yield Fr(0.25); }
function* clickSel(sel,why){ const el=$(sel); if(!vis(el)){ yield* wait(0.3); return; } note(`${why} click ${sel}`); el.click(); yield Fr(rnd(0.3,0.7)); }
function* tapCat(c,why){ const p=scr(headW(c))||scr(midW(c)); if(!p){ yield* panTo(c.g.position,why); return; } yield* tapXY(p.x,p.y,why); }
function* tapZone(c,zone,why){ for(let k=0;k<12;k++){ const t=k/11, w=headW(c).lerp(tailW(c).add(new V3(0,0,0)),0.4+t*0.75), p=scr(w); if(!p)continue; const h=pickAt({clientX:p.x,clientY:p.y}); if(h&&h.cat===c&&h.zone===zone){ yield* tapXY(p.x,p.y,why+' '+zone); return; } }
  yield* tapCat(c,why+' (no '+zone+')'); }
// drag the meadow so a world point comes toward the middle of the screen (needed even by players who never move the camera)
function* panTo(w,why){ const s=toScreen(w); let dx=innerWidth/2-s.x, dy=innerHeight/2-s.y; if(!s.ok){ dx=-dx; dy=-dy; } const L=Math.hypot(dx,dy)||1, k=Math.min(1,260/L); dx*=k; dy*=k;
  note(`${why} pan-to`); yield* drag(innerWidth/2-dx/2,innerHeight/2-dy/2,dx,dy,0.5); }
function* drag(x,y,dx,dy,secs){ const id=++pid, n=Fr(secs); pe('pointerdown',x,y,id); yield 1; for(let i=1;i<=n;i++){ pe('pointermove',x+dx*i/n,y+dy*i/n,id); yield 1; } pe('pointerup',x+dx,y+dy,id); yield Fr(0.2); }
function* pan(){ for(let k=0;k<10;k++){ const x=rnd(50,innerWidth-50), y=rnd(TOP+60,innerHeight-BOT-60); if(!pickAt({clientX:x,clientY:y})&&!nearCat({clientX:x,clientY:y},true)){ const a=rnd(0,6.28), L=rnd(60,220); note('free pan'); yield* drag(x,y,Math.cos(a)*L,Math.sin(a)*L,rnd(0.3,0.8)); return; } } yield* wait(0.5); }
function* pinch(){ const cx=innerWidth/2, cy=innerHeight/2, a=++pid, b=++pid, d0=rnd(50,90), d1=d0*(R()<0.5?rnd(1.5,2.4):rnd(0.4,0.7)), n=Fr(0.5); note('free pinch');
  pe('pointerdown',cx-d0,cy,a); pe('pointerdown',cx+d0,cy,b); yield 1; for(let i=1;i<=n;i++){ const d=d0+(d1-d0)*i/n; pe('pointermove',cx-d,cy,a); pe('pointermove',cx+d,cy,b); yield 1; } pe('pointerup',cx-d1,cy,a); pe('pointerup',cx+d1,cy,b); yield Fr(0.3); }
// petting / brushing: persona speed, one-way (lift and restart) or back-and-forth
function* stroke(c,secs,why,brush){ note(`${why} ${brush?'scrub':'pet'} ${c.name} x${CFG.speed}${CFG.oneDir&&!brush?' oneway':''}`);
  const end=W.time+secs; let dir=1, id=0, x=0, y=0;
  while(W.time<end&&ok(c)&&!W.paused){
    const a=scr(headW(c)), b=scr(tailW(c)); if(!a||!b){ if(id){ pe('pointerup',x,y,id); id=0; } yield* panTo(c.g.position,why); continue; }
    const p0=dir>0?a:b, p1=dir>0?b:a, L=Math.hypot(p1.x-p0.x,p1.y-p0.y); if(L<20){ if(id){ pe('pointerup',x,y,id); id=0; } yield* wait(0.3); continue; }
    const v=(brush?0.7:1)*CFG.speed*vP(c)*rnd(0.85,1.15), n=Math.max(2,Math.round(L/v/DT));
    if(!id){ id=++pid; x=p0.x; y=p0.y; pe('pointerdown',x,y,id); yield 1; }
    for(let i=1;i<=n;i++){ x=p0.x+(p1.x-p0.x)*i/n+rnd(-2,2); y=p0.y+(p1.y-p0.y)*i/n+rnd(-2,2); pe('pointermove',x,y,id); yield 1; if(P.mode!=='stroke'&&P.mode!=='catPending')break; }
    if(P.mode==='carry'){ pe('pointerup',x,y,id); id=0; note('accidental carry'); yield* wait(0.3); continue; }
    if(CFG.oneDir&&!brush){ pe('pointerup',x,y,id); id=0; yield Fr(rnd(0.12,0.5)); } else dir=-dir; }
  if(id)pe('pointerup',x,y,id); yield Fr(0.2); }
function* carry(c,toW,why){ const p=scr(midW(c)); if(!p){ yield* panTo(c.g.position,why); return; } note(`${why} carry ${c.name}`); const id=++pid; pe('pointerdown',p.x,p.y,id); yield Fr(0.6);
  if(P.mode!=='carry'){ pe('pointerup',p.x,p.y,id); note('carry failed mode='+P.mode); yield Fr(0.3); return; }
  const t=toScreen(toW); const tx=Math.max(20,Math.min(innerWidth-20,t.x)), ty=Math.max(TOP+20,Math.min(innerHeight-BOT,t.y)), n=Fr(rnd(0.6,1.2));
  for(let i=1;i<=n;i++){ pe('pointermove',p.x+(tx-p.x)*i/n,p.y+(ty-p.y)*i/n,id); yield 1; } yield Fr(0.15); pe('pointerup',tx,ty,id); yield Fr(0.4); }
function* wave(why){ const cs=active().filter(ok); const c=pick(cs); const w=c?c.g.position.clone().add(new V3(rnd(-1,1),0,rnd(-1,1))):cam.target.clone(); const p=scr(w)||{x:innerWidth/2,y:innerHeight/2};
  note(`${why} wand wave`); const id=++pid; pe('pointerdown',p.x,p.y,id); const n=Fr(rnd(1.5,3)); for(let i=1;i<=n;i++){ pe('pointermove',p.x+Math.sin(i*0.25)*70,p.y+Math.cos(i*0.17)*25,id); yield 1; } pe('pointerup',p.x,p.y,id); yield Fr(0.3); }
function nearW(b,a){ const d=new V3(a.g.position.x-b.g.position.x,0,a.g.position.z-b.g.position.z); if(d.lengthSq()<1e-4)d.set(1,0,0); d.normalize().multiplyScalar(0.8); return b.g.position.clone().add(d); }
function visCats(){ return active().filter(ok).filter(c=>scr(midW(c))); }

// ---- what the game is asking for right now (a lesson / lock / tip), as an action ----
function lessonAct(){
  if(intro.c)return stroke(intro.c,rnd(2,5),'lesson pet');
  if(bt.c){ if(bt.c.blinkBackT>0)return tapCat(bt.c,'lesson blink'); return wait(0.4); }
  if(pl.a){ if(pl.stage==='carry')return carry(pl.a,nearW(pl.b,pl.a),'lesson pair'); return wait(0.5); }
  if(br.c){ if(W.tool!=='brush')return clickSel('[data-tool=brush]','lesson brush'); return stroke(br.c,rnd(2,4),'lesson brush',true); }
  if(firstAdopt()){ if(W.pickHome){ const c=W.cats.find(readyHome); if(c)return tapCat(c,'lesson adopt'); } else if(vis($('#fPick')))return clickSel('#fPick','lesson adopt'); return wait(0.8); }
  if(W.family&&W.family.atGate&&!firstAdopt()){ if(W.pickHome){ const c=W.cats.find(readyHome); if(c)return tapCat(c,'family pick'); } else if(vis($('#fPick'))&&W.cats.some(readyHome))return clickSel('#fPick','family'); }
  const g=shopForce(); if(g)return clickSel('#bShop','lesson shop');
  if(tips.cur&&tips.cur.kind==='butt')return tapZone(tips.cur.c,'rump','tip butt');
  if(tips.cur&&tips.cur.kind==='flea'){ if(W.tool!=='brush')return clickSel('[data-tool=brush]','tip flea'); return stroke(tips.cur.c,rnd(2,4),'tip flea',true); }
  const wf=wandForce(); if(wf==='pick')return clickSel('[data-tool=wand]','lesson wand'); if(wf)return wave('lesson wand');
  const ff=fairForce(); if(ff==='hand')return clickSel('[data-tool=hand]','lesson fair'); if(ff){ if(vis($('#tShow')))return clickSel('#tShow','lesson fair'); const c=W.cats.find(showReady); if(c)return tapCat(c,'lesson fair'); }
  return null; }
function hintXY(){ const m=/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/.exec(hintEl.style.transform||''); return m?{x:+m[1],y:+m[2]}:null; }
function hintAct(){ const h=curHint; if(!h||hintEl.hidden)return null; const p=hintXY(); if(!p)return null; const why='hint '+h.id;
  if(h.g==='tap')return tapXY(p.x,p.y,why);
  const hit=pickAt({clientX:p.x,clientY:p.y})||nearCat({clientX:p.x,clientY:p.y},true);
  if(h.g==='stroke'){ if(W.tool==='wand')return wave(why); if(hit&&hit.cat)return stroke(hit.cat,rnd(2,5),why,W.tool==='brush'); return tapXY(p.x,p.y,why+' (no cat)'); }
  if(h.g==='hold'&&hit&&hit.cat){ const o=active().filter(c=>c!==hit.cat&&ok(c))[0]; return carry(hit.cat,o?nearW(o,hit.cat):cam.target.clone(),why); }
  return tapXY(p.x,p.y,why); }
function* modalAct(){ const mb=$('#mbox'); const g=shopForce(), all=[...mb.querySelectorAll('button:not([disabled]),summary')].filter(b=>!/New|Reset|Start over|Delete/i.test(b.textContent||'')&&!['hLog','hLogShare','hTog'].includes(b.id));
  if(g){ const b=mb.querySelector(`[data-buy="${g}"]`); if(b&&!b.disabled&&R()<CFG.follow){ note('modal shop buy '+g); b.click(); yield Fr(rnd(0.5,1.5)); return; } }
  const other=all.filter(b=>!b.classList.contains('x'));
  if(other.length&&R()<CFG.explore){ const b=pick(other); note('modal explore '+(b.id||b.dataset.buy||(b.textContent||'').trim().slice(0,20))); b.click(); yield Fr(rnd(0.8,3)); return; }
  const x=mb.querySelector('.x'); yield Fr(rnd(1,3)*(CFG.distract>0.4?1.5:1)); if(!$('#modal').hidden){ if(x){ note('modal close'); x.click(); } else if(other.length){ note('modal first '+(other[0].id||(other[0].textContent||'').trim().slice(0,20))); other[0].click(); } } yield Fr(0.3); }
function* freeAct(){ const tool=W.tool, cs=visCats(), wts=[['pet',tool==='hand'&&cs.length?5:0],['scrub',tool==='brush'&&cs.length?3:0],['wave',tool==='wand'?2:0],['tapcat',cs.length?1:0],['pan',CFG.cam*1.5],['pinch',CFG.cam*0.6],['ui',CFG.explore*6],['tool',CFG.explore*3],['ground',0.6],['idle',CFG.distract*6]];
  let s=wts.reduce((a,w)=>a+w[1],0)*R(); let k='idle'; for(const w of wts){ s-=w[1]; if(s<=0){ k=w[0]; break; } }
  if(k==='pet'){ yield* stroke(pick(cs),rnd(2,7)*(CFG.distract>0.4?0.6:1),'free'); return; }
  if(k==='scrub'){ yield* stroke(pick(cs),rnd(2,5),'free',true); return; }
  if(k==='wave'){ yield* wave('free'); return; }
  if(k==='tapcat'){ yield* tapCat(pick(cs),'free'); return; }
  if(k==='pan'){ yield* pan(); return; }
  if(k==='pinch'){ yield* pinch(); return; }
  if(k==='ui'){ const sel=pick(['#bCats','#bShop','#bBadges','#bSnap','#bHints']); yield* clickSel(sel,'free ui'); return; }
  if(k==='tool'){ yield* clickSel(`[data-tool=${pick(['hand','hand','brush','laser'])}]`,'free tool'); return; }
  if(k==='ground'){ yield* tapXY(rnd(30,innerWidth-30),rnd(TOP+40,innerHeight-BOT-20),'free ground'); return; }
  note('idle'); yield Fr(R()<CFG.distract*0.3?rnd(15,40):rnd(1.5,6)); }

// ---- decision loop ----
let sig='', sigT=0;
function curSig(){ return [recLesson(),curHint&&!hintEl.hidden?curHint.id:'',$('#modal').hidden?'':'modal',vis($('#mOk'))?'meet':'',W.paused?'paused':''].join('|'); }
function* decide(){
  const s=curSig(); if(s!==sig){ sig=s; sigT=__simMs()/1000+rnd(0.5,1.5)*CFG.react; }
  if(__simMs()/1000<sigT){ yield 1; return; } // noticing what changed takes a moment
  if(vis($('#mOk'))){ yield Fr(rnd(1,4)*(CFG.distract>0.4?1.6:1)); note('meet hello'); $('#mOk').click(); yield Fr(0.4); return; }
  if(!$('#modal').hidden){ yield* modalAct(); return; }
  if(W.paused){ const b=[...document.querySelectorAll('button')].find(b=>vis(b)&&b.closest('[id]')&&!b.closest('#hud,#dock,.tools,#top')&&/big|ok/i.test(b.className+b.id)); note('paused '+(b?'click '+(b.id||b.textContent.trim().slice(0,15)):'stuck')); if(b)b.click(); yield Fr(1); return; }
  const sk=[$('#introSkip'),$('#lessonSkip')].find(vis); if(sk&&R()<CFG.skip){ note('skip'); sk.click(); yield Fr(0.5); return; }
  if(R()<CFG.follow){ const a=lessonAct(); if(a){ yield* a; yield Fr(rnd(0.1,0.6)*CFG.react); return; } }
  if(R()<CFG.follow*0.8){ const a=hintAct(); if(a){ yield* a; yield Fr(rnd(0.2,0.8)*CFG.react); return; } }
  yield* freeAct(); yield Fr(rnd(0.2,1.2)*(0.5+CFG.distract*2)); }
function simFrame(dt){ __simAdv(dt*1000); recTick(); const t=performance.now()/1000;
  if(W.started&&!W.paused)update(dt); updateTag(dt); for(const c of W.cats)animateCat(c,W.paused?dt*0.6:dt,t);
  updateWand(dt,t); updateLaser(t); updateFamilyMeshes(dt,t); updateFx(dt); if(!W.paused)updateBirds(dt,t); updateCamera(dt); scene.updateMatrixWorld(); camera.updateMatrixWorld(); }
function run(){ rec('cfg',JSON.stringify(CFG)); rec('storage',localStorage.length+' keys, hints='+W.hints); $('#bPlay').click(); let it=decide(), w=0; const lim=CFG.mins*60, t0=Date.now(); let real0=window.__rST?null:null;
  const r0=performance.timeOrigin; let lastWT=-1, lastWTms=0, wasPaused=false;
  function chunk(){ try{ chunkBody(); }catch(e){ rec('boterr','loop '+String(e).slice(0,120)); held.clear(); it=decide(); w=0; mc.port2.postMessage(0); } }
  function chunkBody(){ const stop=__simMs()+1; for(let i=0;i<900;i++){ if(W.time>=lim)return finish(); if(W.time!==lastWT){ lastWT=W.time; lastWTms=__simMs(); } else if(__simMs()-lastWTms>120000){ { const b=$('#mOk'), m=$('#meet'); rec('stuck',`game time frozen 120s paused=${W.paused} meetHidden=${m.hidden} meetDisp=${getComputedStyle(m).display} okVis=${vis(b)} okOP=${!!b.offsetParent} modal=${!$('#modal').hidden} started=${W.started}`); } return finish(); } if(W.paused&&!wasPaused){ wasPaused=true; releaseAll(); it=decide(); w=0; } else if(!W.paused)wasPaused=false; if(w>0)w--; else { let n; try{ n=it.next(); }catch(e){ rec('boterr',String(e).slice(0,120)); n={done:true}; } if(n.done){ if(held.size){ rec('bot','released '+held.size+' stuck finger(s)'); releaseAll(); } it=decide(); } else w=(n.value||1)-1; } simFrame(DT); } mc.port2.postMessage(0); }
  const mc=new MessageChannel(); mc.port1.onmessage=chunk;
  chunk(); }
function finish(){ const out={id:RID,cfg:CFG,simT:W.time,log:REC.L,stat:Object.assign({},W.stat),money:W.money,cats:W.cats.length,homes:W.homes.length,stars:W.stars};
  fetch('http://localhost:8767/'+RID,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(out)}).then(()=>{ window.__uxDone=true; parent.postMessage({uxDone:RID},'*'); }).catch(e=>{ window.__uxDone='post-failed'; parent.postMessage({uxDone:RID,err:String(e)},'*'); }); }
window.__ux={run,CFG};
window.addEventListener('load',()=>window.__rST(run,300));
})();
