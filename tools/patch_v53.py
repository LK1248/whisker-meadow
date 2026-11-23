"""v53: fair photos look like professional show photos.
- Wider framing: the whole cat, the podium, the rosette and the bunting backdrop, with room around them.
- Show stance: the cat stands on the podium in a three-quarter profile (not sitting, staring into the lens).
- Longer lens from about eye level, so the cat isn't distorted the way a close phone shot is."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("FS={sc,disc,cam:new THREE.PerspectiveCamera(30,1,0.1,60)}; }", "FS={sc,disc,cam:new THREE.PerspectiveCamera(22,1,0.1,80)}; }")
rep("FS.sc.add(g); g.position.set(0,0.42,0); c.heading=0.3; c.sit=true; c.state='idle';",
    "FS.sc.add(g); g.position.set(0,0.42,0); c.heading=SHOT_YAW; c.sit=false; c.state='idle';")
rep("g.position.y=0.42; g.rotation.y=0.3;", "g.position.y=0.42; g.rotation.y=SHOT_YAW;")
rep("FS.cam.position.set(0.55,0.95+0.55*s,1.6+3.0*s); FS.cam.lookAt(0.3,0.4+0.5*s,0);",
    "FS.cam.position.set(SHOT_CAM[0],SHOT_CAM[1]+SHOT_CAM[2]*s,SHOT_CAM[3]+SHOT_CAM[4]*s); FS.cam.lookAt(SHOT_AT[0],SHOT_AT[1]+SHOT_AT[2]*s,0);")
rep("let FS=null;", "let FS=null;\n// show-photo framing: three-quarter profile, long lens from about eye level, the whole stage in frame\nlet SHOT_YAW=0.75, SHOT_CAM=[0.4,0.8,0.35,5.8,3.6], SHOT_AT=[0.4,0.72,0.25];")
rep("window.__wm={Snd,", "window.__wm={Snd,setShot:(y,c,a)=>{ SHOT_YAW=y; SHOT_CAM=c; SHOT_AT=a; },")
# rosette a little further from the cat's face
rep("ros.position.set(1.0,0.85,0.2);", "ros.position.set(1.25,0.85,0.1);")
open(P, 'w', encoding='utf-8').write(s); print('ok')
