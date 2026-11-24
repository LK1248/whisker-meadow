"""v80: on touch screens, a soft contact glow with a gentle ripple sits right under the finger, so it's clear the
finger is the touch point (the hand is drawn above it so the finger doesn't hide it)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("</style>", "#touchDot{position:fixed;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;pointer-events:none;z-index:8;border-radius:50%;"
    "background:radial-gradient(circle,rgba(255,255,255,.75) 0 22%,rgba(255,240,246,.35) 40%,rgba(255,255,255,0) 70%);transition:opacity .2s}"
    "#touchDot::after{content:'';position:absolute;inset:6px;border-radius:50%;border:2.5px solid rgba(255,255,255,.85);animation:tdRip 1.1s ease-out infinite}"
    "@keyframes tdRip{0%{transform:scale(.45);opacity:.9}100%{transform:scale(1.35);opacity:0}}\n</style>")
rep('<div id="hand" hidden>', '<div id="touchDot" hidden></div><div id="hand" hidden>')
rep("function updateBeat(){", "function touchDotTick(){ const d=$('#touchDot'), on=W.started&&!W.paused&&P.down&&P.type&&P.type!=='mouse'&&P.mode!=='pinch'&&P.mode!=='pan'&&P.mode!=='none';\n"
    "  if(d.hidden!==!on)d.hidden=!on; if(on)d.style.transform=`translate(${P.hx}px,${P.hy}px)`; }\nfunction updateBeat(){ touchDotTick();")
open(P, 'w', encoding='utf-8').write(s); print('ok')
