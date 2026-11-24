"""v94: a hiding runaway's meow also gets louder as the view gets closer to it: up to +75% when you're right on top of
it, fading to no boost about 8m away (on top of the swell over the first minute)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("const vol=clamp(1-d/40,0.6,1)*RUN_MEOW0*(1+(RUN_PEAK-1)*swell);",
    "const vol=clamp(1-d/40,0.6,1)*(1+RUN_NEAR*clamp(1-d/RUN_NEAR_D,0,1))*RUN_MEOW0*(1+(RUN_PEAK-1)*swell);")
rep("let RUN_MEOW0=0.3, RUN_PEAK=2.3, RUN_SWELL=60;", "let RUN_MEOW0=0.3, RUN_PEAK=2.3, RUN_SWELL=60, RUN_NEAR=0.75, RUN_NEAR_D=8; // NEAR: extra loudness up close, fading out by NEAR_D m")
open(P, 'w', encoding='utf-8').write(s); print('ok')
