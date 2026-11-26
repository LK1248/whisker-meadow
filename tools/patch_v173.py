"""v173: Bengal rosettes lie flat on the coat too (dark ring with a lighter middle, painted on, no bumps)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# flat may be a number: lift the disc that far off the surface (an inner disc sits just above the outer one)
rep("if(flat){ const m=add(parent,G.sph,col,[P.x,P.y,P.z],[r,r,r*0.2],zone);",
    "if(flat){ const lf=typeof flat==='number'?flat:0, m=add(parent,G.sph,col,[P.x+n.x*lf,P.y+n.y*lf,P.z+n.z*lf],[r,r,r*0.2],zone);")
rep("spot(core,dark,d,ax,'back',0.075); spot(core,0xc98a45,d,ax,'back',0.045); }",
    "spot(core,dark,d,ax,'back',0.075,true); spot(core,0xc98a45,d,ax,'back',0.045,0.01); }")
open(P, 'w', encoding='utf-8').write(s)
print('v173 applied')
