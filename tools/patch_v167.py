"""v167: parents stay with their kittens; adopted pairs walk side by side.
- A cat whose kitten is still growing up at the sanctuary can't be adopted (no house icon, not picked as the
  bonded partner either). Tapping it while a family is choosing shows "Staying with the kittens". Once the kittens are
  grown, the parents can find homes again.
- An adopted bonded pair used to follow the exact same path to the car, one almost inside the other. The second cat
  now walks a little to the side of the first. """
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function readyHome(c){ return c.age>=1&&",
    "function hasKits(c){ return W.cats.some(k=>k!==c&&k.age<1&&k.parents&&k.parents.includes(c.id)&&!k.leaving); } // kittens still growing up here\n"
    "function readyHome(c){ return c.age>=1&&!hasKits(c)&&")
rep("floatWorld(c.g.position.clone().setY(1.3),c.forever?'Keeping this one':'Not ready yet');",
    "floatWorld(c.g.position.clone().setY(1.3),c.forever?'Keeping this one':hasKits(c)&&c.age>=1?'Staying with the kittens':'Not ready yet');")
rep("for(const k of f.cats)walkPath(k,[new V3(rand(-.2,.2),0,-h-0.9),new V3(-3.6,0,-h-2.9),new V3(-3.6,0,-h-8.2)],'out',0.85);",
    "f.cats.forEach((k,i)=>{ const o=i*0.6; walkPath(k,[new V3(rand(-.2,.2)+o,0,-h-0.9-o*0.4),new V3(-3.6+o,0,-h-2.9-o*0.3),new V3(-3.6+o,0,-h-8.2)],'out',0.85); }); /* side by side, not one inside the other */")
open(P, 'w', encoding='utf-8').write(s)
print('v167 applied')
