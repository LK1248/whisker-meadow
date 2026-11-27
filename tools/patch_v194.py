"""v194: when the finger comes back down on the cat during the petting window, the petting ring glides over to it
(eased, at most 700 px/s) instead of jumping. Once it catches up it follows the finger directly again."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  el.hidden=false; el.style.transform=`translate(${P.hx+48}px,${P.hy-(P.type==='mouse'?48:104)}px)`;\n",
    "  { const tx=P.hx+48, ty=P.hy-(P.type==='mouse'?48:104), now=performance.now()/1000, dt=Math.min(0.1,now-(el.mT||now)); el.mT=now;\n"
    "    const down=P.mode==='stroke'||P.mode==='catPending'||P.type==='mouse'; /* a mouse pointer is always followed */\n"
    "    if(el.hidden||el.mx==null){ el.mx=tx; el.my=ty; el.glide=false; }\n"
    "    else { if(down&&!el.wasDown)el.glide=true; /* finger back down: glide over, don't jump */\n"
    "      if(el.glide){ const dx=tx-el.mx, dy=ty-el.my, d=Math.hypot(dx,dy), step=Math.min(d,Math.max(120*dt,Math.min(d*(1-Math.exp(-dt*7)),700*dt))); if(d<4){ el.mx=tx; el.my=ty; el.glide=false; } else { el.mx+=dx/d*step; el.my+=dy/d*step; } }\n"
    "      else if(down){ el.mx=tx; el.my=ty; } } /* finger up: stays put */\n"
    "    el.wasDown=down; el.hidden=false; el.style.transform=`translate(${el.mx}px,${el.my}px)`; }\n")
open(P, 'w', encoding='utf-8').write(s)
print('v194 applied')
