"""v115: a shorter opening, care that visibly pays, and goals you can see.
1) Lessons: petting -> brushing -> the cat fair come first (the money loop). Slow blink and carrying two cats wait
   until after the first fair (or 10 min, or if the fair lesson is skipped). Tips no longer wait for the pair lesson.
2) Tips: the donation jar is replaced by each cat leaving small tips, shown over that cat. A cat's tip depends on its
   love, health, coat and fullness (fleas cost a bit); a well-kept cat tips ~$2 every 25s, a neglected one nothing.
   About the same total as the old jar for a cared-for meadow. The first tip explains itself once.
3) Goals strip: under the top-left counters, the next two goals with progress bars plus progress to the next star;
   tap it to open the goals tab, which now says how stars are earned. Finished goals are replaced by new ones (and
   targets grow each full round). The first goals point at the money loop: win a ribbon, brush a coat, fill bowls.
   Hidden during lessons and until the brushing lesson is done."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- 1) lesson order ----
rep("function blinkPending(){ return !W.stat.blinkBack&&!bt.skipped&&!bt.c&&!intro.c; }",
    "function earlyDone(){ return (W.stat.shows||0)>0||!!W.stat.fairSkip||W.time>600; } // blink + pair lessons wait for the first fair\n"
    "function blinkPending(){ return !W.stat.blinkBack&&!bt.skipped&&!bt.c&&!intro.c&&earlyDone(); }")
rep("if(!W.stat.blinkBack&&!bt.c&&!bt.skipped&&!intro.c&&W.started&&!W.paused)startBlinkTut(c);",
    "if(!W.stat.blinkBack&&!bt.c&&!bt.skipped&&!intro.c&&W.started&&!W.paused&&earlyDone())startBlinkTut(c);")
rep("function brushReady(){ return !br.c&&!br.done&&W.stat.pairDone&&!W.stat.brushTut&&",
    "function brushReady(){ return !br.c&&!br.done&&(W.stat.good||0)>=3&&!W.stat.brushTut&&")
rep("&&!W.runaway&&W.time>(W.stat.pairDoneT!=null?W.stat.pairDoneT+25:200); }", "&&!W.runaway&&W.time>70; }")
rep("function pairReady(){ return !firstAdopt()&&", "function pairReady(){ return earlyDone()&&!firstAdopt()&&")
rep("if(!tips.cur){ if(busy||!W.stat.pairDone||curHint||hintGap>0)return;", "if(!tips.cur){ if(busy||!W.stat.brushTut||curHint||hintGap>0)return;")
rep("if(origin==='stray'&&W.stat.pairDone&&c.s.groom<FLEA_AT", "if(origin==='stray'&&W.stat.brushTut&&c.s.groom<FLEA_AT")
rep("if(curHint.id==='show0')hintDone.add('show'); hideHint(); } }",
    "if(curHint.id==='show0'||curHint.id==='show'){ hintDone.add('show'); W.stat.fairSkip=1; } hideHint(); } }")

# ---- 2) per-cat tips instead of the jar ----
rep("donT-=dt; if(donT<=0){ donT=25; const a=active().filter(c=>!c.outside); if(a.length){ const happy=a.reduce((s,c)=>s+(c.s.aff+c.s.health)/2,0)/a.length; const amt=Math.round(a.length*happy/100*2*(1+W.stars*0.2)); if(amt>0){ W.money+=amt; W.earned+=amt; if(W.jarPos)floatWorld(W.jarPos.clone().setY(1.2),'+$'+amt); hud(); } } }",
    "donT-=dt; if(donT<=0){ donT=1; let got=0; for(const c of active()){ if(c.outside||c.carried||c.leaving)continue; c.tipT=(c.tipT??rand(8,25))-1; if(c.tipT>0)continue; c.tipT=rand(22,28);\n"
    "    const s=c.s, care=clamp(((s.aff+s.health+s.groom+s.full)/4-(c.fleas?15:0)-45)/40,0,1), amt=Math.round(2.2*care*(1+W.stars*0.2)); if(amt<=0)continue;\n"
    "    W.money+=amt; W.earned+=amt; W.stat.tips=(W.stat.tips||0)+amt; got+=amt; floatWorld(c.g.position.clone().setY(1.25*c.g.scale.x+0.2),'+$'+amt); }\n"
    "  if(got){ hud(); if(!W.stat.tipNote&&W.started&&!tutLock()){ W.stat.tipNote=1; toast('Happy, groomed, well-fed cats leave tips','badge',4200); } } }")

# ---- 3) goals strip ----
rep("function pickGoals(){ const idx=[...GOALS.keys()].sort(()=>Math.random()-0.5).slice(0,3); W.goals=idx.map(i=>({i,base:GOALS[i][1](),done:false})); }",
    "const GOAL_START=[7,3,2]; // win a ribbon, brush a coat, fill the bowls: the money loop first\n"
    "function pickGoals(){ W.goals=GOAL_START.map(i=>({i,base:GOALS[i][1](),done:false,k:1})); W.goalUsed=[...GOAL_START]; W.goalRound=0; }\n"
    "function goalT(g){ return GOALS[g.i][2]*(g.k||1); }\n"
    "function nextGoal(){ const cur=new Set(W.goals.map(g=>g.i)); W.goalUsed=W.goalUsed||[]; let pool=[...GOALS.keys()].filter(i=>!cur.has(i)&&!W.goalUsed.includes(i));\n"
    "  if(!pool.length){ W.goalRound=(W.goalRound||0)+1; W.goalUsed=[...cur]; pool=[...GOALS.keys()].filter(i=>!cur.has(i)); } const i=pick(pool); W.goalUsed.push(i); return {i,base:GOALS[i][1](),done:false,k:1+(W.goalRound||0)}; }")
rep("function updateGoals(){ for(const g of W.goals){ if(g.done)continue; const [n,f,tg]=GOALS[g.i];",
    "function updateGoals(){ W.goals.forEach((g,j)=>{ if(g.done&&W.time-(g.doneT||0)>4)W.goals[j]=nextGoal(); }); for(const g of W.goals){ if(g.done)continue; const [n,f]=GOALS[g.i], tg=goalT(g);")
rep("if(f()-g.base>=tg){ g.done=true; W.money+=15;", "if(f()-g.base>=tg){ g.done=true; g.doneT=W.time; W.money+=15;")
rep("} } }\n\n/* ================= UI ================= */",
    "} } renderGoals(); }\n"
    "function renderGoals(){ const el=$('#goalStrip'); if(!el)return; const rows=W.goals.slice(0,2).map(g=>{ const [n,f]=GOALS[g.i], tg=goalT(g), v=g.done?tg:Math.max(0,Math.min(tg,f()-g.base));\n"
    "    return `<div class=\"gr${g.done?' done':''}\"><span>${g.done?'✓ ':''}${n}</span><em>${g.done?'+$15':v+'/'+tg}</em></div><div class=\"gb\"><i style=\"width:${Math.round(v/tg*100)}%\"></i></div>`; }).join('');\n"
    "  const sp=starPts(), nx=W.stars<5?STAR_AT[W.stars+1]:0, star=nx?`<div class=\"gr st\"><span>Next ★</span><em>${Math.min(sp,nx)}/${nx}</em></div><div class=\"gb st\"><i style=\"width:${Math.round(Math.min(1,sp/nx)*100)}%\"></i></div>`:'';\n"
    "  el.innerHTML=rows+star; }\n"
    "function goalStripTick(){ const el=$('#goalStrip'); const on=W.started&&!W.paused&&!!W.stat.brushTut&&!tutLock()&&!intro.c&&!lessonOn()&&$('#modal').hidden&&W.goals.length>0; if(el.hidden!==!on){ el.hidden=!on; if(on)renderGoals(); } if(on){ const b=$('.hud-l').getBoundingClientRect().bottom; el.style.top=(b+6)+'px'; } }\n\n"
    "/* ================= UI ================= */")
rep("function updateStars(){ const a=active().filter(c=>!c.outside); const happy=a.length?a.reduce((s,c)=>s+(c.s.aff+c.s.health)/2,0)/a.length:0;\n"
    "  const pts=W.homes.length*12+W.stat.rescues*4+W.ribbons*2+W.level*6+W.stat.kittens*2+W.stat.found*3+(happy>=70?10:happy>=55?5:0);",
    "function starPts(){ const a=active().filter(c=>!c.outside); const happy=a.length?a.reduce((s,c)=>s+(c.s.aff+c.s.health)/2,0)/a.length:0;\n"
    "  return W.homes.length*12+W.stat.rescues*4+W.ribbons*2+W.level*6+W.stat.kittens*2+W.stat.found*3+(happy>=70?10:happy>=55?5:0); }\n"
    "function updateStars(){ const pts=starPts();")
# goals tab: grown targets + how stars work
rep("else body=W.goals.map(g=>{ const [n,f,tg]=GOALS[g.i]; const v=",
    "else body=W.goals.map(g=>{ const [n,f]=GOALS[g.i], tg=goalT(g); const v=")
rep("<span>${g.done?'+$15':`${v} / ${tg}`}</span></div>`; }).join('');",
    "<span>${g.done?'+$15':`${v} / ${tg}`}</span></div>`; }).join('')+`<p class=\"starHow\">Each goal pays $15, and a new one takes its place.<br><b>Stars</b> grow with your sanctuary: a home found +12, a rescue +4, a runaway found +3, a ribbon +2, a kitten +2, each bigger meadow +6, and happy cats +5 / +10. ${W.stars<5?`Next ★ at ${STAR_AT[W.stars+1]} (you have ${starPts()}).`:'All five stars!'} Stars unlock upgrades and raise tips.</p>`;")
# markup, style, hooks
rep('<div class="hud-r">', '<button id="goalStrip" class="pill" hidden aria-label="Goals"></button>\n<div class="hud-r">')
rep(".hud-l{position:fixed;", "#goalStrip{position:fixed;left:calc(10px + env(safe-area-inset-left,0px));top:60px;z-index:5;width:min(220px,55vw);padding:7px 12px 8px;border-radius:16px;text-align:left;font:700 12.5px/1.2 var(--body);color:#6b5546;display:flex;flex-direction:column;gap:3px;cursor:pointer}#goalStrip .gr{display:flex;justify-content:space-between;gap:8px}#goalStrip .gr em{font-style:normal;color:#a08876;font-variant-numeric:tabular-nums}#goalStrip .gr.done{color:#3f8f3a}#goalStrip .gb{height:4px;border-radius:3px;background:#efe3d3;overflow:hidden;margin-bottom:3px}#goalStrip .gb i{display:block;height:100%;background:#5fb35a;border-radius:3px;transition:width .5s}#goalStrip .gb.st i{background:#f6c443}#goalStrip .gr.st{color:#b07d10}.starHow{margin:12px 2px 0;color:var(--muted);font:700 13px/1.45 var(--body)}\n.hud-l{position:fixed;")
rep("$('#bBadges').onclick=()=>openBadges();", "$('#bBadges').onclick=()=>openBadges(); $('#goalStrip').onclick=()=>openBadges('goals');")
rep("function tutLockTick(){ const L=tutLock(), b=document.body;", "function tutLockTick(){ goalStripTick(); const L=tutLock(), b=document.body;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
# new goals only for things the player has already met (blink back, carrying, wand, butt taps)
s = open(P, encoding='utf-8').read()
rep("function nextGoal(){ const cur=new Set(W.goals.map(g=>g.i)); W.goalUsed=W.goalUsed||[]; let pool=[...GOALS.keys()].filter(i=>!cur.has(i)&&!W.goalUsed.includes(i));",
    "const GOAL_OPEN={4:()=>W.stat.blinkBack>0||bt.skipped,5:()=>hintDone.has('wand')||(W.stat.wandPounces||0)>0,6:()=>!!W.stat.pairDone,9:()=>!!W.stat.buttTip||(W.stat.butt||0)>0};\n"
    "function nextGoal(){ const cur=new Set(W.goals.map(g=>g.i)), open=i=>!GOAL_OPEN[i]||GOAL_OPEN[i](); W.goalUsed=W.goalUsed||[]; let pool=[...GOALS.keys()].filter(i=>!cur.has(i)&&!W.goalUsed.includes(i)&&open(i));")
rep("if(!pool.length){ W.goalRound=(W.goalRound||0)+1; W.goalUsed=[...cur]; pool=[...GOALS.keys()].filter(i=>!cur.has(i)); }",
    "if(!pool.length){ pool=[...GOALS.keys()].filter(i=>!cur.has(i)&&!W.goalUsed.includes(i)); if(!pool.length||pool.every(i=>!open(i))){ W.goalRound=(W.goalRound||0)+1; W.goalUsed=[...cur]; pool=[...GOALS.keys()].filter(i=>!cur.has(i)&&open(i)); if(!pool.length)pool=[...GOALS.keys()].filter(i=>!cur.has(i)); } else pool=pool.filter(open).length?pool.filter(open):pool; }")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
