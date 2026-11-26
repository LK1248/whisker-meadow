"""v154: the house icons over adoptable cats (while picking a cat for a family) grow a little when the camera is
far away: normal size up close, up to 1.5x when zoomed far out. Other icons are unchanged."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("c.icon.material.map=iconTexture(kind); c.icon.material.needsUpdate=true;",
    "c.icon.material.map=iconTexture(kind); c.icon.material.needsUpdate=true; c.iconKind=kind;")
rep("  if(c.iconT>0){ c.iconT-=dt; c.icon.material.opacity=Math.min(1,c.iconT/0.4); if(c.iconT<=0)c.icon.visible=false; }",
    "  { const far=c.iconKind==='house'?clamp(1+(camera.position.distanceTo(c.g.position)-10)*0.055,1,1.5):1; c.icon.scale.setScalar(0.42*far); } // house icons stay readable when zoomed out\n"
    "  if(c.iconT>0){ c.iconT-=dt; c.icon.material.opacity=Math.min(1,c.iconT/0.4); if(c.iconT<=0)c.icon.visible=false; }")
open(P, 'w', encoding='utf-8').write(s)
print('v154 applied')
