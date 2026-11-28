"""v200: calmer, self-paced game.
1) Silent achievements: goals and badges no longer pop a toast or play a sound. The star button pulses twice and shows a
   small count of new ones. Opening it lists what's new since the last look, and the reward money is collected then.
2) Fleas only come with strays. They no longer appear out of nowhere when a coat gets scruffy. The first stray after the
   brush lesson always brings fleas (so the flea tip has a clear cause), later strays 25% of the time. Stray fleas stay
   until brushed off, and can still hop to a scruffy cat during play.
3) Belly-up pose: a flopped cat turns so its belly faces the player, lifts its head to look at the camera, slow-blinks
   now and then and wiggles a little, so it reads as an invitation, not a fall.
4) Adaptive pacing (middle settings, to tune later):
   - Each lesson, tip and hint is timed from when it appears to when the player does it. Quick players raise a pace
     value (0.6-1.6, starts at 1), slow ones or hints that time out lower it. Skipping leaves it alone.
   - A learning clock runs at that pace (1.6x faster while the player is active but has nothing to do) and drives when
     hints and lessons unlock, instead of raw play time.
   - After one lesson, tip or hint ends, the next waits 20 s / pace (10-40 s).
   - Background events (strays, dropoffs, runaways) keep a gap of 70 s / pace (45-110 s) early on, which grows with the
     sanctuary's stars (up to 2.4x at 5 stars) and by 1.3x while every cat is happy, so a mature sanctuary settles into
     just watching the cats."""
import sys, re
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- 1) silent achievements ----------
rep('<b class="sn" id="bStarN">1</b>', '<b class="sn" id="bStarN">1</b><b class="nw" id="bNewN" hidden></b>')
rep("#goalStrip{display:none!important}",
    "#goalStrip{display:none!important}#bBadges .nw{position:absolute;z-index:1;right:-5px;top:-5px;min-width:19px;height:19px;padding:0 4px;box-sizing:border-box;border-radius:10px;background:#5bb85d;color:#fff;font:800 11px/19px var(--body);text-align:center;box-shadow:0 0 0 2px var(--cream)}"
    "#bBadges.pulse{animation:wmPulse .7s ease 2}@keyframes wmPulse{50%{transform:scale(1.18)}}"
    ".anew{background:#fff8ef;border-radius:16px;padding:8px 12px;margin:0 0 12px;box-shadow:0 2px 6px rgba(60,40,30,.1)}"
    ".anew .ani{display:flex;align-items:center;gap:8px;font:700 14px var(--body);padding:4px 0}.anew .ani span{margin-left:auto;color:var(--leafd);font:700 16px var(--display)}"
    ".anew .gm{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;flex:none;font-style:normal}.anew .gm .cf{width:70%;height:70%}"
    ".anew .gm.t1{background:#e1a06a}.anew .gm.t2{background:#c9d3de}.anew .gm.t3{background:#f6c443}")
rep("function unlock(){}",
    "function unlock(){}\n"
    "// silent achievements: queued on the star button, collected when the player opens it\n"
    "const AN={list:[]};\n"
    "function achPush(n,t,pay,earn){ const st=W.stat; (st.achNew=st.achNew||[]).push({n,t,pay,earn:earn?pay:0}); achDot(); const b=$('#bBadges'); b.classList.remove('pulse'); void b.offsetWidth; b.classList.add('pulse'); }\n"
    "function achDot(){ const n=(W.stat.achNew||[]).length, el=$('#bNewN'); if(!el)return; el.hidden=!n; el.textContent=n; }\n"
    "function achCollect(){ const L=W.stat.achNew||[]; if(!L.length)return; const pay=L.reduce((a,x)=>a+x.pay,0); W.money+=pay; W.earned+=L.reduce((a,x)=>a+x.earn,0); W.stat.achNew=[]; AN.list=L; Snd.coin(); hud(); }\n"
    "function achNewHTML(){ if(!AN.list.length)return ''; return `<div class=\"anew\">${AN.list.map(a=>`<div class=\"ani\"><i class=\"gm t${a.t}\">${CATF}</i>${a.n} \\u00b7 ${TIER_N[a.t]}<span>+$${a.pay}</span></div>`).join('')}</div>`; }")
