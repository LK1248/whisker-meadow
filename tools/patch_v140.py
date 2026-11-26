"""v140: the first adoption succeeds.
- The first family always wishes for the type (trait) of a cat that is ready to adopt, preferring one that
  isn't scruffy.
- The first family takes any ready cat the player brings, unless it is very low on grooming (under 20, the flea
  level), Love (under 25) or health (under 30). Ready cats already have Love 50+ and health 55+, so in practice
  only a very scruffy cat gets "Needs a brush"."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const want=ready.length&&Math.random()<0.7?pick(ready).trait:pick(TRAITS);",
    "const neat=ready.filter(c=>c.s.groom>=GROOM_HOME), want=ready.length&&!W.homes.length?pick(neat.length?neat:ready).trait:ready.length&&Math.random()<0.7?pick(ready).trait:pick(TRAITS);")
rep("f.match=c.trait===f.want||(c.s.aff>=75&&Math.random()<0.5)||Math.random()<0.15; f.scruffy=c.s.groom<GROOM_HOME&&c.s.aff<90; if(f.scruffy)f.match=false; }",
    "f.match=c.trait===f.want||(c.s.aff>=75&&Math.random()<0.5)||Math.random()<0.15; f.scruffy=c.s.groom<GROOM_HOME&&c.s.aff<90; if(f.scruffy)f.match=false;\n"
    "  if(!W.homes.length){ f.scruffy=c.s.groom<FLEA_AT; f.match=!f.scruffy&&c.s.aff>=25&&c.s.health>=30; } /* the first adoption should succeed */ }")
open(P, 'w', encoding='utf-8').write(s)
print('v140 applied')
