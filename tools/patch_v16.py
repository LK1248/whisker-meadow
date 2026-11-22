"""v16: wordless 'slow down' (hourglass), a big SLOW only for repeat misses; stroke pace loosened to ~0.65/s."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# pace: on-beat from ~1.55s between strokes (was 2.0s); "too fast" only under 1.0s (was 1.3s); brush scaled the same
rep("const rating=frantic||iv<(brush?0.7:1.3)*slow?'fast':(iv>=(brush?1.0:2.0)*slow&&iv<=7)?'good':'neutral';",
    "const rating=frantic||iv<(brush?0.55:1.0)*slow?'fast':(iv>=(brush?0.8:1.55)*slow&&iv<=7)?'good':'neutral';")
rep("g0=(W.tool==='brush'?1.0:2.0)*(c.trait==='shy'?1.15:1);", "g0=(W.tool==='brush'?0.8:1.55)*(c.trait==='shy'?1.15:1);")
rep("g0=(W.tool==='brush'?1.0:2.0)*slow,", "g0=(W.tool==='brush'?0.8:1.55)*slow,")
# feedback: hourglass instead of words; repeated misses earn a big SLOW for a few seconds
rep("""    if(rating==='fast')floatAt(fx,fy,'Too fast!','bad'); else if(rating==='good')floatAt(fx,fy,c.streak>=2?`Purr! ×${c.streak}`:'Purr!','good'); else if(iv<(brush?1.0:2.0)*slow)floatAt(fx,fy,'A bit slower','bad'); }""",
"""    if(rating==='good'){ slowNag.n=0; floatAt(fx,fy,c.streak>=2?`Purr! ×${c.streak}`:'Purr!','good'); }
    else if(rating==='fast'||iv<(brush?0.8:1.55)*slow){ floatHourglass(fx,fy,rating==='fast'); slowNag.n++; if(slowNag.n>=4&&W.time>slowNag.next){ slowNag.n=0; slowNag.next=W.time+40; showSlow(); } } }""")
rep("function floatAt(x,y,text,cls=''){", """const HOURGLASS='<svg viewBox="0 0 40 48"><path d="M8 4h24M8 44h24" stroke="#4a3426" stroke-width="4" stroke-linecap="round"/><path d="M11 6c0 10 9 13 9 18s-9 8-9 18h18c0-10-9-13-9-18s9-8 9-18z" fill="#fff8ee" stroke="#4a3426" stroke-width="3" stroke-linejoin="round"/><path d="M15 13h10c-1 3-5 5-5 7-0-2-4-4-5-7zM13 40c1-5 7-8 7-10 0 2 6 5 7 10z" fill="#f2b04a"/></svg>';
const slowNag={n:0,next:0};
function floatHourglass(x,y,fast){ const d=document.createElement('div'); d.className='float hg'+(fast?' fast':''); d.innerHTML=HOURGLASS; d.style.left=x+'px'; d.style.top=y+'px'; document.body.appendChild(d); setTimeout(()=>d.remove(),1450); }
function showSlow(){ const d=document.createElement('div'); d.className='bigSlow'; d.innerHTML=HOURGLASS+'<b>Slow</b>'; document.body.appendChild(d); setTimeout(()=>d.remove(),2800); }
function floatAt(x,y,text,cls=''){""")
rep(".float{position:fixed;", """.float.hg svg{width:50px;height:60px;display:block;filter:drop-shadow(0 2px 3px rgba(74,52,38,.35))}
.float.hg.fast svg{animation:hgShake .35s ease-in-out 2}
@keyframes hgShake{0%,100%{transform:rotate(0)}25%{transform:rotate(-18deg)}75%{transform:rotate(18deg)}}
.bigSlow{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);z-index:8;pointer-events:none;display:flex;align-items:center;gap:14px;background:rgba(255,250,242,.94);padding:14px 30px;border-radius:26px;box-shadow:0 8px 24px rgba(0,0,0,.25);animation:bigSlow 2.8s ease-in-out forwards}
.bigSlow svg{width:52px;height:62px}.bigSlow b{font:700 58px var(--display);color:#4a3426;letter-spacing:.04em;text-transform:uppercase}
@keyframes bigSlow{0%{opacity:0;transform:translate(-50%,-50%) scale(.7)}10%{opacity:1;transform:translate(-50%,-50%) scale(1)}85%{opacity:1}100%{opacity:0}}
.float{position:fixed;""")
rep("""A ring by your hand fills in about 2 seconds (longer for shy cats). Stroke again when it turns <b>green with a ✓</b>.</li><li>"Purr!" = perfect. "A bit slower" = slightly early. "Too fast!" = frantic.</li>""",
    """A ring by your hand fills in about 1.5 seconds (longer for shy cats). Stroke again when it turns <b>green with a ✓</b>.</li><li>"Purr!" = perfect. An hourglass = slow down (a shaking one = way too fast).</li>""")
rep("window.__wm={animateCat,", "window.__wm={animateCat,slowNag,showSlow,floatHourglass,")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
