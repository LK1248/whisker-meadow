"""v189: the language flag sits inside the title card (top left corner), not in the screen corner."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("b.innerHTML=FLAGS[LANG]; st.appendChild(b);", "b.innerHTML=FLAGS[LANG]; st.querySelector('.card').appendChild(b);")
rep("#bLang{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));left:calc(10px + env(safe-area-inset-left,0px));padding:0;display:grid;place-items:center}",
    "#start .card{position:relative}#bLang{position:absolute;top:14px;left:14px;width:42px;height:42px;min-height:0;padding:0;display:grid;place-items:center;background:#fff;box-shadow:0 2px 0 rgba(74,52,38,.1)}")
open(P, 'w', encoding='utf-8').write(s)
print('v189 applied')
