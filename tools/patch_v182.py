"""v182: a held butt-tap pose.
A cat that likes butt taps rises quickly into a held pose: rump raised as high as it goes (back legs straight),
front shoulders a little lower, head level, tail straight up and still, eyes half closed, and stiff: the petting
sways, purr wobble, kneading and tail swish are damped right down. It holds while the taps continue and for 2.5 s
after the last one, then eases back down. Replaces the 1.2 s bob that restarted on every tap."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# the tap no longer starts the bob
rep("if(c.buttLike){ c.elev=1.2; const fresh=", "if(c.buttLike){ const fresh=")
rep("  if(c.state==='pet'&&c.petT>0&&!c.carried){ swish=Math.max(swish,0.3); swSpd=Math.PI/strokeT(c); }\n",
    "  if(c.state==='pet'&&c.petT>0&&!c.carried){ swish=Math.max(swish,0.3); swSpd=Math.PI/strokeT(c); }\n"
    "  { const on=c.buttLike&&!c.carried&&!c.loafPet&&!moving&&['pet','idle'].includes(st)&&W.time-(c.buttAnimT??-99)<BUTT_HOLD;\n"
    "    c.buttK=on?Math.min(1,(c.buttK||0)+dt*5):Math.max(0,(c.buttK||0)-dt*2.2); const k=c.buttK*c.buttK*(3-2*c.buttK);\n"
    "    if(k>0){ const f=1-0.9*k; /* stiff: the petting sways mostly stop */ hz*=f; hy*=f; rz*=f; c.lean=0;\n"
    "      rx=lerp(rx,0.44,k); coreY=lerp(coreY,0.41,k); hx=lerp(hx,0.08,k); legA=legA.map((v,i)=>lerp(v,i<2?-0.78:-0.46,k));\n"
    "      tailUp=lerp(tailUp,1.5,k); swish=lerp(swish,0.015,k); swSpd=lerp(swSpd,1.2,k); eye=Math.min(eye,1-0.5*k); } } // butt taps: rump up, shoulders low, held still\n")
rep("const SH_D=0.95;", "const SH_D=0.95, BUTT_HOLD=2.5; // butt-tap pose holds this long after the last tap (s)\n")
open(P, 'w', encoding='utf-8').write(s)
print('v182 applied')
