"""v82:
A) Pairing lesson: the hint hand presses on the first cat and stays there while a pink hold ring fills (1.5 s), then
   glides to the second cat. Same look as the real hold ring.
B) Carried cats hang by the scruff: body near vertical, legs and tail dangling, swinging gently like a pendulum.
   Held too long (tolerance grows with love): slow squirm -> pause -> violent struggle -> low-love cats scratch
   (screen claw marks) and jump down, others just wriggle free and walk off."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- A) ghost hold ring ----
rep("gh.classList.remove('tap'); $('#pips').innerHTML=PAIR_EQ;",
    "gh.classList.remove('tap'); gh.insertAdjacentHTML('beforeend','<div class=\"gRing\"></div>'); $('#pips').innerHTML=PAIR_EQ;")
rep("""      const cyc=pl.t%3.4; let x=sa.x,y=sa.y,sc=1;
      if(cyc<1.0){ sc=1-0.12*Math.min(1,cyc/0.3); }
      else if(cyc<2.4){ const k=(cyc-1.0)/1.4, e=k*k*(3-2*k); x=sa.x+(sb.x-sa.x)*e; y=sa.y+(sb.y-sa.y)*e-Math.sin(e*Math.PI)*50; sc=0.88; }""",
"""      const cyc=pl.t%4.6; let x=sa.x,y=sa.y,sc=1; const gr=gh.querySelector('.gRing');
      if(gr){ const rp=cyc<0.3?0:cyc<1.8?(cyc-0.3)/1.5:cyc<3.4?1:0; gr.style.setProperty('--p',rp.toFixed(3)); gr.style.opacity=cyc<0.3||cyc>=3.4?0:1; }
      if(cyc<2.0){ sc=1-0.12*Math.min(1,cyc/0.3); }
      else if(cyc<3.4){ const k=(cyc-2.0)/1.4, e=k*k*(3-2*k); x=sa.x+(sb.x-sa.x)*e; y=sa.y+(sb.y-sa.y)*e-Math.sin(e*Math.PI)*50; sc=0.88; }""")
rep("gh.style.opacity=cyc>2.8?Math.max(0,1-(cyc-2.8)/0.6)*0.9:0.9;", "gh.style.opacity=cyc>4.0?Math.max(0,1-(cyc-4.0)/0.6)*0.9:0.9;")
rep("</style>", "#ghost .gRing{position:absolute;left:30px;top:40px;width:58px;height:58px;margin:-29px 0 0 -29px;border-radius:50%;--p:0;"
    "background:conic-gradient(var(--pink) calc(var(--p)*1turn),rgba(255,255,255,.6) 0);-webkit-mask:radial-gradient(circle,transparent 21px,#000 22px);mask:radial-gradient(circle,transparent 21px,#000 22px);transition:opacity .2s}\n</style>")

# ---- B) scruff hang + staged squirm ----
rep("c.tol=c.s.trust>=70?9999:3+c.s.trust*0.12;", "c.tol=c.s.aff>=75?9999:4+c.s.aff*0.12; /* love sets how long a cat puts up with being held */")
rep("""    if(k<0.35){ rx=kit?-0.75:-0.5; hx=kit?0.5:0.32; legA=[0.6,0.65,0.55+(kit?0.3:0),0.6+(kit?0.3:0)].map((v,i)=>v+Math.sin(t*1.8+i)*0.07); tailUp=-1.45; swish=0.04; eye=c.s.trust>=60?0.45:0.85; }
    else { const a=Math.min(1,(k-0.35)*2.5); rx=-0.25*(1-a); legA=[-0.6*a,-0.6*a,0.7*a,0.7*a]; earOut=a; tailUp=-0.6; swish=0.25+k*0.4; swSpd=6; }
    if(k>0.6){ const a=(k-0.6)*2.2; rz=Math.sin(t*22)*0.25*a; rx+=Math.sin(t*17)*0.2*a; legA=[Math.sin(t*20)*a,Math.cos(t*19)*a,Math.sin(t*21)*a,Math.cos(t*18)*a]; } }""",
"""    // held by the scruff: near vertical, limp, swinging like a pendulum
    const sw=Math.sin(t*1.7+c.id), sw2=Math.sin(t*1.3+c.id*2);
    rx=(kit?-1.25:-1.15)+sw2*0.07; rz=sw*0.13; hx=0.55; hz=sw*0.1; legA=[1.05,1.1,1.2,1.25].map((v,i)=>v+Math.sin(t*1.7+c.id-i*0.5)*0.12); tailUp=-1.5; swish=0.05; swSpd=1.7;
    eye=c.s.aff>=60?0.45:0.85; earOut=c.s.aff<40?0.35:0;
    if(k>=0.4&&k<0.55){ const a=Math.sin((k-0.4)/0.15*Math.PI); legA=legA.map((v,i)=>v-0.5*a*(0.5+0.5*Math.sin(t*4.5+i*1.6))); rz+=Math.sin(t*3.2)*0.12*a; tailUp=-1.1; swish=0.3*a; swSpd=4; earOut=Math.max(earOut,0.4*a); }
    else if(k>=0.55&&k<0.68){ earOut=Math.max(earOut,0.5); hz+=Math.sin(t*0.9)*0.15; } // a tense pause
    else if(k>=0.68){ const a=Math.min(1,(k-0.68)*3.2); rx+=0.5*a; rz=Math.sin(t*22)*0.3*a+sw*0.13*(1-a); legA=[Math.sin(t*20),Math.cos(t*19),Math.sin(t*21),Math.cos(t*18)].map((v,i)=>legA[i]*(1-a)+v*1.1*a); earOut=1; tailUp=-0.4; swish=0.5; swSpd=9; } }""")
rep("if(c.holdT>=c.tol)hopFree(c); return; }",
    "if(c.holdT>=c.tol){ if(c.s.aff<35){ c.bat=0.5; c.snap=0.3; Snd.meow(0.8,0.9); scratchFx(); c.s.trust=Math.max(0,c.s.trust-4); } hopFree(c); } return; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("carryHands[0].position.copy(c.core.localToWorld(new V3(0,-0.36,0.24))); carryHands[1].position.copy(c.core.localToWorld(new V3(0,-0.33,-0.4))); carryHands.forEach(hm=>{hm.visible=true; hm.rotation.y=c.heading;}); }",
    "carryHands[0].position.copy(c.core.localToWorld(new V3(0,0.3,0.3))); carryHands[0].visible=true; carryHands[0].rotation.set(0,c.heading,0); carryHands[1].visible=false; }")
rep("window.__wm={Snd,", "window.__wm={Snd,startCarry,")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
