"""v143: hungry cats ask for food.
- A hungry cat (food under 35) with no filled bowl to go to sits where it is, turns to face the player and
  looks up, instead of wandering off. It keeps asking until a bowl has food (then it goes to eat as before).
- Hungry cats meow for food every 4-7 s (was every 10-24 s, and only under 30)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(b){ const [x,z]=approach(c,b,0.74); goTo(c,x,z,'eat',b); return; } if(Math.random()<0.5)showIcon(c,'hungry',2.5); }",
    "if(b){ const [x,z]=approach(c,b,0.74); goTo(c,x,z,'eat',b); return; }\n"
    "    if(s.full<35&&c.age>0.2){ setState(c,'idle',rand(5,8)); c.sit=true; c.beg=c.stT; showIcon(c,'hungry',2.5); c.meowT=Math.min(c.meowT,rand(0.5,1.5)); return; } /* ask the player for food */\n"
    "    if(Math.random()<0.5)showIcon(c,'hungry',2.5); }")
rep("    if(s.full<30){ showIcon(c,'hungry',3); Snd.meow(1,1.2); }",
    "    if(s.full<35){ showIcon(c,'hungry',3); Snd.meow(1,1.2); c.meowT=rand(4,7); }")
rep("  let arch=0;\n  if(c.stretch>0&&!c.carried){",
    "  else if(c.beg>0&&!c.carried){ c.beg-=dt; if(c.state!=='idle'||c.s.full>=35)c.beg=0; else { const p=c.g.position, yaw=angDiff(c.heading,Math.atan2(camera.position.x-p.x,camera.position.z-p.z));\n"
    "    if(!(c.hopT>0)){ const ex=yaw-clamp(yaw,-0.25,0.25); c.heading+=ex*Math.min(1,dt*2.5); } hy=clamp(yaw,-1.1,1.1); hx=Math.min(hx,-0.4); } }\n"
    "  let arch=0;\n  if(c.stretch>0&&!c.carried){")
open(P, 'w', encoding='utf-8').write(s)
print('v143 applied')
