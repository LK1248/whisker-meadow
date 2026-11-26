"""v164: when the shop lesson points at food, either food will do.
The lesson used to allow only Kibble. Now Kibble and Premium food both glow and both can be bought; buying either
one finishes the lesson. The pointing hand stays on Kibble (the cheaper one)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function shopOk(id){ const g=shopForce(); return !g||id===g; }",
    "const FOODS=['food','premium']; const sameGuide=(a,b)=>a===b||(FOODS.includes(a)&&FOODS.includes(b)); // either food answers a food lesson\n"
    "function shopOk(id){ const g=shopForce(); return !g||sameGuide(id,g); }")
rep("    const gd=it.id===guide;\n    return `<div class=\"item${gd?' guide':''}\"",
    "    const gd=it.id===guide, gd2=!gd&&!!guide&&sameGuide(it.id,guide)&&can;\n    return `<div class=\"item${gd||gd2?' guide':''}\"")
rep("openShop(it.id===guide?null:guide); });", "openShop(sameGuide(it.id,guide)?null:guide); });")
open(P, 'w', encoding='utf-8').write(s)
print('v164 applied')
