"""v183: fleas slowly wear down a cat's health.
While a cat has fleas, its health can't go up (except naps), and it drops by 3 a minute, but never below 55 (the
health a cat needs to be adopted), so fleas can't cost a cat its home. A cat already below 55 isn't lowered further.
Replaces the old hidden -10 on the health target, which normal care cancelled out."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("+(c.nourT>0?6:0)-(c.fleas?10:0); s.health=clamp(s.health+(ht-s.health)*dt*0.04,0,100);",
    "+(c.nourT>0?6:0); { const d=(ht-s.health)*dt*0.04; s.health=clamp(s.health+(c.fleas?Math.min(0,d):d),0,100); }\n"
    "  if(c.fleas&&s.health>FLEA_FLOOR)s.health=Math.max(FLEA_FLOOR,s.health-dt*FLEA_DRAIN); // fleas: a slow drain, never below the adoption line")
rep("const SH_D=0.95,", "const FLEA_DRAIN=0.05, FLEA_FLOOR=55; // health lost per second with fleas, and the floor it stops at\nconst SH_D=0.95,")
open(P, 'w', encoding='utf-8').write(s)
print('v183 applied')
