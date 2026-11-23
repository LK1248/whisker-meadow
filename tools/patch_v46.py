"""v46: fleas are about half the size (visible up close, barely from afar). The first time a cat gets fleas,
a one-time wordless tip floats over it: a magnifier with hopping fleas -> the brush."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("m.scale.set(0.034/sc.x,0.034/sc.y,0.034/sc.z); }); }", "m.scale.set(0.017/sc.x,0.017/sc.y,0.017/sc.z); }); }")

rep("function showTip(kind,c,svg,dur,tap){",
"""const FLEA_TIP=`<svg viewBox="0 0 160 60"><circle cx="26" cy="26" r="18" fill="#fff6ea" stroke="#b9a89a" stroke-width="4"/><path d="M39 39l11 11" stroke="#b9a89a" stroke-width="6" stroke-linecap="round"/>`+
  `<g fill="#2a1e1a"><circle cx="16" cy="33" r="2.4"/><circle cx="34" cy="20" r="2.4"/><circle cx="30" cy="35" r="2.4"/><circle cx="22" cy="21" r="2"/></g><path d="M17 31q5-13 11-5" fill="none" stroke="#e0505f" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 3"/>`+
  `${ARROW(30)}<g transform="translate(92 6) scale(2)" fill="none" stroke="#8a6a52" stroke-width="2.2" stroke-linecap="round"><path d="M4 20l7-7"/><rect x="11" y="4" width="9" height="9" rx="2.5" transform="rotate(45 15.5 8.5)" fill="#8a6a52" stroke="none"/><path d="M13 3.5l-1.5 1.5M16.5 2.5l-1 2M19.5 4l-2 1"/></g></svg>`;
function showTip(kind,c,svg,dur,tap){""")

rep("    const flop=!W.stat.bellyTip&&", """    const flea=!W.stat.fleaTip&&active().find(c=>c.fleas&&!c.carried&&!c.outside&&c.away<=0&&toScreen(c.g.position).ok); if(flea){ showTip('flea',flea,FLEA_TIP,8,false); return; }
    const flop=!W.stat.bellyTip&&""")
rep("(T.kind==='belly'&&c.state!=='flop')", "(T.kind==='belly'&&c.state!=='flop')||(T.kind==='flea'&&!c.fleas)")
rep("window.__wm={Snd,", "window.__wm={Snd,tips,showTip,FLEA_TIP,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
