"""v79:
- Soft over-speed: slightly above the cat's limit the heart still fills, just slower (45% at the edge, fading to 0 by
  ~1.65x past it), the ring starts shifting colour, and the purr fades instead of cutting out. Keep it up and the
  rest is as before (purr stops, flood + hourglass, irritation).
- A cat being petted or brushed is pinned in place: it doesn't walk, and other cats, helpers, items or ponds can't push
  it (the other cat takes the whole push instead)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("c.fastT=performance.now()/1000; c.purr=0; c.purrBlock=now+1.5;",
    "c.fastT=performance.now()/1000; gain=gap*PET_RATE*0.45*Math.max(0,1-(x-tf)/0.5);\n"
    "    c.purr=Math.max(0,c.purr-gap*1.2); if(c.fastM>0.45){ c.purr=0; c.purrBlock=now+1.5; }")
# pinning
rep("  for(let iter=0;iter<2;iter++){\n    const air=c=>c.leap&&c.hopT>0;",
    "  const pinned=c=>!c.carried&&(P.mode==='stroke'||P.mode==='catPending')&&(S.cat===c||P.cat===c);\n"
    "  for(const c of cs){ if(pinned(c)){ if(!c.pinP)c.pinP=c.g.position.clone(); c.speed=0; } else c.pinP=null; }\n"
    "  for(let iter=0;iter<2;iter++){\n    const air=c=>c.leap&&c.hopT>0;")
rep("if(d<m){ const push=(m-d)/2, nx=dx/d, nz=dz/d; a.g.position.x-=nx*push; a.g.position.z-=nz*push; b.g.position.x+=nx*push; b.g.position.z+=nz*push; }",
    "if(d<m){ const wa=a.pinP?0:1, wb=b.pinP?0:1; if(!wa&&!wb)continue; const pa=(m-d)*wa/(wa+wb), pb=(m-d)*wb/(wa+wb), nx=dx/d, nz=dz/d; a.g.position.x-=nx*pa; a.g.position.z-=nz*pa; b.g.position.x+=nx*pb; b.g.position.z+=nz*pb; }")
rep("    for(const c of cs){\n      for(const it of items){",
    "    for(const c of cs){ if(c.pinP){ c.g.position.x=c.pinP.x; c.g.position.z=c.pinP.z; continue; }\n      for(const it of items){")
open(P, 'w', encoding='utf-8').write(s); print('ok')
