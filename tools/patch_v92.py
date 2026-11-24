"""v92: mice are livelier and wary. They scurry in short bursts with brief sniffing pauses (not long stand-stills), and
any cat that comes within ~1.8m (through the fence too) sends them darting away from it."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("      if(rc.path){ rc.path.unshift(p.clone()); rc.chaseLen=rc.path.length; rc.pathSpeed0=rc.pathSpeed; rc.pathSpeed=2.4; } }",
    "      if(rc.path){ rc.path.unshift(p.clone()); rc.chaseLen=rc.path.length; rc.pathSpeed0=rc.pathSpeed; rc.pathSpeed=2.4; } }\n"
    "    m.chk=(m.chk||0)-dt; if(m.chk<=0&&m.flee<0.5){ m.chk=0.15; let nc=null, nd=MOUSE_SCARE*MOUSE_SCARE; // a cat wanders close: dart away from it\n"
    "      for(const c of W.cats){ if(c.away>0||c.carried)continue; const d=dist2(p,c.g.position); if(d<nd){ nd=d; nc=c; } }\n"
    "      if(nc){ m.flee=1.2; m.wait=0; const a0=Math.atan2(p.x-nc.g.position.x,p.z-nc.g.position.z)+rand(-0.4,0.4); /* first clear way out, swerving along the fence if needed */ for(const k of [0,0.7,-0.7,1.4,-1.4,2.1,-2.1]){ const aw=a0+k, t={x:p.x+Math.sin(aw)*2.5,z:p.z+Math.cos(aw)*2.5}; if(!inB(t.x,t.z,-0.4)&&!inB(p.x+Math.sin(aw)*0.4,p.z+Math.cos(aw)*0.4,-0.4)){ m.tgt=t; break; } } } }")
rep("if(!m.flee){ m.wait=rand(0.8,3); const q=outPt(rand(1.2,6)); m.tgt={x:q.x,z:q.z}; }",
    "if(!m.flee){ m.wait=Math.random()<0.7?rand(0.15,0.6):rand(0.8,1.6); const a=rand(0,6.28), r=rand(0.4,1.4); let q={x:p.x+Math.sin(a)*r,z:p.z+Math.cos(a)*r}; if(inB(q.x,q.z,-0.4)||Math.random()<0.15)q=outPt(rand(1.2,6)); m.tgt={x:q.x,z:q.z}; }")
rep("const sp=m.flee?3.2:1.1;", "const sp=m.flee?3.4:1.5;")
rep("const mice=[];", "const mice=[]; let MOUSE_SCARE=1.8; // how close a cat can come before a mouse darts away")
rep("window.__wm={Snd,", "window.__wm={Snd,setMouseScare:v=>{MOUSE_SCARE=v;},")
open(P, 'w', encoding='utf-8').write(s); print('ok')
