"""v150: a soft, quiet pat sound on every butt tap (a muffled little thump), so taps get audio feedback."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  pop(){ if(!this.ac)return;",
    "  pat(){ if(!this.ac)return; const ac=this.ac,t=ac.currentTime, s=ac.createBufferSource(); s.buffer=this.noise; const f=ac.createBiquadFilter(); f.type='lowpass'; f.frequency.value=rand(420,560); f.Q.value=1.2; const g=ac.createGain();\n"
    "    g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.22,t+0.004); g.gain.exponentialRampToValueAtTime(0.0001,t+0.07); s.connect(f); f.connect(g); g.connect(this.sfx); s.start(t,Math.random()*0.5,0.08); },\n"
    "  pop(){ if(!this.ac)return;")
rep("const s=c.s; tagFor(c,3); if(!(W.time<buttEnd(c)))c.buttStart=W.time;",
    "const s=c.s; Snd.pat(); tagFor(c,3); if(!(W.time<buttEnd(c)))c.buttStart=W.time;")
open(P, 'w', encoding='utf-8').write(s)
print('v150 applied')
