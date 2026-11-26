"""v145: the shop can always be closed.
During a guided shop step (opened from a shop hint) the X was hidden, swipe-down and tapping outside did nothing,
and the lesson's Skip button is hidden while a window is open, so the only way out was to buy. Now the X, tap
outside and swipe work there too; closing the shop during the guided step skips that hint."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

i = s.find('shopLock #mbox .x{display:none}')
if i < 0: sys.exit('x rule not found')
j = s.rfind('}', 0, i) + 1  # start of this rule (after the previous rule)
rule = s[j:i + len('shopLock #mbox .x{display:none}')]
if '{' in rule.replace('#mbox .x{display:none}', ''): sys.exit('unexpected rule shape: ' + rule)
s = s[:j] + s[i + len('shopLock #mbox .x{display:none}'):]
rep("function userClose(){ if(shopForce()&&document.querySelector('#mbox [data-buy]'))return; closeModal(); }",
    "function userClose(){ const g=shopForce(); if(g&&curHint&&document.querySelector('#mbox [data-buy]')){ rec('skip','shop:'+g); hintDone.add(curHint.id); hideHint(); } closeModal(); }")
rep("const can=()=>!!mb.querySelector(':scope > .x')&&!(shopForce()&&mb.querySelector('[data-buy]'));",
    "const can=()=>!!mb.querySelector(':scope > .x');")
open(P, 'w', encoding='utf-8').write(s)
print('v145 applied; removed rule:', rule)
