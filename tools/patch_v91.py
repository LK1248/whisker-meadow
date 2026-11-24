"""v91: during the butt-tap lesson the cat turns side-on to the camera (whichever side needs less turning), so its
rump is plainly visible next to the tapping hand."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);",
    "  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);\n"
    "  if(T.kind==='butt'&&!c.buttKnown&&['idle','sit'].includes(c.state)){ const w=a=>Math.atan2(Math.sin(a),Math.cos(a)); // side-on: facing at right angles to the view\n"
    "    const v=Math.atan2(camera.position.x-c.g.position.x,camera.position.z-c.g.position.z), d1=w(v+Math.PI/2-c.heading), d2=w(v-Math.PI/2-c.heading), d=Math.abs(d1)<Math.abs(d2)?d1:d2; c.heading+=d*Math.min(1,dt*4); }")
rep("||tips.cur&&tips.cur.kind==='flea'&&tips.cur.c===c);", "||tips.cur&&['flea','butt'].includes(tips.cur.kind)&&tips.cur.c===c);")
rep("if(['idle','watch','shelter'].includes(c.state)&&!(c.hopT>0)){ const ex=yaw", "if(['idle','watch','shelter'].includes(c.state)&&!(c.hopT>0)&&!(tips.cur&&tips.cur.kind==='butt'&&tips.cur.c===c)){ const ex=yaw")
open(P, 'w', encoding='utf-8').write(s); print('ok')
