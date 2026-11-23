"""v39b: the music button works on the title screen (moved onto the start overlay until play begins)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("#start{position:fixed;", "#start .hbtn.ontitle{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));right:calc(10px + env(safe-area-inset-right,0px))}\n#start{position:fixed;")
rep("$('#bPlay').onclick=()=>{", "const musT={b:$('#bMusic')}; musT.home=musT.b.parentElement; musT.next=musT.b.nextSibling; musT.b.classList.add('ontitle'); $('#start').appendChild(musT.b);\n$('#bPlay').onclick=()=>{")
rep("function begin(){ Snd.init();", "function begin(){ Snd.init(); if(musT.b.classList.contains('ontitle')){ musT.b.classList.remove('ontitle'); musT.home.insertBefore(musT.b,musT.next); }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
