"""v155: brushing too fast irritates a cat again.
Measured (close zoom, love 50): brushing only counted as too fast above ~570 px/s and only irritated the cat at
~1500 px/s, while petting the same cat irritates at ~250 px/s; a much-loved cat could take twice that, so in
practice brushing almost never upset anyone.
- Too fast now starts at 1.5x the cat's comfortable brushing speed (was 2.2x), very fast at 3x (was 4.5x).
- Too-fast strokes wind the cat up faster (0.6 / 1.4 per brush-length, was 0.5 / 1.2).
- Love still widens the limits, but less at the top (max 1.15x instead of 1.3x).
- During the brushing lesson the limits stay 30% looser, so the lesson itself stays gentle."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("loveF=br.c===c?Math.max(1,clamp((c.s.aff-10)/60,0.4,1.3)):clamp((c.s.aff-10)/60,0.4,1.3), vMax=D*0.7*1.4*loveF*(c.trait==='shy'?0.87:1),",
    "loveF=br.c===c?1.3*Math.max(1,clamp((c.s.aff-10)/60,0.4,1.15)):clamp((c.s.aff-10)/60,0.4,1.15), vMax=D*0.7*1.4*loveF*(c.trait==='shy'?0.87:1),")
rep("    if(v>vMax*2.2){ const hard=v>vMax*4.5; c.over+=len/D*(hard?1.2:0.5);",
    "    if(v>vMax*1.5){ const hard=v>vMax*3; c.over+=len/D*(hard?1.4:0.6);")
open(P, 'w', encoding='utf-8').write(s)
print('v155 applied')
