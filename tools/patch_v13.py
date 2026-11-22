"""v13: pair lesson accepts any carry-and-drop next to any cat (not only the two it picked)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("""  const pa=a.g.position, pb=b.g.position, close=dist2(pa,pb)<1.9*1.9;
  if(pl.stage==='carry'){""", """  const held=W.cats.find(c=>c.carried); if(held)pl.held=held;
  if(pl.stage==='carry'&&W.stat.drops>pl.lastDrop&&!held){ pl.lastDrop=W.stat.drops; const d=pl.held;
    // whichever cat was carried, whichever cat it landed next to: that's the pair we watch
    const o=d&&active().filter(k=>k!==d&&!k.carried).sort((x,y)=>dist2(x.g.position,d.g.position)-dist2(y.g.position,d.g.position))[0];
    if(o&&dist2(o.g.position,d.g.position)<1.9*1.9){ pl.a=d; pl.b=o; pl.stage='watch'; pl.t=0; $('#ghost').hidden=true; if(d.state!=='boop'&&canBoop(d)&&canBoop(o)){ d.boopCD=o.boopCD=0; boop(d,o); } updatePairTut(0); return; } }
  const pa=a.g.position, pb=b.g.position;
  if(pl.stage==='carry'){""")
rep("""    if(W.stat.drops>pl.lastDrop&&!a.carried&&!b.carried){ if(close){ pl.stage='watch'; pl.t=0; $('#ghost').hidden=true; if(a.state!=='boop'&&canBoop(a)&&canBoop(b)){ a.boopCD=b.boopCD=0; boop(a,b); } } else pl.lastDrop=W.stat.drops; } }""", "  }")
# ghost: if some other cat is being carried, point at the nearer of the two
rep("const carried=a.carried?a:b.carried?b:null,", "const carried=held||null,")
rep("const tgt=carried===a?sb:sa,", "const tgt=carried===a?sb:carried===b?sa:(dist2(carried.g.position,pa)<dist2(carried.g.position,pb)?sa:sb),")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
