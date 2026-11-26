"""v168: newborn kittens get a family photo.
When kittens are born at the sanctuary, their welcome card now has a big pink heart above it with a family photo
inside: mum and dad at the back, the new kitten (or twins) in front. The heart pulses gently. Below it is the usual
card with the cats' list (the new kittens highlighted) and the Hello! button. Twins now share one card
("Name & Name") instead of two cards in a row."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# one card for the whole litter
rep("function meet(c,origin,parents){", "function meet(c,origin,parents,kits){")
rep("coatNow(c); meetQ.push({c,origin,parents});", "coatNow(c); if(kits)kits.forEach(coatNow); meetQ.push({c,origin,parents,kits});")
rep("  if(!famMoment(ks,a,b,mid))for(const k of ks)meet(k,'born',[a,b]);", "  if(!famMoment(ks,a,b,mid))meet(ks[0],'born',[a,b],ks);")
rep("for(const k of F.ks)meet(k,'born',[F.a,F.b]); } }", "meet(F.ks[0],'born',[F.a,F.b],F.ks); } }")
# the heart above the card
rep('<div id="meet" hidden><div class="sheet">', '<div id="meet" hidden><div id="mFam" hidden><img alt=""></div><div class="sheet">')
rep("#meet .big{margin-top:12px;flex:none}",
    "#meet .big{margin-top:12px;flex:none}#meet{flex-direction:column;align-items:center}#mFam{flex:none;margin-bottom:-14px;z-index:1;pointer-events:none}"
    "#mFam img{display:block;width:min(240px,56vw,30vh);height:auto;filter:drop-shadow(0 6px 14px rgba(120,40,60,.35));animation:famPulse 1.5s ease-in-out infinite}"
    "@keyframes famPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}")
rep("  $('#mName').textContent=m.c.name;",
    "  const kits=m.kits||[m.c]; $('#mName').textContent=kits.map(k=>k.name).join(' & ');\n"
    "  { const fe=$('#mFam'), im=m.origin==='born'?famPhoto(m.parents.filter(p=>p.g.parent),kits):null; fe.hidden=!im; if(im)fe.querySelector('img').src=im; }")
rep("<div class=\"rc ${c===m.c?'new':''}\">", "<div class=\"rc ${kits.includes(c)?'new':''}\">")
rep("$('#meet').hidden=false; handVis(); Snd.meow(m.c.age<1?1.45:1.15,0.6);",
    "$('#meet').hidden=false; handVis(); Snd.meow(m.c.age<1?1.45:1.15,0.6); if(m.origin==='born')Snd.chime();")
# the photo: parents behind, kittens in front, inside a big pink heart
rep("// ---- postcards from new homes: little staged photos ----",
    "function famPhoto(par,kits){ try{ if(!pRen)portrait(par[0]||kits[0]); const all=[...par,...kits], sc=(par[0]||kits[0]).g.scale.x;\n"
    "  const saved=all.map(c=>({c,parent:c.g.parent,pos:c.g.position.clone(),rot:c.g.rotation.y,hd:c.heading,st:c.state,stT:c.stT,sit:c.sit,iv:c.icon.visible,go:c.glow.material.opacity}));\n"
    "  for(const c of all){ pScene.add(c.g); c.icon.visible=false; c.glow.material.opacity=0; }\n"
    "  par.forEach((c,i)=>{ c.g.position.set((par.length>1?(i?0.48:-0.48):0)*sc,0,-0.35*sc); cardPose(c,'idle',true,par.length>1?(i?-0.4:0.4):0); });\n"
    "  kits.forEach((c,i)=>{ const n=kits.length; c.g.position.set((n>1?(i?0.28:-0.28):0)*sc,0,0.42*sc); cardPose(c,'idle',true,n>1?(i?-0.3:0.3):0); });\n"
    "  pCam.fov=30; pCam.position.set(0,1.4*sc,3.95*sc); pCam.lookAt(0,0.4*sc,0); pCam.aspect=1; pCam.updateProjectionMatrix(); pRen.setSize(440,440,false); pRen.render(pScene,pCam);\n"
    "  const cv=document.createElement('canvas'); cv.width=cv.height=360; const x=cv.getContext('2d'), H=new Path2D('M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z');\n"
    "  const at=k=>x.setTransform(k,0,0,k,180-12*k,186-13.3*k); // heart centred at (180,186)\n"
    "  at(21.5); const g=x.createLinearGradient(0,4,0,22); g.addColorStop(0,'#ff9fbf'); g.addColorStop(1,'#ff5f8f'); x.fillStyle=g; x.fill(H);\n"
    "  at(19); x.fillStyle='#fff3f7'; x.fill(H); x.save(); x.clip(H); x.setTransform(1,0,0,1,0,0); x.fillStyle='rgba(255,182,206,.45)'; x.beginPath(); x.ellipse(180,262,120,30,0,0,7); x.fill(); x.drawImage(pRen.domElement,22,40,316,316); x.restore();\n"
    "  for(const v of saved){ const c=v.c; v.parent.add(c.g); c.g.position.copy(v.pos); c.g.rotation.y=v.rot; c.heading=v.hd; c.state=v.st; c.stT=v.stT; c.sit=v.sit; c.icon.visible=v.iv; c.glow.material.opacity=v.go; c.bat=0; }\n"
    "  pCam.aspect=4/3; pCam.updateProjectionMatrix(); pRen.setSize(320,240,false);\n"
    "  return cv.toDataURL('image/png'); }catch(e){ return null; } }\n"
    "// ---- postcards from new homes: little staged photos ----")
open(P, 'w', encoding='utf-8').write(s)
print('v168 applied')
