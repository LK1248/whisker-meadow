"""v85: the butt-tap tip is forced like the lessons. While it shows, everything is locked except tapping the shown
cat (taps only: no stroking, no camera, no buttons, no tools), it doesn't time out, and it ends once you tap."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("  { const g=shopForce(); if(g)return {cats:[],tools:[],shop:g}; }",
    "  { const g=shopForce(); if(g)return {cats:[],tools:[],shop:g}; }\n  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};")
# taps only: a drag on the cat doesn't turn into petting
rep("if(P.mode==='catPending'&&P.moved){ P.mode='stroke';",
    "if(P.mode==='catPending'&&P.moved&&(tutLock()||{}).tapOnly){ P.mode='none'; P.cat=null; }\n  if(P.mode==='catPending'&&P.moved){ P.mode='stroke';")
# a tap on a small far cat must not just zoom in during the tip
rep("else if(!lessonOn()&&!(c.blinkBackT>0)&&(!cam.close||cam.close.c!==c)&&catScreenH(c)<75)focusClose(c);",
    "else if(!lessonOn()&&!(tips.cur&&tips.cur.kind==='butt')&&!(c.blinkBackT>0)&&(!cam.close||cam.close.c!==c)&&catScreenH(c)<75)focusClose(c);")
# no timeout for the butt tip; hand tool on start
rep("tips.t>T.dur||", "(tips.t>T.dur&&T.kind!=='butt')||")
rep("function showTip(kind,c,svg,dur,tap){ ", "function showTip(kind,c,svg,dur,tap){ if(kind==='butt'&&W.tool!=='hand')setTool('hand'); ")
open(P, 'w', encoding='utf-8').write(s); print('ok')
