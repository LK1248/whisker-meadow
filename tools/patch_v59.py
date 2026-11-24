"""v59: every cat has its own petting tempo; families and runaways wait like strays.
Petting tempo
- Each cat has a favourite stroking speed: some like long slow strokes, some quick ones (shy cats slower, playful
  cats quicker, kittens a bit quicker). It comes from the cat's existing (saved) pace value, so old saves keep
  their cats' personalities.
- Love widens how forgiving a cat is: a new cat only purrs for strokes close to its tempo, a cat that loves you
  enjoys almost anything gentle. The cat in the first lesson is extra forgiving.
- In tempo: full progress, purrs and hearts. A little slow: half progress, no harm. Too quick: slower progress,
  the cat gets fidgety, hourglass. Much too quick: the old frantic response.
How it's shown (wordless)
- A small metronome gauge floats above the hand while petting. The green band is the cat's sweet spot (its width
  is the love tolerance, so it visibly grows as the cat warms up). The needle is your stroke speed: left slow,
  right fast, and it glows green in the band.
- The cat's tail swishes in its tempo while it's being petted: a diegetic metronome to follow.
- The cat tag has a tiny metronome that ticks at that cat's tempo, so you can read it before you start.
Flea scratching
- The hind paw comes up to the ear, the head tilts down into it and the body leans; the kicks speed up, then
  the paw freezes for a beat and the cat finishes with an ear twitch and a tail flick (2.4-3.2 s instead of 1.4-2.2).
Holds
- Families and runaways now wait under the same rules as strays: tutorial done (or 15 min), 40 s after the
  brush lesson, and not while follow-up guidance is on screen."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- holds ----------
rep("if(!tutQuiet()&&!W.runaway&&!W.family&&W.time>120&&", "if(!tutQuiet()&&!strayHold()&&!W.runaway&&!W.family&&W.time>120&&")
rep("if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()){", "if(W.cats.some(readyHome)&&!W.runaway&&(W.night||0)<0.55&&!tutQuiet()&&!strayHold()){")

# ---------- CSS + DOM ----------
rep("#hand{position:fixed;", "#tempo{position:fixed;left:0;top:0;width:78px;height:46px;margin:-23px 0 0 -39px;pointer-events:none;z-index:9;transition:opacity .3s;filter:drop-shadow(0 2px 3px rgba(74,52,38,.35))}\n"
    "#tempo .bg{fill:none;stroke:rgba(255,248,236,.92);stroke-width:12;stroke-linecap:round}#tempo .band{fill:none;stroke:#8fd17d;stroke-width:8;stroke-linecap:round}\n"
    "#tempo .ndl{stroke:#4a3426;stroke-width:4.5;stroke-linecap:round}#tempo.on .ndl{stroke:#3f9b46}#tempo.fast .ndl{stroke:#e8743b}#tempo .hub{fill:#4a3426}\n"
    ".metro{display:inline-block;width:14px;height:16px;margin-left:5px;vertical-align:-2px}.metro .arm{transform-origin:7px 14px;animation:metro 1s ease-in-out infinite alternate}\n"
    "@keyframes metro{from{transform:rotate(-26deg)}to{transform:rotate(26deg)}}\n#hand{position:fixed;")
rep("<div id=\"hand\" hidden>", "<div id=\"tempo\" hidden><svg viewBox=\"0 0 100 60\"><path class=\"bg\" d=\"\"/><path class=\"band\" d=\"\"/><line class=\"ndl\" x1=\"50\" y1=\"53\" x2=\"50\" y2=\"18\"/><circle class=\"hub\" cx=\"50\" cy=\"53\" r=\"5.5\"/></svg></div><div id=\"hand\" hidden>")

# ---------- tempo model ----------
rep("// ---- continuous petting ----",
r"""// ---- petting tempo: every cat has a favourite stroking speed; love widens how forgiving it is ----
function tempoOf(c){ if(c.tempo==null){ let m=0.22+clamp((3.3-(c.pace||2.8))/0.9,0,1)*0.38; if(c.trait==='shy')m*=0.8; else if(c.trait==='playful')m*=1.25; if(c.age<1)m*=1.15; c.tempo=m; } return c.tempo; }
function strokeT(c){ return 0.38/tempoOf(c); } // seconds for one gentle stroke at this cat's tempo
function tempoTol(c){ return (0.3+0.7*c.s.aff/100)*(c.trait==='shy'?0.85:1)+(intro.c===c?0.35:0); } // in log-speed units
const TG={x:0,shown:0}, TG_A=72, tgPt=(a,r)=>{ const t=a*Math.PI/180; return (50+r*Math.sin(t)).toFixed(1)+' '+(53-r*Math.cos(t)).toFixed(1); };
const tgArc=(a0,a1,r=38)=>`M${tgPt(a0,r)} A${r} ${r} 0 0 1 ${tgPt(a1,r)}`;
document.querySelector('#tempo .bg').setAttribute('d',tgArc(-TG_A,TG_A));
function updateTempo(dt){ const el=$('#tempo'), c=S.cat, on=W.started&&!W.paused&&W.tool==='hand'&&P.mode==='stroke'&&c&&!c.carried&&$('#modal').hidden;
  if(on){ TG.shown=0.8; TG.c=c; } else TG.shown-=dt; if(TG.shown<=0||!TG.c){ el.hidden=true; return; }
  const k=TG.c, vP=2.5*Math.max(60,Math.min(400,catScreenH(k)))*tempoOf(k), x=Math.log(Math.max(1,S.v==null?vP:S.v)/vP), tol=tempoTol(k);
  TG.x=lerp(TG.x,on?x:-2.4,Math.min(1,dt*7)); const a=clamp(TG.x/2.4,-1,1)*TG_A, b=clamp(tol/2.4,0.08,1)*TG_A;
  el.hidden=false; el.style.opacity=on?1:Math.max(0,TG.shown/0.8); el.style.transform=`translate(${P.hx}px,${P.hy-(P.type==='mouse'?96:146)}px)`;
  const band=el.querySelector('.band'), d=tgArc(-b,b); if(band.getAttribute('d')!==d)band.setAttribute('d',d);
  el.querySelector('.ndl').setAttribute('transform',`rotate(${a.toFixed(1)} 50 53)`); el.classList.toggle('on',Math.abs(TG.x)<=tol); el.classList.toggle('fast',TG.x>tol); }