rep("W.achT[id]=t; snapAch(id); W.money+=rw; W.earned+=rw; hud(); Snd.chime(); toast(`<span class=\"tc\">${CATF}</span>${n} · ${TIER_N[t]} +$${rw}`,'badge',3400);",
    "W.achT[id]=t; snapAch(id); achPush(n,t,rw,true); /* silent: shown on the star button */")
rep("st.goalT[i]=t; W.money+=pay; hud(); toast(`✓ ${g[0]} · ${TIER_N[t]} +$${pay}`,'badge',3000); Snd.coin(); rec('goal',`${g[0]} ${TIER_N[t]}`);",
    "st.goalT[i]=t; achPush(g[0],t,pay,false); rec('goal',`${g[0]} ${TIER_N[t]}`);")
rep("$('#bBadges').onclick=()=>openBadges(); $('#goalStrip').onclick=()=>openBadges('goals');",
    "$('#bBadges').onclick=()=>{ AN.list=[]; achCollect(); openBadges(); }; $('#goalStrip').onclick=()=>{ AN.list=[]; achCollect(); openBadges('goals'); };")
rep("$('#bStarN').textContent=st; }", "$('#bStarN').textContent=st; } achDot();")
rep("openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3><div class=\"sstat\"><span>${W.stars} / 5</span><i class=\"bar\"><i style=\"width:${Math.round(sp*100)}%\"></i></i><span>${RIB} ${W.ribbons}</span></div>${tabs}",
    "openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3><div class=\"sstat\"><span>${W.stars} / 5</span><i class=\"bar\"><i style=\"width:${Math.round(sp*100)}%\"></i></i><span>${RIB} ${W.ribbons}</span></div>${achNewHTML()}${tabs}")

# ---------- 2) fleas only from strays ----------
rep("if(!c.fleas&&s.groom<FLEA_AT&&!c.outside&&Math.random()<dt/40)c.fleas=5+Math.floor(rand(0,4));",
    "/* fleas only arrive with strays now (and hop over during play), they don't appear from a scruffy coat */")
rep("if(origin==='stray'&&W.stat.brushTut&&c.s.groom<FLEA_AT&&!c.fleas&&Math.random()<0.4)c.fleas=5+Math.floor(rand(0,4));",
    "if(origin==='stray'&&W.stat.brushTut&&!c.fleas&&(!W.stat.fleaStray||Math.random()<0.25)){ c.fleas=5+Math.floor(rand(0,4)); c.fleaCaught=true; c.s.groom=Math.min(c.s.groom,30); W.stat.fleaStray=1; } /* first stray after the brush lesson always brings fleas */")

# ---------- 3) belly-up pose ----------
rep("else if(st==='flop'){ rz=2.45; coreY=0.36; legA=[Math.sin(t*2)*0.3,Math.sin(t*2+1)*0.3,0.3,0.3]; tailUp=0; swish=0.25; eye=purring?0.4:0.8; hz=-0.6; if(c.trap>0){ legA=[-1.2,-1.2,1.0,1.0]; } }",
    "else if(st==='flop'){ const inv=!c.carried&&!(c.trap>0); rz=inv?2.05+Math.sin(t*1.4+c.id)*0.12:2.45; coreY=0.36; legA=inv?[-0.9+Math.sin(t*2)*0.25,-0.9+Math.sin(t*2+1)*0.25,0.4,0.3]:[Math.sin(t*2)*0.3,Math.sin(t*2+1)*0.3,0.3,0.3]; tailUp=0; swish=inv?0.35:0.25; swSpd=inv?1.4:swSpd;\n"
    "    eye=purring?0.4:0.85; if(inv&&((t*0.45+c.id*0.37)%3.2)<0.5)eye=0.12; /* a slow blink now and then */ hz=-0.6; if(c.trap>0){ legA=[-1.2,-1.2,1.0,1.0]; }\n"
    "    if(inv){ const dx=camera.position.x-c.g.position.x, dz=camera.position.z-c.g.position.z, want=Math.atan2(-dz,dx); let d=want-c.heading; d=Math.atan2(Math.sin(d),Math.cos(d)); c.heading+=d*Math.min(1,dt*3); } } /* belly toward the player */")
