"""v72: loose speed limit. The fast edge of the petting band is capped at about 2.3x the cat's favourite speed
(log 0.85), so early-game permissiveness no longer lets players rush strokes. Going past it still only slows the
fill (and shows the hourglass); only far faster strokes upset the cat early on."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("return tempoTol(c)+early; }", "return Math.min(FAST_CAP,tempoTol(c)+early); }\nconst FAST_CAP=0.85; // loose top speed: about 2.3x the cat's favourite stroke speed")
open(P, 'w', encoding='utf-8').write(s); print('ok')
