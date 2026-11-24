"""v95: loud meows (the runaway's) stay loud but stop grating. Above an everyday meow's level, extra loudness is
eased in on a soft curve (peaking ~3x a normal meow instead of ~4x), and the brightest overtones are rolled off
with a gentle low-pass, more so the louder the meow, so it carries without the harsh buzzy edge in headphones.
(Browsers can't tell reliably whether headphones are plugged in, so this is tuned to be comfortable for both.)"""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("  meow(p=1,loud=1){ if(!this.ac)return; const ac=this.ac,t=ac.currentTime,d=0.5+Math.random()*0.15;",
    "  meow(p=1,loud=1){ if(!this.ac)return; const ac=this.ac,t=ac.currentTime,d=0.5+Math.random()*0.15;\n"
    "    const hot=Math.max(0,loud-0.4); if(hot>0)loud=0.4+hot/(1+hot*0.9); // soft knee: loud stays loud, never piercing (1.2 -> ~0.95)")
rep("o.connect(f); f.connect(g); g.connect(this.sfx); o.start(t); o.stop(t+d+0.05); },",
    "if(hot>0){ const lp=ac.createBiquadFilter(); lp.type='lowpass'; lp.Q.value=0.5; lp.frequency.value=Math.max(1500,3400-hot*2200); o.connect(f); f.connect(lp); lp.connect(g); } else { o.connect(f); f.connect(g); } g.connect(this.sfx); o.start(t); o.stop(t+d+0.05); },")
open(P, 'w', encoding='utf-8').write(s); print('ok')
