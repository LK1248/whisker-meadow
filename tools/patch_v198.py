"""v198: a runaway's paw prints point the way it walked. The toe direction was mirrored left-right (rotation PI-heading
instead of PI+heading), and it now uses the actual step direction rather than the cat's turning heading."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const side=(R.pawI++%2?0.08:-0.08), hd=c.heading; const m=new THREE.Mesh(pawGeo,pawMat); m.rotation.x=-Math.PI/2; m.rotation.z=Math.PI-hd;",
    "const side=(R.pawI++%2?0.08:-0.08), hd=R.lastPaw?Math.atan2(p.x-R.lastPaw.x,p.z-R.lastPaw.z):c.heading; /* the way it walked */ const m=new THREE.Mesh(pawGeo,pawMat); m.rotation.x=-Math.PI/2; m.rotation.z=Math.PI+hd; /* toes forward */")
open(P, 'w', encoding='utf-8').write(s)
print('v198 applied')
