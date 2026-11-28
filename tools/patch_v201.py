"""v201: belly-rub invitations read by pose, and depend on love.
- A cat with love 75+ that flops shows the belly toward the player and stretches in a slow rhythm: neck and chin reach
  away from the belly, front legs reach forward and hind legs back, then it relaxes and stretches again. No more
  looking straight at the camera.
- A cat with less love that flops is still guarded: paws tucked to the chest, ears back, tail flicking. Rubbing that
  belly still gets a scratch, so the pose itself tells the player which bellies are safe.
- The belly lesson (whose tip shows love -> heart, low love -> claw) now starts only with a cat at love 75+, so the
  first belly rub always goes well."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# pose block (three lines written by v200)
a = s.index("  else if(st==='flop'){ const inv=!c.carried&&!(c.trap>0);")
b = s.index("/* belly toward the player */", a) + len("/* belly toward the player */")
s = s[:a] + (
    "  else if(st==='flop'){ const free=!c.carried&&!(c.trap>0), inv=free&&c.s.aff>=75, grd=free&&!inv; c.flopS=0; c.flopInv=inv;\n"
    "    rz=2.45; coreY=0.36; legA=[Math.sin(t*2)*0.3,Math.sin(t*2+1)*0.3,0.3,0.3]; tailUp=0; swish=0.25; eye=purring?0.4:0.8; hz=-0.6;\n"
    "    if(inv){ const ph=(t*0.5+c.id*0.37)%1, k2=0.5-0.5*Math.cos(ph*Math.PI*2); c.flopS=k2; /* slow rhythmic stretch: reach out, relax, reach out */\n"
    "      rz=2.05+Math.sin(t*1.1+c.id)*0.08; legA=[-0.45-1.0*k2,-0.55-0.9*k2,0.35+0.95*k2,0.45+0.85*k2]; hx=1.0-0.4*k2; hz=-0.6; /* face in three-quarter profile, chin reaching forward */ swish=0.3; swSpd=1.2; eye=purring?0.35:0.6-0.3*k2; }\n"
    "    else if(grd){ rz=2.3; legA=[1.15,1.05,-0.8,-0.9]; swish=0.55; swSpd=4.5; earOut=0.55; eye=0.95; hx=0.15; } /* not sure yet: paws tucked, ears back, tail flicking */\n"
    "    if(c.trap>0){ legA=[-1.2,-1.2,1.0,1.0]; }\n"
    "    if(free){ const dx=camera.position.x-c.g.position.x, dz=camera.position.z-c.g.position.z, want=Math.atan2(-dz,dx); let d=want-c.heading; d=Math.atan2(Math.sin(d),Math.cos(d)); c.heading+=d*Math.min(1,dt*3); } } /* belly toward the player */"
) + s[b:]

# head: stretch the neck along the body in time with the stretch, instead of looking at the camera
a = s.index("function flopLook(c,dt,on){")
b = s.index("// the head keeps looking at the player", a) + len("// the head keeps looking at the player")
s = s[:a] + ("function flopLook(c,dt,on){ if(!c.headP0)c.headP0=c.head.position.clone(); const inv=on&&c.flopInv, k2=inv?(c.flopS||0):0;\n"
             "  FL_V.copy(c.headP0); if(inv){ FL_V.y-=0.42; FL_V.z+=0.2+0.12*k2; } /* head level with the body, neck reaching out */ c.head.position.lerp(FL_V,Math.min(1,dt*8)); } // neck reaches out with the stretch") + s[b:]
rep("const FL_M=new THREE.Matrix4(), FL_Q=new THREE.Quaternion(), FL_P=new THREE.Quaternion(), FL_H=new THREE.Vector3(), FL_V=new THREE.Vector3(), FL_UP=new THREE.Vector3();",
    "const FL_V=new THREE.Vector3();")

# the belly lesson starts with a cat that will enjoy it
rep("!W.stat.bellyTip&&(W.stat.good||0)>=10&&s.aff>=35&&", "!W.stat.bellyTip&&(W.stat.good||0)>=10&&s.aff>=75&&")
open(P, 'w', encoding='utf-8').write(s)
print('v201 applied')
