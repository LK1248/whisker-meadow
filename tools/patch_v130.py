"""v130: volunteers. At 8+ cats one volunteer turns up at the gate (a second at 14+). They're free (no wages, never
rest for lack of pay, not counted in shop/save/hints), walk slower and take long breaks between jobs, so they do
about a third of a helper's work. If the sanctuary shrinks they leave when idle. Mint shirt, not saved (they
come back on their own)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function makeHelper(){ const last=helpers[helpers.length-1], m=personMesh({woman:last?!last.woman:Math.random()<0.5});",
    "function paidN(){ let n=0; for(const h of helpers)if(!h.vol)n++; return n; }\nfunction makeHelper(o={}){ const last=helpers[helpers.length-1], m=personMesh(Object.assign({woman:last?!last.woman:Math.random()<0.5},o));")
rep("if(W.unpaid&&hp.state!=='rest'){", "if(W.unpaid&&!hp.vol&&hp.state!=='rest'){")
rep("hp.speed=lerp(hp.speed,Math.min(1.1,d*2.5),", "hp.speed=lerp(hp.speed,Math.min(hp.vol?0.6:1.1,d*2.5),")
rep("      hp.task=null; hp.state='idle'; hp.t=rand(1.5,3); }", "      hp.task=null; hp.state='idle'; hp.t=hp.vol?rand(16,26):rand(1.5,3); }")
rep("W.money>=8+(active().some(c=>c.s.full<35)?0:helpers.length*3)", "W.money>=8+(active().some(c=>c.s.full<35)?0:paidN()*3)")
rep("helpers.length>0&&W.money<helpers.length*3", "paidN()>0&&W.money<paidN()*3")
rep("buy(){ const hp=helpers.pop(); if(hp){", "buy(){ const hp=[...helpers].reverse().find(h=>!h.vol); if(hp){ helpers.splice(helpers.indexOf(hp),1);")
rep("it.id==='helper'?helpers.length:", "it.id==='helper'?paidN():", 2)
rep("it.id!=='fire'||helpers.length", "it.id!=='fire'||paidN()")
rep("{id:'helper',when:()=>!helpers.length&&", "{id:'helper',when:()=>!paidN()&&")
rep("done:()=>helpers.length>0},", "done:()=>paidN()>0},")
rep("helpers:helpers.length,", "helpers:paidN(),")
rep("const cost=helpers.length*3;", "const cost=paidN()*3;")
rep("  for(const hp of helpers)updateHelper(hp,dt,performance.now()/1000);",
    "  volTick(dt); for(const hp of helpers)updateHelper(hp,dt,performance.now()/1000);")
rep("function paidN(){",
    """let volT=8;
function volTick(dt){ if((volT-=dt)>0)return; volT=6; const n=W.cats.length, want=n>=14?2:n>=8?1:0, vs=helpers.filter(h=>h.vol);
  if(vs.length<want&&!tutQuiet()&&!firstAdopt()&&!W.paused){ const hp=makeHelper({shirt:0x8fd6c3}); hp.vol=true; hp.t=3; spawnFx('h',hp.g.position.clone().setY(1.3),3,0.3); rec('volunteer','arrive '+n+' cats'); }
  else if(vs.length>want){ const hp=vs[vs.length-1]; if(hp.state==='idle'&&!hp.task){ helpers.splice(helpers.indexOf(hp),1); scene.remove(hp.g); if(hp.bub)scene.remove(hp.bub); rec('volunteer','leave'); } } }
function paidN(){""")
open(P, 'w', encoding='utf-8').write(s)
print('v130 applied')
