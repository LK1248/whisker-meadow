"""v175: the first adoption is easier to follow.
- While the first family drives up and walks to the gate, the camera slowly glides to frame the gate and the family
  (from the parking spot to the gate), so they're on screen when they arrive.
- Once they're at the gate, a warm pulsing glow sits under each family member, and the "Pick a cat" button pulses,
  until the button is pressed. Then the highlights go off and the cats with a little house can be picked as before."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# camera: frame the gate + the arriving family before the Pick button is pressed
rep("  if(firstAdopt()&&W.family){ const f=W.family, m=",
    "  if(firstAdopt()&&W.family&&!W.pickHome&&!W.family.cat&&['arrive','wait'].includes(W.family.state)){ const f=W.family, h=LV().half, gate=new V3(0,0,-h), park=new V3(-3.6,0,-h-8.3), ms=f.members.filter(m=>m.g.visible);\n"
    "    return ['adoptIn',ms.length?ms:[{g:{position:park}}],f.atGate?[gate,...W.cats.filter(readyHome).slice(0,3).map(c=>c.g.position)]:[gate,park]]; } /* at the gate: family and the cats they could take */\n"
    "  if(firstAdopt()&&W.family){ const f=W.family, m=")
rep("  if(!L)return; LF.offT=offScreen(L[1])?",
    "  if(L&&L[0]==='adoptIn')LF.glide=1; // keeps following the family as it walks in\n"
    "  if(!L)return; LF.offT=offScreen(L[1])?")
rep("const f=fitFor(L[1],L[2]), k=Math.min(1,dt*(LF.back?1.6:2.5));",
    "const f=fitFor(L[1],L[2]), k=Math.min(1,dt*(L[0]==='adoptIn'?0.7:LF.back?1.6:2.5)); // the family's approach: a slow glide")
# glow under the family at the gate
rep("  const f=W.family;\n  if((famLogT-=dt)<=0){",
    "  const f=W.family; famGlow(f);\n  if((famLogT-=dt)<=0){")
rep("function renderFamily(msg,noX){",
    "let famGlows=null;\n"
    "function famGlow(f){ const on=!!(f&&firstAdopt()&&f.atGate&&!W.pickHome&&!f.cat&&['arrive','wait'].includes(f.state));\n"
    "  if(!famGlows){ if(!on)return; const cv=document.createElement('canvas'); cv.width=cv.height=128; const x=cv.getContext('2d'), g=x.createRadialGradient(64,64,4,64,64,62);\n"
    "    g.addColorStop(0,'rgba(255,236,160,1)'); g.addColorStop(0.45,'rgba(255,205,110,.75)'); g.addColorStop(1,'rgba(255,190,90,0)'); x.fillStyle=g; x.fillRect(0,0,128,128);\n"
    "    const tex=new THREE.CanvasTexture(cv); famGlows=[0,1,2].map(()=>{ const m=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:tex,transparent:true,depthWrite:false})); m.rotation.x=-Math.PI/2; m.renderOrder=2; scene.add(m); return m; });\n"
    "    const c2=document.createElement('canvas'); c2.width=c2.height=128; const y=c2.getContext('2d'); y.fillStyle='rgba(255,214,120,.55)'; y.beginPath(); y.arc(64,52,46,0,7); y.fill();\n"
    "    y.fillStyle='#ff6f91'; y.strokeStyle='#fff'; y.lineWidth=7; y.beginPath(); y.moveTo(64,80); y.bezierCurveTo(14,46,34,8,64,32); y.bezierCurveTo(94,8,114,46,64,80); y.closePath(); y.stroke(); y.fill();\n"
    "    y.fillStyle='#fff'; y.beginPath(); y.moveTo(46,98); y.lineTo(82,98); y.lineTo(64,122); y.closePath(); y.fill();\n"
    "    famGlows.mark=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c2),transparent:true,depthTest:false,depthWrite:false})); famGlows.mark.renderOrder=9; scene.add(famGlows.mark); }\n"
    "  famGlows.forEach((m,i)=>{ const p=on&&f.members[i]; m.visible=!!p; if(!p)return; const k=0.5+0.5*Math.sin(W.time*4), sz=(p.g.scale.x<0.9?1.1:1.5)*(1+0.12*k);\n"
    "    m.position.set(p.g.position.x,0.03,p.g.position.z); m.scale.set(sz,sz,1); m.material.opacity=0.55+0.35*k; });\n"
    "  const mk=famGlows.mark; mk.visible=on; if(on){ const ms=f.members, cx=ms.reduce((a,m)=>a+m.g.position.x,0)/ms.length, cz=ms.reduce((a,m)=>a+m.g.position.z,0)/ms.length, b=Math.abs(Math.sin(W.time*3));\n"
    "    const zs=Math.max(1,cam.dist/8); mk.position.set(cx,2.1+0.3*zs+b*0.25*zs,cz); mk.scale.setScalar((0.85+0.08*b)*zs); } } /* a heart marker bobbing over the family: the fence hides the ground glow from inside the meadow */\n"
    "function renderFamily(msg,noX){")
# the Pick a cat button pulses during the first adoption
rep("<button class=\"go\" id=\"fPick\">Pick a cat</button>",
    "<button class=\"go${firstAdopt()?' hl':''}\" id=\"fPick\">Pick a cat</button>")
rep("#family .fb .go{background:var(--leaf);color:#fff}",
    "#family .fb .go{background:var(--leaf);color:#fff}#family .fb .go.hl{animation:fPickHl 1.1s ease-in-out infinite}@keyframes fPickHl{0%,100%{box-shadow:0 0 0 0 rgba(255,196,80,.9);transform:scale(1)}50%{box-shadow:0 0 0 7px rgba(255,196,80,.45),0 0 18px 6px rgba(255,214,120,.7);transform:scale(1.07)}}")
open(P, 'w', encoding='utf-8').write(s)
print('v175 applied')
