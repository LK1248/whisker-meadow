"""v89: the butt-tap lesson zooms in close on its cat (held there until the tap), and that cat always likes butt taps,
so the first tap shows what the action is for."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function showTip(kind,c,svg,dur,tap){ if(kind==='butt'&&W.tool!=='hand')setTool('hand');",
    "function showTip(kind,c,svg,dur,tap){ if(kind==='butt'&&W.tool!=='hand')setTool('hand');\n"
    "  if(kind==='butt'){ c.buttLike=true; if(!cam.close)cam.close={want:cam.want}; cam.close.c=c; cam.close.idle=0; cam.want=Math.min(cam.want,BUTT_ZOOM); cam.focus=c; cam.focusT=0.3; }")
rep("const busy=P.cat===c&&P.mode&&P.mode!=='none'||S.cat===c||",
    "const busy=P.cat===c&&P.mode&&P.mode!=='none'||S.cat===c||tips.cur&&tips.cur.kind==='butt'&&tips.cur.c===c||")
rep("function updateClose(dt){", "let BUTT_ZOOM=2.4; // camera distance for the butt-tap lesson\nfunction updateClose(dt){")
rep("window.__wm={Snd,", "window.__wm={Snd,setButtZoom:v=>{BUTT_ZOOM=v;},")
open(P, 'w', encoding='utf-8').write(s); print('ok')
