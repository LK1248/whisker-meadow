"""v148: nicer thank-you postcards (still phone snapshots, just a bit better).
- Laptop card: a real desk, open laptop (keys, trackpad, glowing screen) and a mug; the cat sits on the keyboard.
- Phone-camera card ("figured out the phone camera"): the phone lies on the floor looking up past the cat's face
  at the ceiling: ceiling fan, light, crown moulding and the tops of curtains. The cat is soft (out of focus), the
  ceiling sharp.
- Every card: a soft contact shadow under the cat, slightly stronger warm light, a little more room detail
  (baseboard, a framed picture in the plain room), and a light phone-photo finish (warm tint, vignette, grain)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# warmer, slightly stronger light (shared by portraits and postcards)
rep("pScene.add(new THREE.HemisphereLight(0xfffdf5,0xd9b48a,0.75)); const d=new THREE.DirectionalLight(0xfff0d0,0.7); d.position.set(2,4,3);",
    "pScene.add(new THREE.HemisphereLight(0xfff8ee,0xc9a27a,0.62)); const d=new THREE.DirectionalLight(0xffe6c4,0.98); d.position.set(2.6,4,2.4);", count=2)

# selfie: phone on the floor looking up past the cat at the ceiling
rep("if(scene==='selfie'){ cardPose(a,'idle',true,0); a.g.updateMatrixWorld(true); const h=a.head.getWorldPosition(new V3()); pCam.fov=55; pCam.position.set(h.x+0.1*sc,h.y+0.12*sc,h.z+0.85*sc); pCam.lookAt(h.x,h.y-0.02*sc,h.z); pCam.rotateZ(0.16); rect=[0,0,320,240]; }",
    "if(scene==='selfie'){ cardPose(a,'idle',true,0); a.g.updateMatrixWorld(true); const h=a.head.getWorldPosition(new V3()); pCam.fov=60; pCam.position.set(h.x+0.12*sc,0.06*sc,h.z+1.15*sc); pCam.lookAt(h.x-0.05*sc,h.y+0.75*sc,h.z-0.2*sc); pCam.rotateZ(0.2); rect=[0,0,320,240]; }")
# laptop: real desk + laptop, cat sitting on the keyboard
rep("else if(scene==='laptop'){ cardPose(a,'flop',false,-0.4); camAt([0.4,1.4,2.4],[0,0.3,0]); rect=[40,20,240,180]; }",
    "else if(scene==='laptop'){ const k=sc, L=(c)=>new THREE.MeshLambertMaterial({color:c}), B=(w,h,d,m,x0,y0,z0,g)=>{ const o=new THREE.Mesh(new THREE.BoxGeometry(w*k,h*k,d*k),m); o.position.set(x0*k,y0*k,z0*k); (g||pX).add(o); return o; }, pX=new THREE.Group(); pScene.add(pX); cardX.push(pX);\n"
    "    const desk=new THREE.Mesh(new THREE.PlaneGeometry(7*k,2.6*k),L(0xc28e5a)); desk.rotation.x=-Math.PI/2; desk.position.z=-0.2*k; pX.add(desk);\n"
    "    B(1.3,0.05,0.86,L(0xa3abb6),0,0.025,0); B(1.1,0.012,0.44,L(0x3a3f48),0,0.054,-0.08); B(0.36,0.008,0.2,L(0x8f97a3),0,0.052,0.28);\n"
    "    const lid=new THREE.Group(); lid.position.set(0,0.05*k,-0.43*k); lid.rotation.x=-0.3; pX.add(lid); B(1.3,0.82,0.035,L(0x98a1ad),0,0.41,0,lid); const scr=new THREE.Mesh(new THREE.PlaneGeometry(1.16*k,0.7*k),new THREE.MeshBasicMaterial({color:0xa9d8ff})); scr.position.set(0,0.42*k,0.02*k); lid.add(scr);\n"
    "    const mug=new THREE.Mesh(new THREE.CylinderGeometry(0.11*k,0.1*k,0.24*k,18),L(0xf4efe6)); mug.position.set(1.0*k,0.12*k,0.25*k); pX.add(mug); const tea=new THREE.Mesh(new THREE.CircleGeometry(0.095*k,18),new THREE.MeshBasicMaterial({color:0x8a5a35})); tea.rotation.x=-Math.PI/2; tea.position.set(1.0*k,0.235*k,0.25*k); pX.add(tea);\n"
    "    a.g.position.set(0.02*k,0.06*k,-0.06*k); cardPose(a,'idle',true,0.45); camAt([1.05,1.6,3.15],[0.08,0.52,-0.12]); rect=[0,0,320,240]; }")
# contact shadows + render + clean up extra props
rep("  pCam.aspect=rect[2]/rect[3]; pCam.updateProjectionMatrix(); pRen.setSize(rect[2]*2,rect[3]*2,false); pRen.render(pScene,pCam);\n",
    "  if(!['box','laundry','window','selfie'].includes(scene))for(const c of cats){ const r=(c.state==='flop'||c.state==='sleep'?0.5:0.36)*c.g.scale.x, m=new THREE.Mesh(new THREE.CircleGeometry(r,28),new THREE.MeshBasicMaterial({color:0x3a2618,transparent:true,opacity:0.2,depthWrite:false})); m.rotation.x=-Math.PI/2; m.position.set(c.g.position.x,c.g.position.y+0.004*sc,c.g.position.z); m.scale.set(1,1.35,1); pScene.add(m); cardX.push(m); }\n"
    "  pCam.aspect=rect[2]/rect[3]; pCam.updateProjectionMatrix(); pRen.setSize(rect[2]*2,rect[3]*2,false); pRen.render(pScene,pCam);\n"
    "  for(const o of cardX.splice(0)){ pScene.remove(o); o.traverse(q=>{ if(q.geometry)q.geometry.dispose(); if(q.material)q.material.dispose(); }); }\n")
rep("function postcard(cats){ try{", "const cardX=[];\nfunction postcard(cats){ try{")
# backgrounds: ceiling for the selfie, desk wall for the laptop, a bit more detail in the plain room
rep("  if(scene==='selfie'){ R(wall,0,0,320,240); R('#fff',230,20,70,60); R('#bfe8f7',235,25,60,50); }",
    "  if(scene==='selfie'){ const g=x.createLinearGradient(0,0,320,240); g.addColorStop(0,'#f7f3ec'); g.addColorStop(1,'#e6ddcf'); x.fillStyle=g; x.fillRect(0,0,320,240);\n"
    "    x.fillStyle=wall; x.beginPath(); x.moveTo(0,120); x.lineTo(150,240); x.lineTo(0,240); x.fill(); x.strokeStyle='#fbf7f0'; x.lineWidth=7; x.beginPath(); x.moveTo(0,118); x.lineTo(152,240); x.stroke(); x.strokeStyle='rgba(0,0,0,.08)'; x.lineWidth=2; x.beginPath(); x.moveTo(0,124); x.lineTo(146,240); x.stroke();\n"
    "    const cu=pick(['#c86b6b','#6b8fc8','#7fae78','#d9a35a']); x.fillStyle=cu; x.beginPath(); x.moveTo(0,142); x.lineTo(124,240); x.lineTo(0,240); x.fill(); for(let i=1;i<10;i++){ const t=i/10, ax=124*t, ay=142+98*t; x.strokeStyle='rgba(0,0,0,.14)'; x.lineWidth=3; x.beginPath(); x.moveTo(ax,ay+5); x.quadraticCurveTo(ax-30,ay+28,ax-62,ay+62); x.stroke(); x.strokeStyle='rgba(255,255,255,.13)'; x.lineWidth=2; x.beginPath(); x.moveTo(ax+5,ay+8); x.quadraticCurveTo(ax-25,ay+32,ax-56,ay+66); x.stroke(); } x.strokeStyle='#7a5a3e'; x.lineWidth=4; x.beginPath(); x.moveTo(0,138); x.lineTo(130,242); x.stroke(); for(let i=0;i<8;i++){ E('#6b4c34',4+i*16,141+i*12.6,3.2,3.2); } E('#5a4030',6,140,6,6);\n"
    "    x.save(); x.translate(205,92); x.scale(1,0.55); for(let i=0;i<5;i++){ x.save(); x.rotate(i*Math.PI*2/5+0.3); x.fillStyle='#8a6446'; x.beginPath(); x.ellipse(52,0,46,11,0,0,7); x.fill(); x.fillStyle='rgba(0,0,0,.12)'; x.beginPath(); x.ellipse(52,3,44,6,0,0,7); x.fill(); x.restore(); } x.restore(); E('#d9d2c4',205,92,15,11); E('#fff8dc',205,96,10,7); E('rgba(255,248,215,.35)',205,96,40,28); R('#b9b0a2',203,40,4,46); E('#cfc6b6',205,40,10,5); }")
rep("  else if(scene==='box'||scene==='laundry'||scene==='laptop'||scene==='pillow'){ R(wall,0,0,320,240); R('#d9b48a',0,170,320,70); E(rug,160,205,120,24); if(scene==='pillow'){ E('#fff',160,180,130,40); E('#eef3fb',160,170,105,30); } }",
    "  else if(scene==='laptop'){ R(wall,0,0,320,240); R('#fff',18,14,96,84); R('#cfe9f5',24,20,84,72); R('#fff',64,20,4,72); E('rgba(255,236,170,.35)',70,60,70,55); R('#f1ece3',226,22,62,46); R(pick(['#f2a65a','#7fb2e5','#e58fb5']),232,28,50,34); E('rgba(255,255,255,.5)',248,40,8,6); R('#5fb35a',290,96,6,30); E('#6cc06a',293,92,14,10); }\n"
    "  else if(scene==='box'||scene==='laundry'||scene==='pillow'){ R(wall,0,0,320,240); R('#f1ece3',220,26,64,48); R(pick(['#f2a65a','#7fb2e5','#e58fb5']),226,32,52,36); R('#d9b48a',0,170,320,70); R('#efe6d6',0,164,320,7); E(rug,160,205,120,24); if(scene==='pillow'){ E('#fff',160,180,130,40); E('#eef3fb',160,170,105,30); } }")
# draw the cat: soft (out of focus) for the phone-camera card
rep("  x.drawImage(pRen.domElement,...rect); pRen.setSize(320,240,false);",
    "  if(scene==='selfie'){ const sm=document.createElement('canvas'); sm.width=90; sm.height=68; const sx=sm.getContext('2d'); sx.imageSmoothingQuality='high'; sx.drawImage(pRen.domElement,0,0,90,68); x.imageSmoothingQuality='high'; x.drawImage(sm,...rect); x.globalAlpha=0.35; x.drawImage(pRen.domElement,...rect); x.globalAlpha=1; }\n"
    "  else x.drawImage(pRen.domElement,...rect); pRen.setSize(320,240,false);")
# old flat laptop prop is gone (the laptop is 3D now)
rep("  if(scene==='laptop'){ x.fillStyle='#8d97a6'; x.beginPath(); x.moveTo(190,200); x.lineTo(300,200); x.lineTo(310,222); x.lineTo(180,222); x.fill(); R('#5b6573',200,140,90,62); R('#9fd3ff',206,146,78,50); }\n", "")
# phone-photo finish: warm tint, vignette, faint grain
rep("  const n=W.homes.length, first=n<3, grumpy=",
    "  { x.fillStyle='rgba(255,214,160,.07)'; x.fillRect(0,0,320,240); const vg=x.createRadialGradient(160,120,90,160,120,215); vg.addColorStop(0,'rgba(40,25,15,0)'); vg.addColorStop(1,'rgba(40,25,15,.28)'); x.fillStyle=vg; x.fillRect(0,0,320,240);\n"
    "    for(let i=0;i<900;i++){ x.fillStyle=Math.random()<0.5?'rgba(255,255,255,.05)':'rgba(0,0,0,.05)'; x.fillRect(Math.random()*320,Math.random()*240,1,1); } }\n"
    "  const n=W.homes.length, first=n<3, grumpy=")
rep("camAt([1.2,1.1,2.6],[0,0.5,0]); rect=[60,8,200,150]; }", "camAt([1.2,1.1,2.6],[0,0.5,0]); rect=[60,scene==='box'?46:36,200,150]; } /* sits in the box, not on it */")
open(P, 'w', encoding='utf-8').write(s)
print('v148 applied')
