"""v184: clearer house icons when picking a cat for a family.
25% bigger; opacity swings 1 -> 0.5 -> 1 (about 0.75 on average, was about 0.5); one pulse every 0.8 s (half the
speed of the old 0.4 s fade-and-restart)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("c.icon.scale.setScalar(0.42*far); }", "c.icon.scale.setScalar(0.42*far*(c.iconKind==='house'?1.25:1)); }")
rep("  if(c.iconT>0){ c.iconT-=dt; c.icon.material.opacity=Math.min(1,c.iconT/0.4); if(c.iconT<=0)c.icon.visible=false; }\n  else if(W.pickHome&&readyHome(c))showIcon(c,'house',0.4);",
    "  if(W.pickHome&&readyHome(c)&&(c.iconKind==='house'||!(c.iconT>0))){ if(!(c.iconKind==='house'&&c.icon.visible))showIcon(c,'house',0.5);\n"
    "    if(c.iconKind==='house'&&c.icon.visible){ c.iconT=0.5; c.icon.material.opacity=0.75+0.25*Math.cos(W.time*Math.PI*2/0.8); } } // steady slow pulse while picking\n"
    "  else if(c.iconT>0){ c.iconT-=dt; c.icon.material.opacity=Math.min(c.icon.material.opacity,c.iconT/0.4,1); if(c.iconT<=0)c.icon.visible=false; }")
open(P, 'w', encoding='utf-8').write(s)
print('v184 applied')
