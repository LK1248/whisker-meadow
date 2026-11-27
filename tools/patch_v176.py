"""v176: lessons and events never overlap.
One check, tutAny(), is true while any lesson is on: the petting / blink / pair / brush lessons, the belly, butt and
flea tips, the shop, wand and fair lessons, the guided hints that hold events back, and the first adoption.
- While it's true, none of these start: kittens being born, strays, runaways, visiting families, rain, romps, and
  new-cat cards (they wait in the queue and show once the lesson ends).
- The other way round: tips, the brush / pair / blink / belly lessons and the guided hints don't start while an event
  is on (a stray or family at the gate, a runaway, a new-cat card).
- __wm.forceEv() (testing): zeroes the event timers and tries a birth right away."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function lessonBusy(){ return !!(bt.c||pl.a||br.c); }",
    "function lessonBusy(){ return !!(bt.c||pl.a||br.c); }\n"
    "// any lesson at all: nothing else may start while this is true\n"
    "function tutAny(){ return !!(W.started&&(lessonOn()||tips.cur||shopForce()||wandForce()||fairForce()||firstAdopt()||(curHint&&HINT_HOLD.has(curHint.id)))); }\n"
    "function evBusy(){ return eventOn()||cardUp(); }")
# --- events wait for lessons ---
rep("function tryFamily(){ if(firstAdopt()||tutQuiet())return;", "function tryFamily(){ if(firstAdopt()||tutQuiet()||tutAny()||cardUp()||cam.meet)return;")
rep("function startDropoff(gift){ if(firstAdopt()||tutQuiet())return;", "function startDropoff(gift){ if(firstAdopt()||tutQuiet()||(!gift&&tutAny()))return;")
rep("if(!tutQuiet()&&!strayHold()&&!W.runaway&&!W.family&&W.time>120", "if(!tutQuiet()&&!tutAny()&&!strayHold()&&!W.runaway&&!W.family&&W.time>120")
rep("if((rdy||W.homes.length>0)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()){", "if((rdy||W.homes.length>0)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()&&!tutAny()){")
rep("if(!weather.raining&&weather.t<=0&&tutQuiet())weather.t=20;", "if(!weather.raining&&weather.t<=0&&(tutQuiet()||tutAny()))weather.t=20;")
rep("  if(!tutQuiet()&&Math.random()<(c.age<1?0.25:0.12)&&s.fun<95", "  if(!tutQuiet()&&!tutAny()&&Math.random()<(c.age<1?0.25:0.12)&&s.fun<95")
# new-cat cards wait for any lesson
rep("meetQ.push({c,origin,parents,kits}); if(!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy())nextMeet(); }",
    "meetQ.push({c,origin,parents,kits}); if(!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny())nextMeet(); }")
rep("if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy())nextMeet();",
    "if(meetQ.length&&!cam.meet&&!playerBusy()&&!cardUp()&&!lessonBusy()&&!tutAny())nextMeet();")
# --- lessons wait for events ---
rep("function updateTips(dt){ const busy=tutQuiet()||br.c||", "function updateTips(dt){ const busy=evBusy()||tutQuiet()||br.c||")
rep("function brushReady(){ return !br.c&&", "function brushReady(){ return !evBusy()&&!tips.cur&&!br.c&&")
rep("function pairReady(){ return earlyDone()&&", "function pairReady(){ return !evBusy()&&!tips.cur&&!shopForce()&&!wandForce()&&!fairForce()&&earlyDone()&&")
rep("function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tutLock())return;",
    "function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tutLock()||evBusy()||tips.cur)return;")
rep("&&s.aff>=35&&c.state==='pet'&&c.age>=0.5&&!lessonOn()&&!tips.cur&&!tutLock()){ setState(c,'flop',30);",
    "&&s.aff>=35&&c.state==='pet'&&c.age>=0.5&&!lessonOn()&&!tips.cur&&!tutLock()&&!evBusy()&&!shopForce()&&!wandForce()&&!fairForce()){ setState(c,'flop',30);")
rep("  for(const h of HINTS){ if(hintDone.has(h.id)||(hintRetry[h.id]&&W.time<hintRetry[h.id]))continue;",
    "  for(const h of HINTS){ if(hintDone.has(h.id)||(hintRetry[h.id]&&W.time<hintRetry[h.id]))continue; if(HINT_HOLD.has(h.id)&&evBusy())continue; /* guided lessons wait for events */")
# test hook
rep("window.__wm={", "window.__wm={tutAny,evBusy,addBond,forceEv:()=>{ strayT=0; visitT=0; runT=0; weather.t=0; tryFamily(); },")
open(P, 'w', encoding='utf-8').write(s)
print('v176 applied')
