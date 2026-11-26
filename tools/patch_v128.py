"""v128: quick fixes from the phone play-test, plus families that keep coming.
1 no fair trips at night; 2 goals strip hidden; 3 ring keeps its colour when a stroke resumes; 4 lift-then-pan only
redirects near the cat itself; 5 locked laser -> small bubble pointing at the shop (no window); 6 butt tip shows '?';
7 butt taps: likers purr (no chirp), dislikers meow twice then walk off; 8 global meow limit; 9 butt-tap focus lasts
0.5s after lift; 10 no 'carry' hint; 11 cards queue (fair result never covers a postcard); 12 no hints during the whole
first adoption; 13 strays/families/meet sheets wait while a card is open, and the meadow slows to 1/3 after 10s.
Families: their clock keeps ticking while the player is busy (only the arrival waits), they get priority over strays
when due, and after the first adoption they also visit when no cat is ready, look around and leave 'Maybe later!'.
Play log records family/stray events and a family clock line every 30s."""
import sys, re
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# 1 fair: not at night
rep("function showReady(c){ const s=c.s; return !tutQuiet()&&", "function showReady(c){ const s=c.s; return (W.night||0)<0.55&&!tutQuiet()&&")
# 2 hide goals strip
rep("#goalStrip{position:fixed;", "#goalStrip{display:none!important}#bShop.nudge{animation:wmNudge .5s ease 3}@keyframes wmNudge{50%{transform:scale(1.14)}}\n#lockTip{position:fixed;z-index:9;display:flex;align-items:center;gap:4px;padding:6px 10px;border-radius:14px;background:#fffaf2;box-shadow:0 4px 14px rgba(74,52,38,.25);pointer-events:auto}\n#goalStrip0{position:fixed;")
# 3 ring colour continuity
rep("const st=P.mode==='stroke'&&S.cat===c?(c.beatSt=TG.c===c&&TG.shown>0.5?TG.st:null):petGrace(c)?c.beatSt:null;",
    "const st=P.mode==='stroke'&&S.cat===c?(TG.c===c&&TG.shown>0.5?(c.beatT=W.time,c.beatSt=TG.st):W.time-(c.beatT??-99)<1.6?c.beatSt:(c.beatSt=null)):petGrace(c)||(P.mode==='catPending'&&P.cat===c&&W.time-(c.beatT??-99)<1.6)?c.beatSt:null;")
# 4 redirect only near the cat
rep("const PG={c:null,until:-1,x:0,y:0}, PG_T=1;",
    "function nearCat(c,e){ const sc=toScreen(c.g.position.clone().setY(0.35*c.g.scale.y)); if(!sc.ok)return false; const m=e.pointerType==='mouse'; return Math.hypot(e.clientX-sc.x,e.clientY-sc.y)<clamp(catScreenH(c)*0.9,m?40:60,m?120:160); }\nconst PG={c:null,until:-1,x:0,y:0}, PG_T=1;")
