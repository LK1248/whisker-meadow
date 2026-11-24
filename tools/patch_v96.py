"""v96: the 'Wand pounces' goal (and the wand lesson) count only pounces at the wand. Cats leaping at birds and
butterflies on their own used to count too, paying the wand goal out when the wand was never used."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("c.reach=0.6; c.pounceT=1.2; reward(c,8); }", "c.reach=0.6; c.pounceT=1.2; reward(c,8,true); }")
rep("c.lunge=0.5; c.pounceT=1.1; reward(c,9); }", "c.lunge=0.5; c.pounceT=1.1; reward(c,9,true); }")
rep("function reward(c,f){", "function reward(c,f,atWand){ if(atWand)W.stat.wandPounces=(W.stat.wandPounces||0)+1;")
rep("['Wand pounces',()=>W.stat.pounces,10]", "['Wand pounces',()=>W.stat.wandPounces||0,10]")
rep("done:()=>W.stat.pounces>=3},", "done:()=>(W.stat.wandPounces||0)>=3},")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("const [n,f,tg]=GOALS[g.i]; if(f()-g.base>=tg){", "const [n,f,tg]=GOALS[g.i]; if(g.base>f())g.base=f(); /* a counter that was redefined (old saves) */ if(f()-g.base>=tg){")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
