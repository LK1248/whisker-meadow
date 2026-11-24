"""v86: pairing lesson camera fits both cats. Each frame the wanted distance is raised so both cats (plus a margin
for the hint hand) fit the narrower of the horizontal/vertical view - important in portrait."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("const mid=pa.clone().add(pb).multiplyScalar(0.5); cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));",
    "const mid=pa.clone().add(pb).multiplyScalar(0.5); cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));\n"
    "  { const vh=camera.fov*Math.PI/360, hh=Math.atan(Math.tan(vh)*camera.aspect), half=Math.min(vh,hh), need=(Math.sqrt(dist2(pa,pb))/2+1.1)/Math.tan(half)*0.95;\n"
    "    cam.want=Math.max(cam.want,Math.min(need,LV().zoom*1.6)); }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("window.__wm={Snd,", "window.__wm={Snd,camera,")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
