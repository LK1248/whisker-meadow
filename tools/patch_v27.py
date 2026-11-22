"""v27: focused brush lesson ~45s after the first three lessons: burrs + brush = shine; tap the brush, scrub the coat."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function endPairTut(ok){ const {a,b}=pl; if(!a)return; pl.a=null; pl.done=true; W.stat.pairDone=1;",
    "function endPairTut(ok){ const {a,b}=pl; if(!a)return; pl.a=null; pl.done=true; W.stat.pairDone=1; W.stat.pairDoneT=W.time;")
rep("$('#introSkip').onclick=()=>{ if(pl.a){", "$('#introSkip').onclick=()=>{ if(br.c){ endBrushTut(false); return; } if(pl.a){")
rep("function tapGesture(t,x,y){", r"""// ---- lesson 4: grooming. A scruffy cat, the brush, scrub until it shines ----
const br={c:null,t:0,stage:'tool'};
const BRUSH_ICON='<svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="#4a3426" stroke-width="2.2" stroke-linecap="round"><path d="M4 20l7-7"/><rect x="11" y="4" width="9" height="9" rx="2.5" transform="rotate(45 15.5 8.5)" fill="#4a3426" stroke="none"/></svg>';
const SHINE_ICON='<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z" fill="#f2c94c"/></svg>';
function brushReady(){ return !br.c&&!br.done&&W.stat.pairDone&&!W.stat.brushTut&&!intro.c&&!bt.c&&!pl.a&&!firstAdopt()&&W.started&&!W.paused&&$('#modal').hidden&&!W.runaway&&W.time>(W.stat.pairDoneT!=null?W.stat.pairDoneT+45:200); }
function startBrushTut(){ let c=scruffiest(); if(!c){ c=active().filter(k=>!k.carried&&!k.outside&&k.age>=0.5&&['idle','walk','sit','watch'].includes(k.state)).sort((a,b)=>a.s.groom-b.s.groom)[0]; if(!c)return; c.s.groom=Math.min(c.s.groom,22); }
  Object.assign(br,{c,t:0,stage:W.tool==='brush'?'scrub':'tool',want:cam.want}); cam.want=Math.min(cam.want,4); hideHint(); hintDone.add('brush'); hintDone.add('brush2'); tag.c=null;
  document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; $('#intro').classList.remove('off');
  const gh=$('#ghost'); gh.innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; gh.classList.remove('tap');
  $('#pips').innerHTML=`<div class="eq eq3">${BURR_SVG.replace('width="30" height="30"','width="34" height="34"')}<b style="font-size:24px;color:#4a3426">+</b>${BRUSH_ICON}<b style="font-size:24px;color:#4a3426">=</b>${SHINE_ICON}</div>`; }
function endBrushTut(ok){ const c=br.c; if(!c)return; br.c=null; br.done=true; W.stat.brushTut=1; cam.want=Math.max(br.want||0,LV().zoom*0.75); document.body.classList.remove('intro');
  $('#intro').classList.add('off'); setTimeout(()=>{ if(!intro.c&&!bt.c&&!pl.a&&!br.c)$('#intro').hidden=true; },750); for(const id of ['#ghost','#pips','#introSkip'])$(id).hidden=true; $('#ghost').classList.remove('tap');
  if(ok){ spawnFx('spark',c.g.position.clone().setY(0.9*c.g.scale.y),14,0.5,0.18); Snd.chime(); tagFor(c,4); } hintGap=8; }
function updateBrushTut(dt){
  if(!br.c){ br.wait=(br.wait||0)-dt; if(br.wait<=0){ br.wait=3; if(brushReady())startBrushTut(); } return; }
  const c=br.c; if(c.away>0||c.outside||c.leaving||c.carried){ endBrushTut(false); return; } br.t+=dt; tag.c=null;
  if(burrCount(c)===0){ endBrushTut(true); return; }
  if(br.stage==='tool'&&W.tool==='brush'){ br.stage='scrub'; br.t=0; }
  if(br.stage==='scrub'&&W.tool!=='brush')br.stage='tool';
  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));
  if(!['pet','sleep'].includes(c.state)){ if(c.state!=='idle')setState(c,'idle',3); c.stT=Math.max(c.stT||0,2); }
  const b=toScreen(bodyOf(c)); if(!b.ok)return;
  const io=$('#intro'); io.style.setProperty('--x',b.x+'px'); io.style.setProperty('--y',b.y+'px'); io.style.setProperty('--r','120px');
  const gh=$('#ghost');
  if(br.stage==='tool'){ const t=elC('[data-tool=brush]'); gh.classList.add('tap'); gh.style.opacity=''; tapGesture(br.t,t.x,t.y); }
  else { gh.classList.remove('tap'); const busy=P.mode==='stroke'||(P.mode&&P.mode!=='none'); gh.style.opacity=busy?0:0.9; const sx=Math.sin(br.t*7)*38; gh.style.transform=`translate(${b.x-30+sx}px,${b.y-40}px) rotate(${sx*0.3}deg)`; } }
function tapGesture(t,x,y){""")
rep("updateIntro(dt); updateBlinkTut(dt); updatePairTut(dt);", "updateIntro(dt); updateBlinkTut(dt); updatePairTut(dt); updateBrushTut(dt);")
rep("function updateHints(dt){ if(intro.c||bt.c||pl.a||", "function updateHints(dt){ if(intro.c||bt.c||pl.a||br.c||")
rep("function updateTips(dt){ const busy=firstAdopt()||intro.c||", "function updateTips(dt){ const busy=br.c||firstAdopt()||intro.c||")
rep("window.__wm={animateCat,", "window.__wm={animateCat,br,startBrushTut,")
rep('#pips .eq svg{width:150px;height:46px}', '#pips .eq svg{width:150px;height:46px}
#pips .eq3{display:flex;align-items:center;gap:10px}#pips .eq3 svg{width:36px;height:36px}')
open(P, 'w', encoding='utf-8').write(s); print('ok')