const METRO=c=>`<svg class="metro" viewBox="0 0 14 16" aria-hidden="true"><path d="M3 15L5.5 2h3L11 15z" fill="#c99a6b"/><g class="arm" style="animation-duration:${strokeT(c).toFixed(2)}s"><path d="M7 14V3" stroke="#4a3426" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="6" r="1.8" fill="#ff6f99"/></g></svg>`;
// ---- continuous petting ----""")
rep("""  const D=2.5*Math.max(60,Math.min(400,catScreenH(c))), vMax=D*0.7*(c.trait==='shy'?0.87:1), v=S.v||0, now=W.time;
  let gain=0;
  if(v>vMax*4.5){ c.over+=len/D*0.9; if(now>(c.hgT||0)){ c.hgT=now+0.9; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),true); slowNag.n++; } }
  else if(v>vMax*2.2){ c.over+=len/D*0.2; if(now>(c.hgT||0)){ c.hgT=now+1.1; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),false); slowNag.n++; } }
  else gain=len/D*Math.min(1,vMax/Math.max(1,v));""",
"""  const D=2.5*Math.max(60,Math.min(400,catScreenH(c))), vP=D*tempoOf(c), v=S.v==null?vP:S.v, now=W.time, tol=tempoTol(c), x=Math.log(Math.max(1,v)/vP);
  let gain=0;
  if(x>tol+1.3){ c.over+=len/D*0.9; if(now>(c.hgT||0)){ c.hgT=now+0.9; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),true); slowNag.n++; } }
  else if(x>tol){ c.over+=len/D*0.15*(x-tol+0.3); gain=len/D*0.35; if(now>(c.hgT||0)){ c.hgT=now+1.3; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),false); slowNag.n++; } }
  else if(x<-tol)gain=len/D*0.5;
  else gain=len/D*1.1;""")
