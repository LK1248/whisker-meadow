"""v113: the butt-tap ring cat wears the tapped cat's coat colours. It pops its rump up twice as before, then keeps the
rump and tail raised with a very slow quiver for as long as the taps keep coming. After 1s with no tap it lowers and
the moment ends."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
# a tap starts a new moment only if the last one has ended
rep("tagFor(c,3); c.buttAnimT=W.time; c.petProg=0;",
    "tagFor(c,3); if(!(W.time<buttEnd(c)))c.buttStart=W.time; c.buttAnimT=W.time; c.petProg=0;")
rep("function buttTap(c){",
    "function buttEnd(c){ return c.buttStart==null?-99:Math.max((c.buttAnimT??-99)+1,c.buttStart+2.2); }\nfunction buttTap(c){")
# ring: on while tapping (or the 2.2s intro), then 0.5s lowering
rep("bt=W.time-(c.buttAnimT??-99)<2.4&&c.buttAnimT>c.lastStroke-0.01, p=bt?0:fresh?1:clamp(c.petProg||0,0,1);\n"
    "  el.classList.toggle('butt',bt&&!!c.buttLike); if(bt&&!el.dataset.bt){ el.dataset.bt=1; const g=$('#beatButt'); g.classList.remove('go'); void g.getBoundingClientRect(); g.classList.add('go'); } if(!bt)delete el.dataset.bt;",
    "bE=buttEnd(c), bOk=c.buttAnimT>c.lastStroke-0.01, bOn=bOk&&W.time<bE, bDn=bOk&&!bOn&&W.time<bE+0.5, bt=bOn||bDn, p=bt?0:fresh?1:clamp(c.petProg||0,0,1);\n"
    "  el.classList.toggle('butt',bt&&!!c.buttLike); { const g=$('#beatButt'); if(bOn&&el.dataset.bt!==String(c.buttStart)){ el.dataset.bt=String(c.buttStart); const co=COATS[c.coat.base]||COATS.orange, hx=n=>'#'+n.toString(16).padStart(6,'0'); g.style.setProperty('--bb',hx(co.body)); g.style.setProperty('--bs',hx(co.stripe)); g.style.setProperty('--bl',mixHex(hx(co.body),hx(co.stripe),0.55)); g.classList.remove('go','dn'); void g.getBoundingClientRect(); g.classList.add('go'); } if(bDn&&!g.classList.contains('dn')){ g.classList.remove('go'); g.classList.add('dn'); } if(!bt){ delete el.dataset.bt; g.classList.remove('go','dn'); } }")
# markup: colours via CSS vars
rep('<path class="bbLeg" d="M22.6 27.5v6" stroke="#c47a3a"', '<path class="bbLeg" d="M22.6 27.5v6" style="stroke:var(--bl,#c47a3a)"')
rep('<ellipse cx="13" cy="25" rx="12.5" ry="6.4" fill="#e8964a"/>', '<ellipse cx="13" cy="25" rx="12.5" ry="6.4" style="fill:var(--bb,#e8964a)"/>')
rep('fill="none" stroke="#c47a3a" stroke-width="1.5"', 'fill="none" style="stroke:var(--bs,#c47a3a)" stroke-width="1.5"')
rep('<path class="bbTail" d="M24.6 22.4q4.6-2.8 4-9.6" fill="none" stroke="#e8964a"', '<path class="bbTail" d="M24.6 22.4q4.6-2.8 4-9.6" fill="none" style="stroke:var(--bb,#e8964a)"')
# CSS: two pops ending raised, then a slow quiver; .dn lowers
rep("#beatButt.go .bbBody{animation:bbUp 1.1s ease-in-out 2}#beatButt.go .bbLeg{animation:bbLeg 1.1s ease-in-out 2}#beatButt.go .bbTail{animation:bbTail 1.1s ease-in-out 2}",
    "#beatButt.go .bbBody{animation:bbUp 2.2s ease-in-out forwards,bbUpQ 1.8s ease-in-out 2.2s infinite}#beatButt.go .bbLeg{animation:bbLeg 2.2s ease-in-out forwards,bbLegQ 1.8s ease-in-out 2.2s infinite}#beatButt.go .bbTail{animation:bbTail 2.2s ease-in-out forwards,bbTailQ 2.4s ease-in-out 2.2s infinite}"
    "#beatButt.dn .bbBody{animation:bbUpD .45s ease-in forwards}#beatButt.dn .bbLeg{animation:bbLegD .45s ease-in forwards}#beatButt.dn .bbTail{animation:bbTailD .45s ease-in forwards}")
rep("@keyframes bbUp{0%,100%{transform:rotate(0)}45%,62%{transform:rotate(-17deg)}}@keyframes bbLeg{0%,100%{transform:scaleY(1)}45%,62%{transform:scaleY(1.75)}}@keyframes bbTail{0%,100%{transform:rotate(0)}45%{transform:rotate(14deg)}55%{transform:rotate(4deg)}62%{transform:rotate(12deg)}}",
    "@keyframes bbUp{0%,50%{transform:rotate(0)}22%,31%,72%,100%{transform:rotate(-17deg)}}@keyframes bbLeg{0%,50%{transform:scaleY(1)}22%,31%,72%,100%{transform:scaleY(1.75)}}@keyframes bbTail{0%,50%{transform:rotate(0)}22%{transform:rotate(14deg)}27%{transform:rotate(4deg)}31%{transform:rotate(12deg)}72%{transform:rotate(14deg)}86%{transform:rotate(8deg)}100%{transform:rotate(12deg)}}"
    "@keyframes bbUpQ{0%,100%{transform:rotate(-17deg)}50%{transform:rotate(-18.6deg)}}@keyframes bbLegQ{0%,100%{transform:scaleY(1.75)}50%{transform:scaleY(1.83)}}@keyframes bbTailQ{0%,100%{transform:rotate(12deg)}50%{transform:rotate(16deg)}}"
    "@keyframes bbUpD{from{transform:rotate(-17deg)}to{transform:rotate(0)}}@keyframes bbLegD{from{transform:scaleY(1.75)}to{transform:scaleY(1)}}@keyframes bbTailD{from{transform:rotate(12deg)}to{transform:rotate(0)}}")
open(P, 'w', encoding='utf-8').write(s); print('ok')
