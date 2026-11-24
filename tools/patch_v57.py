"""v57: the brush lesson points at the brush; rain leads to the roof in the shop.
- After a short look at the scruffy cat, the spotlight moves to the brush button, which pulses with a gold glow
  until it's picked (the ghost hand keeps tapping it). Switching back to the hand brings the spotlight and glow back.
- Petting the cat with the hand during the lesson gives the brush button a little shake.
- Snapshots wait until the whole tutorial is over (brush lesson done + 30 s); before, one could fire in the gap
  between lessons once the 8-minute quiet window ran out.
- Rain: the roof hint wins over the general shop hint; the shop points at the roof whenever it's raining with no roof,
  and after buying something else (kibble) the pointer moves on to the roof."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("body.intro.tools .dock{opacity:1;pointer-events:auto;z-index:7}",
    "body.intro.tools .dock{opacity:1;pointer-events:auto;z-index:7}\n"
    ".tool.tutGlow{animation:tutGlow 1.1s ease-in-out infinite;background:#fff6d6}\n"
    "@keyframes tutGlow{0%,100%{box-shadow:0 0 0 0 rgba(246,196,67,.95);transform:scale(1)}50%{box-shadow:0 0 0 12px rgba(246,196,67,0);transform:scale(1.14)}}\n"
    ".tool.nudge{animation:nudge .45s ease-in-out}\n"
    "@keyframes nudge{0%,100%{transform:rotate(0)}20%{transform:rotate(-14deg) scale(1.15)}45%{transform:rotate(12deg) scale(1.15)}70%{transform:rotate(-6deg)}}")
# spotlight: cat first, then the brush button while the brush isn't picked
rep("  const io=$('#intro'); io.style.setProperty('--x',b.x+'px'); io.style.setProperty('--y',b.y+'px'); io.style.setProperty('--r','120px');\n  const gh=$('#ghost');\n  if(br.stage==='tool'){",
    "  const io=$('#intro'), bb=$('[data-tool=brush]'), onTool=br.stage==='tool'&&br.t>1.6;\n"
    "  if(onTool){ const t=elC('[data-tool=brush]'); io.style.setProperty('--x',t.x+'px'); io.style.setProperty('--y',t.y+'px'); io.style.setProperty('--r','58px'); }\n"
    "  else { io.style.setProperty('--x',b.x+'px'); io.style.setProperty('--y',b.y+'px'); io.style.setProperty('--r','120px'); }\n"
    "  bb.classList.toggle('tutGlow',br.stage==='tool');\n"
    "  // petting instead of brushing: shake the brush button and point back at it\n"
    "  if(br.stage==='tool'&&(P.mode==='stroke'||P.mode==='catPending')&&W.time>(br.nudgeT||0)){ br.nudgeT=W.time+1.5; br.t=Math.max(br.t,1.6); bb.classList.remove('nudge'); void bb.offsetWidth; bb.classList.add('nudge'); }\n"
    "  const gh=$('#ghost');\n  if(br.stage==='tool'){")
rep("function endBrushTut(ok){ const c=br.c; if(!c)return; br.c=null; br.done=true; W.stat.brushTut=1;",
    "function endBrushTut(ok){ const c=br.c; if(!c)return; br.c=null; br.done=true; W.stat.brushTut=1; W.stat.brushTutT=W.time; $('[data-tool=brush]').classList.remove('tutGlow','nudge');")
rep("function snapOk(){ return W.started&&!W.paused&&", "function snapOk(){ return W.started&&!W.paused&&W.stat.brushTut&&W.time>(W.stat.brushTutT||0)+30&&")
# ---------- rain: the shop leads to the roof ----------
# the general shop hint steps aside while it rains with no roof, so the roof hint shows instead
rep("{id:'shop',when:()=>W.time>80&&W.money>=12,", "{id:'shop',when:()=>W.time>80&&W.money>=12&&!(weather.raining&&!countItems('shelter')),")
# opening the shop in the rain with no roof points at the roof; after a purchase the pointer moves on to the roof instead of disappearing
rep("function openShop(guide){\n", "function rainGuide(){ return weather.raining&&!countItems('shelter')?'shelter':null; }\nfunction openShop(guide){ guide=guide||rainGuide();\n")
rep("const it=SHOP.find(x=>x.id===b.dataset.buy); const cost=it.cost(); if(W.money<cost)return; W.money-=cost; it.buy(); W.stat.buys++; Snd.coin(); hud(); if($('#modal').hidden)return; openShop(); });",
    "const it=SHOP.find(x=>x.id===b.dataset.buy); const cost=it.cost(); if(W.money<cost)return; W.money-=cost; it.buy(); W.stat.buys++; Snd.coin(); hud(); if($('#modal').hidden)return; openShop(it.id===guide?null:guide); });")
rep("window.__wm={Snd,", "window.__wm={Snd,endBrushTut,openShop,weather,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