rep("&&Math.hypot(e.clientX-PG.x,e.clientY-PG.y)<(e.pointerType==='mouse'?90:140))hit={cat:PG.c,zone:'back'};", "&&nearCat(PG.c,e))hit={cat:PG.c,zone:'back'};")
# 5 locked laser bubble
rep("function setTool(t){ if(t==='laser'&&!W.laser){ openShop('laser'); return; }",
    """function lockTip(){ let el=$('#lockTip'); if(!el){ el=document.createElement('div'); el.id='lockTip'; document.body.appendChild(el); el.onclick=()=>{ el.style.display='none'; }; }
  const b=$('#bShop'), r=b.getBoundingClientRect(); el.innerHTML=hIco(IC.laser,26)+'<svg viewBox="0 0 24 24" width="18" height="18"><path d="M4 12h14m-5-5l5 5-5 5" fill="none" stroke="#4a3426" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'+hIco('<path d="M4 9h16l-1.5 11h-13z" fill="#ffb3c6"/><path d="M8 9V7a4 4 0 0 1 8 0v2" fill="none" stroke="#4a3426" stroke-width="2.2"/>',26);
  el.style.top=Math.round(r.bottom+8)+'px'; el.style.right=Math.round(innerWidth-r.right)+'px'; el.style.display='flex'; b.classList.remove('nudge'); void b.offsetWidth; b.classList.add('nudge');
  clearTimeout(el.tm); el.tm=setTimeout(()=>{ el.style.display='none'; b.classList.remove('nudge'); },2600); rec('lockTip','laser'); }
function setTool(t){ if(t==='laser'&&!W.laser){ lockTip(); return; }""")
# 6 butt tip '?'
rep('const BUTT_TIP=`<svg viewBox="0 0 160 46">', 'const BUTT_TIP=`<svg viewBox="0 0 186 46">')
rep('<path d="M113 32q6-6 12 0"/></g></svg>`;\nconst FLEA_TIP', '<path d="M113 32q6-6 12 0"/></g><text x="166" y="38" text-anchor="middle" font-family="Fredoka,sans-serif" font-weight="700" font-size="34" fill="#8a6a52">?</text></svg>`;\nconst FLEA_TIP')
# 7 butt sounds
rep("c.purr=Math.max(c.purr,0.6); if(W.time-(c.buttSndT??-99)>1.5){ c.buttSndT=W.time; Snd.chirp(); }", "c.purr=Math.max(c.purr,0.8);")
rep("if(W.time-(c.buttSndT??-99)>2.5){ c.buttSndT=W.time; Snd.meow(0.85,0.7); } if(!c.buttKnown)floatWorld(c.g.position.clone().setY(1.3),'Not a fan'); }",
    "c.buttNo=(W.time-(c.buttNoT??-99)<5?(c.buttNo||0):0)+1; c.buttNoT=W.time; if(c.buttNo<=2)Snd.meow(c.buttNo>1?0.8:0.88,0.6); if(!c.buttKnown)floatWorld(c.g.position.clone().setY(1.3),'Not a fan'); if(c.buttNo>=2){ c.buttNo=0; walkAway(c,false); c.leaveT=1.2; } }")
# 8 global meow limit (urgent runaway calls exempt; delayed calls only ride along with an allowed meow)
rep("meow(p=1,loud=1,u=0,t0=0){ if(!this.ac)return;",
    "meow(p=1,loud=1,u=0,t0=0){ if(!this.ac)return; { const nw=performance.now(); if(u<=0.05){ if(t0>0){ if(nw-(this.mOk??-1e9)>80)return; } else { this.mQ=(this.mQ||[]).filter(x=>nw-x<10000); if(nw-(this.mOk??-1e9)<650||this.mQ.length>=5)return; this.mQ.push(nw); this.mOk=nw; } } }")
# 9 butt tap keeps focus 0.5s
rep("P.zone==='rump'&&!(c.blinkBackT>0))buttTap(c); else", "P.zone==='rump'&&!(c.blinkBackT>0)){ buttTap(c); PG.c=c; PG.until=W.time+0.5; PG.x=P.hx; PG.y=P.hy; } else")
# 10 drop carry hint
m = re.search(r"\n  \{id:'carry',.*?done:\(\)=>W\.stat\.drops>0\},", s)
if not m: sys.exit('carry hint not found')
s = s[:m.start()] + s[m.end():]
# 12 no hints during the whole first adoption
rep("||(firstAdopt()&&W.family.cat)){ hintEl.hidden=true; return; }", "||firstAdopt()){ hintEl.hidden=true; return; }")
# 11/13 card queue, events wait, slow-down
rep("function closeModal(){ $('#modal').hidden=true; }",
    "const cardQ=[]; let cardOpen=false, cardT=0;\nfunction showCard(fn){ if(!$('#modal').hidden||cam.meet||cardQ.length){ cardQ.push(fn); return; } cardOpen=true; cardT=0; fn(); }\nfunction cardOn(){ return (cardOpen&&!$('#modal').hidden)||cardQ.length>0; }\nfunction closeModal(){ $('#modal').hidden=true; cardOpen=false; }")
rep("  openModal(`<div class=\"${shot?'fairpic':'center'}\">", "  showCard(()=>{ openModal(`<div class=\"${shot?'fairpic':'center'}\">")
rep("  $('#collect').onclick=closeModal;\n}", "  $('#collect').onclick=closeModal; });\n}")
rep("if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!W.paused&&!tutQuiet()){ const pq=W.postQ.shift(), hm=W.homes[pq.i]; if(hm){",
    "if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused){ const fn=cardQ.shift(); cardOpen=true; cardT=0; fn(); }\n  if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!cardQ.length&&!W.paused&&!tutQuiet()){ const pq=W.postQ.shift(), hm=W.homes[pq.i]; if(hm){ cardOpen=true; cardT=0;")
