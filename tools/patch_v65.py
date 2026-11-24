"""v65: rhythm difficulty grows with play time (W.time, in-game seconds).
- 0-3 min: very relaxed. Only very rapid strokes count as too fast; slow is always fine.
- 3-10 min: permissive. Still only quite rapid strokes upset a cat; slow is always fine.
- 10-15 min: gentle ramp to normal windows; some cats (about 1 in 3) become stricter; slow strokes start to count as off-beat.
- 15-20 min: cat tempos spread out to their full range, and some cats get extreme tempos (very slow or very rapid)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.age<1)m*=1.15; c.tempo=m; } return c.tempo*TEMPO_K; }",
    "if(c.age<1)m*=1.15; c.tempo=m; }\n"
    "  if(c.tempoExt==null){ const r=Math.random(); c.tempoExt=r<0.22?0.55:r<0.42?1.7:1; c.strictK=Math.random()<0.33?0.5:1; }\n"
    "  const v=rPhase(900,1200), spread=0.45+0.55*v, ext=1+(c.tempoExt-1)*v;\n"
    "  return 0.36*Math.pow(c.tempo/0.36,spread)*ext*TEMPO_K; }\n"
    "// play-time phases: 0..1 ramp between two times (in-game seconds)\n"
    "function rPhase(a,b){ return clamp((W.time-a)/(b-a),0,1); }\n"
    "function slowOk(){ return W.time<600; } // first 10 minutes: slow strokes are never off-beat\n"
    "function tolFast(c){ const early=W.time<180?1.6:0.9*(1-rPhase(600,900)); return tempoTol(c)+early; }")
rep("function tempoTol(c){ return (0.3+0.7*c.s.aff/100)*(c.trait==='shy'?0.85:1)+(intro.c===c?0.35:0); }",
    "function tempoTol(c){ tempoOf(c); const k=1+((c.strictK||1)-1)*rPhase(600,900); return (0.3+0.7*c.s.aff/100)*(c.trait==='shy'?0.85:1)*k+(intro.c===c?0.35:0); }")
# petting: fast checks use the relaxed fast window, slow only counts once the early phase is over
rep("if(x>tol+1.3){", "const tf=tolFast(c), fr=W.time<180?1.0:0; if(x>tf+1.3+fr){")
rep("else if(x>tol){ c.over+=len/D*0.15*(x-tol+0.3);", "else if(x>tf){ c.over+=len/D*0.15*(x-tf+0.3);")
rep("else if(x<-tol)gain=len/D*0.5/TEMPO_K;", "else if(x<-tol&&!slowOk())gain=len/D*0.5/TEMPO_K;")
rep("TG.st=TG.x>tol?'fast':TG.x<-tol?'slow':'on';", "TG.st=TG.x>tolFast(k)?'fast':TG.x<-tol&&!slowOk()?'slow':'on';")
rep("window.__wm={Snd,", "window.__wm={Snd,tolFast,rPhase,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
