"""v9: pairing lesson (carry one cat next to another, watch them play) + wordless belly / butt-tap tips later on."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# spotlight radius can grow to hold two cats
rep('transparent 0,transparent 110px,rgba(30,20,45,.6) 230px)', 'transparent 0,transparent var(--r,110px),rgba(30,20,45,.6) calc(var(--r,110px) + 120px))')
rep('#introSkip{', '''#tip{position:fixed;left:0;top:0;z-index:6;pointer-events:none;background:rgba(255,250,242,.94);border-radius:18px;padding:6px 10px;box-shadow:0 4px 14px rgba(0,0,0,.22);transition:opacity .4s}
#tip svg{display:block;width:150px;height:auto}
#introSkip{''')
rep('<button id="introSkip"', '<div id="tip" hidden></div><button id="introSkip"')
rep("function updateHints(dt){ if(intro.c||bt.c){", "function updateHints(dt){ if(intro.c||bt.c||pl.a){")
rep("  updateIntro(dt); updateBlinkTut(dt);", "  updateIntro(dt); updateBlinkTut(dt); updatePairTut(dt); updateTips(dt);")
rep("function startIntro(){ if(bt.c)return;", "function startIntro(){ if(bt.c||pl.a)return;")
rep("function startBlinkTut(c){ if(bt.c||intro.c)return;", "function startBlinkTut(c){ if(bt.c||intro.c||pl.a)return;")
rep("setTimeout(()=>{ if(!intro.c&&!bt.c)$('#intro').hidden=true; },750);", "setTimeout(()=>{ if(!intro.c&&!bt.c&&!pl.a)$('#intro').hidden=true; },750);", 2)
rep("$('#introSkip').onclick=()=>{ if(bt.c){", "$('#introSkip').onclick=()=>{ if(pl.a){ endPairTut(false); return; } if(bt.c){")
rep('window.__wm={animateCat,', 'window.__wm={animateCat,pl,startPairTut,tips,')

rep("function begin(){", r'''// ---- lesson 3: friends. Hold one cat, carry it next to another, watch them boop and play ----
const pl={a:null,b:null,t:0,stage:'',lastDrop:0};
const catFace=(x,col)=>`<g transform="translate(${x},25)"><path d="M-13 -3L-12 -18-3 -11zM13 -3L12 -18 3 -11z" fill="${col}"/><circle r="13" fill="${col}"/><circle cx="-4.5" cy="-1" r="2" fill="#4a3426"/><circle cx="4.5" cy="-1" r="2" fill="#4a3426"/><path d="M-2 4h4l-2 2z" fill="#ff8fa3"/></g>`;
const HEART=(x,y,sc)=>`<path transform="translate(${x},${y}) scale(${sc})" d="M0 9s-8.5-5.2-8.5-11a4.5 4.5 0 0 1 8.5-2.5 4.5 4.5 0 0 1 8.5 2.5c0 5.8-8.5 11-8.5 11z" fill="#ff6f99"/>`;
const PAIR_EQ=`<div class="eq"><svg viewBox="0 0 150 46">${catFace(20,'#f3a64a')}${catFace(52,'#9a9aa6')}<path d="M76 18h14M76 28h14" stroke="#4a3426" stroke-width="5" stroke-linecap="round"/>${HEART(120,24,1.9)}</svg></div>`;
function pairReady(){ return !pl.a&&!pl.done&&!intro.c&&!bt.c&&W.started&&!W.paused&&!W.stat.pairDone&&W.stat.good>=3&&(W.stat.blinkBack>0||W.time>150)&&W.time>70&&$('#modal').hidden; }
function startPairTut(){ const ok=c=>!c.carried&&!c.outside&&!c.leaving&&c.away<=0&&c.age>=0.3&&['idle','walk','watch','sit','groom'].includes(c.state);
  const cs=active().filter(ok).sort((x,y)=>y.s.trust-x.s.trust); if(cs.length<2)return false; const a=cs[0];
  const b=cs.slice(1).sort((x,y)=>dist2(x.g.position,a.g.position)-dist2(y.g.position,a.g.position))[0];
  // keep them apart enough that a carry is needed
  if(dist2(a.g.position,b.g.position)<4){ const p=b.g.position, d=new V3(p.x-a.g.position.x,0,p.z-a.g.position.z).normalize(); goTo(b,p.x+(d.x||1)*2,p.z+d.z*2,null); }
  Object.assign(pl,{a,b,t:0,stage:'carry',want:cam.want,romp:false,lastDrop:W.stat.drops}); cam.want=Math.max(5.5,cam.want*0.8); hideHint(); hintDone.add('carry'); tag.c=null; if(W.tool!=='pet')setTool('pet');
  document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; $('#intro').classList.remove('off');
  const gh=$('#ghost'); gh.innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; gh.classList.remove('tap'); $('#pips').innerHTML=PAIR_EQ; return true; }
function endPairTut(ok){ const {a,b}=pl; if(!a)return; pl.a=null; pl.done=true; W.stat.pairDone=1; cam.want=Math.max(pl.want||0,LV().zoom*0.75); document.body.classList.remove('intro');
  $('#intro').classList.add('off'); $('#intro').style.setProperty('--r','110px'); setTimeout(()=>{ if(!intro.c&&!bt.c&&!pl.a)$('#intro').hidden=true; },750); for(const id of ['#ghost','#pips','#introSkip'])$(id).hidden=true;
  if(ok){ addBond(a,b,15); const m=a.g.position.clone().add(b.g.position).multiplyScalar(0.5).setY(1); spawnFx('h',m,14,0.9,0.6); Snd.chime(); }
  hintGap=8; }
function updatePairTut(dt){
  if(!pl.a){ pl.wait=(pl.wait||0)-dt; if(pl.wait<=0){ pl.wait=3; if(pairReady())startPairTut(); } return; }
  const {a,b}=pl; if([a,b].some(c=>c.away>0||c.outside||c.leaving)){ endPairTut(false); return; } pl.t+=dt; tag.c=null;
  const pa=a.g.position, pb=b.g.position, close=dist2(pa,pb)<1.9*1.9;
  if(pl.stage==='carry'){
    for(const c of [a,b])if(!c.carried&&c.state!=='boop'){ if(c.state==='walk'&&c===b&&c.path)continue; if(c.state!=='idle')setState(c,'idle',3); c.stT=Math.max(c.stT||0,2); }
    if(W.stat.drops>pl.lastDrop&&!a.carried&&!b.carried){ if(close){ pl.stage='watch'; pl.t=0; $('#ghost').hidden=true; if(a.state!=='boop'&&canBoop(a)&&canBoop(b)){ a.boopCD=b.boopCD=0; boop(a,b); } } else pl.lastDrop=W.stat.drops; } }
  // camera + spotlight on both cats
  const mid=pa.clone().add(pb).multiplyScalar(0.5); cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));
  const sa=toScreen(new V3(pa.x,0.5,pa.z)), sb=toScreen(new V3(pb.x,0.5,pb.z)); if(!sa.ok||!sb.ok)return;
  const carried=a.carried?a:b.carried?b:null, mx=(sa.x+sb.x)/2, my=(sa.y+sb.y)/2;
  $('#intro').style.setProperty('--x',mx+'px'); $('#intro').style.setProperty('--y',my+'px'); $('#intro').style.setProperty('--r',Math.round(Math.hypot(sa.x-sb.x,sa.y-sb.y)/2+100)+'px');
  if(pl.stage==='carry'){ const gh=$('#ghost'); gh.style.opacity=(P.mode&&P.mode!=='none'&&!carried)?0:'';
    if(carried){ // already holding one: point at the other cat
      const tgt=carried===a?sb:sa, bob=Math.sin(pl.t*6)*8; gh.style.transform=`translate(${tgt.x-30}px,${tgt.y-70+bob}px)`; gh.style.opacity=0.8; }
    else { // press and hold on the first cat, then glide over to the second one
      const cyc=pl.t%3.4; let x=sa.x,y=sa.y,sc=1;
      if(cyc<1.0){ sc=1-0.12*Math.min(1,cyc/0.3); }
      else if(cyc<2.4){ const k=(cyc-1.0)/1.4, e=k*k*(3-2*k); x=sa.x+(sb.x-sa.x)*e; y=sa.y+(sb.y-sa.y)*e-Math.sin(e*Math.PI)*50; sc=0.88; }
      else { x=sb.x; y=sb.y; sc=1; }
      gh.style.opacity=cyc>2.8?Math.max(0,1-(cyc-2.8)/0.6)*0.9:0.9; gh.style.transform=`translate(${x-30}px,${y-40}px) scale(${sc})`; } }
  else if(pl.stage==='watch'){
    if(!pl.romp&&a.state!=='boop'&&b.state!=='boop'&&pl.t>1){ pl.romp=true; pl.rompT=pl.t; startRomp(a,b); }
    if(pl.romp&&pl.t-pl.rompT>6)endPairTut(true);
    if(pl.t>20)endPairTut(true); } }

// ---- later, one-time wordless tips: belly rubs (only with high trust) and butt taps (some love them, some don't) ----
const tips={cur:null,t:0};
const CLAW='<g stroke="#e0505f" stroke-width="4" stroke-linecap="round"><path d="M92 68l10-13M100 72l10-13M108 76l10-13"/></g>';
const trustIco=(x,y,w)=>ICO_T.replace('<svg ',`<svg x="${x}" y="${y}" width="${w}" height="${w}" `);
const ARROW=y=>`<path d="M50 ${y}h24m-8-7l8 7-8 7" fill="none" stroke="#b9a89a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`;
const BELLY_TIP=`<svg viewBox="0 0 160 84">${trustIco(4,2,36)}${ARROW(20)}${HEART(104,18,1.6)}${trustIco(14,50,18)}${ARROW(60)}${CLAW}</svg>`;
const BUTT_TIP=`<svg viewBox="0 0 160 46">${HEART(36,22,1.8)}<path d="M72 36l14-26" stroke="#b9a89a" stroke-width="4" stroke-linecap="round"/><g fill="none" stroke="#e0505f" stroke-width="4" stroke-linecap="round"><path d="M110 14q6 6 0 12"/><path d="M128 14q-6 6 0 12"/><path d="M113 32q6-6 12 0"/></g></svg>`;
function showTip(kind,c,svg,dur,tap){ tips.cur={kind,c,dur,tap}; tips.t=0; $('#tip').innerHTML=svg; $('#tip').hidden=false; $('#tip').style.opacity=1; if(tap){ const gh=$('#ghost'); gh.innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; gh.classList.add('tap'); gh.hidden=false; } W.stat[kind+'Tip']=1; }
function endTip(){ if(!tips.cur)return; if(tips.cur.tap){ $('#ghost').hidden=true; $('#ghost').classList.remove('tap'); } tips.cur=null; $('#tip').hidden=true; }
function updateTips(dt){ const busy=intro.c||bt.c||pl.a||!W.started||W.paused||!$('#modal').hidden;
  if(!tips.cur){ if(busy||!W.stat.pairDone)return; tips.wait=(tips.wait||0)-dt; if(tips.wait>0)return; tips.wait=2;
    const flop=!W.stat.bellyTip&&active().find(c=>c.state==='flop'&&c.offer&&!c.carried); if(flop){ showTip('belly',flop,BELLY_TIP,7,false); return; }
    if(!W.stat.buttTip&&W.time>240&&!W.stat.butt){ const c=active().filter(c=>!c.carried&&!c.outside&&c.away<=0&&c.s.trust>=45&&['idle','sit'].includes(c.state)).sort((x,y)=>dist2(x.g.position,cam.target)-dist2(y.g.position,cam.target))[0]; if(c)showTip('butt',c,BUTT_TIP,9,true); }
    return; }
  const T=tips.cur, c=T.c; tips.t+=dt; if(busy||c.away>0||c.carried||c.outside||tips.t>T.dur||(T.kind==='belly'&&c.state!=='flop')||(T.kind==='butt'&&c.buttKnown&&tips.t>1.5)){ endTip(); return; }
  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);
  const top=toScreen(c.g.position.clone().setY(1.35*c.g.scale.x+0.45)); if(!top.ok)return; const el=$('#tip'), w=el.offsetWidth, hh=el.offsetHeight;
  el.style.transform=`translate(${clamp(top.x-w/2,8,innerWidth-w-8)}px,${clamp(top.y-hh,60,innerHeight-hh-90)}px)`; el.style.opacity=tips.t>T.dur-0.6?0:1;
  if(T.tap){ const p=c.g.position, s2=c.g.scale.x, r=toScreen(new V3(p.x-Math.sin(c.heading)*0.5*s2,0.55*s2,p.z-Math.cos(c.heading)*0.5*s2)); if(r.ok){ const cyc=tips.t%1.6, up=cyc<0.8?36*(1-Math.sin(cyc/0.8*Math.PI/2)):cyc<1.0?0:36*((cyc-1.0)/0.6); $('#ghost').style.opacity=''; $('#ghost').style.transform=`translate(${r.x-18}px,${r.y-8-up}px)`; } } }
function begin(){''')
# belly flop hint was text; the wordless tip replaces it
rep("{id:'belly',when:()=>W.cats.some(c=>c.state==='flop'&&c.offer&&c.s.trust<75)", "{id:'belly',when:()=>false&&W.cats.some(c=>c.state==='flop'&&c.offer&&c.s.trust<75)")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
