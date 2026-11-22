"""v7: wordless petting intro, size-scaled stat icons, fair photo + badge button."""
import re, sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- CSS ----------
rep('#hint{position:fixed;', '''#intro{position:fixed;inset:0;pointer-events:none;z-index:3;background:radial-gradient(circle at var(--x,50%) var(--y,50%),transparent 0,transparent 110px,rgba(30,20,45,.6) 230px);transition:opacity .7s}
#intro.off{opacity:0}
#ghost{position:fixed;left:0;top:0;width:76px;height:76px;pointer-events:none;z-index:6;filter:drop-shadow(0 5px 6px rgba(0,0,0,.35))}
#ghost svg{width:100%;height:100%}
#pips{position:fixed;left:50%;top:16%;transform:translateX(-50%);display:flex;gap:14px;z-index:6;pointer-events:none}
#pips svg{width:38px;height:38px;transition:transform .3s}
#pips svg path{fill:rgba(255,255,255,.3);stroke:#fff;stroke-width:2;transition:fill .3s}
#pips svg.on{transform:scale(1.25)}#pips svg.on path{fill:#ff6f99}
#introSkip{position:fixed;right:14px;bottom:calc(100px + env(safe-area-inset-bottom,0px));z-index:7;width:46px;height:46px;border-radius:50%;background:rgba(255,250,242,.85);font-size:20px;color:#8c7666}
body.intro .dock,body.intro #hud,body.intro .top{opacity:.25;pointer-events:none}
.ic3{display:flex;justify-content:space-around;align-items:flex-end;margin-top:4px;height:44px}
.ic{width:36px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.ic svg{width:32px;height:32px;transform-origin:50% 100%;transition:transform .35s,opacity .35s}
.ic .lb{font:700 10px var(--body);color:var(--muted)}
.ic.pulse svg{animation:ipulse .45s ease-out}
.fairpic{position:relative;margin:2px 0 10px}
.fairpic img{width:100%;border-radius:16px;display:block}
.fairpic .fb{position:absolute;left:6px;top:4px;width:78px;height:78px}
#hint{position:fixed;''')

# ---------- HTML ----------
rep('<div id="tag" hidden></div>', '<div id="tag" hidden></div><div id="intro" hidden></div><div id="ghost" hidden></div><div id="pips" hidden></div><button id="introSkip" hidden aria-label="Skip">&#9197;</button>')

# ---------- stat icons instead of bars ----------
rep('''  <div class="t3" id="rA">${ICO_A}<span class="lb">Love</span><div class="tb"><i id="tA" style="background:#ff7aa2"></i></div></div>
  <div class="t3" id="rT">${ICO_T}<span class="lb">Trust</span><div class="tb"><i id="tT" style="background:#5b9be6"></i></div></div>
  <div class="t3" id="rH">${ICO_H}<span class="lb">Health</span><div class="tb"><i id="tH" style="background:#5fb35a"></i></div></div>
  <div class="tbtns"><button id="tShow" hidden>${RIB_SVG}Fair!</button>''',
'''  <div class="ic3"><div class="ic" id="rA">${ICO_A}<span class="lb">Love</span></div><div class="ic" id="rT">${ICO_T}<span class="lb">Trust</span></div><div class="ic" id="rH">${ICO_H}<span class="lb">Health</span></div></div>
  <div class="tbtns"><button id="tShow" hidden aria-label="Cat fair"></button>''')
rep('''r.classList.toggle('lab',lab); r.querySelector('.lb').hidden=!lab; }''', '''r.querySelector('.lb').hidden=!lab; }''')
rep('''  $('#tA').style.width=c.s.aff+'%'; $('#tT').style.width=c.s.trust+'%'; $('#tH').style.width=c.s.health+'%';''',
'''  for(const [id,v] of [['rA',c.s.aff],['rT',c.s.trust],['rH',c.s.health]]){ const g=$('#'+id+' svg'); g.style.transform=`scale(${(0.4+0.75*v/100).toFixed(3)})`; g.style.opacity=(0.55+0.45*v/100).toFixed(2); }''')
rep('''  $('#tShow').hidden=!showReady(c);''', '''  const ts=$('#tShow'); ts.hidden=!showReady(c); if(!ts.hidden&&ts.dataset.b!==String(c.bestPlace||0)){ ts.dataset.b=String(c.bestPlace||0); ts.innerHTML=fairBadge(c.bestPlace||0,46); }''')

