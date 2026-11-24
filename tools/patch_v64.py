"""v64: the metronome is training wheels. After 10 recent strokes with at most one rhythm slip, it fades out of the
petting ring; 3 slips (hourglasses) among the last 6 bring it back. Remembered in the save (W.stat.metroOff/metroRec)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

for fr in ('true', 'false'):
    rep(f"floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),{fr}); slowNag.n++;",
        f"floatHourglass(P.hx,P.hy-(P.type==='mouse'?62:112),{fr}); slowNag.n++; c.strokeErr=1; metroLearn(1);")
rep("c.petProg=0; let z='back'", "if(!c.strokeErr)metroLearn(0); c.strokeErr=0; c.petProg=0; let z='back'")
rep("function strokeT(c){",
    "// metronome as training wheels: hide it once the rhythm is learned, bring it back if slips pile up\n"
    "function metroLearn(err){ const r=W.stat.metroRec||(W.stat.metroRec=[]); r.push(err?1:0); if(r.length>10)r.shift(); const bad=a=>a.reduce((x,y)=>x+y,0);\n"
    "  if(!W.stat.metroOff&&r.length>=10&&bad(r)<=1)W.stat.metroOff=1;\n"
    "  else if(W.stat.metroOff&&bad(r.slice(-6))>=3){ W.stat.metroOff=0; r.length=0; const b=$('#beat'); b.classList.remove('mback'); void b.offsetWidth; b.classList.add('mback'); } }\n"
    "function strokeT(c){")
rep("#beat .mArm{transform-box:view-box;transform-origin:22px 31px}",
    "#beat .mArm{transform-box:view-box;transform-origin:22px 31px}#beat .metro{transition:opacity .5s}#beat.nometro .metro{opacity:0}"
    "#beat.mback .metro{animation:mBack .6s ease-out}@keyframes mBack{0%{opacity:0;transform:scale(.4)}60%{transform:scale(1.2)}}#beat .metro{transform-box:view-box;transform-origin:22px 22px}")
rep("el.classList.toggle('on',st==='on');", "el.classList.toggle('nometro',!!W.stat.metroOff); el.classList.toggle('on',st==='on');")
rep("window.__wm={Snd,", "window.__wm={Snd,metroLearn,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