rep("updateFirstAdopt(dt); snapTick(dt);", "updateFirstAdopt(dt); snapTick(dt); updateTempo(dt);")
# the tail swishes in the cat's tempo while it's petted
rep("  if(c.flick>0){ c.flick-=dt; swish=0.5; swSpd=10; tailUp=0.9; }",
    "  if(c.state==='pet'&&c.petT>0&&!c.carried){ swish=Math.max(swish,0.3); swSpd=Math.PI/strokeT(c); }\n  if(c.flick>0){ c.flick-=dt; swish=0.5; swSpd=10; tailUp=0.9; }")
# tag: a little metronome at the cat's tempo
rep("$('#tName').innerHTML=`${c.name}${c.age<1?' <small>kitten</small>':''}`;", "$('#tName').innerHTML=`${c.name}${c.age<1?' <small>kitten</small>':''}${METRO(c)}`;")
# ---------- flea scratching: hind paw up to the ear, kicks speeding up, a sharp stop, then an ear twitch ----------
rep("if(['idle','walk'].includes(c.state)&&Math.random()<dt/9)setState(c,'itch',rand(1.4,2.2));",
    "if(['idle','walk'].includes(c.state)&&Math.random()<dt/9){ setState(c,'itch',rand(2.4,3.2)); c.itchDur=c.stT; c.itchPh=0; }")
rep("case 'itch': if(c.stT<=0)setState(c,'idle',1); break;", "case 'itch': if(c.stT<=0){ setState(c,'idle',1); c.earTw=0.35; c.flick=0.3; } break;")
rep("else if(st==='itch'){ rx=-0.45; coreY=0.44; legA=[0.45,0.45,-2.1+Math.sin(t*34)*0.5,-1.0]; hx=0.1; hy=0.55; hz=0.5; eye=0.3; earOut=0.7; tailUp=-0.2; swish=0.3; swSpd=6; }",
    "else if(st==='itch'){ const D=c.itchDur||2, p=clamp(1-c.stT/D,0,1), hold=p>0.88; c.itchPh=(c.itchPh||0)+dt*(13+38*p*p); const amp=hold?0:0.34*(0.55+0.45*p);\n"
    "    rx=-0.45; coreY=0.44; rz=-0.2; legA=[0.45,0.45,-2.55+Math.sin(c.itchPh)*amp,-1.0]; hx=0.12; hy=0.3; hz=-0.55+(hold?0:Math.sin(c.itchPh)*0.06); eye=hold?0.7:0.2; earOut=0.85; tailUp=-0.2; swish=hold?0.04:0.3; swSpd=6; }")
rep("c.legs.forEach((L,i)=>{ L.rotation.x=lerp(L.rotation.x,legA[i],moving||c.carried?1:k); });",
    "c.legs.forEach((L,i)=>{ L.rotation.x=lerp(L.rotation.x,legA[i],moving||c.carried?1:(st==='itch'&&i===2?Math.min(1,dt*22):k)); });\n"
    "  { const L=c.legs[2], p0=L.userData.p0||(L.userData.p0=L.position.clone()), on=st==='itch'&&!c.carried, kk=Math.min(1,dt*(on?10:16));\n"
    "    L.position.set(lerp(L.position.x,p0.x+(on?0.14:0),kk),lerp(L.position.y,p0.y+(on?0.38:0),kk),lerp(L.position.z,p0.z+(on?0.5:0),kk)); L.rotation.z=lerp(L.rotation.z,on?-0.5:0,kk); }")
rep("window.__wm={Snd,", "window.__wm={Snd,tempoOf,tempoTol,strokeT,updateTempo,S,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
