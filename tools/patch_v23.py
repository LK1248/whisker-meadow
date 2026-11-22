"""v23: stroking a moving cat: if it wants pets it stops for you; if not, it squirms, hops and trots off."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function beginStroke(c,now){", """function petReact(c){ if(!c||c.carried||c.outside||c.leaving||c.away>0)return true;
  const moving=c.speed>0.12||['walk','chase','stalk','zoom','pounce','laser'].includes(c.state); if(!moving||['path','greet','bye','hiding','boop','romp'].includes(c.state))return true;
  const wants=c.s.trust>=30&&c.over<1.4&&!['chase','laser','pounce'].includes(c.state);
  if(wants){ setState(c,'pet',3); c.speed=0; c.path=null; c.petT=3; c.lean=0.6; return true; }
  if((c.dodgeCD||0)<=W.time){ c.dodgeCD=W.time+2.5; hop(c,0.35,0.45); c.flick=0.8; showIcon(c,'huff',1.2); walkAway(c); Snd.meow(0.85,0.35); }
  return false; }
function beginStroke(c,now){""")
# start of a stroke on a cat: let it react; a cat that dodges isn't stroked
rep("  if(P.mode==='catPending'&&P.moved){ P.mode='stroke'; $('#ring').hidden=true; beginStroke(P.cat,performance.now()); }",
    "  if(P.mode==='catPending'&&P.moved){ P.mode='stroke'; $('#ring').hidden=true; if(W.tool==='hand'&&!petReact(P.cat)){ P.mode='none'; P.cat=null; } else beginStroke(P.cat,performance.now()); }")
rep("  if(h.cat!==S.cat){ if(S.cat)finishStroke(); beginStroke(h.cat,now); }",
    "  if(h.cat!==S.cat){ if(S.cat)finishStroke(); if(W.tool==='hand'&&!petReact(h.cat)){ S.cat=null; return; } beginStroke(h.cat,now); }")
rep("window.__wm={animateCat,", "window.__wm={animateCat,petReact,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
