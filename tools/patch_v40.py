"""v40: Herding Cats badge. Lead a group of 3 / 6 / 10 cats together with the wand or the laser.
A cat counts once it has followed the lure at least 3 m from where it started following, and is still close to the lure."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("['ouch','Band-Aid Club','Scratches (oops)',()=>W.stat.scratches,[1,5,15]]];",
    "['ouch','Band-Aid Club','Scratches (oops)',()=>W.stat.scratches,[1,5,15]],\n  ['herd','Herding Cats','Cats led together with the wand or laser',()=>W.stat.herd||0,[3,6,10]]];")

rep("const TIER_N=['','Bronze','Silver','Gold'];", """const TIER_N=['','Bronze','Silver','Gold'];
// herding: each following cat remembers where it joined; it counts once it has travelled 3 m with the lure and is still with it
let herdT=0, herdShow=0;
function herdTick(dt){ herdT-=dt; if(herdT>0)return; herdT=0.25;
  const lure=W.tool==='wand'&&wand.active?wand.feather:W.tool==='laser'&&laser.active?laser.pos:null, st=W.tool==='wand'?'chase':'laser'; let n=0;
  for(const c of W.cats){ const on=lure&&(c.state===st||c.state==='pounce')&&!c.outside&&!c.leaving;
    if(!on){ c.herdOff=(c.herdOff||0)+0.25; if(c.herdOff>2||!lure)c.herdFrom=null; continue; } c.herdOff=0;
    if(!c.herdFrom)c.herdFrom=c.g.position.clone(); if(dist2(c.g.position,c.herdFrom)>=3&&dist2(c.g.position,lure)<3)n++; }
  if(n>(W.stat.herd||0))W.stat.herd=n;
  if(n>=3&&n>herdShow){ herdShow=n; floatWorld(lure.clone().setY(1.2),'🐾×'+n); } if(n<3)herdShow=0; }""")

rep("  extraT-=dt; if(extraT<=0){", "  herdTick(dt); extraT-=dt; if(extraT<=0){")
rep("window.__wm={Snd,", "window.__wm={Snd,laser,wand,")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