# ---------- fair badge + photo ----------
rep("const STAY_SVG=", '''// rosette: pink before a cat's first fair, then the colour of its best ribbon so far
function fairBadge(best,w){ const col=['#ff8fb1','#ffcf3f','#c9d3de','#e1a06a'][best]||'#ff8fb1', tail=best?'#5b8def':'#ff6f99';
  return `<svg viewBox="0 0 40 46" width="${w}" height="${Math.round(w*46/40)}"><path d="M13 24l-5 19 6-3 4 5 3-15zM27 24l5 19-6-3-4 5-3-15z" fill="${tail}"/><circle cx="20" cy="17" r="15.5" fill="${col}" stroke="#fff" stroke-width="3.2" stroke-dasharray="3.2 2.2"/><circle cx="20" cy="17" r="9.5" fill="#fff" opacity=".55"/><g fill="#4a3426" opacity=".75"><ellipse cx="20" cy="20" rx="4" ry="3.2"/><circle cx="15.6" cy="15.6" r="1.7"/><circle cx="18.4" cy="13.4" r="1.7"/><circle cx="21.6" cy="13.4" r="1.7"/><circle cx="24.4" cy="15.6" r="1.7"/></g></svg>`; }
let FS=null;
// a little photo of the cat on a podium at the fair, rendered with the real cat model
function fairShot(c,place){ try{
  if(!FS){ const sc=new THREE.Scene(); sc.background=new THREE.Color(0xffe3ec);
    sc.add(new THREE.HemisphereLight(0xffffff,0xe8c4a0,0.85)); const dl=new THREE.DirectionalLight(0xffffff,0.75); dl.position.set(2,4,3); sc.add(dl);
    const floor=new THREE.Mesh(new THREE.CircleGeometry(8,32),M(0xf3d2b8)); floor.rotation.x=-Math.PI/2; sc.add(floor);
    const back=new THREE.Mesh(new THREE.PlaneGeometry(14,7),M(0xffb7cb)); back.position.set(0,3.2,-2.6); sc.add(back);
    const pcols=[0xffcf3f,0x5b8def,0xff7aa2,0x8fd16a,0xffffff];
    for(let i=-8;i<=8;i++){ const f=new THREE.Mesh(new THREE.CircleGeometry(0.2,3),M(pcols[(i+8)%pcols.length])); f.rotation.z=-Math.PI/2; f.position.set(i*0.42,2.25+0.004*i*i,-2.5); sc.add(f); }
    const pod=new THREE.Mesh(new THREE.CylinderGeometry(0.78,0.86,0.42,36),M(0xfff6ea)); pod.position.y=0.21; sc.add(pod);
    const trim=new THREE.Mesh(new THREE.CylinderGeometry(0.8,0.8,0.08,36),M(0xff7aa2)); trim.position.y=0.38; sc.add(trim);
    const ros=new THREE.Group(); const disc=new THREE.Mesh(new THREE.CircleGeometry(0.3,24),M(0xffcf3f)); disc.position.z=0.02; ros.add(disc);
    const rim=new THREE.Mesh(new THREE.CircleGeometry(0.36,12),M(0xffffff)); ros.add(rim);
    for(const sx of [-1,1]){ const t=new THREE.Mesh(new THREE.PlaneGeometry(0.15,0.5),M(0x5b8def)); t.position.set(sx*0.1,-0.42,-0.01); t.rotation.z=sx*0.25; ros.add(t); }
    const stick=new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.025,0.9,8),M(0xb08050)); stick.position.set(0,-0.5,-0.03); ros.add(stick);
    ros.position.set(1.15,0.95,0.15); ros.rotation.y=-0.25; sc.add(ros);
    FS={sc,disc,cam:new THREE.PerspectiveCamera(30,1,0.1,60)}; }
  FS.disc.material=M([0xffcf3f,0xffcf3f,0xc9d3de,0xe1a06a][place]);
  const g=c.g, par=g.parent, pos=g.position.clone(), rot=g.rotation.y, hd=c.heading, sit=c.sit, st=c.state, iv=c.icon&&c.icon.visible;
  FS.sc.add(g); g.position.set(0,0.42,0); c.heading=0.3; c.sit=true; c.state='idle'; if(c.icon)c.icon.visible=false; g.visible=true;
  for(let i=0;i<30;i++)animateCat(c,0.05,W.time+i*0.05); g.position.y=0.42; g.rotation.y=0.3;
  const cv0=renderer.domElement, s=g.scale.x; FS.cam.aspect=cv0.width/cv0.height; FS.cam.updateProjectionMatrix();
  FS.cam.position.set(0.55,0.95+0.55*s,1.6+3.0*s); FS.cam.lookAt(0.3,0.4+0.5*s,0); renderer.render(FS.sc,FS.cam);
  const out=document.createElement('canvas'); out.width=480; out.height=360; const x=out.getContext('2d'); const ar=4/3; let cw=cv0.width, ch=cw/ar; if(ch>cv0.height){ ch=cv0.height; cw=ch*ar; }
  x.drawImage(cv0,(cv0.width-cw)/2,(cv0.height-ch)/2,cw,ch,0,0,480,360); const url=out.toDataURL('image/jpeg',0.86);
  par.add(g); g.position.copy(pos); c.heading=hd; g.rotation.y=rot; c.sit=sit; c.state=st; if(c.icon)c.icon.visible=iv;
  return url; }catch(e){ console.error(e); return null; } }
const STAY_SVG=''')
rep('''W.ribbons++; W.money+=prize;''', '''c.bestPlace=c.bestPlace?Math.min(c.bestPlace,place):place; W.ribbons++; W.money+=prize;''')
rep('''  openModal(`<div class="center"><svg viewBox="0 0 100 100" width="120" height="120">''',
'''  const shot=fairShot(c,place);
  openModal(`<div class="${shot?'fairpic':'center'}">${shot?`<img src="${shot}" alt="">`:''}<svg ${shot?'class="fb"':''} viewBox="0 0 100 100" width="${shot?78:120}" height="${shot?78:120}">''')

