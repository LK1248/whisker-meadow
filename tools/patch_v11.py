"""v11: fix carry (lessons set a non-existent 'pet' tool) and tap a far cat to glide in close."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# the tool is called 'hand'; 'pet' silently disabled hold-to-carry after the first lesson
rep("if(W.tool!=='pet')setTool('pet');", "if(W.tool!=='hand')setTool('hand');", 3)
# repair saves that stored the bad tool
rep("W.stat=Object.assign({},STAT0,d.W.stat||{});", "W.stat=Object.assign({},STAT0,d.W.stat||{}); if(!['hand','brush','wand','laser'].includes(W.tool))W.tool='hand';")

# close-up: tapping a cat that looks small on screen glides the camera in instead of acting
rep("function toScreen(v){", """function catScreenH(c){ const p=c.g.position, a=toScreen(p.clone().setY(0)), b=toScreen(p.clone().setY(0.9*c.g.scale.y)); return a.ok&&b.ok?Math.abs(a.y-b.y):999; }
function lessonOn(){ return !!(intro.c||bt.c||pl.a); }
function focusClose(c){ if(!cam.close)cam.close={want:cam.want}; cam.close.c=c; cam.close.idle=0; cam.want=Math.min(cam.want,3.8); cam.focus=c; cam.focusT=0.3; tagFor(c,4); Snd.chirp(); }
function leaveClose(restore){ const k=cam.close; if(!k)return; cam.close=null; if(cam.focus===k.c)cam.focus=null; if(restore)cam.want=Math.max(cam.want,k.want); }
function updateClose(dt){ const k=cam.close; if(!k)return; const c=k.c;
  if(lessonOn()||cam.meet||!W.cats.includes(c)||c.away>0||c.outside||c.leaving){ leaveClose(false); return; }
  if(P.mode==='pinch'||(P.mode==='pan'&&P.moved)){ leaveClose(false); return; }
  const busy=P.cat===c&&P.mode&&P.mode!=='none'||S.cat===c||tag.c===c&&W.time-c.lastStroke<2; k.idle=busy?0:k.idle+dt;
  if(k.idle>8){ leaveClose(true); return; } if(!c.carried){ cam.focus=c; cam.focusT=0.3; } }
function toScreen(v){""")
rep("else if(W.pickHome)pickForHome(c); else if(P.zone==='rump'",
    "else if(W.pickHome)pickForHome(c); else if(!lessonOn()&&!(c.blinkBackT>0)&&(!cam.close||cam.close.c!==c)&&catScreenH(c)<75)focusClose(c); else if(P.zone==='rump'")
rep("else if(!tapWildlife(e))tag.c=null; }", "else if(!tapWildlife(e)){ tag.c=null; leaveClose(true); } }")
rep("  if(P.mode==='stroke'&&S.cat&&S.len>=40&&performance.now()-S.last>260)", "  updateClose(dt);\n  if(P.mode==='stroke'&&S.cat&&S.len>=40&&performance.now()-S.last>260)")
rep("window.__wm={animateCat,", "window.__wm={animateCat,toScreen,catScreenH,step:dt=>{ update(dt); updateCamera(dt); renderer.render(scene,camera); },focusClose,leaveClose,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
