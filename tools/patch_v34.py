"""v34: tutorial quiet mode. While any lesson runs, and until the first three (pet, slow blink, pair) are done, the meadow holds
its events: no families, arrivals, runaways, births, rain, romps, boops, hints or tips, no gazes except the blink lesson's,
and no icons from cats other than the lesson cat(s) or the one in your hand. A 6-minute failsafe ends it for players who never pet."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function lessonOn(){ return !!(intro.c||bt.c||pl.a); }",
"""function lessonOn(){ return !!(intro.c||bt.c||pl.a||br.c); }
// quiet while a lesson runs, and until the three opening lessons are through
function tutQuiet(){ return !!(W.started&&(lessonOn()||(!W.stat.pairDone&&W.time<360))); }
function lessonCat(c){ return !!c&&(c===intro.c||c===bt.c||c===pl.a||c===pl.b||c===br.c); }
function blinkPending(){ return !W.stat.blinkBack&&!bt.skipped&&!bt.c&&!intro.c; }""")

# icons: only the lesson cat(s) and the cat you're touching may pop icons
rep("function showIcon(c,kind,dur=2.5){ c.icon.material.map=",
    "function showIcon(c,kind,dur=2.5){ if(tutQuiet()&&!lessonCat(c)&&!c.carried&&S.cat!==c&&P.cat!==c&&!(c.petT>0&&handOn(c)))return; c.icon.material.map=")

# gazes / slow blinks: only the one that starts the blink lesson
rep("if(s.trust>=35&&!c.carried&&['idle','pet','shelter','watch'].includes(c.state)&&c.gaze<=0){ c.gazeT-=dt;",
    "if(s.trust>=35&&!c.carried&&['idle','pet','shelter','watch'].includes(c.state)&&c.gaze<=0&&(!tutQuiet()||(blinkPending()&&!lessonOn()&&!S.cat&&P.mode!=='carry'))){ c.gazeT-=dt;")

# events
rep("function tryFamily(){ if(firstAdopt())return;", "function tryFamily(){ if(firstAdopt()||tutQuiet())return;")
rep("function startDropoff(gift){ if(firstAdopt())return;", "function startDropoff(gift){ if(firstAdopt()||tutQuiet())return;")
rep("if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55){ visitT-=dt;", "if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()){ visitT-=dt;")
rep("runT-=dt; if(runT<=0){ runT=15; if(!W.runaway&&!W.family&&", "runT-=dt; if(runT<=0){ runT=15; if(!tutQuiet()&&!W.runaway&&!W.family&&")
rep("  if(!weather.raining&&weather.t<=0){ weather.raining=true;", "  if(!weather.raining&&weather.t<=0&&tutQuiet())weather.t=20;\n  if(!weather.raining&&weather.t<=0){ weather.raining=true;")
rep("if(Math.random()<(c.age<1?0.25:0.12)&&s.fun<95&&c.age>0.2){", "if(!tutQuiet()&&Math.random()<(c.age<1?0.25:0.12)&&s.fun<95&&c.age>0.2){")
rep("    for(let i=0;i<act.length;i++)for(let j=i+1;j<act.length;j++){ const a=act[i],b=act[j]; if(dist2(a.g.position,b.g.position)<1.9){",
    "    for(let i=0;i<act.length;i++)for(let j=i+1;j<act.length;j++){ const a=act[i],b=act[j]; if(dist2(a.g.position,b.g.position)<1.9){ const hush=tutQuiet()&&!(lessonCat(a)&&lessonCat(b));")
rep("if(getBond(a,b)>10&&canBoop(a)&&canBoop(b)&&Math.random()<0.09)boop(a,b); else if(getBond(a,b)>15&&Math.random()<0.05)heartBetween(a,b);",
    "if(hush){} else if(getBond(a,b)>10&&canBoop(a)&&canBoop(b)&&Math.random()<0.09)boop(a,b); else if(getBond(a,b)>15&&Math.random()<0.05)heartBetween(a,b);")
rep("if(act.length>LV().cap&&getBond(a,b)<20&&Math.random()<0.03){", "if(!hush&&act.length>LV().cap&&getBond(a,b)<20&&Math.random()<0.03){")
# hints and tips wait too
rep("function updateHints(dt){ if(intro.c||bt.c||pl.a||br.c||", "function updateHints(dt){ if(tutQuiet()||intro.c||bt.c||pl.a||br.c||")
rep("function updateTips(dt){ const busy=br.c||", "function updateTips(dt){ const busy=tutQuiet()||br.c||")
# after the petting lesson, a friendly cat looks over soon so the blink lesson doesn't keep you waiting
rep("function endIntro(){ const c=intro.c; if(!c)return; intro.c=null;",
    "function endIntro(){ const c=intro.c; if(!c)return; intro.c=null; for(const k of W.cats)k.gazeT=Math.min(k.gazeT||99,rand(6,12));")
rep("window.__wm={animateCat,", "window.__wm={animateCat,tutQuiet,lessonCat,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
