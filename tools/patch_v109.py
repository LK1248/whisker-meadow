"""v109: romping cats no longer pass through each other. Collisions skipped any cat that was mid-hop (a real leap clears
another cat), but romp hops are tiny tussle bounces, so wrestling cats slid into one another. Romping cats now stay
solid to each other (and everyone) through their hops."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("&&!(c.state==='sleep'&&c.useItem)&&(c.jump<0.15||c.leap); }", "&&!(c.state==='sleep'&&c.useItem)&&(c.jump<0.15||c.leap||c.state==='romp'); }")
rep("const air=c=>c.leap&&c.hopT>0;", "const air=c=>c.leap&&c.hopT>0&&c.state!=='romp';")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
# the chaser pulls up at touching distance instead of driving into the runner, and the tussle keeps that spacing
rep("c.target.set(op.x,0,op.z); moveToward(c,dt,2.95,0.5); if(d<0.95){", "c.target.set(op.x,0,op.z); moveToward(c,dt,2.95,1.05); if(d<1.15){")
rep("else { c.speed=lerp(c.speed,0,Math.min(1,dt*6)); c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); c.rompT-=dt;",
    "else { c.speed=lerp(c.speed,0,Math.min(1,dt*6)); c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); c.rompT-=dt;\n"
    "        { const gap=1.05*(c.g.scale.x+o.g.scale.x)/2; if(d<gap&&d>0.01){ const k=Math.min(1,dt*3)*(gap-d)/2; p.x+=(p.x-op.x)/d*k; p.z+=(p.z-op.z)/d*k; } } /* tussle at arm's length */")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
