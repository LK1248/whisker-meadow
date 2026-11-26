"""v144: a cat only starts its slow-blink gaze (and so the slow-blink lesson) when it can look at the player.
A cat being petted or brushed can't turn its body (only its head, about 60 degrees), so it now only starts a gaze
if it is already roughly facing the camera (within about 55 degrees). Idle, watching and sheltering cats still
turn round to face the player as before."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(s.aff>=35&&!c.carried&&['idle','pet','shelter','watch'].includes(c.state)&&c.gaze<=0&&",
    "if(s.aff>=35&&!c.carried&&['idle','pet','shelter','watch'].includes(c.state)&&c.gaze<=0&&(c.state!=='pet'||Math.abs(angDiff(c.heading,Math.atan2(camera.position.x-c.g.position.x,camera.position.z-c.g.position.z)))<0.95)&&")
open(P, 'w', encoding='utf-8').write(s)
print('v144 applied')
