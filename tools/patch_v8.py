"""v8: focused first slow-blink lesson (cat looks at you, blinks slowly, wait for a nose boop)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep('#introSkip{', '''#ghost.tap{width:58px;height:58px;opacity:.6}
#pips .eq{background:rgba(255,250,242,.92);border-radius:22px;padding:6px 14px;box-shadow:0 4px 14px rgba(0,0,0,.25)}
#pips .eq svg{width:150px;height:46px}
#introSkip{''')
# slow blink length can vary (the lesson uses a really slow one)
rep('const ph=1-c.slowBlink/1.9;', 'const ph=1-c.slowBlink/(c.sbLen||1.9);')
# tapping a cat that is waiting for a blink back always counts, even on the rump
rep("else if(P.zone==='rump')buttTap(c);", "else if(P.zone==='rump'&&!(c.blinkBackT>0))buttTap(c);")
# first gaze of the game starts the lesson
rep("c.blinkBackT=10.5; W.stat.gazes++;", "c.blinkBackT=10.5; W.stat.gazes++; if(!W.stat.blinkBack&&!bt.c&&!bt.skipped&&!intro.c&&W.started&&!W.paused)startBlinkTut(c);")
rep("function updateHints(dt){ if(intro.c){", "function updateHints(dt){ if(intro.c||bt.c){")
rep("  updateIntro(dt); updateHints(dt);", "  updateIntro(dt); updateBlinkTut(dt); updateHints(dt);")
rep("$('#introSkip').onclick=endIntro;", '''$('#introSkip').onclick=()=>{ if(bt.c){ bt.skipped=true; endBlinkTut(false); } else endIntro(); };
// first slow blink: spotlight the face, the cat looks right at you and blinks very slowly; "closed eyes = love"; a faint hand boops the nose
const bt={c:null,t:0,n0:0,lastB:-9};
const BLINK_EQ='<div class="eq"><svg viewBox="0 0 150 46"><g fill="none" stroke="#4a3426" stroke-width="5" stroke-linecap="round"><path d="M10 20q12 12 24 0"/><path d="M44 20q12 12 24 0"/><path d="M80 17h14M80 27h14"/></g><path d="M122 40s-17-10.5-17-22a9 9 0 0 1 17-5 9 9 0 0 1 17 5c0 11.5-17 22-17 22z" fill="#ff6f99"/></svg></div>';
function startBlinkTut(c){ if(bt.c||intro.c)return; Object.assign(bt,{c,t:0,n0:W.stat.blinkBack,lastB:-9,want:cam.want}); cam.want=3.3; hideHint(); hintDone.add('blink'); tag.c=null; if(W.tool!=='pet')setTool('pet');
  document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; $('#intro').classList.remove('off');
  const gh=$('#ghost'); gh.innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; gh.classList.add('tap'); $('#pips').innerHTML=BLINK_EQ; }
function endBlinkTut(ok){ const c=bt.c; if(!c)return; bt.c=null; cam.want=Math.max(bt.want||0,LV().zoom*0.75); document.body.classList.remove('intro');
  $('#intro').classList.add('off'); setTimeout(()=>{ if(!intro.c&&!bt.c)$('#intro').hidden=true; },750); for(const id of ['#ghost','#pips','#introSkip'])$(id).hidden=true; $('#ghost').classList.remove('tap'); c.sbLen=1.9;
  if(ok){ const s=c.s; s.aff=Math.min(100,s.aff+18); s.trust=Math.min(100,s.trust+5); spawnFx('h',c.g.position.clone().setY(1.0*c.g.scale.x+0.2),16,0.9,0.6); Snd.chime(); tagFor(c,6); }
  hintGap=6; }
function updateBlinkTut(dt){ const c=bt.c; if(!c)return; if(c.away>0||c.outside||c.leaving||c.carried){ endBlinkTut(false); return; }
  if(W.stat.blinkBack>bt.n0){ endBlinkTut(true); return; } bt.t+=dt; tag.c=null;
  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));
  if(c.state!=='idle')setState(c,'idle',3); c.stT=Math.max(c.stT||0,2); c.sit=true; c.heading=Math.atan2(camera.position.x-p.x,camera.position.z-p.z);
  c.gaze=Math.max(c.gaze,5); c.gazeBl=c.gazeBl2=true; c.blinkBackT=Math.max(c.blinkBackT,5);
  if(bt.t-bt.lastB>5){ bt.lastB=bt.t; c.sbLen=3.4; c.slowBlink=3.4; }
  const n=toScreen(c.head.localToWorld(new V3(0,-0.02,0.3))); if(!n.ok)return;
  $('#intro').style.setProperty('--x',n.x+'px'); $('#intro').style.setProperty('--y',n.y+'px');
  // the hand shows up after the first blink: lift, then a gentle tap on the nose
  const cyc=(bt.t-1.5)%1.8, up=cyc<0?40:cyc<0.9?40*(1-Math.sin(cyc/0.9*Math.PI/2)):cyc<1.1?0:40*((cyc-1.1)/0.7);
  const gh=$('#ghost'); gh.style.opacity=bt.t<1.5||(P.mode&&P.mode!=='none')?0:''; gh.style.transform=`translate(${n.x-18}px,${n.y-8-up}px)`; }''')
rep('window.__wm={animateCat,', 'window.__wm={animateCat,bt,startBlinkTut,')
open(P, 'w', encoding='utf-8').write(s)
print('ok')
