"""v172: Savannah spots lie flat on the coat.
They were little half-buried balls that stood out of the fur and read like burrs or fleas. Now each spot is a very
thin disc lying along the fur, so it looks painted on."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("    const spot=(parent,col,dir,eax,zone,r)=>{",
    "    const spot=(parent,col,dir,eax,zone,r,flat)=>{")
rep("      const m=add(parent,G.sph,col,[P.x-n.x*r*0.6,P.y-n.y*r*0.6,P.z-n.z*r*0.6],[r,r,r],zone); return m; };",
    "      if(flat){ const m=add(parent,G.sph,col,[P.x,P.y,P.z],[r,r,r*0.2],zone); m.quaternion.setFromUnitVectors(new V3(0,0,1),n); return m; } /* a thin disc along the fur */\n"
    "      const m=add(parent,G.sph,col,[P.x-n.x*r*0.6,P.y-n.y*r*0.6,P.z-n.z*r*0.6],[r,r,r],zone); return m; };")
rep("spot(core,dark,[rand(-1,1),rand(-0.2,1),rand(-0.9,0.9)],ax,'back',0.05); for(let i=0;i<4;i++)spot(head,dark,[rand(-0.8,0.8),rand(0.5,1),rand(-0.6,0.1)],[0.3,0.27,0.27],'head',0.035);",
    "spot(core,dark,[rand(-1,1),rand(-0.2,1),rand(-0.9,0.9)],ax,'back',0.05,true); for(let i=0;i<4;i++)spot(head,dark,[rand(-0.8,0.8),rand(0.5,1),rand(-0.6,0.1)],[0.3,0.27,0.27],'head',0.035,true);")
open(P, 'w', encoding='utf-8').write(s)
print('v172 applied')
