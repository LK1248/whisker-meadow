"""v87: a petting or brushing stroke stays locked to the cat it started on until the mouse is released or the finger
lifted. Sliding off that cat pauses the stroke (nothing else gets petted); sliding back onto it continues."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("P.mode='stroke'; $('#ring').hidden=true; if(W.tool==='hand'&&!petReact(P.cat)){ P.mode='none'; P.cat=null; } else beginStroke(P.cat,performance.now()); }",
    "P.mode='stroke'; $('#ring').hidden=true; if(W.tool==='hand'&&!petReact(P.cat)){ P.mode='none'; P.cat=null; } else { S.lock=P.cat; beginStroke(P.cat,performance.now()); } }")
rep("  if(!h||!h.cat){ if(W.tool==='hand'&&S.cat)return; if(S.cat)finishStroke(); S.cat=null; return; }",
    "  if(S.lock&&(!h||h.cat!==S.lock))return; // locked to the first cat until release: off it, the stroke just pauses\n"
    "  if(!h||!h.cat){ if(W.tool==='hand'&&S.cat)return; if(S.cat)finishStroke(); S.cat=null; return; }")
rep("function endPointer(e){", "function endPointer(e){ S.lock=null;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
