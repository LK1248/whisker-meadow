"""v104: owl flight looks like a bird, not a cannonball.
- Wings hinge at the shoulder (they used to spin around their own centres) and open wide in flight.
- Take-off: a short crouch, then a push up with deep, quick wingbeats while it builds speed (no instant full speed);
  it keeps the way it was facing and turns smoothly toward where it's going.
- Cruise: slow, deep owl wingbeats alternating with glides on outstretched wings, a slight body bob and forward lean.
- Hopping to another tree eases in and out and ends with a landing flare (wings up, body back). Leaving for the night
  is a longer, gentler climbing flight that speeds up as it goes, out over the trees."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
# shoulder-hinged wings
rep("  for(const sx of [1,-1]){ body.add(mesh(G.sph,dk,{p:[0.17*sx,0.22,-0.01],s:[0.07,0.18,0.14]})); body.add(mesh(G.sphLo,0xe0a030,",
    "  const wings=[]; for(const sx of [1,-1]){ const wp=new THREE.Group(); wp.position.set(0.15*sx,0.34,-0.01); wp.userData.sx=sx; body.add(wp); wings.push(wp); wp.add(mesh(G.sph,dk,{p:[0.02*sx,-0.12,0],s:[0.07,0.18,0.14]})); body.add(mesh(G.sphLo,0xe0a030,")
rep("return {g,body,head,eyes,wings:body.children.filter(m=>Math.abs(m.position.x)>0.15)}; }", "return {g,body,head,eyes,wings}; }")
# flight timing
rep("o.flyT=0.55; o.fly={from,to,t:0,dur:away?3.2:Math.max(1.4,from.distanceTo(to)/4.5),away}; }",
    "o.flyT=0.5; o.fly={from,to,t:0,dur:away?6.5:Math.max(2,from.distanceTo(to)/3),away,ph:0,wa:0,lean:0}; }")
old_start = s.index("function owlFlight(o,dt){")
old_end = s.index("function updateOwls(dt){")
s = s[:old_start] + r"""function owlFlight(o,dt){ const f=o.fly;
  if(o.flyT>0){ o.flyT-=dt; const k=1-Math.max(0,o.flyT)/0.5; o.body.scale.set(1+0.06*k,1-0.1*k,1+0.06*k); o.wings.forEach(w=>w.rotation.z=w.userData.sx*0.5*k); // crouch, wings loosen
    if(o.flyT>0)return; o.body.scale.setScalar(1); const par=o.g.parent.parent||scene; par.attach(o.g); o.flyPar=par; o.inv=1; o.g.rotation.x=0; o.g.rotation.z=0; }
  f.t=Math.min(1,f.t+dt/f.dur); const q=f.t;
  const sP=f.away?0.18*q+0.82*q*q:q*q*(3-2*q); // leaving: speeds up as it goes; tree hop: eases in and out
  const p=f.from.clone().lerp(f.to,sP); p.y+=f.away?Math.min(1,q*4)*0.8:Math.sin(q*Math.PI)*0.9+Math.min(1,q*6)*0.15*(1-q);
  o.g.position.copy(o.flyPar.worldToLocal(p));
  o.g.rotation.y=angLerp(o.g.rotation.y,Math.atan2(f.to.x-f.from.x,f.to.z-f.from.z),Math.min(1,dt*5));
  const take=q<(f.away?0.16:0.22), land=!f.away&&q>0.8, glide=!take&&!land&&((W.time*0.55)%1)<0.4;
  let amp, rate, base;
  if(take){ amp=0.75; rate=12; base=1.15; } else if(land){ amp=0.15; rate=7; base=1.75; } else if(glide){ amp=0.06; rate=3; base=1.45; } else { amp=0.6; rate=8; base=1.2; }
  f.ph+=dt*rate; f.wa=lerp(f.wa,base+amp*Math.sin(f.ph),Math.min(1,dt*14));
  o.wings.forEach(w=>{ w.rotation.z=w.userData.sx*f.wa; });
  f.lean=lerp(f.lean,take?-0.15:land?-0.4:0.32,Math.min(1,dt*4)); o.body.rotation.x=f.lean;
  o.body.position.y=(glide?0:-0.035*Math.sin(f.ph+0.6))*(take?1.3:1);
  if(q>=1){ o.fly=null; o.body.rotation.x=0; o.body.position.y=0; o.wings.forEach(w=>w.rotation.z=0); if(f.away){ o.gone=true; o.g.visible=false; } else perchOwl(o,o.dest); } }
""" + s[old_end:]
open(P, 'w', encoding='utf-8').write(s); print('ok')
