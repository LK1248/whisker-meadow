"""v58: the friends lesson is one clear action.
While the lesson waits for the carry:
- Only the first cat can be picked up. Taps on other cats or on items do nothing (the screen just pans), and the
  dock and top buttons stay off as before.
- The first cat never wiggles free while it's held.
- Other cats are walked out of the way, so none wander between the two or into the drop spot.
- Only dropping the first cat next to the second cat counts; dropping it anywhere else replays the guide.
The two lesson cats stay the pair for the boop and romp that follow, still with no other cats crowding in.
- Strays wait until the lessons are done (or 15 min in), then 40 s more, and never arrive while follow-up guidance
  (wand, brush, shop, feeding, litter, carry, roof) is on screen."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# pointer down: during the carry lesson only the first cat responds
rep("  if(hit&&hit.item&&hit.item.kind!=='shelter'){ P.mode='item'; P.item=hit.item; handVis(); return; }\n  if(W.tool==='wand'){",
    "  if(pl.a&&pl.stage==='carry'&&hit&&hit.cat!==pl.a)hit=null;\n"
    "  if(hit&&hit.item&&hit.item.kind!=='shelter'){ P.mode='item'; P.item=hit.item; handVis(); return; }\n  if(W.tool==='wand'){")
# held cat doesn't wiggle free during the lesson
rep("if(c.carried){ c.speed=0; c.holdT+=dt; if(c.holdT>=c.tol)hopFree(c); return; }",
    "if(c.carried){ c.speed=0; c.holdT+=dt; if(pl.a===c&&pl.stage==='carry')c.holdT=0; if(c.holdT>=c.tol)hopFree(c); return; }")
# only "first cat dropped next to the second" counts
rep("""    // whichever cat was carried, whichever cat it landed next to: that's the pair we watch
    const o=d&&active().filter(k=>k!==d&&!k.carried).sort((x,y)=>dist2(x.g.position,d.g.position)-dist2(y.g.position,d.g.position))[0];
    if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){ pl.a=d; pl.b=o;""",
"""    // the first cat, dropped next to the second one
    const o=d===a?b:null;
    if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){""")
# keep the other cats out of the way during the whole lesson
rep("""  const pa=a.g.position, pb=b.g.position;
  if(pl.stage==='carry'){""",
"""  const pa=a.g.position, pb=b.g.position;
  pl.clearT=(pl.clearT||0)-dt; if(pl.clearT<=0){ pl.clearT=0.5; const mid=pa.clone().add(pb).multiplyScalar(0.5), rad=Math.max(2.4,Math.sqrt(dist2(pa,pb))/2+1.6);
    for(const c of active()){ if(c===a||c===b||c.carried||c.outside||c.leaving||c.away>0)continue; const p=c.g.position, d=Math.sqrt(dist2(p,mid));
      if(d<rad&&!(c.state==='walk'&&c.clearing)){ const dir=new V3(p.x-mid.x,0,p.z-mid.z); if(dir.lengthSq()<1e-4)dir.set(1,0,0); dir.normalize(); goTo(c,mid.x+dir.x*(rad+1.2),mid.z+dir.z*(rad+1.2),null); c.clearing=true; }
      else if(c.state!=='walk')c.clearing=false; } }
  if(pl.stage==='carry'){""")
rep("function endPairTut(ok){ const {a,b}=pl; if(!a)return;", "function endPairTut(ok){ const {a,b}=pl; if(!a)return; for(const c of W.cats)c.clearing=false;")
# strays wait for the tutorial and its follow-up guidance: the whole lesson set done (or 15 min in), 40 s of breathing
# room after the brush lesson, and no stray while the wand/brush/shop/feeding guidance is on screen
rep("if(!firstBye()&&W.cats.length<LV().cap&&avgH>=50)startDropoff();",
    "if(!firstBye()&&!strayHold()&&W.cats.length<LV().cap&&avgH>=50)startDropoff();")
rep("function strayGap(){", "const HINT_HOLD=new Set(['feed','litter','carry','shop','wand','wand2','brush','brush2','roof']);\n"
    "function strayHold(){ return (!W.stat.brushTut&&W.time<900)||W.time<(W.stat.brushTutT||0)+40||!!(curHint&&HINT_HOLD.has(curHint.id)); }\nfunction strayGap(){")
rep("window.__wm={Snd,", "window.__wm={Snd,endPairTut,strayHold,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
