"""v111: a butt tap gets its own look in the petting ring. The ring empties (no leftover progress, heart or colour from
the last stroke), keeps its purr wobble, and if the cat likes it, the back half of a cat pops its rump up in the air
inside the ring, tail high, twice. Cats that don't like it just get the empty ring.
Also: the ring's progress resets after 5s without petting."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
# mark the tap and clear progress
rep("function buttTap(c){ if(c.away>0||c.carried||c.outside||c.leaving||['path','greet','bye'].includes(c.state))return; const s=c.s; tagFor(c,3);",
    "function buttTap(c){ if(c.away>0||c.carried||c.outside||c.leaving||['path','greet','bye'].includes(c.state))return; const s=c.s; tagFor(c,3); c.buttAnimT=W.time; c.petProg=0;")
# ring: empty while the butt-tap moment plays, and show the rump animation for cats that like it
rep("const fresh=W.time-c.lastStroke<0.45, p=fresh?1:clamp(c.petProg||0,0,1);",
    "const fresh=W.time-c.lastStroke<0.45, bt=W.time-(c.buttAnimT??-99)<2.4&&c.buttAnimT>c.lastStroke-0.01, p=bt?0:fresh?1:clamp(c.petProg||0,0,1);\n"
    "  el.classList.toggle('butt',bt&&!!c.buttLike); if(bt&&!el.dataset.bt){ el.dataset.bt=1; const g=$('#beatButt'); g.classList.remove('go'); void g.getBoundingClientRect(); g.classList.add('go'); } if(!bt)delete el.dataset.bt;")
# markup: the back half of a cat (front cut off by the ring's inner circle), rump + tail rise, hind leg straightens
rep("<rect id=\"beatFlood\" x=\"7\" y=\"36.5\" width=\"30\" height=\"0\" fill=\"#ef6f63\" fill-opacity=\".55\" clip-path=\"url(#beatClip)\"/></svg>",
    "<rect id=\"beatFlood\" x=\"7\" y=\"36.5\" width=\"30\" height=\"0\" fill=\"#ef6f63\" fill-opacity=\".55\" clip-path=\"url(#beatClip)\"/>"
    "<g id=\"beatButt\" clip-path=\"url(#beatClip)\"><path d=\"M7 33.6h30\" stroke=\"#e8d9c6\" stroke-width=\"1.4\"/>"
    "<path class=\"bbLeg\" d=\"M22.6 27.5v6\" stroke=\"#c47a3a\" stroke-width=\"4.2\" stroke-linecap=\"round\"/>"
    "<g class=\"bbBody\"><ellipse cx=\"13\" cy=\"25\" rx=\"12.5\" ry=\"6.4\" fill=\"#e8964a\"/><path d=\"M10 20.2q4 1.5 3 9.2M16 19.4q3.4 1.8 2.4 8.8\" fill=\"none\" stroke=\"#c47a3a\" stroke-width=\"1.5\" stroke-linecap=\"round\"/>"
    "<path class=\"bbTail\" d=\"M24.6 22.4q4.6-2.8 4-9.6\" fill=\"none\" stroke=\"#e8964a\" stroke-width=\"3.2\" stroke-linecap=\"round\"/></g></g></svg>")
rep("#beat .metro{transition:opacity .5s}",
    "#beat .metro{transition:opacity .5s}"
    "#beatButt{opacity:0;transition:opacity .2s}#beat.butt #beatButt{opacity:1}#beat.butt #beatTx{display:none}"
    "#beatButt .bbBody{transform-box:view-box;transform-origin:6px 28px}#beatButt .bbLeg{transform-box:view-box;transform-origin:22.6px 33.5px}#beatButt .bbTail{transform-box:view-box;transform-origin:24.6px 22.4px}"
    "#beatButt.go .bbBody{animation:bbUp 1.1s ease-in-out 2}#beatButt.go .bbLeg{animation:bbLeg 1.1s ease-in-out 2}#beatButt.go .bbTail{animation:bbTail 1.1s ease-in-out 2}"
    "@keyframes bbUp{0%,100%{transform:rotate(0)}45%,62%{transform:rotate(-17deg)}}@keyframes bbLeg{0%,100%{transform:scaleY(1)}45%,62%{transform:scaleY(1.75)}}@keyframes bbTail{0%,100%{transform:rotate(0)}45%{transform:rotate(14deg)}55%{transform:rotate(4deg)}62%{transform:rotate(12deg)}}")
# ring progress resets after 5s without petting (love etc. untouched)
rep("if(gain>0){ c.petProg=(c.petProg||0)+gain; c.petIdle=0;",
    "if(gain>0){ if(W.time-(c.petLast??-99)>5){ c.petProg=0; c.strokeErr=0; } c.petLast=W.time; c.petProg=(c.petProg||0)+gain; c.petIdle=0;")
rep("const fresh=W.time-c.lastStroke<0.45, bt=", "if(c.petProg&&W.time-(c.petLast??-99)>5){ c.petProg=0; c.strokeErr=0; } const fresh=W.time-c.lastStroke<0.45, bt=")
open(P, 'w', encoding='utf-8').write(s); print('ok')
