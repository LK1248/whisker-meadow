"""v45: the cat fair hint first points at the Pet tool when another tool (wand, laser, brush) is selected,
because tapping a cat with the wand doesn't open the fair. The step repeats until the first fair."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("""  {id:'show',when:()=>W.cats.some(showReady),""",
"""  {id:'show0',when:()=>W.tool!=='hand'&&!W.stat.shows&&W.cats.some(showReady),el:'[data-tool=hand]',g:'tap',label:'Pet',done:()=>W.tool==='hand',redo:true},
  {id:'show',when:()=>W.tool==='hand'&&W.cats.some(showReady),""")
rep("    if(h.done&&h.done()){ hintDone.add(h.id); hideHint(); return; }",
    "    if(h.done&&h.done()){ if(!h.redo)hintDone.add(h.id); hideHint(); return; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
