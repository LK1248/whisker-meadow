"""v166: the first belly rub is a short modal lesson.
- On the 10th good stroke of the game, the cat being petted rolls onto its side with its belly turned toward the
  camera and stays there. Everything else locks (like the other lessons; Skip is available), only that cat can be
  touched, the love -> heart / low love -> claw bubble shows above it and a ghost hand rubs over its belly.
- Before that lesson, cats don't offer their belly on their own any more, so the first offer is always the lesson.
- When the belly is rubbed: enough love -> hearts, and the bubble fades after a moment. Not enough love -> the scratch,
  then the bubble stays one more second with its bottom line (low love -> claw) pulsing, so the cause is clear."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# bubble: second row in its own group so it can pulse
rep("${HEART(104,18,1.6)}${loveIco(14,50,18)}${ARROW(60)}${CLAW}</svg>`;",
    "${HEART(104,18,1.6)}<g class=\"row2\">${loveIco(14,50,18)}${ARROW(60)}${CLAW}</g></svg>`;")
rep("#tip svg{display:block;width:150px;height:auto}",
    "#tip svg{display:block;width:150px;height:auto}#tip .row2.pulse{animation:tipPulse .5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes tipPulse{50%{transform:scale(1.22)}}")
# the lesson starts on the 10th good stroke; no random belly offers before it
rep("    if(!brush&&c.streak>=3){ const r=Math.random();\n      if(r<0.28&&s.aff>=35&&c.state==='pet'&&!lessonOn()){",
    "    if(!brush&&!W.stat.bellyTip&&(W.stat.good||0)>=10&&s.aff>=35&&c.state==='pet'&&c.age>=0.5&&!lessonOn()&&!tips.cur&&!tutLock()){ setState(c,'flop',30); c.offer=true; c.petT=3; showTip('belly',c,BELLY_TIP,999,false); }\n"
    "    else if(!brush&&c.streak>=3){ const r=Math.random();\n      if(r<0.28&&s.aff>=35&&c.state==='pet'&&!lessonOn()&&W.stat.bellyTip){")
rep("    const flop=!W.stat.bellyTip&&active().find(c=>c.state==='flop'&&c.offer&&!c.carried); if(flop){ showTip('belly',flop,BELLY_TIP,7,false); return; }\n", "")
# result of the rub
rep("function belly(c,frantic){\n  const s=c.s; if(frantic)c.over+=1;",
    "function belly(c,frantic){\n  const s=c.s; if(frantic)c.over+=1;\n"
    "  { const T=tips.cur; if(T&&T.kind==='belly'&&T.c===c&&!T.res&&tips.t<1)return; /* the stroke that started the lesson doesn't count */ if(T&&T.kind==='belly'&&T.c===c&&!T.res){ T.res=s.aff>=75?'ok':'scratch'; T.dur=tips.t+(T.res==='ok'?1.8:1.35); $('#ghost').hidden=true; if(T.res==='scratch'){ const r2=$('#tip .row2'); if(r2)r2.classList.add('pulse'); } } }")
# modal while waiting for the rub
rep("  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};",
    "  if(tips.cur&&tips.cur.kind==='belly'&&!tips.cur.res)return {cats:[tips.cur.c],tools:[]};\n"
    "  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};")
rep("  if(tips.cur&&(tips.cur.kind==='butt'||tips.cur.kind==='flea')){ endTip(); return; }",
    "  if(tips.cur&&(tips.cur.kind==='butt'||tips.cur.kind==='flea')){ endTip(); return; }\n"
    "  if(tips.cur&&tips.cur.kind==='belly'){ const c=tips.cur.c; endTip(); if(c.state==='flop'){ c.stT=0.5; c.petT=0; } return; }")
# tip ticking: hold the pose, belly toward the camera, ghost hand rubs; after the result it lingers (not cut by the cat getting up)
rep("(T.kind==='belly'&&c.state!=='flop')", "(T.kind==='belly'&&!T.res&&c.state!=='flop')")
rep("  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);",
    "  if(T.kind==='belly')tag.c=null; // the cat's card would cover the bubble\n"
    "  if(T.kind==='belly'&&!T.res){ c.stT=Math.max(c.stT||0,2); c.offer=true; const p=c.g.position, v=Math.atan2(camera.position.x-p.x,camera.position.z-p.z); c.heading=angLerp(c.heading,v-Math.PI/2,Math.min(1,dt*5)); // belly toward the player\n"
    "    tag.c=null; if(!camUser()){ cam.target.lerp(new V3(p.x,0.3,p.z),Math.min(1,dt*2.5)); cam.want=lerp(cam.want,Math.min(cam.want,4.2),Math.min(1,dt*2)); } // frame the cat\n"
    "    if(tips.t>0.8){ const gh=$('#ghost'); if(gh.hidden){ gh.innerHTML=`<svg viewBox=\"0 0 64 64\">${HAND_SVG.replace(/id=\"h(Scr|Aid)\"/g,'')}</svg>`; gh.classList.remove('tap'); gh.hidden=false; }\n"
    "      const b=toScreen(c.core.localToWorld(new V3(0,-0.12,0.04))); if(b.ok){ const sx=Math.sin(tips.t*5)*26; gh.style.opacity=P.mode&&P.mode!=='none'?0:0.9; gh.style.transform=`translate(${b.x-30+sx}px,${b.y-36}px) rotate(${sx*0.3}deg)`; } } }\n"
    "  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);")
rep("el.style.opacity=tips.t>T.dur-0.6&&T.kind!=='flea'?0:1;",
    "el.style.opacity=tips.t>T.dur-(T.kind==='belly'?0.35:0.6)&&T.kind!=='flea'?0:1;")
rep("function endTip(){ if(!tips.cur)return; if(tips.cur.tap||tips.cur.kind==='flea'){",
    "function endTip(){ if(!tips.cur)return; if(tips.cur.tap||tips.cur.kind==='flea'||tips.cur.kind==='belly'){")
open(P, 'w', encoding='utf-8').write(s)
print('v166 applied')
