"""v69: the petting ring shows the cat's rhythm with a soft pulsing disc instead of a metronome.
One pulse per stroke, on the same clock as the tail swish. Pink while waiting/slow, green in rhythm, red when too fast.
The training-wheels rule from v64 still applies (the pulse fades once the rhythm is learned)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep('<g class="metro"><path d="M16.5 33L19.6 10.5h4.8L27.5 33z" fill="#e6c9a3"/><path d="M15 33.2h14" stroke="#c99a6b" stroke-width="2.4" stroke-linecap="round"/>'
    '<g class="mArm"><path d="M22 31V11.5" stroke-width="1.8" stroke-linecap="round"/><circle cx="22" cy="17" r="2.7"/></g></g></svg>',
    '<circle class="metro" cx="22" cy="22" r="13.5"/></svg>')
rep("el.querySelector('.mArm').style.transform=`rotate(${(30*Math.sin(performance.now()/1000*Math.PI/strokeT(c))).toFixed(1)}deg)`;",
    "{ const k=Math.pow(0.5+0.5*Math.cos(performance.now()/1000*2*Math.PI/strokeT(c)),2), pu=el.querySelector('.metro'); pu.style.transform=`scale(${(0.5+0.5*k).toFixed(3)})`; pu.style.fillOpacity=(0.35+0.65*k).toFixed(2); }")
rep("#beat .metro{transform-box:view-box;transform-origin:22px 22px}",
    "#beat .metro{transform-box:view-box;transform-origin:22px 22px;fill:#ffb3c9}#beat.on .metro{fill:#a9dc9c}#beat.fast .metro{fill:#f08c82}")
open(P, 'w', encoding='utf-8').write(s); print('ok')
