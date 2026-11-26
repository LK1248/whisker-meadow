"""v157: licking.
- Self-grooming: only cats with groom over 40 stop to lick themselves now (mostly a front paw, sometimes the flank or
  a back leg). It still helps a little, but much less than before (+0.15/s while licking instead of +0.7/s), so it only
  slows the coat getting scruffy and can't keep a cat clean by itself.
- Licking a friend: a cat with love over 50 that is bonded to another cat (bond 40+) now and then walks over and
  licks its head for a few seconds.
- Parents and kittens: a kitten whose mum or dad is at the sanctuary gets licked by them now and then, on the head or
  the body, whatever anyone's stats. Being licked raises the licked cat's groom very slowly (+0.2/s kittens,
  +0.12/s grown cats), same scale as self-licking.
- Rain: a cat out in the rain (not under a rain roof) loses groom a little (0.08/s extra, about -2 per shower).
  Once it is out of the rain (under a roof, or the shower ends) it licks itself much more often for the next 20 seconds.
- Help: the rain roof line now mentions that rain makes cats a bit scruffy."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# --- self-grooming: only well-groomed cats, mostly front paws, small effect; more often while drying off ---
rep("  if(r<0.47&&c.age>0.25){ setState(c,'groom',rand(4,7)); c.groomKind=pick(['paw','paw','flank','tail','behind']); return; }",
    "  if(r<0.47&&c.age>0.25&&s.groom>40){ selfLick(c); return; }")
rep("    case 'groom': if(s.full>=60&&s.fun>=45)s.groom=Math.min(100,s.groom+dt*0.7); if(c.stT<=0){ if(c.groomKind==='paw'&&Math.random()<0.4){ c.groomKind=pick(['flank','tail']); c.stT=rand(3,5); } else setState(c,'idle',rand(2,4)); } break;",
    "    case 'groom': s.groom=Math.min(100,s.groom+dt*LICK_GAIN); if(c.stT<=0){ if(c.groomKind==='paw'&&Math.random()<0.35){ c.groomKind=pick(['flank','behind']); c.stT=rand(2.5,4); } else setState(c,'idle',rand(2,4)); } break;")
# drying off: lick more often (also from under the rain roof while it still rains)
rep("  const r=Math.random();\n  if(W.time>20&&(W.night||0)<0.5&&Math.random()<0.11){",
    "  if(c.dryT>0&&c.age>0.25&&Math.random()<0.45){ selfLick(c); return; } // just out of the rain: lots of licking\n"
    "  if(lickSocial(c))return;\n"
    "  const r=Math.random();\n  if(W.time>20&&(W.night||0)<0.5&&Math.random()<0.11){")
rep("    case 'shelter': c.petT-=dt; if(c.stT<=0){ if(weather.raining)c.stT=rand(3,6); else setState(c,'idle',1); } break;",
    "    case 'shelter': c.petT-=dt; if(c.dryT>0&&c.age>0.25&&Math.random()<dt/5){ selfLick(c,true); break; } if(c.stT<=0){ if(weather.raining)c.stT=rand(3,6); else setState(c,'idle',1); } break;")
# --- rain: groom loss while wet, then a drying-off window ---
rep("  s.groom=Math.max(0,s.groom-dt*0.04);\n",
    "  s.groom=Math.max(0,s.groom-dt*(0.04+(wet&&!c.outside?RAIN_GROOM:0)));\n"
    "  if(wet&&!c.outside){ c.wetAcc=(c.wetAcc||0)+dt; c.dryT=0; } else { if((c.wetAcc||0)>2)c.dryT=DRY_T; c.wetAcc=0; if(c.dryT>0)c.dryT-=dt; }\n")
# --- licking another cat (boop machinery, lick variant) ---
rep("function boop(a,b){",
    "const LICK_GAIN=0.15, LICKED_GAIN=0.12, LICKED_KIT=0.2, RAIN_GROOM=0.08, DRY_T=20;\n"
    "function selfLick(c,short){ setState(c,'groom',short?rand(2.5,4):rand(3.5,6)); c.groomKind=pick(['paw','paw','paw','paw','flank','behind']); }\n"
    "function lickable(o){ return o&&!o.carried&&o.away<=0&&!o.outside&&!o.leaving&&o.age>0.05&&['idle','groom','watch','sleep'].includes(o.state)&&!(o.petT>0); }\n"
    "function kidsOf(c){ return W.cats.filter(k=>k.age<1&&k.parents&&k.parents.includes(c.id)&&lickable(k)); }\n"
    "// a parent licks its kitten (any stats); a loving cat licks a bonded friend's head\n"
    "function lickSocial(c){ if(tutQuiet()||c.age<1||(c.lickCD||0)>W.time)return false; const p=c.g.position;\n"
    "  if(Math.random()<0.16){ const k=pick(kidsOf(c)); if(k){ c.lickCD=W.time+rand(25,45); goNear(c,k,k.age<0.5?0.7:0.9,{o:k,part:Math.random()<0.5?'head':'body'}); return true; } }\n"
    "  if(c.s.aff>50&&Math.random()<0.06){ const o=active().filter(o=>o!==c&&o.age>=0.25&&getBond(c,o)>=40&&lickable(o)&&dist2(o.g.position,p)<9).sort((a,b)=>getBond(c,b)-getBond(c,a))[0]; if(o){ c.lickCD=W.time+rand(60,100); goNear(c,o,1.1,{o,part:'head'}); return true; } }\n"
    "  return false; }\n"
    "function goNear(c,o,d,data){ const op=o.g.position, p=c.g.position, dx=p.x-op.x, dz=p.z-op.z, n=Math.hypot(dx,dz)||1; goTo(c,op.x+dx/n*d,op.z+dz/n*d,'lick',data); }\n"
    "function lickStart(a,b,part){ if(!lickable(b)||dist2(a.g.position,b.g.position)>2.2)return false; const dur=rand(3.5,5);\n"
    "  for(const c of [a,b]){ setState(c,'boop',dur); c.boopP=c===a?b:a; c.boopKind='lick'; c.licker=c===a; c.lickPart=c===a?part:null; c.lickBody=c===b&&part==='body'; }\n"
    "  a.boopCD=b.boopCD=rand(30,50); if(b.age<1&&b.parents&&b.parents.includes(a.id))spawnFx('h',b.g.position.clone().setY(0.7*b.g.scale.y+0.4),1,.1); return true; }\n"
    "function boop(a,b){")
rep("  const a=c.after, it=c.afterData; c.after=null; c.run=false;\n",
    "  const a=c.after, it=c.afterData; c.after=null; c.run=false;\n"
    "  if(a==='lick'){ if(it&&lickStart(c,it.o,it.part))return; setState(c,'idle',rand(1.5,3)); return; }\n")
# boop state: a licked cat slowly gets groomed; a body-lick target doesn't turn to face; body-lick distance is shorter
rep(" want=(c.boopKind==='lick'?1.32:1.56)*(c.g.scale.x+o.g.scale.x)/2;",
    " want=c.licker&&c.lickPart==='body'?0.62*c.g.scale.x+0.22*o.g.scale.x:c.licker&&o.age<1?0.6*c.g.scale.x+0.55*o.g.scale.x:(c.boopKind==='lick'?1.32:1.56)*(c.g.scale.x+o.g.scale.x)/2;\n"
    "      if(o.licker&&c.boopKind==='lick')s.groom=Math.min(100,s.groom+dt*(c.age<1?LICKED_KIT:LICKED_GAIN));")
rep("      c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); if(c.landTo||o.landTo){",
    "      if(!c.lickBody)c.heading=angLerp(c.heading,Math.atan2(op.x-p.x,op.z-p.z),dt*6); if(c.landTo||o.landTo){")
rep("if(c.licker){ hx=0.15+Math.sin(t*9)*0.18; hz=Math.sin(t*4.5)*0.2; eye=0.5; }",
    "if(c.licker){ hx=(c.lickPart==='body'?0.5:c.boopP&&c.boopP.age<1?0.35:0.15)+Math.sin(t*9)*0.18; hz=Math.sin(t*4.5)*0.2; eye=0.5; }")
# help note
rep("<li>A rain roof keeps cats dry in showers.</li>",
    "<li>A rain roof keeps cats dry in showers. Cats left out in the rain get a little scruffy.</li>")
open(P, 'w', encoding='utf-8').write(s)
print('v157 applied')
