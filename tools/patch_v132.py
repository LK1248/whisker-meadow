"""v132: fix vanishing birds and cats.
A bird that landed and pecked before its first hop got y=NaN (hopY was undefined); when it flew off its whole
position went NaN. A cat watching that bird turned to a NaN heading, and collisions then spread NaN into the cat
positions (cats disappear). Birds now start with hopY/peck/tilt at 0, cats only watch birds with a finite position,
and a safety net puts any cat with a non-finite position or heading back on the meadow."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const b={g,head,wings,state:'fly',tgt:new V3(),t:0,hopT:0,heading:0,land:null};",
    "const b={g,head,wings,state:'fly',tgt:new V3(),t:0,hopT:0,hopY:0,peck:0,tilt:0,heading:0,land:null};")
rep("c.watchBird){ const bp=c.watchBird.g.position;", "c.watchBird&&Number.isFinite(c.watchBird.g.position.x+c.watchBird.g.position.z)){ const bp=c.watchBird.g.position;")
rep("function collide(){\n  const cs=active().filter(solid);\n",
    "function collide(){\n  for(const c of W.cats){ const p=c.g.position; if(!Number.isFinite(p.x+p.y+p.z)){ p.set(rand(-1,1),0,rand(-1,1)); c.speed=0; c.target&&c.target.copy(p); rec('nanfix',c.name); } if(!Number.isFinite(c.heading))c.heading=0; }\n  const cs=active().filter(solid);\n")
open(P, 'w', encoding='utf-8').write(s)
print('v132 applied')