rep("function calmHold(){ return playerBusy()||", "function calmHold(){ return cardOn()||playerBusy()||")
rep("if(meetQ.length&&!cam.meet&&!playerBusy())nextMeet();", "if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardOn())nextMeet();")
rep("if(!cam.meet&&!playerBusy())nextMeet(); }", "if(!cam.meet&&!playerBusy()&&!cardOn())nextMeet(); }")
rep("  if(W.started&&!W.paused)update(dt); else if(W.paused){",
    "  if(cardOpen&&!$('#modal').hidden&&!W.paused)cardT+=dt; else cardT=0; const gdt=cardT>10?dt/3:dt;\n  if(W.started&&!W.paused)update(gdt); else if(W.paused){")
rep("for(const c of W.cats)animateCat(c,W.paused?dt*0.6:dt,t);", "for(const c of W.cats)animateCat(c,W.paused?dt*0.6:gdt,t);")
# families
rep("let visitT=rand(60,90);",
    "let visitT=rand(60,90), famLogT=5;\nfunction famHold(){ return cardOn()||!!cam.meet||meetQ.length>0||!!(W.dropoff&&!W.dropoff.gift)||!!W.runaway||!!fairForce()||!!tips.cur||W.time-(W.lastEv??-999)<20; }\nfunction famDue(){ return !W.family&&visitT<=0&&(W.night||0)<0.55&&(W.cats.some(readyHome)||W.homes.length>0); }")
rep("if(!f){ if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()&&!strayHold()){ visitT-=dt*(W.homes.length?1:3); if(visitT<=0)spawnFamily(); } }",
    "if((famLogT-=dt)<=0){ famLogT=30; rec('famclock',`ready=${W.cats.filter(readyHome).length}/${W.cats.length} visit=${Math.round(visitT)} fam=${f?f.state:'-'} hold=${famHold()?1:0}`); }\n  if(!f){ const rdy=W.cats.some(readyHome); if((rdy||W.homes.length>0)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()){ visitT-=dt*(W.homes.length?(rdy?1:0.6):3); if(visitT<=0&&!famHold()&&(W.homes.length||!strayHold()))spawnFamily(); } }")
rep("if(!f.atGate&&f.state==='arrive'&&f.members.every(m=>m.g.visible&&m.route&&arrived(m))){ f.atGate=true; Snd.chime(); renderFamily(); }",
    "if(!f.atGate&&f.state==='arrive'&&f.members.every(m=>m.g.visible&&m.route&&arrived(m))){ f.atGate=true; Snd.chime(); renderFamily(); }\n    if(f.atGate&&W.homes.length&&!W.pickHome&&['arrive','wait'].includes(f.state)&&!W.cats.some(readyHome)){ f.look=(f.look||0)+dt; if(f.look>7)familyLeave('Maybe later!'); } else f.look=0;")
rep("function spawnFamily(){ const ready=W.cats.filter(readyHome); if(!ready.length)return; const h=LV().half;\n  const want=Math.random()<0.7?pick(ready).trait:pick(TRAITS);",
    "function spawnFamily(){ const ready=W.cats.filter(readyHome); if(!ready.length&&!W.homes.length)return; const h=LV().half; rec('family',ready.length?`arrive, ${ready.length} ready`:'arrive, none ready');\n  const want=ready.length&&Math.random()<0.7?pick(ready).trait:pick(TRAITS);")
rep("function familyLeave(msg){ const f=W.family; if(!f||f.state==='leaving'||f.state==='bye')return;", "function familyLeave(msg){ const f=W.family; if(!f||f.state==='leaving'||f.state==='bye')return; rec('family','leave: '+msg);")
rep("function adoptOK(c){ const f=W.family;", "function adoptOK(c){ const f=W.family; rec('family','adopt '+c.name);")
rep("function startDropoff(gift){ if(firstAdopt()||tutQuiet())return; if(W.dropoff||(!gift&&W.cats.length>=LV().cap))return; const h=LV().half;",
    "function startDropoff(gift){ if(firstAdopt()||tutQuiet())return; if(W.dropoff||(!gift&&W.cats.length>=LV().cap))return; const h=LV().half; rec('stray',gift?'gift':'dropoff');")
rep("if(!firstBye()&&!strayHold()&&W.cats.length<LV().cap&&avgH>=50)startDropoff();", "if(!firstBye()&&!strayHold()&&!famDue()&&W.cats.length<LV().cap&&avgH>=50)startDropoff();")
open(P, 'w', encoding='utf-8').write(s)
print('v128 applied')
