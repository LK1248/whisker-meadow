"""v63: slower petting tempos (-30%, range kept) and a steady metronome.
- tempoOf scales the cached per-cat tempo by 0.7; stroke gains scale up so a lap of the ring takes about as long as before.
- The metronome arm is driven from the same clock as the tail swish, so it never restarts and stays in step with the tail."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.age<1)m*=1.15; c.tempo=m; } return c.tempo; }",
    "if(c.age<1)m*=1.15; c.tempo=m; } return c.tempo*TEMPO_K; }\nconst TEMPO_K=0.7; // overall pace: lower = slower, calmer strokes")
rep("else if(x<-tol)gain=len/D*0.5;\n  else gain=len/D*1.1;",
    "else if(x<-tol)gain=len/D*0.5/TEMPO_K;\n  else gain=len/D*1.1/TEMPO_K;")
rep("gain=len/D*0.35; if(now>(c.hgT||0))", "gain=len/D*0.35/TEMPO_K; if(now>(c.hgT||0))")
# metronome: no CSS animation, angle set every frame from the shared clock
rep("#beat .mArm{transform-box:view-box;transform-origin:22px 31px;animation:bMetro 1s ease-in-out infinite alternate}",
    "#beat .mArm{transform-box:view-box;transform-origin:22px 31px}")
rep("if(el.lastC!==c){ el.lastC=c; el.querySelector('.mArm').style.animationDuration=strokeT(c).toFixed(2)+'s'; }",
    "el.querySelector('.mArm').style.transform=`rotate(${(30*Math.sin(performance.now()/1000*Math.PI/strokeT(c))).toFixed(1)}deg)`;")
rep("window.__wm={Snd,", "window.__wm={Snd,updateBeat,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
