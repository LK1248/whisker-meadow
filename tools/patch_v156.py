"""v156: a kitten born at the sanctuary gets a family moment before its welcome card.
The kitten appears between its parents; mum and dad both turn to it and rub noses with it (the nose-to-nose boop
pose) while little hearts float up one after another between them for about 3 seconds, with the camera easing
over to the family. Then the usual "new cat" card shows with both parents' names. Twins: each parent nuzzles one."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("addBond(k,a,50); addBond(k,b,50); meet(k,'born',[a,b]); }",
    "addBond(k,a,50); addBond(k,b,50); ks.push(k); }\n"
    "  if(!famMoment(ks,a,b,mid))for(const k of ks)meet(k,'born',[a,b]);")
rep("  const room=LV().cap-W.cats.length; const n=(room>=2&&Math.random()<0.35)?2:1; const mid=a.g.position.clone().add(b.g.position).multiplyScalar(0.5);",
    "  const room=LV().cap-W.cats.length; const n=(room>=2&&Math.random()<0.35)?2:1; const mid=a.g.position.clone().add(b.g.position).multiplyScalar(0.5), ks=[];")
rep("spawnFx('h',mid.clone().setY(.8),8,.6,0.5); Snd.chime(); W.stat.kittens+=n;",
    "spawnFx('h',mid.clone().setY(.8),4,.4,0.4); Snd.chime(); W.stat.kittens+=n;")
rep("function updateBoops(dt){",
    "// newborn family moment: the parents nuzzle their kitten nose to nose while hearts float up, then the welcome card\n"
    "let FAM=null;\n"
    "function famMoment(ks,a,b,mid){ if([a,b].some(c=>c.carried||c.away>0||c.outside||c.leaving))return false;\n"
    "  const mom=a.sex==='f'?a:b, dad=mom===a?b:a, k1=ks[0], k2=ks[1]||null;\n"
    "  k1.g.position.set(mid.x,0,mid.z); if(k2){ const o=mom.g.position; k2.g.position.set(mid.x+(mid.x-o.x)*0.35,0,mid.z+(mid.z-o.z)*0.35); }\n"
    "  for(const c of [mom,dad,...ks]){ c.path=null; c.boopKind='boop'; c.licker=false; c.boopCD=rand(40,70); setState(c,'boop',3.4); }\n"
    "  k1.boopP=mom; mom.boopP=k1; if(k2){ k2.boopP=dad; dad.boopP=k2; } else dad.boopP=k1;\n"
    "  FAM={ks,mom,dad,t:0,next:0.3,i:0,w0:cam.want,a,b}; cam.focus={g:{position:mid.clone()}}; cam.focusT=3.4; cam.want=Math.min(cam.want,6.5); return true; }\n"
    "function famTick(dt){ const F=FAM; if(!F||W.paused)return; F.t+=dt;\n"
    "  if(F.t>=F.next&&F.t<3){ F.next+=0.3; const par=F.i%2?F.dad:F.mom, kit=F.ks.length>1&&F.i%2?F.ks[1]:F.ks[0], p=par.g.position, q=kit.g.position; F.i++;\n"
    "    spawnFx('h',new V3((p.x+q.x)/2+rand(-0.08,0.08),0.55+0.25*kit.g.scale.y+rand(0,0.12),(p.z+q.z)/2+rand(-0.08,0.08)),1,.12,0.32); if(F.i%3===1)Snd.ding(); }\n"
    "  if(F.t>=3.4){ FAM=null; cam.want=F.w0; for(const k of F.ks)meet(k,'born',[F.a,F.b]); } }\n"
    "function updateBoops(dt){")
rep("  updateBoops(dt); updateDropoff(dt);", "  updateBoops(dt); famTick(dt); updateDropoff(dt);")
open(P, 'w', encoding='utf-8').write(s)
print('v156 applied')
