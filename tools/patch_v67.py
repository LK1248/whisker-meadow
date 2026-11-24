"""v67: helper shop tutorial. Shows (once affordable) when there are more than 8 cats, or when for over a minute
more than 2 cats stay hungry or more than 1 cat has fleas. Same pattern as the other shop hints: tap Shop, then the
hand points at Helper."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(why==='roof')return 'shelter';", "if(why==='helper')return 'helper'; if(why==='roof')return 'shelter';")
rep("  {id:'space',",
    "  {id:'helper',when:()=>!helpers.length&&(W.cats.length>8||(W.needT||0)>60)&&shopCan(SHOP.find(x=>x.id==='helper')),el:'#bShop',g:'tap',label:()=>hIco(IC.helper),done:()=>helpers.length>0},\n  {id:'space',")
rep("function updateHints(dt){ ",
    "function needTick(dt){ const cs=active(), hungry=cs.filter(c=>c.s.full<30).length, fleas=cs.filter(c=>c.fleas).length; W.needT=hungry>2||fleas>1?(W.needT||0)+dt:Math.max(0,(W.needT||0)-dt*0.5); }\n"
    "function updateHints(dt){ needTick(dt); ")
open(P, 'w', encoding='utf-8').write(s); print('ok')
