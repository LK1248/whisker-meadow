"""v75: petting by feel.
- Fixed rate: while you stroke within the cat's band, the heart fills at a fixed rate per second of stroking, whatever
  the speed and whatever the cat. Too slow (after the first 10 min) fills at half rate; too fast fills nothing.
- Top speed +25%: fast edge ~1.46x the cat's favourite speed (was 1.17x).
- Purr you can see: the ring vibrates while the cat purrs, harder purr = bigger vibration.
- Too fast escalates: 1) purring stops, 2) the inside of the ring floods red and hourglasses show, 3) the cat gets
  irritated (overstimulation reaction). Calm strokes drain the flood again."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const FAST_CAP=0.16; // top speed: about 1.17x the cat's favourite stroke speed",
    "const FAST_CAP=0.38; // top speed: about 1.46x the cat's favourite stroke speed\nconst PET_RATE=1/1.8; // hearts per second of in-band stroking")
old_block = """  let gain=0;
  const tf=tolFast(c), fr=W.time<180?1.0:0; if(x>tf+1.3+fr){ c.over+=len/D*0.9; if(now>(c.hgT||0)){ c.hgT=now+0.9; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),true); slowNag.n++; c.strokeErr=1; metroLearn(1); } }
  else if(x>tf){ c.over+=len/D*0.15*(x-tf+0.3); gain=len/D*0.35/TEMPO_K; if(now>(c.hgT||0)){ c.hgT=now+1.3; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),false); slowNag.n++; c.strokeErr=1; metroLearn(1); } }
  else if(x<-tol&&!slowOk())gain=len/D*0.5/TEMPO_K;
  else gain=len/D*1.1/TEMPO_K;"""
new_block = """  let gain=0; const gap=Math.min(0.12,Math.max(0,performance.now()/1000-(c.pmT||0))); c.pmT=performance.now()/1000;
  const tf=tolFast(c);
  if(x>tf){ // too fast: 1) purr stops  2) ring floods + hourglass  3) irritated
    c.fastM=Math.min(3.4,(c.fastM||0)+gap*(0.6+Math.min(1.5,x-tf))); c.purr=0; c.purrBlock=now+1.5;
    if(c.fastM>0.8&&now>(c.hgT||0)){ c.hgT=now+1.1; floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),c.fastM>2.6); slowNag.n++; c.strokeErr=1; metroLearn(1); }
    if(c.fastM>2.6&&!(W.time<180&&x<tf+1.5))c.over+=gap*2.6; }
  else { c.fastM=Math.max(0,(c.fastM||0)-gap*1.2); gain=gap*PET_RATE*(x<-tol&&!slowOk()?0.5:1); }"""
rep(old_block, new_block)
rep("if(c.petT<=0){ c.purr=Math.max(0,c.purr-dt*0.6);", "if((c.purrBlock||0)>W.time)c.purr=0; if(c.petT<=0){ c.purr=Math.max(0,c.purr-dt*0.6);")
rep("if(gain>0){ c.petProg=(c.petProg||0)+gain; c.petIdle=0; c.purr=Math.max(c.purr,0.15);",
    "if(gain>0){ c.petProg=(c.petProg||0)+gain; c.petIdle=0; if(!((c.purrBlock||0)>now))c.purr=Math.max(c.purr,0.15);")
# flood layer inside the ring (under the gauge)
rep('<g class="metro"><path class="gTrk"',
    '<clipPath id="beatClip"><circle cx="22" cy="22" r="14.4"/></clipPath><rect id="beatFlood" x="7" y="36.5" width="30" height="0" fill="#ef6f63" fill-opacity=".55" clip-path="url(#beatClip)"/>'
    '<g class="metro"><path class="gTrk"')
# purr vibration + flood level, every frame
rep("const nx=st?TG.x:-1.2; el.querySelector('.gNdl').setAttribute('transform',`rotate(${m(nx).toFixed(1)} 22 25)`); }",
    "const nx=st?TG.x:-1.2; el.querySelector('.gNdl').setAttribute('transform',`rotate(${m(nx).toFixed(1)} 22 25)`); }"
    " { if(!(P.mode==='stroke'&&S.cat===c))c.fastM=Math.max(0,(c.fastM||0)-0.02); const fl=clamp(((c.fastM||0)-0.8)/1.8,0,1), fe=$('#beatFlood'); fe.setAttribute('y',(36.5-29*fl).toFixed(2)); fe.setAttribute('height',(29*fl).toFixed(2));"
    " const pr=c.purr>0.05&&!el.classList.contains('fast')?c.purr:0, a=pr?0.5+2.3*pr:0; el.querySelector('svg').style.transform=a?`translate(${rand(-a,a).toFixed(2)}px,${rand(-a,a).toFixed(2)}px)`:''; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("fg.style.stroke=p>=1||st==='on'?'#5fb35a':st==='fast'?'#e2574c':'#f0a13a';",
    "const hot=st==='fast'&&(c.fastM||0)>0.8; fg.style.stroke=p>=1||st==='on'||(st==='fast'&&!hot)?'#5fb35a':hot?'#e2574c':'#f0a13a';")
rep("el.classList.toggle('fast',st==='fast');", "el.classList.toggle('fast',hot);")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
s = open(P, encoding='utf-8').read()
rep("window.__wm={Snd,", "window.__wm={Snd,catScreenH,")
open(P, 'w', encoding='utf-8').write(s); print('ok3')
