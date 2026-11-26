"""v151: lessons keep the player near the cat that needs them.
- Rim marker: while a lesson/tip is running and its cat is out of view, a softly pulsing cream bubble with a cat face
  sits on the screen edge in the cat's direction, with a little arrow pointing at it. Tapping it glides back.
- Gentle return: if the lesson's cat has been out of view for 4 seconds, the camera slowly glides back to it, even if
  the player is still panning around. (Before, it only came back once the player had stopped moving the camera.)"""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#hint{position:fixed;left:0;top:0;pointer-events:none;z-index:6}",
    "#hint{position:fixed;left:0;top:0;pointer-events:none;z-index:6}\n"
    "#lessonRim{position:fixed;left:0;top:0;width:0;height:0;z-index:6;pointer-events:none}\n"
    "#lessonRim .bb{position:absolute;left:-25px;top:-25px;width:50px;height:50px;border-radius:50%;background:var(--cream);color:var(--pink);display:grid;place-items:center;pointer-events:auto;cursor:pointer;box-shadow:0 3px 0 rgba(74,52,38,.12),0 6px 16px rgba(74,52,38,.28);animation:rimPulse 1.3s ease-in-out infinite}\n"
    "#lessonRim .bb svg{width:30px;height:30px}\n"
    "#lessonRim .ar{position:absolute;left:0;top:0;width:0;height:0}\n"
    "#lessonRim .ar::after{content:'';position:absolute;left:27px;top:-8px;border:8px solid transparent;border-left:11px solid var(--pink)}\n"
    "@keyframes rimPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.13);box-shadow:0 3px 0 rgba(74,52,38,.12),0 0 0 7px rgba(255,122,162,.28)}}")
rep("const LF={key:'',pts:null,glide:0,want0:null,user0:-99};",
    "const LF={key:'',pts:null,glide:0,want0:null,user0:-99,offT:0,back:false};\n"
    "// edge marker pointing at the lesson's cat while it is out of view\n"
    "function rimTick(L){ let el=$('#lessonRim'); if(!el){ el=document.createElement('div'); el.id='lessonRim'; el.hidden=true; el.innerHTML=`<div class=\"ar\"></div><button class=\"bb\" aria-label=\"Back to the cat\">${CATF}</button>`; document.body.appendChild(el);\n"
    "    el.querySelector('.bb').addEventListener('pointerdown',e=>{ e.stopPropagation(); e.preventDefault(); LF.glide=2.2; LF.back=true; LF.offT=0; Snd.ding(); }); }\n"
    "  if(!L||!W.started||W.paused||!$('#modal').hidden||P.mode==='carry'){ el.hidden=true; return; }\n"
    "  const s=toScreen(L[1][0].g.position.clone().setY(0.4)); let x=s.x, y=s.y; if(!s.ok){ x=innerWidth-x; y=innerHeight-y; }\n"
    "  if(s.ok&&x>-10&&x<innerWidth+10&&y>40&&y<innerHeight-60){ el.hidden=true; return; }\n"
    "  const m=40, top=110, bot=118, cx=innerWidth/2, cy=innerHeight/2, dx=x-cx, dy=y-cy;\n"
    "  const k=Math.min((cx-m)/Math.max(1e-6,Math.abs(dx)),(dy<0?cy-top:innerHeight-bot-cy)/Math.max(1e-6,Math.abs(dy)));\n"
    "  el.hidden=false; el.style.transform=`translate(${cx+dx*k}px,${cy+dy*k}px)`; el.querySelector('.ar').style.transform=`rotate(${Math.atan2(dy,dx)}rad)`; }")
rep("function lessonFrame(dt){ if(cam.meet)return; const L=lessonPts(), key=L?L[0]+':'+L[1].map(c=>c.name).join(','):'';",
    "function lessonFrame(dt){ if(cam.meet){ rimTick(null); return; } const L=lessonPts(), key=L?L[0]+':'+L[1].map(c=>c.name).join(','):'';\n"
    "  const IL=!L&&W.started&&intro.c&&intro.c.g&&!intro.c.carried?['intro',[intro.c]]:null; rimTick(L||IL); // the petting lesson frames itself, but gets the marker and the glide back too\n"
    "  if(IL){ LF.offT=offScreen(IL[1])?LF.offT+dt:0; if(LF.offT>=4){ LF.ib=2.2; LF.offT=0; } if(LF.ib>0){ LF.ib-=dt; cam.target.lerp(fitFor(IL[1]).t,Math.min(1,dt*1.6)); } } else if(!L){ LF.offT=0; LF.ib=0; }")
rep("    if(key){ if(!was){ LF.want0=cam.want; LF.user0=cam.userT??-99; } LF.glide=2.5; } }\n"
    "  if(!L)return; if(camUser()){ LF.glide=0; return; }",
    "    if(key){ if(!was){ LF.want0=cam.want; LF.user0=cam.userT??-99; } LF.glide=2.5; } LF.offT=0; LF.back=false; }\n"
    "  if(!L)return; LF.offT=offScreen(L[1])?LF.offT+dt:0; if(LF.offT>=4&&!(LF.back&&LF.glide>0)){ LF.glide=2.2; LF.back=true; LF.offT=0; } // out of view for 4 s: glide back\n"
    "  if(!LF.back&&W.time-(cam.userT??-99)<4){ LF.glide=0; return; }")
rep("  if(LF.glide<=0)return; LF.glide-=dt; const f=fitFor(L[1],L[2]), k=Math.min(1,dt*2.5);",
    "  if(LF.glide<=0){ LF.back=false; return; } LF.glide-=dt; const f=fitFor(L[1],L[2]), k=Math.min(1,dt*(LF.back?1.6:2.5));")
open(P, 'w', encoding='utf-8').write(s)
print('v151 applied')
