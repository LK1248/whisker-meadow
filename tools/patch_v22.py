"""v22: money trouble made visible and gentle. Unpaid helpers sit down with a no-coin bubble; the money chip pulses
when the next wage can't be covered; a neighbour drops off kibble when food and money both run dry; helpers don't
spend wage money on food unless a cat is hungry."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# bubble icon: a coin with a slash
rep("    case 'spark': x.fillSt", """    case 'nocoin': x.fillStyle='#fff'; x.beginPath(); x.arc(64,58,50,0,7); x.fill(); x.beginPath(); x.moveTo(50,100); x.lineTo(64,124); x.lineTo(76,100); x.fill();
      x.fillStyle='#f6c443'; x.strokeStyle='#d99a1e'; x.lineWidth=6; x.beginPath(); x.arc(64,58,30,0,7); x.fill(); x.stroke(); x.fillStyle='#8a5a00'; x.font='800 36px sans-serif'; x.textAlign='center'; x.fillText('$',64,71);
      x.strokeStyle='#e0505f'; x.lineWidth=9; x.lineCap='round'; x.beginPath(); x.moveTo(36,30); x.lineTo(92,86); x.stroke(); break;
    case 'spark': x.fillSt""")
# helpers rest (sit) while unpaid, with a bubble; stand up with a coin sparkle when paid
rep("""  if(W.unpaid&&hp.state!=='idle'){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; hp.task=null; hp.state='idle'; }
  if(W.unpaid)hp.t=Math.max(hp.t,1);""", """  if(!hp.bub){ hp.bub=new THREE.Sprite(new THREE.SpriteMaterial({map:iconTexture('nocoin'),transparent:true,depthWrite:false})); hp.bub.scale.setScalar(0.36); hp.bub.visible=false; scene.add(hp.bub); }
  if(W.unpaid&&hp.state!=='rest'){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; hp.task=null; hp.state='rest'; }
  hp.bub.visible=hp.state==='rest'&&hp.g.visible; if(hp.bub.visible)hp.bub.position.set(p.x,1.35+Math.sin(t*2.5)*0.04,p.z);
  if(hp.state==='rest'){ hp.speed=0; if(!W.unpaid){ hp.state='idle'; hp.t=0.6; spawnFx('spark',p.clone().setY(1.1),5,0.25,0.14); } }""")
rep("  const kneel=hp.state==='kneel', kk=Math.min(1,dt*6);", "  const kneel=hp.state==='kneel'||hp.state==='rest', kk=Math.min(1,dt*6);")
rep("buy(){ const hp=helpers.pop(); if(hp){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; scene.remove(hp.g); } }", "buy(){ const hp=helpers.pop(); if(hp){ if(hp.task&&hp.task.cat)hp.task.cat.helped=null; scene.remove(hp.g); if(hp.bub)scene.remove(hp.bub); } }")
# helpers keep wage money unless a cat is actually hungry
rep("if(W.food<=0&&W.money>=8){ W.money-=8; W.food+=12; }", "if(W.food<=0&&W.money>=8+(active().some(c=>c.s.full<35)?0:helpers.length*3)){ W.money-=8; W.food+=12; }")
# money chip pulses when the next wage can't be covered; wage float is just the number
rep(".chip{display:flex;", """.chip.low{animation:lowPulse 1.1s ease-in-out infinite}
@keyframes lowPulse{0%,100%{box-shadow:0 0 0 0 rgba(224,80,95,0)}50%{box-shadow:0 0 0 5px rgba(224,80,95,.55)}}
.chip{display:flex;""")
rep("function hud(){ $('#hMoney').textContent=Math.floor(W.money);", "function hud(){ $('#hMoney').textContent=Math.floor(W.money); $('#hMoney').parentElement.classList.toggle('low',helpers.length>0&&W.money<helpers.length*3);")
rep("floatAt(70,62,'-$'+cost+' wages');", "floatAt(70,62,'-$'+cost);")
# safety net: a neighbour brings kibble when food and money are both gone
rep("function startDropoff(){ if(firstAdopt())return; if(W.dropoff||W.cats.length>=LV().cap)return; const h=LV().half;",
    "function startDropoff(gift){ if(firstAdopt())return; if(W.dropoff||(!gift&&W.cats.length>=LV().cap))return; const h=LV().half;")
rep("box.add(mesh(G.box,0x7fb2e5,{s:[0.42,0.3,0.3]})); box.add(mesh(G.box,0x3d3532,{p:[0,0,0.155],s:[0.26,0.18,0.01],cast:false})); per.hips.add(box); per.box=box;",
    "if(gift){ box.add(mesh(G.box,0xd9b07a,{s:[0.34,0.42,0.2]})); box.add(mesh(G.sph,0xd9b07a,{p:[0,0.22,0],s:[0.15,0.06,0.09]})); box.add(mesh(G.sph,0xf2b04a,{p:[0,0.02,0.105],s:[0.09,0.06,0.01],cast:false})); } else { box.add(mesh(G.box,0x7fb2e5,{s:[0.42,0.3,0.3]})); box.add(mesh(G.box,0x3d3532,{p:[0,0,0.155],s:[0.26,0.18,0.01],cast:false})); } per.hips.add(box); per.box=box;")
rep("W.dropoff={p:per,car,stage:'walkin',t:0}; }", "W.dropoff={p:per,car,stage:'walkin',t:0,gift:!!gift}; }")
rep("D.done=true; D.p.box.visible=false; D.p.carry=false; arriveStray(); }", "D.done=true; D.p.box.visible=false; D.p.carry=false; if(D.gift)giftFood(D.p.g.position); else arriveStray(); }")
rep("function updateDropoff(dt){", """function giftFood(at){ W.food+=12; W.stat.gifts=(W.stat.gifts||0)+1; spawnFx('h',at.clone().setY(1.2),6,0.4,0.4); spawnFx('spark',at.clone().setY(0.4),8,0.4); floatWorld(at.clone().setY(1.6),'+12'); Snd.chime(); hud(); }
function updateSafetyNet(dt){ W.netT=(W.netT||0)-dt; if(W.netT>0)return; W.netT=5;
  if(W.started&&!W.dropoff&&(W.food||0)+(W.premium||0)<=0&&W.money<8&&W.time>(W.netNext||0)&&!items.some(i=>i.kind==='bowl'&&i.portions>0)&&active().some(c=>c.s.full<50)){ W.netNext=W.time+240; startDropoff(true); } }
function updateDropoff(dt){""")
rep("  updateFirstAdopt(dt); updateCoats(dt);", "  updateFirstAdopt(dt); updateCoats(dt); updateSafetyNet(dt);")
rep("window.__wm={animateCat,", "window.__wm={animateCat,giftFood,updateSafetyNet,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
