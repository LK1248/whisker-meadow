"""v14: when a hint sends you to the shop, the shop points at the purchase that fits the moment."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep(".item{border:2px solid var(--line);", """.item.guide{border-color:#ff8fb1;animation:guideGlow 1.2s ease-in-out infinite;position:relative}
@keyframes guideGlow{0%,100%{box-shadow:0 0 0 0 rgba(255,143,177,.0)}50%{box-shadow:0 0 0 6px rgba(255,143,177,.45)}}
.item .gHand{position:absolute;right:-4px;bottom:-14px;width:44px;height:44px;pointer-events:none;opacity:.85;filter:drop-shadow(0 3px 4px rgba(0,0,0,.3));animation:gTap 1.5s ease-in-out infinite}
@keyframes gTap{0%,30%{transform:translate(0,-12px)}45%,55%{transform:translate(0,0) scale(.88)}70%,100%{transform:translate(0,-12px)}}
.item{border:2px solid var(--line);""")

# what to buy right now
rep("function openShop(){", """function guidePick(why){ const can=id=>{ const it=SHOP.find(x=>x.id===id); if(!it)return false; const av=it.avail?it.avail():true, mx=it.max?it.max():Infinity; return av&&countItems(id)<mx&&W.money>=it.cost(); };
  if(why==='roof')return 'shelter'; if(why==='space')return 'expand'; if(why==='food')return 'food'; if(why==='laser')return 'laser';
  const meals=(W.food||0)+(W.premium||0), n=active().length;
  if(weather.raining&&can('shelter'))return 'shelter';
  if(meals<Math.max(6,n*2)&&can('food'))return 'food';
  const lit=items.filter(i=>i.kind==='litter'); if(lit.length&&lit.every(i=>i.dirt>=2)&&can('litter'))return 'litter';
  if(n>countItems('bowl')*3&&can('bowl'))return 'bowl';
  if(!countItems('bed')&&can('bed'))return 'bed';
  if(can('ball'))return 'ball'; return 'food'; }
const GUIDE_LABEL={food:'Buy food',shelter:'Rain roof',litter:'Litter box',bowl:'Food bowl',bed:'Cozy bed',ball:'Buy a toy',expand:'More room',laser:'Laser'};
function openShop(guide){""")
rep("""    return `<div class="item"><div class="ico"><svg viewBox="0 0 24 24">${IC[it.id]}""", """    const gd=it.id===guide;
    return `<div class="item${gd?' guide':''}"${gd?' data-guide':''}><div class="ico"><svg viewBox="0 0 24 24">${IC[it.id]}""")
rep("""<button data-buy="${it.id}" ${can?'':'disabled'}>${lbl}</button></div>`; }).join('');""",
    """<button data-buy="${it.id}" ${can?'':'disabled'}>${lbl}</button>${gd?`<svg class="gHand" viewBox="0 0 64 64">${HAND_SVG.replace(/id="h(Scr|Aid)"/g,'')}</svg>`:''}</div>`; }).join('');""")
rep("""  openModal(`<h3>Shop</h3><div class="grid">${cards}</div>${ups?`<h3 style="margin-top:18px">Upgrades</h3><div class="grid">${ups}</div>`:''}`);""",
    """  openModal(`<h3>Shop</h3><div class="grid">${cards}</div>${ups?`<h3 style="margin-top:18px">Upgrades</h3><div class="grid">${ups}</div>`:''}`);
  const gEl=document.querySelector('[data-guide]'); if(gEl)setTimeout(()=>gEl.scrollIntoView({block:'center',behavior:'smooth'}),60);""")
# callers: the hint that is pointing at the shop decides; out-of-food and laser go straight to their item
rep("$('#bShop').onclick=()=>openShop();", "$('#bShop').onclick=()=>openShop(curHint&&curHint.el==='#bShop'?guidePick(curHint.id):null);")
rep("floatWorld(it.pos.clone().setY(.5),'No food!'); openShop(); return; }", "floatWorld(it.pos.clone().setY(.5),'No food!'); openShop('food'); return; }")
rep("if(t==='laser'&&!W.laser){ openShop(); return; }", "if(t==='laser'&&!W.laser){ openShop('laser'); return; }")
rep("g:'tap',label:'Buy a toy',done:()=>W.stat.buys>0}", "g:'tap',label:()=>GUIDE_LABEL[guidePick('shop')]||'Shop',done:()=>W.stat.buys>0}")
rep("window.__wm={animateCat,", "window.__wm={animateCat,guidePick,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
