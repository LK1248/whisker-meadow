"""v84: shop tutorials are forced, like the lessons. While a shop hint (first purchase, helper, roof in the rain,
more space) is up and its item is affordable: only the Shop button works, the shop can't be closed, and only the
guided item can be bought. Buying it ends the lesson. If the item isn't affordable, the hint stays a gentle hint."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function tutLock(){", "const SHOP_FORCE=new Set(['shop','helper','roof','space']);\n"
    "function shopForce(){ if(!curHint||!SHOP_FORCE.has(curHint.id)||!W.started)return null; const g=guidePick(curHint.id), it=SHOP.find(x=>x.id===g); return it&&shopCan(it)?g:null; }\n"
    "function shopOk(id){ const g=shopForce(); return !g||id===g; }\n"
    "function userClose(){ if(shopForce()&&document.querySelector('#mbox [data-buy]'))return; closeModal(); }\n"
    "function tutLock(){")
rep("  if(firstAdopt())return {cats:W.pickHome?W.cats.filter(readyHome):[],tools:[],fam:true};",
    "  if(firstAdopt())return {cats:W.pickHome?W.cats.filter(readyHome):[],tools:[],fam:true};\n  { const g=shopForce(); if(g)return {cats:[],tools:[],shop:g}; }")
rep("b.classList.toggle('faLock',!!(L&&L.fam));", "b.classList.toggle('faLock',!!(L&&L.fam)); b.classList.toggle('shopLock',!!(L&&L.shop));")
rep("body.faLock #fX,", "body.shopLock #bShop{pointer-events:auto;opacity:1;filter:none}body.shopLock #mbox .x{display:none}body.faLock #fX,")
# shop buttons respect the forced item
rep("const hn=it.homes?it.homes():0, hOk=W.homes.length>=hn; const can=shopCan(it);", "const hn=it.homes?it.homes():0, hOk=W.homes.length>=hn; const can=shopCan(it)&&shopOk(it.id);")
rep("can=sOk&&W.money>=cost;\n", "can=sOk&&W.money>=cost&&!shopForce();\n")
rep("can=shopCan(it); } else can=upCan(b.dataset.up);", "can=shopCan(it)&&shopOk(it.id); } else can=upCan(b.dataset.up)&&!shopForce();")
# no closing the shop mid-lesson (x, backdrop, Escape)
rep("$('#modal').addEventListener('pointerdown',e=>{ if(e.target.id==='modal')closeModal(); });", "$('#modal').addEventListener('pointerdown',e=>{ if(e.target.id==='modal')userClose(); });")
rep("if(e.key==='Escape')closeModal(); });", "if(e.key==='Escape')userClose(); });")
rep("const x=$('#mbox .x'); if(x)x.onclick=closeModal; }", "const x=$('#mbox .x'); if(x)x.onclick=userClose; }")
# keyboard tool shortcuts obey lessons too
rep("const k={'1':'hand','2':'brush','3':'wand','4':'laser'}[e.key]; if(k)setTool(k);",
    "const k={'1':'hand','2':'brush','3':'wand','4':'laser'}[e.key]; if(k){ const L=tutLock(); if(!L||k===W.tool||L.tools.includes(k))setTool(k); }")
# forced hints don't time out
rep("if(hintT>22){", "if(hintT>22&&!shopForce()){")
rep("window.__wm={Snd,", "window.__wm={Snd,shopForce,getHint:()=>curHint,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
