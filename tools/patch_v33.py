"""v33: zoomies leap over low things (bowls, beds, litter, benches, small flower beds, other cats) and steer around big ones (trees, bushes, ponds);
petting speed is averaged over half a second and jitter no longer counts as movement."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- obstacles: tag decor with a kind and a height ----------
rep("const t=treeMesh(rand(0.9,1.3)); t.position.set(x,0,z); grp.add(t); W.decoObst.push([x,z,0.3]);",
    "const t=treeMesh(rand(0.9,1.3)); t.position.set(x,0,z); grp.add(t); W.decoObst.push([x,z,0.3,'big',0]);")
rep("s:[rand(.35,.6),rand(.3,.45),rand(.35,.55)]})); W.decoObst.push([q.x,q.z,0.55]); }",
    "s:[rand(.35,.6),rand(.3,.45),rand(.35,.55)]})); W.decoObst.push([q.x,q.z,0.55,'big',0]); }")
rep("W.decoObst.push([q.x,q.z,Math.max(w,d)/2]); }",
    "W.decoObst.push([q.x,q.z,Math.max(w,d)/2,Math.max(w,d)/2<0.8?'low':'big',0.3]); }")
rep("grp.add(bg); W.decoObst.push([bx,bz,0.5]); }", "grp.add(bg); W.decoObst.push([bx,bz,0.5,'low',0.85]); }")

# ---------- steering + leaping inside moveToward ----------
rep("""function moveToward(c,dt,speed,stop=0.15){
  const p=c.g.position, dx=c.target.x-p.x, dz=c.target.z-p.z, d=Math.hypot(dx,dz);
  if(d<stop){ c.speed=lerp(c.speed,0,Math.min(1,dt*10)); return true; }
  c.heading=angLerp(c.heading,Math.atan2(dx,dz),dt*(speed>2?10:7));""",
"""// things in the meadow a moving cat cares about: [x, z, radius, 'big'|'low'|'cat', jump height]
function obstAround(c){ const L=[], p=c.g.position;
  for(const it of items){ if(c.afterData===it||c.useItem===it||it.kind==='shelter')continue; const r=itemR(it); if(!r||(it.kind==='ball'&&it.tier===1))continue;
    L.push(it.kind==='tree'?[it.pos.x,it.pos.z,r,'big',0]:[it.pos.x,it.pos.z,r,'low',({bowl:0.32,litter:0.5,bed:0.42,ball:0.45})[it.kind]||0.4]); }
  for(const [x,z,r] of ponds())L.push([x,z,r,'big',0]);
  for(const o of W.decoObst||[])L.push(o[3]?o:[o[0],o[1],o[2],'big',0]);
  for(const o of W.cats)if(o!==c&&o.away<=0&&!o.carried&&!o.outside&&!o.leaving&&dist2(o.g.position,p)<4)L.push([o.g.position.x,o.g.position.z,0.28*o.g.scale.x+0.05,'cat',0.5*o.g.scale.x]);
  return L; }
// look ahead toward the target: sprinting cats leap low things, every cat swerves around big ones
function steerAround(c,dx,dz,d){ let want=Math.atan2(dx,dz); if(c.outside||c.carried||c.state==='path'||d<0.6)return want;
  const p=c.g.position, ux=dx/d, uz=dz/d, sprint=c.speed>1.8, sc=c.g.scale.x; let block=null, bAlong=1e9;
  c.leapCD=Math.max(0,(c.leapCD||0)-(c.lastDt||0.016));
  for(const o of obstAround(c)){ const rx=o[0]-p.x, rz=o[1]-p.z, along=rx*ux+rz*uz; if(along<=0||along>Math.min(d-o[2]*0.6,sprint?3.2:2.2))continue;
    const lat=rx*uz-rz*ux, R=o[2]+0.3*sc; if(Math.abs(lat)>=R)continue;
    const jumpable=o[3]!=='big'&&!(o[3]==='low'&&o[2]>0.8);
    if(sprint&&jumpable){ if(c.hopT<=0&&c.leapCD<=0&&along-o[2]<0.45+c.speed*0.1){ const dist=along+o[2]+0.4*sc, dur=clamp(dist/Math.max(c.speed,2),0.34,0.72);
        hop(c,(o[4]||0.4)+0.12,dur); c.leap=true; c.leapCD=dur+0.2; if(o[3]==='cat')W.stat.leaps=(W.stat.leaps||0)+1; }
      continue; }
    if(c.leap&&c.hopT>0)continue;
    if(along<bAlong){ bAlong=along; block=[rx,rz,R+0.15]; } }
  if(block){ const dc=Math.hypot(block[0],block[1])||0.001, ac=Math.atan2(block[0],block[1]), off=Math.asin(Math.min(1,block[2]/dc));
    const a1=ac+off, a2=ac-off, df=a=>Math.abs(Math.atan2(Math.sin(a-want),Math.cos(a-want)));
    // keep the side we already picked for this obstacle so the cat doesn't dither
    const side=c.avoidSide&&Math.abs(c.avoidAc-ac)<0.6?c.avoidSide:(df(a1)<=df(a2)?1:-1); c.avoidSide=side; c.avoidAc=ac; want=side>0?a1:a2; }
  else c.avoidSide=0;
  return want; }
function moveToward(c,dt,speed,stop=0.15){
  const p=c.g.position, dx=c.target.x-p.x, dz=c.target.z-p.z, d=Math.hypot(dx,dz);
  if(d<stop){ c.speed=lerp(c.speed,0,Math.min(1,dt*10)); return true; }
  c.lastDt=dt; c.heading=angLerp(c.heading,steerAround(c,dx,dz,d),dt*(speed>2?10:7));""")

# mid-leap cats sail over other cats and low items instead of being shoved by them
rep("for(let i=0;i<cs.length;i++)for(let j=i+1;j<cs.length;j++){ const a=cs[i],b=cs[j]; if(dist2(a.g.position,b.g.position)>1.6||",
    "const air=c=>c.leap&&c.hopT>0;\n    for(let i=0;i<cs.length;i++)for(let j=i+1;j<cs.length;j++){ const a=cs[i],b=cs[j]; if(air(a)||air(b)||dist2(a.g.position,b.g.position)>1.6||")
rep("      for(const it of items){ if(c.afterData===it||c.useItem===it)continue;",
    "      for(const it of items){ if(c.afterData===it||c.useItem===it||(air(c)&&it.kind!=='tree'&&it.kind!=='shelter'))continue;")
rep("for(const [px,pz,r] of ponds().concat(W.decoObst||[]))for(const cc of catCircles(c)){",
    "for(const [px,pz,r,kd] of ponds().concat(W.decoObst||[])){ if(kd==='low'&&air(c))continue; for(const cc of catCircles(c)){")
rep("if(d<m){ c.g.position.x+=dx/d*(m-d); c.g.position.z+=dz/d*(m-d); } }\n      for(const hp of helpers)",
    "if(d<m){ c.g.position.x+=dx/d*(m-d); c.g.position.z+=dz/d*(m-d); } } }\n      for(const hp of helpers)")
# solid() excludes cats high in the air; keep leaping cats in the list so ponds/trees still push them
rep("&&!(c.state==='sleep'&&c.useItem)&&c.jump<0.15; }", "&&!(c.state==='sleep'&&c.useItem)&&(c.jump<0.15||c.leap); }")

# leap pose: stretched out, front paws reaching, nose up on take-off and down for the landing
rep("  if(c.hopT>0){ c.hopT-=dt; c.jump=Math.sin(clamp(1-c.hopT/c.hopDur,0,1)*Math.PI)*c.hopH; } else c.jump=0;",
    "  if(c.hopT>0){ c.hopT-=dt; c.jump=Math.sin(clamp(1-c.hopT/c.hopDur,0,1)*Math.PI)*c.hopH; } else { c.jump=0; c.leap=false; }")
rep("  let stretch=0, gal=false;\n",
    """  let stretch=0, gal=false;
  if(c.leap&&c.hopT>0&&!c.carried){ const q=clamp(1-c.hopT/c.hopDur,0,1); gal=true; legA=[-1.35,-1.25,1.2,1.1]; rx=-0.38+0.76*q; coreY=0.44; stretch=0.16; tailUp=0.25; swish=0.03; earOut=Math.max(earOut,0.5); hx=-0.1; }
  else """)

# ---------- petting: speed over a half-second window, jitter isn't movement ----------
rep("  const len0=Math.hypot(dx,dy), dtm=Math.max(0.008,(now-(S.tm||now-16))/1000); S.tm=now; const inst=len0/dtm; S.v=S.v==null?inst:lerp(S.v,inst,0.35);",
"""  const len0=Math.hypot(dx,dy), dtm=Math.max(0.008,(now-(S.tm||now-16))/1000); S.tm=now;
  if(W.tool==='hand'){ const sm=S.samp||(S.samp=[]); sm.push([now,e.clientX,e.clientY]); while(sm.length>1&&now-sm[0][0]>500)sm.shift();
    let path=0,x0=1e9,x1=-1e9,y0=1e9,y1=-1e9; for(let i=0;i<sm.length;i++){ const q=sm[i]; if(i)path+=Math.hypot(q[1]-sm[i-1][1],q[2]-sm[i-1][2]); if(now-q[0]<=200){ x0=Math.min(x0,q[1]); x1=Math.max(x1,q[1]); y0=Math.min(y0,q[2]); y1=Math.max(y1,q[2]); } }
    S.v=path/Math.max(0.25,(now-sm[0][0])/1000); S.moving=Math.hypot(x1-x0,y1-y0)>=5; }
  else { const inst=len0/dtm; S.v=S.v==null?inst:lerp(S.v,inst,0.35); }""")
rep("  if(W.tool==='hand'){ S.last=now; S.zones[h.zone]=(S.zones[h.zone]||0)+len; petMove(S.cat,len,h.zone);",
    "  if(W.tool==='hand'){ if(!S.moving)return; S.last=now; S.zones[h.zone]=(S.zones[h.zone]||0)+len; petMove(S.cat,len,h.zone);")
rep("function beginStroke(c,now){ S.v=null; S.tm=null;", "function beginStroke(c,now){ S.v=null; S.tm=null; S.samp=[]; S.moving=false;")
rep("      if(c.hopT<=0)moveToward(c,dt,4.6,0.3); break; }", "      if(c.hopT<=0||c.leap)moveToward(c,dt,4.6,0.3); break; }")
rep("window.__wm={animateCat,", "window.__wm={animateCat,steerAround,obstAround,moveToward,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
