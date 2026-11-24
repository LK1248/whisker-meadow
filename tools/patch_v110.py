"""v110: the butt-tap lesson's ghost hand taps right on the cat's rump. It used to aim at a point floating above and
behind the body; it now aims at the top of the rump on the body itself (the spot the game counts as a butt tap),
so the tap ring lands on the cat."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("if(T.tap){ const p=c.g.position, s2=c.g.scale.x, r=toScreen(new V3(p.x-Math.sin(c.heading)*0.5*s2,0.55*s2,p.z-Math.cos(c.heading)*0.5*s2));",
    "if(T.tap){ const r=toScreen(c.core.localToWorld(new V3(0,BUTT_AIM[0],BUTT_AIM[1])));")
rep("let BUTT_ZOOM=2.4;", "let BUTT_ZOOM=2.4, BUTT_AIM=[0.15,-0.4]; // BUTT_AIM: rump spot in the body's own frame (up, back)")
rep("window.__wm={Snd,", "window.__wm={Snd,pickAt,setButtAim:(y,z)=>{BUTT_AIM=[y,z];},")
open(P, 'w', encoding='utf-8').write(s); print('ok')
