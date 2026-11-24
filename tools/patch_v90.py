"""v90: the flea lesson is forced like the brush lesson: only the brush can be picked and only the flea cat brushed,
the cat stays put until its fleas are gone, the lesson doesn't time out, and no events arrive meanwhile."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};",
    "  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};\n"
    "  if(tips.cur&&tips.cur.kind==='flea')return {cats:W.tool==='brush'?[tips.cur.c]:[],tools:['brush']};")
rep("const pinned=c=>!c.carried&&(P.mode==='stroke'||P.mode==='catPending')&&(S.cat===c||P.cat===c);",
    "const pinned=c=>!c.carried&&((P.mode==='stroke'||P.mode==='catPending')&&(S.cat===c||P.cat===c)||tips.cur&&tips.cur.kind==='flea'&&tips.cur.c===c);")
rep("(tips.t>T.dur&&T.kind!=='butt')", "(tips.t>T.dur&&T.kind!=='butt'&&T.kind!=='flea')")
rep("function calmHold(){ return playerBusy()||", "function calmHold(){ return playerBusy()||!!(tips.cur&&tips.cur.kind==='flea')||")
rep("if(flea){ showTip('flea',flea,FLEA_TIP,8,false); return; }",
    "if(flea){ if(!['sit','idle','sleep','flop'].includes(flea.state))setState(flea,'idle'); showTip('flea',flea,FLEA_TIP,8,false); return; }")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);",
    "  if(T.kind==='butt'&&c.state==='idle')c.stT=Math.max(c.stT||0,2);\n"
    "  if(T.kind==='flea'){ if(['walk','run','trot','zoom'].includes(c.state))setState(c,'idle'); if(c.state==='idle')c.stT=Math.max(c.stT||0,2); }")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
s = open(P, encoding='utf-8').read()
rep("function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt())return;",
    "function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tips.cur&&['flea','butt'].includes(tips.cur.kind))return;")
open(P, 'w', encoding='utf-8').write(s); print('ok3')
