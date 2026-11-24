"""v71: the petting ring holds a small speed gauge instead of a pulse: a needle shows how fast you stroke, the green
band shows what this cat enjoys (left edge = too slow, right edge = too fast; band widens with love and in the early game).
A completed stroke shows a quick heart pulse instead of a check mark. The training-wheels fade (v64) applies to the gauge."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep('<circle class="metro" cx="22" cy="22" r="13.5"/></svg>',
    '<g class="metro"><path class="gTrk" fill="none" stroke="#eadfce" stroke-width="3.4" stroke-linecap="round"/>'
    '<path class="gBand" fill="none" stroke="#8fd17d" stroke-width="3.4" stroke-linecap="round"/>'
    '<line class="gNdl" x1="22" y1="25" x2="22" y2="14.5" stroke="#4a3426" stroke-width="2" stroke-linecap="round"/>'
    '<circle cx="22" cy="25" r="2.1" fill="#4a3426"/></g></svg>')
rep("{ const k=Math.pow(0.5+0.5*Math.cos(performance.now()/1000*2*Math.PI/strokeT(c)),2), pu=el.querySelector('.metro'); pu.style.transform=`scale(${(0.5+0.5*k).toFixed(3)})`; pu.style.fillOpacity=(0.35+0.65*k).toFixed(2);"
    " el.querySelector('svg').style.transform=W.stat.metroOff?'':`scale(${(0.9+0.16*k).toFixed(3)})`; }",
    "{ const A=68, m=v=>clamp(v/2.4,-1,1)*A, tol=tempoTol(c), tf=tolFast(c), a0=slowOk()?-A:m(-tol), a1=m(tf);"
    " if(!el.gInit){ el.gInit=1; el.querySelector('.gTrk').setAttribute('d',gArc(-A,A)); }"
    " const bd=gArc(a0,Math.max(a0+4,a1)), bp=el.querySelector('.gBand'); if(bp.getAttribute('d')!==bd)bp.setAttribute('d',bd);"
    " const nx=st?TG.x:-2.4; el.querySelector('.gNdl').setAttribute('transform',`rotate(${m(nx).toFixed(1)} 22 25)`); }")
rep("$('#beatTx').textContent=p>=1?'✓':'';",
    "{ const tx=$('#beatTx'), hv=p>=1; if(!!tx.firstChild!==hv)tx.innerHTML=hv?'<svg class=\"bHeart\" viewBox=\"0 0 24 24\"><path d=\"M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z\" fill=\"#ff6f99\"/></svg>':''; }")
rep("#beat .metro{transform-box:view-box;transform-origin:22px 22px;fill:#ffb3c9}#beat.on .metro{fill:#a9dc9c}#beat.fast .metro{fill:#f08c82}",
    "#beat .metro{transform-box:view-box;transform-origin:22px 22px}#beat.fast .gNdl{stroke:#d9453a}"
    "#beat .bHeart{width:26px;height:26px;animation:bHeart .45s ease-out both}@keyframes bHeart{0%{transform:scale(.3)}45%{transform:scale(1.3)}100%{transform:scale(1)}}"
    "#beat.ready svg{animation:none}")
rep("function updateBeat(){", "const gArc=(a0,a1,r=8.6)=>{ const P2=a=>{ const t=a*Math.PI/180; return (22+r*Math.sin(t)).toFixed(2)+' '+(25-r*Math.cos(t)).toFixed(2); }; return `M${P2(a0)} A${r} ${r} 0 0 1 ${P2(a1)}`; };\nfunction updateBeat(){")
open(P, 'w', encoding='utf-8').write(s); print('ok')
