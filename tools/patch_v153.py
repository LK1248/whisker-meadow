"""v153: first-photo camera choreography.
Before, the camera jumped to the corkboard and stayed there. Now, for the first photo only:
1) the photo shows big while the camera slowly zooms out until the corkboard is in view (if it already is, no zoom);
2) the photo glides into the corkboard; 3) half a second after it lands, the camera gently returns to where it was.
If the player moves the camera meanwhile, the camera choreography stops and the camera stays the player's."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

old_start = s.find("function snapFly(img){")
old_end = s.find("function boardPop(){")
if old_start < 0 or old_end < 0: sys.exit('snapFly not found')
s = s[:old_start] + (
"const SF={on:false};\n"
"function boardView(){ if(!cardBoard)return {ok:true,x:0,y:0}; const q=cardBoard.getWorldPosition(new V3()).project(camera); return {ok:q.z<1&&Math.abs(q.x)<0.8&&q.y<0.62&&q.y>-0.55,x:q.x,y:q.y,z:q.z}; }\n"
"function snapFly(img){ const d=document.createElement('div'); d.className='snapFly'; d.innerHTML=`<img src=\"${img}\" alt=\"\">`; document.body.appendChild(d);\n"
"  Object.assign(SF,{on:true,ph:'out',t:0,el:d,t0:cam.target.clone(),w0:cam.want,u0:cam.userT??-99,cam:!cam.meet,goal:null}); }\n"
"// the smallest change that brings the board into view: zoom out first, drift toward the board only as much as needed\n"
"function boardGoal(){ if(!cardBoard)return null; const bp=cardBoard.getWorldPosition(new V3()), t0=SF.t0, w0=SF.w0, cp=camera.position.clone(), tt=new V3();\n"
"  const look=(t,d)=>{ camera.position.set(t.x+d*Math.sin(cam.phi)*Math.sin(cam.theta),t.y+d*Math.cos(cam.phi),t.z+d*Math.sin(cam.phi)*Math.cos(cam.theta)); camera.lookAt(t); camera.updateMatrixWorld(); return boardView().ok; };\n"
"  let g=null; if(look(t0,w0))g={t:t0.clone(),d:w0,move:false};\n"
"  for(let f=0;!g&&f<=0.9001;f+=0.1)for(let d=w0;d<=Math.max(w0,Math.min(LV().zoom*2.2,w0*1.7))+0.01;d+=w0*0.1){ tt.lerpVectors(t0,new V3(bp.x,t0.y,bp.z),f); if(look(tt,d)){ g={t:tt.clone(),d:d+w0*0.05,move:true}; break; } }\n"
"  camera.position.copy(cp); camera.lookAt(cam.target); camera.updateMatrixWorld(); return g; }\n"
"function snapFlyGo(){ const d=SF.el; let tx=innerWidth*0.85, ty=innerHeight*0.4; const v=boardView(); if(v.z<1){ tx=(v.x+1)/2*innerWidth; ty=(1-v.y)/2*innerHeight; }\n"
"  tx=Math.max(24,Math.min(innerWidth-24,tx)); ty=Math.max(24,Math.min(innerHeight-24,ty)); const r=d.getBoundingClientRect(), dx=tx-(r.left+r.width/2), dy=ty-(r.top+r.height/2);\n"
"  d.style.animation='none'; d.style.transform=`translate(${dx}px,${dy}px) rotate(6deg) scale(.12)`; d.style.opacity='0'; }\n"
"// runs every frame from updateCamera: zoom out -> fly -> land -> wait 0.5 s -> glide back\n"
"function snapFlyTick(dt){ if(!SF.on)return; SF.t+=dt; const mine=SF.cam&&(cam.userT??-99)===SF.u0&&!cam.meet; if(!mine)SF.cam=false;\n"
"  if(SF.ph==='out'){ if(SF.cam&&!SF.goal)SF.goal=boardGoal();\n"
"    if(SF.cam&&SF.goal){ const e=Math.min(1,SF.t/1.8), k=e*e*(3-2*e); cam.target.lerpVectors(SF.t0,SF.goal.t,k); cam.want=cam.dist=SF.w0+(SF.goal.d-SF.w0)*k; }\n"
"    if(SF.t>=(SF.cam&&SF.goal&&SF.goal.move?1.9:1.3)){ SF.ph='fly'; SF.t=0; snapFlyGo(); } }\n"
"  else if(SF.ph==='fly'){ if(SF.t>=1.95){ SF.el.remove(); boardPop(); Snd.ding(); SF.ph='rest'; SF.t=0; } }\n"
"  else if(SF.ph==='rest'){ if(SF.t>=0.5){ SF.ph='back'; SF.t=0; } }\n"
"  else if(SF.ph==='back'){ if(SF.cam){ const k=Math.min(1,dt*1.4); cam.target.lerp(SF.t0,k); cam.want=lerp(cam.want,SF.w0,k); } if(SF.t>=2.6||!SF.cam){ if(SF.cam)cam.want=SF.w0; SF.on=false; } } }\n"
) + s[old_end:]
rep("function updateCamera(dt){ lessonFrame(dt); petZoom(dt);", "function updateCamera(dt){ snapFlyTick(dt); lessonFrame(dt); petZoom(dt);")
rep("cam.dist=lerp(cam.dist,cam.want,Math.min(1,dt*4));", "cam.dist=lerp(cam.dist,cam.want,Math.min(1,dt*4));")
open(P, 'w', encoding='utf-8').write(s)
print('v153 applied')
