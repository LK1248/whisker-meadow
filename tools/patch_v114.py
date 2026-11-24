"""v114: cats no longer overlap each other. Each frame, two cats on the ground that are closer than their bodies allow
(a cat is about 0.7m wide and 1.3m nose-to-rump, so the space it needs depends on which way it faces) ease apart
slowly. Cats busy with something in place (eating, litter, sleeping, being petted...) hold still and the other one
moves; a romping pair keeps its own spacing. Cats also steer around each other a little wider."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("if(!c.carried&&!c.outside)setState(c,'idle',1); } updateCat(c,dt); }",
    "if(!c.carried&&!c.outside)setState(c,'idle',1); } updateCat(c,dt); }\n  catSpace(dt);")
rep("function updateCat(c,dt){",
    "// cats ease apart when their bodies overlap; how much room a cat needs depends on which way it faces\n"
    "const PIN_ST=['litter','eat','perch','sleep','flop','pet','boop','groom','hiding','path','greet','bye','shelter','itch'];\n"
    "function catReach(c,ux,uz){ return c.g.scale.x*(0.34+0.31*Math.abs(Math.sin(c.heading)*ux+Math.cos(c.heading)*uz)); }\n"
    "function catSpace(dt){ const cs=W.cats.filter(c=>c.away<=0&&!c.carried&&!c.outside&&!c.leaving&&!(c.hopT>0)&&!(c.g.position.y>0.15));\n"
    "  for(let i=0;i<cs.length;i++)for(let j=i+1;j<cs.length;j++){ const a=cs[i], b=cs[j], pa=a.g.position, pb=b.g.position; let dx=pb.x-pa.x, dz=pb.z-pa.z; const d=Math.hypot(dx,dz); if(d>1.6)continue;\n"
    "    if(a.state==='romp'&&a.rompP===b)continue; if(d<1e-4){ dx=1; dz=0; } else { dx/=d; dz/=d; }\n"
    "    const m=catReach(a,dx,dz)+catReach(b,dx,dz); if(d>=m)continue;\n"
    "    const fa=PIN_ST.includes(a.state)?0:1, fb=PIN_ST.includes(b.state)?0:1; if(!fa&&!fb)continue;\n"
    "    const push=Math.min(m-d,dt*(0.7+0.9*Math.max(a.speed||0,b.speed||0)))/(fa+fb); pa.x=clampX(pa.x-dx*push*fa,0.3); pa.z=clampZ(pa.z-dz*push*fa,0.3); pb.x=clampX(pb.x+dx*push*fb,0.3); pb.z=clampZ(pb.z+dz*push*fb,0.3); } }\n"
    "function updateCat(c,dt){")
rep("L.push([o.g.position.x,o.g.position.z,0.28*o.g.scale.x+0.05,'cat',0.5*o.g.scale.x]);",
    "L.push([o.g.position.x,o.g.position.z,0.36*o.g.scale.x+0.05,'cat',0.5*o.g.scale.x]);")
open(P, 'w', encoding='utf-8').write(s); print('ok')
# runaway meows: as they swell, they also come faster (every ~4s -> ~1.3s), sound more urgent (shorter, higher,
# sharper rise, a waver at the peak) and near the peak sometimes come as a quick double "mew-mew"
s = open(P, encoding='utf-8').read()
rep("meow(p=1,loud=1){ if(!this.ac)return; const ac=this.ac,t=ac.currentTime,d=0.5+Math.random()*0.15;",
    "meow(p=1,loud=1,u=0,t0=0){ if(!this.ac)return; const ac=this.ac,t=ac.currentTime+t0,d=(0.5+Math.random()*0.15)*(1-0.3*u);")
rep("o.frequency.setValueAtTime(470*p,t); o.frequency.linearRampToValueAtTime(800*p,t+d*0.35); o.frequency.linearRampToValueAtTime(540*p,t+d);",
    "o.frequency.setValueAtTime(470*p,t); if(u>0.05){ o.frequency.linearRampToValueAtTime((800+220*u)*p,t+d*0.3); o.frequency.linearRampToValueAtTime((760+120*u)*p,t+d*0.45); o.frequency.linearRampToValueAtTime((820+200*u)*p,t+d*0.6); } else o.frequency.linearRampToValueAtTime(800*p,t+d*0.35); o.frequency.linearRampToValueAtTime(540*p,t+d);")
rep("g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(0.16*loud,t+0.06);",
    "g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(0.16*loud,t+0.06-0.03*u);")
rep("R.meowT=rand(3.2,5)*(1-0.45*urgency); const d=dist2(cam.target,c.g.position);",
    "const k=Math.max(urgency,swell); R.meowT=rand(3.2,5)*(1-0.68*k); const d=dist2(cam.target,c.g.position);")
rep("Snd.meow(1.2-0.15*urgency,vol); if(d<6||urgency>0.6)showIcon(c,'sniff',1.6);",
    "Snd.meow((1.2-0.15*urgency)*(1+0.12*k),vol,k); if(k>0.6&&Math.random()<k-0.4)Snd.meow((1.25+0.1*k),vol*0.85,k,0.42); if(d<6||k>0.6)showIcon(c,'sniff',1.6);")
open(P, 'w', encoding='utf-8').write(s); print('ok3')
# roofs never overlap: a roof is ~2.6m across, so a new one keeps 3m from other roofs; and when the meadow is too full
# for a clean spot, take the roomiest spot found instead of a random one
s = open(P, encoding='utf-8').read()
rep("function placeSpot(minD=1.4,edge=0.9){ for(let k=0;k<160;k++){ const q=rIn(edge), x=q.x, z=q.z; if(Math.abs(x)<1&&z<-LV().half+1.2)continue; if(inPond(x,z,1))continue; if((W.decoObst||[]).some(([ox,oz,orr])=>Math.hypot(x-ox,z-oz)<orr+0.9))continue; if(items.every(it=>Math.hypot(it.pos.x-x,it.pos.z-z)>(it.kind==='shelter'?Math.max(minD,2):minD))) return new V3(x,0,z);} const q=rIn(edge); return new V3(q.x,0,q.z); }",
    "function placeSpot(minD=1.4,edge=0.9,roof=false){ let best=null, bv=-1e9; for(let k=0;k<240;k++){ const q=rIn(edge), x=q.x, z=q.z; if(Math.abs(x)<1&&z<-LV().half+1.2)continue; if(inPond(x,z,1))continue; if((W.decoObst||[]).some(([ox,oz,orr])=>Math.hypot(x-ox,z-oz)<orr+0.9))continue;\n"
    "  let v=1e9; for(const it of items){ const need=it.kind==='shelter'?(roof?3.0:Math.max(minD,2)):(roof&&k>=120?Math.min(minD,1.2):minD); v=Math.min(v,Math.hypot(it.pos.x-x,it.pos.z-z)-need); } if(v>0)return new V3(x,0,z); if(v>bv){ bv=v; best=new V3(x,0,z); } }\n"
    "  if(best)return best; const q=rIn(edge); return new V3(q.x,0,q.z); }")
rep("pos=pos||(kind==='shelter'?placeSpot(2.3,1.5):", "pos=pos||(kind==='shelter'?placeSpot(2.3,1.5,true):")
open(P, 'w', encoding='utf-8').write(s); print('ok4')
# Mochi is the sanctuary's own cat from the start (marked to stay, can be switched off), so the first family picks
# from the other cats; the first visit comes sooner once someone else is ready
s = open(P, encoding='utf-8').read()
rep("if(m){ m.heading=0.55+Math.PI/2;", "if(m){ m.forever=true; m.heading=0.55+Math.PI/2;")
rep("!tutQuiet()&&!strayHold()){ visitT-=dt; if(visitT<=0)spawnFamily(); } }",
    "!tutQuiet()&&!strayHold()){ visitT-=dt*(W.homes.length?1:3); if(visitT<=0)spawnFamily(); } }")
# a Skip button for every forced lesson that didn't have one (first adoption, shop, wand, fair, butt/flea tips)
rep("function firstAdopt(){ return !!(W.family&&!W.homes.length); }",
    "function firstAdopt(){ return !!(W.family&&!W.homes.length&&!W.stat.faSkip); }\n"
    "function skipLesson(){ if(firstAdopt()){ const f=W.family; W.stat.faSkip=1; if(!['walking','greet','bye'].includes(f.state))familyLeave('Maybe another day!'); return; }\n"
    "  if(tips.cur&&(tips.cur.kind==='butt'||tips.cur.kind==='flea')){ endTip(); return; }\n"
    "  if(curHint&&(shopForce()||wandForce()||fairForce())){ hintDone.add(curHint.id); if(curHint.id==='wand')hintDone.add('wand2'); if(curHint.id==='show0')hintDone.add('show'); hideHint(); } }")
rep("function tutLockTick(){ const L=tutLock(), b=document.body;",
    "function tutLockTick(){ const L=tutLock(), b=document.body; { const sk=$('#lessonSkip'), on=!!L&&!intro.c&&!bt.c&&!pl.a&&!br.c&&$('#modal').hidden; if(sk.hidden!==!on)sk.hidden=!on; }")
rep('<button id="introSkip" hidden aria-label="Skip">&#9197;</button>',
    '<button id="introSkip" hidden aria-label="Skip">&#9197;</button><button id="lessonSkip" hidden aria-label="Skip">&#9197;</button>')
rep("#introSkip{position:fixed;right:14px;", "#introSkip,#lessonSkip{position:fixed;right:14px;")
rep("$('#introSkip').onclick=()=>{", "$('#lessonSkip').onclick=()=>skipLesson();\n$('#introSkip').onclick=()=>{")
open(P, 'w', encoding='utf-8').write(s); print('ok5')
