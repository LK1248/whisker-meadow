"""v68: calmer pacing.
- Breathing room: after any event (stray drop-off, adoption family, runaway, welcome sheet) ends, no new one starts
  for 90 s in the first 15 minutes of play, 50 s after that.
- Don't interrupt play: no new event starts while the player is petting, brushing, or playing with the wand/laser
  (and for 6 s after their last touch). Welcome sheets (e.g. newborn kittens) wait for the same quiet moment."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function strayHold(){ return ",
    "// calm pacing: a player who is busy with a cat or a toy is never interrupted, and events get breathing room\n"
    "function playerBusy(){ if(W.time-(W.lastInput||-99)>=6)return false; return W.tool!=='hand'||!!(S.cat&&S.cat.petT>0)||P.mode==='carry'||P.mode==='stroke'; }\n"
    "function eventOn(){ return !!(W.dropoff&&!W.dropoff.gift)||!!W.family||!!W.runaway||!!cam.meet||meetQ.length>0; }\n"
    "function calmTick(){ if(eventOn())W.lastEv=W.time; }\n"
    "function calmHold(){ return playerBusy()||W.time-(W.lastEv??-999)<(W.time<900?90:50); }\n"
    "function strayHold(){ return calmHold()||")
rep("function meet(c,origin,parents){", "function meet(c,origin,parents){ W.lastEv=W.time;")
rep("meetQ.push({c,origin,parents}); if(!cam.meet)nextMeet(); }",
    "meetQ.push({c,origin,parents}); if(!cam.meet&&!playerBusy())nextMeet(); }")
rep("function updateHints(dt){ needTick(dt); ",
    "function updateHints(dt){ needTick(dt); calmTick(); if(meetQ.length&&!cam.meet&&!playerBusy())nextMeet(); ")
rep("window.__wm={Snd,", "window.__wm={Snd,playerBusy,calmHold,eventOn,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("if(P.pointers.has(e.pointerId))P.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});",
    "if(P.pointers.has(e.pointerId)){ P.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY}); if(!W.paused)W.lastInput=W.time; }")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
