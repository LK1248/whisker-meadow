"""v17: the first adoption gets the stage: no new cats, births, runaways or lessons while it plays out; camera follows it."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# while the very first family is here (no cat adopted yet), hold everything else
rep("function tryFamily(){", """function firstAdopt(){ return !!(W.family&&!W.homes.length); }
function updateFirstAdopt(dt){ const f=W.family, on=firstAdopt()&&f.cat&&['walking','greet','bye'].includes(f.state)&&!f.cat.outside;
  if(on){ if(cam.fa==null){ cam.fa=cam.want; leaveClose(false); tag.c=null; hideHint(); } cam.focus=f.cat; cam.focusT=0.3; cam.want=lerp(cam.want,Math.min(cam.fa,5.5),Math.min(1,dt*1.5)); }
  else if(cam.fa!=null){ cam.want=Math.max(cam.want,cam.fa); cam.fa=null; } }
function tryFamily(){ if(firstAdopt())return;""")
rep("function startDropoff(){ if(W.dropoff||", "function startDropoff(){ if(firstAdopt())return; if(W.dropoff||")
rep("function pairReady(){ return !pl.a&&", "function pairReady(){ return !firstAdopt()&&!pl.a&&")
rep("function updateTips(dt){ const busy=intro.c||", "function updateTips(dt){ const busy=firstAdopt()||intro.c||")
rep("function updateHints(dt){ if(intro.c||bt.c||pl.a){", "function updateHints(dt){ if(intro.c||bt.c||pl.a||(firstAdopt()&&W.family.cat)){")
rep("  updateIntro(dt); updateBlinkTut(dt);", "  updateFirstAdopt(dt); updateIntro(dt); updateBlinkTut(dt);")
rep("window.__wm={animateCat,", "window.__wm={animateCat,firstAdopt,")
rep("function startBlinkTut(c){ if(bt.c||intro.c||pl.a)return;", "function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt())return;")
# a drop-off already at the gate waits with its box until the first adoption is done
rep("else if(D.stage==='drop'){ D.t+=dt;", "else if(D.stage==='drop'){ if(!(firstAdopt()&&!D.done))D.t+=dt;")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
