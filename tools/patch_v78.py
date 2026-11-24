"""v78:
A) Agitation is gradual. Petting too fast builds agitation (c.fastM): the ring blends from green to red over the first
   stage, then the inside floods, then the cat gets irritated. Slowing down or stopping drains it 2.5x faster than it
   built up (time-based, also while the finger rests).
B) Lessons lock input. While any lesson runs (first pet, slow blink, pairing, brushing, first adoption), only the action
   the lesson asks for works: other cats, items, tools, toys, camera drag/pinch/rotate and the HUD buttons are disabled.
   - Pairing: only the first cat can be picked up; once dropped, everything is locked until the boop + romp finish.
   - Brushing: only the brush button, then only the lesson cat.
   - First adoption: the family can't be sent away; only "Pick a cat" and then a cat with a little house can be tapped."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---------- A) gradual agitation ----------
rep("c.fastM=Math.min(3.4,(c.fastM||0)+gap*(0.6+Math.min(1.5,x-tf)));",
    "c.fastM=Math.min(3.4,(c.fastM||0)+gap*(0.6+Math.min(1.5,x-tf))); c.fastT=performance.now()/1000;")
rep("else { c.fastM=Math.max(0,(c.fastM||0)-gap*1.2); gain=", "else { gain=")
rep("{ if(!(P.mode==='stroke'&&S.cat===c))c.fastM=Math.max(0,(c.fastM||0)-0.02);",
    "{ const tn=performance.now()/1000, bdt=Math.min(0.1,tn-(el.bT||tn)); el.bT=tn; if(tn-(c.fastT||0)>0.15)c.fastM=Math.max(0,(c.fastM||0)-bdt*AGI_CALM);")
rep("const hot=st==='fast'&&(c.fastM||0)>0.8; fg.style.stroke=p>=1||st==='on'||(st==='fast'&&!hot)?'#5fb35a':hot?'#e2574c':'#f0a13a';",
    "const ag=clamp((c.fastM||0)/0.8,0,1), hot=(c.fastM||0)>0.8; fg.style.stroke=mixHex(p>=1||st==='on'||st==='fast'||ag>0?'#5fb35a':'#f0a13a','#e2574c',ag);")
rep("function rimPts(", "const AGI_CALM=2.75; // agitation drains ~2.5x faster than typical build-up (~1.1/s)\n"
    "function mixHex(a,b,k){ const A=parseInt(a.slice(1),16), B=parseInt(b.slice(1),16), ch=sh=>Math.round(((A>>sh)&255)*(1-k)+((B>>sh)&255)*k); return `rgb(${ch(16)},${ch(8)},${ch(0)})`; }\n"
    "function rimPts(")

# ---------- B) lesson input lock ----------
rep("function lessonOn(){", """// what the running lesson allows: null = no lesson. cats: tappable/pettable cats; tools: dock tools that may be chosen
function tutLock(){
  if(intro.c)return {cats:[intro.c],tools:[]};
  if(bt.c)return {cats:[bt.c],tools:[]};
  if(pl.a)return {cats:pl.stage==='carry'?[pl.a]:[],tools:[]};
  if(br.c)return {cats:W.tool==='brush'?[br.c]:[],tools:['brush']};
  if(firstAdopt())return {cats:W.pickHome?W.cats.filter(readyHome):[],tools:[],fam:true};
  return null; }
function tutLockTick(){ const L=tutLock(), b=document.body; b.classList.toggle('tutLock',!!L); b.classList.toggle('faLock',!!(L&&L.fam));
  document.querySelectorAll('.tool').forEach(t=>t.classList.toggle('tutOk',!!(L&&L.tools.includes(t.dataset.tool)))); }
function lessonOn(){""")
rep("function updateHints(dt){ needTick(dt);", "function updateHints(dt){ tutLockTick(); needTick(dt);")
rep("  if(P.pointers.size===2){ if(P.mode==='carry')dropCat(P.cat);",
    "  if(P.pointers.size===2&&tutLock()){ P.mode='none'; return; }\n  if(P.pointers.size===2){ if(P.mode==='carry')dropCat(P.cat);")
rep("  if(e.button===2){ P.mode='rotate'; return; }",
    "  if(e.button===2){ P.mode=tutLock()?'none':'rotate'; return; }")
rep("  if(pl.a&&pl.stage==='carry'&&hit&&hit.cat!==pl.a)hit=null;",
    "  if(pl.a&&pl.stage==='carry'&&hit&&hit.cat!==pl.a)hit=null;\n"
    "  { const L=tutLock(); if(L){ if(hit&&(!hit.cat||!L.cats.includes(hit.cat)))hit=null; if(!hit||W.tool==='wand'||W.tool==='laser'){ P.mode='none'; handVis(); return; } } }")
rep("function setTool(t){ ", "function setTool(t){ { const L=tutLock(); if(L&&t!==W.tool&&!L.tools.includes(t))return; } ")
rep("</style>", "body.tutLock .hbtn,body.tutLock #bCats,body.tutLock .tool:not(.tutOk):not(.on){pointer-events:none;opacity:.45;filter:saturate(.4)}"
    "body.faLock #fX,body.faLock #fNo,body.faLock #fCancel{display:none}\n</style>")
rep("window.__wm={Snd,", "window.__wm={Snd,tutLock,mixHex,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("function setTool(t){ { const L=tutLock(); if(L&&t!==W.tool&&!L.tools.includes(t))return; } ", "function setTool(t){ ")
rep("document.querySelectorAll('.tool').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));",
    "document.querySelectorAll('.tool').forEach(b=>b.onclick=()=>{ const L=tutLock(), t=b.dataset.tool; if(L&&t!==W.tool&&!L.tools.includes(t))return; setTool(t); });")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
