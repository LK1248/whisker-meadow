"""v202: during butt taps the cat stretches its head forward and a little higher (about 10%), looking ahead instead of
down at the ground."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("rx=lerp(rx,0.2,k); coreY=lerp(coreY,0.44,k); hx=lerp(hx,0.05,k);",
    "rx=lerp(rx,0.2,k); coreY=lerp(coreY,0.44,k); hx=lerp(hx,BUTT_HX,k); /* chin up: looking ahead, not at the ground */")
rep("/* head level with the body, neck reaching out */",
    "/* head level with the body, neck reaching out */ { const b=c.buttK||0; if(b>0&&!inv){ const kb=b*b*(3-2*b); FL_V.z+=BUTT_HZ*kb; FL_V.y+=BUTT_HY*kb; } } /* butt taps: neck stretches forward and a bit up */")
rep("function flopLook(c,dt,on){", "let BUTT_HX=-0.3, BUTT_HZ=0.12, BUTT_HY=0.1;\nfunction flopLook(c,dt,on){")
rep("window.__wm={AW,", "window.__wm={setButtHead:(x,z,y)=>{ BUTT_HX=x; BUTT_HZ=z; BUTT_HY=y; },AW,")
open(P, 'w', encoding='utf-8').write(s)
print('v202 applied')
