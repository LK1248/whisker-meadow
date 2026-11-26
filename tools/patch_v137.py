"""v137: the flea lesson shows what to do, like the brush lesson does.
- Brush not selected: the brush button glows and a ghost hand taps it. Trying to touch the cat with the hand
  shakes the brush button.
- Brush selected (also when it was already selected when the lesson started): the ghost hand brushes back and
  forth over the cat, so the player isn't left waiting to select the brush again."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function endTip(){ if(!tips.cur)return; if(tips.cur.tap){ $('#ghost').hidden=true; $('#ghost').classList.remove('tap'); }",
    "function endTip(){ if(!tips.cur)return; if(tips.cur.tap||tips.cur.kind==='flea'){ const gh=$('#ghost'); gh.hidden=true; gh.classList.remove('tap'); gh.style.opacity=''; } if(tips.cur.kind==='flea')$('[data-tool=brush]').classList.remove('tutGlow','nudge');")
rep("  if(T.kind==='flea'){ if(['walk','run','trot','zoom'].includes(c.state))setState(c,'idle'); if(c.state==='idle')c.stT=Math.max(c.stT||0,2); }\n",
    """  if(T.kind==='flea'){ if(['walk','run','trot','zoom'].includes(c.state))setState(c,'idle'); if(c.state==='idle')c.stT=Math.max(c.stT||0,2);
    const gh=$('#ghost'), bb=$('[data-tool=brush]'), on=W.tool==='brush'; if(gh.hidden){ gh.innerHTML=`<svg viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`; gh.hidden=false; }
    bb.classList.toggle('tutGlow',!on);
    if(!on&&P.down&&P.lockPan&&W.time>(T.nudgeT||0)){ T.nudgeT=W.time+1.5; bb.classList.remove('nudge'); void bb.offsetWidth; bb.classList.add('nudge'); }
    if(!on){ const t=elC('[data-tool=brush]'); gh.classList.add('tap'); gh.style.opacity=''; tapGesture(tips.t,t.x,t.y); }
    else { gh.classList.remove('tap'); const b=toScreen(bodyOf(c)); if(b.ok){ const sx=Math.sin(tips.t*7)*38; gh.style.opacity=P.mode&&P.mode!=='none'?0:0.9; gh.style.transform=`translate(${b.x-30+sx}px,${b.y-40}px) rotate(${sx*0.3}deg)`; } } }
""")
open(P, 'w', encoding='utf-8').write(s)
print('v137 applied')