# head looks at the camera while flopped (after the normal head pose is applied)
rep("c.head.rotation.y=lerp(c.head.rotation.y,hy,Math.min(1,dt*(c.snap>0?20:5)));",
    "c.head.rotation.y=lerp(c.head.rotation.y,hy,Math.min(1,dt*(c.snap>0?20:5)));\n"
    "  flopLook(c,dt,st==='flop'&&!c.carried&&!(c.trap>0)&&c.g.parent===scene);")
rep("function animateCat(c,dt,t){",
    "const FL_M=new THREE.Matrix4(), FL_Q=new THREE.Quaternion(), FL_P=new THREE.Quaternion(), FL_H=new THREE.Vector3(), FL_V=new THREE.Vector3(), FL_UP=new THREE.Vector3();\n"
    "function flopLook(c,dt,on){ if(!c.headP0)c.headP0=c.head.position.clone();\n"
    "  if(!on){ if(c.lookQ){ c.head.position.lerp(c.headP0,Math.min(1,dt*6)); if(c.head.position.distanceToSquared(c.headP0)<1e-5){ c.head.position.copy(c.headP0); c.lookQ=null; } } return; }\n"
    "  c.g.updateMatrixWorld(true); const sc=c.g.scale.x; c.core.getWorldPosition(FL_H); FL_H.x+=Math.sin(c.heading)*0.42*sc; FL_H.z+=Math.cos(c.heading)*0.42*sc; FL_H.y+=0.2*sc; /* head lifted off the ground */\n"
    "  c.head.position.lerp(c.core.worldToLocal(FL_V.copy(FL_H)),Math.min(1,dt*4)); c.head.getWorldPosition(FL_H);\n"
    "  FL_UP.set(0.25*Math.sin(W.time*0.7+c.id),1,0).normalize(); /* a playful head tilt */ FL_M.lookAt(camera.position,FL_H,FL_UP); FL_Q.setFromRotationMatrix(FL_M); c.core.getWorldQuaternion(FL_P); FL_P.invert().multiply(FL_Q);\n"
    "  if(!c.lookQ)c.lookQ=c.head.quaternion.clone(); c.lookQ.slerp(FL_P,Math.min(1,dt*4)); c.head.quaternion.copy(c.lookQ); } // the head keeps looking at the player\n"
    "function animateCat(c,dt,t){")

# ---------- 4) adaptive pacing ----------
rep("function calmTick(){ if(eventOn())W.lastEv=W.time; }",
    "function calmTick(){ if(eventOn())W.lastEv=W.time; }\n"
    "// adaptive pacing: how fast the player picks things up sets how fast new things arrive\n"
    "const PACE={k:null,t0:0,res:null,end:-99};\n"
    "function pace(){ return W.stat.pace||1; }\n"
    "function LT(){ return W.stat.lt??W.time; } // learning clock: drives hint and lesson unlocks\n"
    "function teachOk(){ return W.time-PACE.end>=clamp(20/pace(),10,40); } // a breather after each lesson, tip or hint\n"
    "function evGap(){ const happy=W.cats.length&&W.cats.every(c=>c.s.aff>=70); return clamp(70/pace(),45,110)*(1+0.35*((W.stars||1)-1))*(happy?1.3:1); } // grows as the sanctuary matures\n"
    "function teachKey(){ return intro.c?'L:intro':bt.c?'L:blink':pl.a?'L:pair':br.c?'L:brush':tips.cur?'T:'+tips.cur.kind:curHint?'H:'+curHint.id:null; }\n"
    "function paceTick(dt){ if(!W.started||W.paused)return; const st=W.stat; if(st.lt==null)st.lt=W.time;\n"
    "  const bored=W.time-(W.lastInput||-99)<15&&!petRecent()&&!uiUp()&&!eventOn()&&W.cats.length>0&&W.cats.every(c=>c.s.aff>=60); /* active, but nothing to do */\n"
    "  st.lt+=dt*pace()*(bored?1.6:1);\n"
    "  const k=teachKey(); if(k===PACE.k)return;\n"
    "  if(PACE.k){ const dur=W.time-PACE.t0, E=PACE.k[0]==='L'?20:PACE.k[0]==='T'?8:10;\n"
    "    if(PACE.res!=='skip'&&PACE.k!=='H:pet'){ const r=PACE.res==='slow'?0.5:clamp(E/Math.max(1,dur),0.4,2.5); st.pace=clamp(Math.pow(pace(),0.7)*Math.pow(r,0.3),0.6,1.6); rec('pace',`${PACE.k} ${dur.toFixed(1)}s -> ${st.pace.toFixed(2)}`); }\n"
    "    PACE.end=W.time; }\n"
    "  PACE.k=k; PACE.t0=W.time; PACE.res=null; }")
