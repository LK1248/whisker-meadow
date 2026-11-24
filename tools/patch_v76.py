"""v76: no gauge; the ring's rim purrs. While the cat purrs, the rim becomes a sine wave with 12 bumps around the
ring that travels clockwise (one turn per 1.2 s) and pulses up and down 12 times a second (half the purr sound's
24 Hz flutter). Louder purr = bigger wave. The progress arc follows the same wavy rim."""
import sys, re
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep('<circle cx="22" cy="22" r="17" fill="rgba(255,250,242,.9)" stroke="#e8d9c6" stroke-width="5"/><circle id="beatFg" cx="22" cy="22" r="17" fill="none" stroke-width="5" stroke-linecap="round" transform="rotate(-90 22 22)" stroke-dasharray="106.8" stroke-dashoffset="106.8"/>',
    '<circle cx="22" cy="22" r="17" fill="rgba(255,250,242,.9)"/><path id="beatBg" fill="none" stroke="#e8d9c6" stroke-width="5" stroke-linejoin="round"/><path id="beatFg" fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
# gauge markup and code out
n0 = len(s); s = re.sub(r'<g class="metro"><path class="gTrk".*?</g></svg>', '</svg>', s, count=1); assert len(s) < n0
rep_old = re.search(r"\{ const A=68, m=v=>clamp\(v/1\.2,-1,1\)\*A,.*?rotate\(\$\{m\(nx\)\.toFixed\(1\)\} 22 25\)`\); \}", s).group(0)
rep(rep_old, "")
# rigid jitter -> wavy rim
rep("const pr=c.purr>0.05&&!el.classList.contains('fast')?c.purr:0, a=pr?0.5+2.3*pr:0; el.querySelector('svg').style.transform=a?`translate(${rand(-a,a).toFixed(2)}px,${rand(-a,a).toFixed(2)}px)`:''; }",
    "const pr=c.purr>0.05&&!el.classList.contains('fast')?c.purr:0; rimDraw(pr*1.3,p>=1?1:p); }")
rep("const gArc=", "// wavy rim: 12 bumps travelling clockwise (1 turn / 1.2 s), pulsing at 12 Hz; amp in viewBox units\n"
    "function rimPts(f0,f1,amp,t){ const N=12, n=Math.max(2,Math.ceil((f1-f0)*120)), puls=0.55+0.45*Math.sin(t*2*Math.PI*12), out=[];\n"
    "  for(let i=0;i<=n;i++){ const th=(f0+(f1-f0)*i/n)*2*Math.PI, r=17+amp*puls*Math.sin(N*(th-t*2*Math.PI/1.2)); out.push((22+r*Math.sin(th)).toFixed(2)+' '+(22-r*Math.cos(th)).toFixed(2)); }\n"
    "  return 'M'+out.join('L'); }\n"
    "function rimDraw(amp,p){ const t=performance.now()/1000, bg=$('#beatBg'), fg=$('#beatFg'); bg.setAttribute('d',rimPts(0,1,amp,t)+'Z'); fg.setAttribute('d',p>0.005?rimPts(0,Math.min(1,p),amp,t):''); }\n"
    "const gArc=")
open(P, 'w', encoding='utf-8').write(s); print('ok')
