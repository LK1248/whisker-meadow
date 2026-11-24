"""v61: one compact petting widget. The metronome swings inside the progress ring at the cat's tempo;
the ring fills green in rhythm, amber when too slow, and turns red with a shake when too fast (hourglass kept).
The separate tempo gauge and the name-tag metronome are gone."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# bigger ring (50 -> 58px) and the metronome styles
rep("#beat{position:fixed;left:0;top:0;width:50px;height:50px;margin:-25px 0 0 -25px;",
    "#beat{position:fixed;left:0;top:0;width:58px;height:58px;margin:-29px 0 0 -29px;")
rep("#beat.ready svg{animation:ipulse .7s ease-in-out infinite}",
    "#beat.ready svg{animation:ipulse .7s ease-in-out infinite}"
    "#beat .mArm{transform-box:view-box;transform-origin:22px 31px;animation:bMetro 1s ease-in-out infinite alternate}"
    "@keyframes bMetro{from{transform:rotate(-30deg)}to{transform:rotate(30deg)}}"
    "#beat .mArm path{stroke:#4a3426}#beat .mArm circle{fill:#ff6f99}#beat .metro{transition:opacity .15s}"
    "#beat.on .mArm circle{fill:#5fb35a}#beat.fast .mArm circle{fill:#e2574c}#beat.fast .mArm path{stroke:#b8433a}"
    "#beat.fast svg{animation:bShake .28s linear infinite}@keyframes bShake{25%{transform:translateX(-2px) rotate(-4deg)}75%{transform:translateX(2px) rotate(4deg)}}"
    "#beat.ready .metro{opacity:0}")
rep('<circle id="beatFg" cx="22" cy="22" r="17" fill="none" stroke-width="5" stroke-linecap="round" transform="rotate(-90 22 22)" stroke-dasharray="106.8" stroke-dashoffset="106.8"/></svg>',
    '<circle id="beatFg" cx="22" cy="22" r="17" fill="none" stroke-width="5" stroke-linecap="round" transform="rotate(-90 22 22)" stroke-dasharray="106.8" stroke-dashoffset="106.8"/>'
    '<g class="metro"><path d="M16.5 33L19.6 10.5h4.8L27.5 33z" fill="#e6c9a3"/><path d="M15 33.2h14" stroke="#c99a6b" stroke-width="2.4" stroke-linecap="round"/>'
    '<g class="mArm"><path d="M22 31V11.5" stroke-width="1.8" stroke-linecap="round"/><circle cx="22" cy="17" r="2.7"/></g></g></svg>')
# ring colour + metronome speed follow the tempo state
rep("const fg=$('#beatFg'); fg.style.strokeDashoffset=106.8*(1-p); fg.style.stroke=p>=1?'#5fb35a':'#f0a13a'; el.classList.toggle('ready',p>=1);",
    "const st=P.mode==='stroke'&&S.cat===c&&TG.c===c&&TG.shown>0.5?TG.st:null;"
    " if(el.lastC!==c){ el.lastC=c; el.querySelector('.mArm').style.animationDuration=strokeT(c).toFixed(2)+'s'; }"
    " const fg=$('#beatFg'); fg.style.strokeDashoffset=106.8*(1-p); fg.style.stroke=p>=1||st==='on'?'#5fb35a':st==='fast'?'#e2574c':'#f0a13a';"
    " el.classList.toggle('on',st==='on'); el.classList.toggle('fast',st==='fast'); el.classList.toggle('ready',p>=1);")
# gauge: still computes the smoothed tempo state, but is never shown
rep("el.hidden=false; el.style.opacity=on?1:Math.max(0,TG.shown/0.8);",
    "TG.st=TG.x>tol?'fast':TG.x<-tol?'slow':'on'; el.hidden=true; return; el.hidden=false; el.style.opacity=on?1:Math.max(0,TG.shown/0.8);")
# no metronome in the name tag any more
rep("$('#tName').innerHTML=`${c.name}${c.age<1?' <small>kitten</small>':''}${METRO(c)}`;",
    "$('#tName').innerHTML=`${c.name}${c.age<1?' <small>kitten</small>':''}`;")
open(P, 'w', encoding='utf-8').write(s); print('ok')