# ---------- save / load bestPlace ----------
rep('wins:c.wins,pace:c.pace,', 'wins:c.wins,bestPlace:c.bestPlace||0,pace:c.pace,')
rep('wins:s.wins||0,pace:s.pace||c.pace,', 'wins:s.wins||0,bestPlace:s.bestPlace||0,pace:s.pace||c.pace,')

# ---------- wordless petting intro ----------
rep('function begin(){ Snd.init(); $(\'#start\').hidden=true; W.started=true; cam.theta=0.55; Snd.meow(1.2,0.5); pickGoals(); handVis(); hud(); }',
'''// first-time intro: spotlight one friendly cat, a ghost hand shows the slow stroke, three hearts fill as the player does it
const intro={c:null,t:0,g0:0};
const PIP='<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z"/></svg>';
function startIntro(){ const c=W.cats.find(k=>k.name==='Mochi'&&k.away<=0&&!k.outside)||active().slice().sort((a,b)=>b.s.trust-a.s.trust)[0]; if(!c)return;
  Object.assign(intro,{c,t:0,g0:W.stat.good,want:cam.want}); cam.want=4.3; hintDone.add('pet'); hideHint(); if(W.tool!=='pet')setTool('pet');
  document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; $('#intro').classList.remove('off');
  $('#ghost').innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; $('#pips').innerHTML=PIP+PIP+PIP; }
function endIntro(){ const c=intro.c; if(!c)return; intro.c=null; cam.want=Math.max(intro.want||0,LV().zoom*0.75); document.body.classList.remove('intro');
  $('#intro').classList.add('off'); setTimeout(()=>{ $('#intro').hidden=true; },750); for(const id of ['#ghost','#pips','#introSkip'])$(id).hidden=true;
  spawnFx('h',c.g.position.clone().setY(0.9),10,0.7,0.5); Snd.chime(); hintGap=6; }
function updateIntro(dt){ const c=intro.c; if(!c)return; if(c.away>0||c.outside||c.leaving){ endIntro(); return; } intro.t+=dt;
  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));
  if(c.state==='idle')c.stT=Math.max(c.stT||0,2); else if(!c.carried&&!['pet','flop','boop','groom'].includes(c.state))setState(c,'idle',3);
  const n=W.stat.good-intro.g0; [...$('#pips').children].forEach((e,i)=>e.classList.toggle('on',i<n)); if(n>=3){ endIntro(); return; }
  const s=c.g.scale.x, h=toScreen(headOf(c)), b=toScreen(new V3(p.x-Math.sin(c.heading)*0.45*s,0.62*s,p.z-Math.cos(c.heading)*0.45*s)); if(!h.ok)return;
  $('#intro').style.setProperty('--x',h.x+'px'); $('#intro').style.setProperty('--y',h.y+'px');
  const cyc=intro.t%2.8, k=clamp(cyc/1.2,0,1), e=k*k*(3-2*k), lift=cyc>1.2?(cyc-1.2)*30:0;
  const gh=$('#ghost'); gh.style.opacity=(handOn(c)||P.mode!=='none')?0:cyc<1.2?0.92:Math.max(0,0.92-(cyc-1.2)*1.6);
  gh.style.transform=`translate(${lerp(h.x,b.x,e)-30}px,${lerp(h.y,b.y,e)-30-lift}px)`; }
$('#introSkip').onclick=endIntro;
function begin(){ Snd.init(); $('#start').hidden=true; W.started=true; cam.theta=0.55; Snd.meow(1.2,0.5); pickGoals(); handVis(); hud(); if((W.stat.good||0)<3)setTimeout(startIntro,700); }''')
rep('  updateHints(dt); updateWeather(dt);', '  updateIntro(dt); updateHints(dt); updateWeather(dt);')
rep('function updateHints(dt){', 'function updateHints(dt){ if(intro.c){ hintEl.hidden=true; return; }')
rep('window.__wm={animateCat,', 'window.__wm={animateCat,intro,startIntro,endIntro,fairShot,returnFromShow,')
open(P, 'w', encoding='utf-8').write(s)
print('ok')
