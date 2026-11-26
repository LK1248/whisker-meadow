"""v158: a proper head shake.
- Shape (0.95 s): a slow lean of the head to one side, then a very rapid side-to-side burst (~9 shakes/s for ~0.3 s)
  with the ears flopping sideways and lagging behind the head, then a slow settle with a small fading wobble.
  Replaces the old uniform 0.65 s wiggle everywhere it was used (rain, pond swipes, digging...).
- Out of the rain: a cat that has been wet shakes its head as soon as it is out of the rain (under a roof or when the
  shower ends), and only starts its drying-off licks after the shake.
- After a long petting or brushing session (8 s or more of actual stroking) ends, the cat shakes its head about half
  the time before going back to what it was doing."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("c.shake=0.65", "c.shake=SH_D", 3)
rep("  if(c.shake>0){ c.shake-=dt; const k=Math.sin(clamp(1-c.shake/0.65,0,1)*Math.PI); hz=Math.sin(t*38)*0.55*k; hy+=Math.sin(t*38+1)*0.25*k; earOut=Math.max(earOut,k); eye=Math.min(eye,1-0.8*k); }",
    "  if(c.shake>0){ c.shake-=dt; const p=clamp(1-c.shake/SH_D,0,1), side=c.shSide||(c.shSide=Math.random()<0.5?1:-1); let tilt=0, fast=0, wob=0;\n"
    "    if(p<0.3){ tilt=Math.sin(p/0.3*Math.PI/2); } // slow lean-in\n"
    "    else if(p<0.62){ const e=(p-0.3)/0.32; tilt=1-e; fast=Math.sin(e*Math.PI); } // the rapid burst\n"
    "    else { const e=(p-0.62)/0.38; wob=(1-e)*(1-e); } // slow settle\n"
    "    const ph=t*55; hz=side*0.32*tilt+Math.sin(ph)*0.62*fast+Math.sin(t*10)*0.14*wob; hy+=Math.sin(ph+1)*0.16*fast; rz+=Math.sin(ph)*0.05*fast; hx=Math.min(hx,0.1)-0.08*fast;\n"
    "    c.flop=-Math.sin(ph-1.1)*0.95*fast+Math.sin(t*10-0.9)*0.25*wob; earOut=Math.max(earOut,0.35*tilt+0.55*fast); eye=Math.min(eye,1-0.4*tilt-0.5*fast);\n"
    "    if(c.shake<=0){ c.shSide=0; c.flop=0; } } else c.flop=0;")
rep("  c.ears.forEach((e,i)=>{ const sx=i?-1:1; e.rotation.z=lerp(e.rotation.z,(-0.35-earOut*0.9)*sx+(c.earTw>0&&i===0?0.3*Math.sin(t*40):0),k); });",
    "  c.ears.forEach((e,i)=>{ const sx=i?-1:1; e.rotation.z=lerp(e.rotation.z,(-0.35-earOut*0.9)*sx+(c.earTw>0&&i===0?0.3*Math.sin(t*40):0)+(c.flop||0),c.flop?1:k); }); // flop: both ears swing the same way during a head shake")
# the head follows the shake exactly (the usual smoothing would flatten the rapid burst)
rep("c.head.rotation.x=lerp(c.head.rotation.x,hx,k); c.head.rotation.z=lerp(c.head.rotation.z,hz,k);",
    "{ const kh=c.shake>0&&c.shake<SH_D-0.08?1:c.shake>0?Math.max(k,Math.min(1,dt*20)):k; c.head.rotation.x=lerp(c.head.rotation.x,hx,kh); c.head.rotation.z=lerp(c.head.rotation.z,hz,kh); }")
# out of the rain: shake first, then the licking
rep("if((c.wetAcc||0)>2)c.dryT=DRY_T;", "if((c.wetAcc||0)>2){ c.dryT=DRY_T; if(!c.carried)c.shake=SH_D; }")
rep("if(c.dryT>0&&c.age>0.25&&Math.random()<0.45)", "if(c.dryT>0&&c.age>0.25&&!(c.shake>0)&&Math.random()<0.45)")
rep("if(c.dryT>0&&c.age>0.25&&Math.random()<dt/5)", "if(c.dryT>0&&c.age>0.25&&!(c.shake>0)&&Math.random()<dt/5)")
# after a long petting / brushing session
rep("    case 'pet': c.petT-=dt; if(c.turnTo!==undefined){",
    "    case 'pet': c.petT-=dt; if(c.petT>2)c.sessT=(c.sessT||0)+dt; if(c.turnTo!==undefined){")
rep("if(c.petT<=0&&c.gaze<=0)setState(c,'idle',rand(1.5,3)); break;",
    "if(c.petT<=0&&c.gaze<=0){ setState(c,'idle',rand(1.5,3)); if((c.sessT||0)>=8&&Math.random()<0.5)c.shake=SH_D; c.sessT=0; } break;")
rep("const LICK_GAIN=0.15,", "const SH_D=0.95; // head shake length (s)\nconst LICK_GAIN=0.15,")
open(P, 'w', encoding='utf-8').write(s)
print('v158 applied')
