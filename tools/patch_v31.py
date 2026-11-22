"""v31: clear family greeting (sniff, then a sideways belly show if it likes them, or turn and walk back if not); wider house sign whose text fits."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- greeting ----------
rep("function famGreet(c){ const f=W.family; f.state='greet'; f.greetT=3; f.members[0].kneel=true; c.heading=Math.PI; showIcon(c,'sniff',2); }",
"""function famGreet(c){ const f=W.family; f.state='greet'; f.greetT=3.4; f.decided=false; c.greetFlop=0; setState(c,'greet'); f.members[0].kneel=true; c.heading=Math.PI; showIcon(c,'sniff',1.3);
  f.match=c.trait===f.want||(c.s.trust>=75&&Math.random()<0.5)||Math.random()<0.15; }""")
rep("""    if(f.state==='greet'&&f.greetT>0){ f.greetT-=dt; if(f.greetT<=0){ const c=f.cat; const match=c.trait===f.want||(c.s.trust>=75&&Math.random()<0.5)||Math.random()<0.15;
        if(match)adoptOK(c); else { f.tries++; f.members[0].kneel=false; floatWorld(c.g.position.clone().setY(1.2),'Not quite'); backFromGate(c); if(f.tries>=2)familyLeave("We'll keep looking!"); else { f.state='wait'; f.cat=null; renderFamily(); } } } }""",
"""    if(f.state==='greet'&&f.greetT>0){ f.greetT-=dt; const c=f.cat;
      // after a short sniff the cat decides: roll over on its side for them, or turn its back and go home
      if(!f.decided&&f.greetT<=2.1){ f.decided=true;
        if(f.match){ c.greetFlop=1; c.heading=Math.PI+(Math.random()<0.5?1.25:-1.25); c.purr=1; showIcon(c,'h',1.8); spawnFx('h',c.g.position.clone().setY(0.7),4,0.4,0.3); Snd.chirp(); }
        else { f.greetT=0; f.tries++; f.members[0].kneel=false; c.heading=0; showIcon(c,'huff',1.4); floatWorld(c.g.position.clone().setY(1.2),'Not quite'); backFromGate(c);
          if(f.tries>=2)familyLeave("We'll keep looking!"); else { f.state='wait'; f.cat=null; renderFamily(); } } }
      if(f.greetT<=0&&f.match&&f.state==='greet'){ c.greetFlop=0; adoptOK(c); } }""")
# sideways belly show pose (rolls onto its side, paws kneading the air)
rep("  else if(st==='greet'||st==='bye'){ rx=-0.45;",
"""  else if(st==='greet'&&c.greetFlop){ rz=1.55+Math.sin(t*2.4)*0.12; coreY=0.34; legA=[Math.sin(t*4)*0.5-0.3,Math.sin(t*4+1.6)*0.5-0.3,0.4,0.4]; tailUp=0.1; swish=0.35; swSpd=4; eye=0.45; hz=-0.5; hx=-0.2; }
  else if(st==='greet'||st==='bye'){ rx=-0.45;""")
rep("c.icon.position.y=1.35+(st==='flop'?-0.3:0)", "c.icon.position.y=1.35+(st==='flop'||(st==='greet'&&c.greetFlop)?-0.3:0)")

# ---------- sign: text always fits its board ----------
rep("lines.forEach(([t,font,col,y])=>{ x.font=font; x.fillStyle=col; x.fillText(t,w/2,y); });",
    "lines.forEach(([t,font,col,y])=>{ x.font=font; const mw=x.measureText(t).width, lim=w-56; if(mw>lim)x.font=font.replace(/(\\d+)px/,(m,n)=>Math.floor(n*lim/mw)+'px'); x.fillStyle=col; x.fillText(t,w/2,y); });")
rep("""  for(const sx of [-0.6,0.6]) sign.add(mesh(G.box,0xa5754a,{p:[sx,0.6,0],s:[0.1,1.2,0.1]}));
  const board=new THREE.Mesh(new THREE.PlaneGeometry(1.5,0.56),new THREE.MeshBasicMaterial({map:textTex([['Whisker Meadow','700 72px Fredoka, sans-serif','#4a3426',78],['Cat Sanctuary','700 46px Nunito, sans-serif','#e0577f',140]])}));
  board.position.set(0,1.05,0.06); sign.add(board); sign.add(mesh(G.box,0xa5754a,{p:[0,1.05,0],s:[1.6,0.64,0.08]})); g.add(sign);""",
"""  for(const sx of [-0.85,0.85]) sign.add(mesh(G.box,0xa5754a,{p:[sx,0.62,0],s:[0.1,1.24,0.1]}));
  const signTex=()=>textTex([['Whisker Meadow','700 80px Fredoka, sans-serif','#4a3426',86],['Cat Sanctuary','700 58px Nunito, sans-serif','#e0577f',160]],680,224);
  const board=new THREE.Mesh(new THREE.PlaneGeometry(2.1,0.69),new THREE.MeshBasicMaterial({map:signTex()}));
  board.position.set(0,1.08,0.06); sign.add(board); sign.add(mesh(G.box,0xa5754a,{p:[0,1.08,0],s:[2.2,0.78,0.08]})); g.add(sign);
  // redraw once the web fonts have loaded so the measured width matches the real lettering
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{ board.material.map=signTex(); board.material.needsUpdate=true; });""")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
