"""v147: a cat that likes the adopting family rolls over with its belly toward them.
- The happy roll at the gate now always turns the belly toward the family (it was a random side, so half the
  time the belly faced away).
- In about 60% of adoptions the cat rolls further, nearly onto its back (belly up), paws waving; otherwise it is
  the side roll as before."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(f.match){ c.greetFlop=1; c.heading=Math.PI+(Math.random()<0.5?1.25:-1.25);",
    "if(f.match){ c.greetFlop=Math.random()<0.6?2:1; { const fm=f.members[0].g.position, cp=c.g.position, fd=Math.atan2(fm.x-cp.x,fm.z-cp.z); c.heading=fd+BELLY_SIDE*(c.greetFlop===2?1.45:1.25); }")
rep("  else if(st==='greet'&&c.greetFlop){ rz=1.55+Math.sin(t*2.4)*0.12;",
    "  else if(st==='greet'&&c.greetFlop===2){ rz=2.35+Math.sin(t*2.4)*0.1; coreY=0.36; legA=[Math.sin(t*4)*0.55-0.1,Math.sin(t*4+1.6)*0.55-0.1,0.35+Math.sin(t*3)*0.25,0.35+Math.sin(t*3+1)*0.25]; tailUp=0; swish=0.35; swSpd=4; eye=0.45; hz=-0.6; hx=-0.2; }\n"
    "  else if(st==='greet'&&c.greetFlop){ rz=1.55+Math.sin(t*2.4)*0.12;")
rep("function famGreet(c){", "const BELLY_SIDE=-1; // which way to turn so a roll (core rz>0) shows the belly toward a target\nfunction famGreet(c){")
open(P, 'w', encoding='utf-8').write(s)
print('v147 applied')
