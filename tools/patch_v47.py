"""v47: no more burr icons. The brushing hint shows a brush; the brush tutorial reads
'scruffy coat (dust + leaf) + brush = shine'. Cat icons fade out over their last 0.4s, and after a
blink-back the slow-blink icon fades out within about a second."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# icons
i0 = s.index("const BURR_SVG='"); i1 = s.index("\n", i0)
s = s[:i0] + """const SCRUFF_SVG='<svg viewBox="0 0 32 32" width="30" height="30"><g fill="#d9c7a0"><circle cx="11" cy="19" r="7"/><circle cx="20" cy="16" r="8"/><circle cx="24" cy="23" r="5.5"/><circle cx="14" cy="25" r="5"/></g><path d="M5 9q7-5 12 1-7 4-12-1z" fill="#d9a23a"/><path d="M19 6l9 4M24 8l1-4" stroke="#7a5232" stroke-width="2" stroke-linecap="round"/></svg>',
  BRUSH_HINT='<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#4a3426" stroke-width="2.2" stroke-linecap="round"><path d="M4 20l7-7"/><rect x="11" y="4" width="9" height="9" rx="2.5" transform="rotate(45 15.5 8.5)" fill="#4a3426" stroke="none"/><path d="M13 3.5l-1.5 1.5M16.5 2.5l-1 2M19.5 4l-2 1"/></svg>';""" + s[i1:]
rep("g:'tap',label:()=>BURR_SVG,done:()=>W.tool==='brush'}", "g:'tap',label:()=>BRUSH_HINT,done:()=>W.tool==='brush'}")
rep("label:()=>BURR_SVG+'<span", "label:()=>BRUSH_HINT+'<span")
rep("${BURR_SVG.replace('width=\"30\" height=\"30\"','width=\"34\" height=\"34\"')}", "${SCRUFF_SVG.replace('width=\"30\" height=\"30\"','width=\"34\" height=\"34\"')}")
if 'BURR_SVG' in s: sys.exit('BURR_SVG still used')

# icon fade-out
rep("c.icon.visible=true; c.iconT=dur; c.iconKind=kind; }", "c.icon.visible=true; c.icon.material.opacity=1; c.iconT=dur; c.iconKind=kind; }")
rep("  if(c.iconT>0){ c.iconT-=dt; if(c.iconT<=0)c.icon.visible=false; }",
    "  if(c.iconT>0){ c.iconT-=dt; c.icon.material.opacity=Math.min(1,c.iconT/0.4); if(c.iconT<=0)c.icon.visible=false; }")
# blinking back: the cat's slow-blink icon goes away quickly
rep("function blinkBack(c){ c.blinkBackT=0; c.gaze=0;", "function blinkBack(c){ c.blinkBackT=0; c.gaze=0; if(c.iconKind==='blink'&&c.iconT>0.9)c.iconT=0.9;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
