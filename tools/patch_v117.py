"""v117: the petting lesson's hand strokes at the cat's own favourite speed. It used to cross head-to-back in a fixed
1.2s with a strong ease (avg ~1.5x, peak ~2.25x the cat's tempo, past the 'too fast' line), teaching the wrong pace.
Now each stroke lasts (screen path length / the cat's favourite speed) x1.1, with a nearly even speed (peak ~1.07x)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("const ht=intro.t-2.8, cyc=Math.max(0,ht)%2.8, k=clamp(cyc/1.2,0,1), e=k*k*(3-2*k), lift=cyc>1.2?(cyc-1.2)*30:0;",
    "const ht=intro.t-2.8, vP=2.5*Math.max(60,Math.min(400,catScreenH(c)))*tempoOf(c), dur=clamp(Math.hypot(b.x-h.x,b.y-h.y)/Math.max(1,vP)*1.1,0.9,6), cT=dur+1.6;\n"
    "  if(ht>=0)intro.gp=((intro.gp||0)+dt/cT)%1; const cyc=(intro.gp||0)*cT, k=clamp(cyc/dur,0,1), e=k+(k*k*(3-2*k)-k)*0.35, lift=cyc>dur?(cyc-dur)*30:0; // even, cat-paced stroke")
rep("gh.style.opacity=(ht<0||handOn(c)||(P.mode&&P.mode!=='none'))?0:cyc<1.2?0.92:Math.max(0,0.92-(cyc-1.2)*1.6);",
    "gh.style.opacity=(ht<0||handOn(c)||(P.mode&&P.mode!=='none'))?0:cyc<dur?0.92:Math.max(0,0.92-(cyc-dur)*1.6);")
open(P, 'w', encoding='utf-8').write(s); print('ok')