rep("W.time-(W.lastEv??-999)<(W.time<900?90:50); }", "W.time-(W.lastEv??-999)<evGap(); }")
rep("function updateHints(dt){ tutLockTick(); needTick(dt); calmTick();", "function updateHints(dt){ tutLockTick(); needTick(dt); calmTick(); paceTick(dt);")
rep("function skipLesson(){ rec('skip',recLesson());", "function skipLesson(){ rec('skip',recLesson()); PACE.res='skip';")
rep("if(h.auto&&hintT>h.auto){", "if(h.auto&&hintT>h.auto){ PACE.res='skip';")
rep("if(hintT>22&&!shopForce()&&!fairForce()&&!wandForce()){ hintRetry[h.id]=W.time+50;", "if(hintT>22&&!shopForce()&&!fairForce()&&!wandForce()){ PACE.res='slow'; hintRetry[h.id]=W.time+50;")
# hints unlock on the learning clock, and wait for the breather (except urgent / petting ones)
i = s.index('const HINTS=['); j = s.index('\n];', i)
block = s[i:j]; n = block.count('W.time>')
s = s[:i] + block.replace('W.time>', 'LT()>') + s[j:]
print('hint time checks moved to the learning clock:', n)
rep("if(petting&&h.id!=='pet'&&h.id!=='belly')continue; /* don't cut into petting */",
    "if(petting&&h.id!=='pet'&&h.id!=='belly')continue; /* don't cut into petting */ if(!teachOk()&&!['pet','find','roof','show0'].includes(h.id))continue; /* a breather between lessons */")
rep("!W.runaway&&W.time>70; }", "!W.runaway&&LT()>70&&teachOk(); }")
rep("(W.stat.blinkBack>0||W.time>150)&&W.time>70&&", "(W.stat.blinkBack>0||LT()>150)&&LT()>70&&teachOk()&&")
rep("if(bt.c||intro.c||pl.a||firstAdopt()||tutLock()||evBusy()||tips.cur||!uiGapOk()||petRecent())return;",
    "if(bt.c||intro.c||pl.a||firstAdopt()||tutLock()||evBusy()||tips.cur||!uiGapOk()||petRecent()||!teachOk())return;")
rep("const flea=active().find(c=>c.fleas&&(!W.stat.fleaTip||", "const flea=teachOk()&&active().find(c=>c.fleas&&(!W.stat.fleaTip||")
rep("(!W.stat.brushTut&&W.time<900)", "(!W.stat.brushTut&&LT()<900)")
rep("W.time>120&&W.time-W.lastInput<30", "LT()>120&&W.time-W.lastInput<30")
rep("window.__wm={AW,cardQ,uiGapOk,petRecent,", "window.__wm={AW,cardQ,uiGapOk,petRecent,PACE,evGap,teachOk,LT,achPush,flopLook,")
open(P, 'w', encoding='utf-8').write(s)
print('v200 applied')
