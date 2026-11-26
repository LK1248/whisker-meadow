"""v174: starting money, the laser as a milestone, and cats that actually chase the laser.
- New games start with $100 instead of $40, so the first shop visit can try a few things.
- The laser pointer needs 2 sanctuary stars and costs $150. The locked tool shows "★2" until then, then the price.
- Laser fix: cats used to ignore the dot completely once their fun was 98+, and only looked at it when they finished
  whatever they were doing. Now an idle / wandering / watching / licking cat within reach notices the moving dot
  within about a second. Cats with full fun still chase, just in shorter bursts with a rest between."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("time:0,money:40,food:10,", "time:0,money:100,food:10,")
# laser: 2 stars + $150
rep("{id:'laser',name:()=>'Laser pointer',desc:'Zoomies!',cost:()=>100,avail:()=>!W.laser,buy(){W.laser=true;refreshDock();}},",
    "{id:'laser',name:()=>'Laser pointer',desc:'Zoomies!',cost:()=>LASER_COST,need:()=>LASER_STARS,avail:()=>!W.laser,buy(){W.laser=true;refreshDock();}},")
rep('<span class="lock">$100</span>', '<span class="lock">★2</span>')
rep("function refreshDock(){ const lb=$('[data-tool=laser]'); lb.classList.toggle('locked',!W.laser); lb.querySelector('.lock').hidden=W.laser; }",
    "const LASER_COST=150, LASER_STARS=2;\n"
    "function refreshDock(){ const lb=$('[data-tool=laser]'); lb.classList.toggle('locked',!W.laser); const lk=lb.querySelector('.lock'); lk.hidden=W.laser; lk.textContent=W.stars>=LASER_STARS?'$'+LASER_COST:'★'+LASER_STARS; }")
rep("if(st>W.stars){ W.stars=st; toast(", "if(st>W.stars){ W.stars=st; refreshDock(); toast(")
# laser: decide() no longer refuses cats with full fun (rests instead)
rep("if(laser.active&&s.fun<98&&dist2(p,laser.pos)<9){ setState(c,'laser',8); return; }",
    "if(laser.active&&W.time>(c.laserCD||0)&&dist2(p,laser.pos)<9){ laserGo(c); return; }")
rep("case 'laser': { if(!laser.active||s.fun>=99){ setState(c,'idle',1.5); break; }",
    "case 'laser': { if(!laser.active){ setState(c,'idle',1.5); break; } if(c.stT<=0.05){ c.laserCD=W.time+(s.fun>=95?rand(4,9):rand(1.5,3.5)); setState(c,'idle',rand(1,2)); break; }")
# notice the moving dot without waiting for the current activity to end
rep("  c.stT-=dt;\n  if(!['walk','chase','laser',",
    "  c.stT-=dt;\n"
    "  if(laser.active&&W.time>(c.laserCD||0)&&(LASER_SEE.includes(c.state)||(c.state==='walk'&&!c.after))&&c.away<=0&&!c.outside&&!c.leaving&&c.age>0.1&&!(c.petT>0)&&!c.helped&&dist2(c.g.position,laser.pos)<9&&Math.random()<dt*(c.s.fun>=95?0.6:1.8))laserGo(c);\n"
    "  if(!['walk','chase','laser',")
rep("function decide(c){",
    "const LASER_SEE=['idle','watch','groom','sit'];\n"
    "function laserGo(c){ setState(c,'laser',c.s.fun>=95?rand(3,5):rand(7,11)); } // a cat with full fun chases in short bursts\n"
    "function decide(c){")
open(P, 'w', encoding='utf-8').write(s)
print('v174 applied')
