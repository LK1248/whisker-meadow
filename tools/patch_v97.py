"""v97: the wand lesson is forced like the others. First only the wand can be picked from the dock; then, while the
lesson asks you to sway it, the wand is the only thing that works (no tool switching, cat taps, shop or dock) until
3 cats pounce at it. If no cat bites within a minute it lets go instead of trapping the player. No events meanwhile."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function shopForce(){",
    "function wandForce(){ if(!curHint||!W.started)return null; if(curHint.id==='wand')return 'pick'; if(curHint.id==='wand2'&&W.tool==='wand'&&hintT<60)return 'sway'; return null; }\n"
    "function shopForce(){")
rep("  { const f=fairForce();",
    "  { const f=wandForce(); if(f==='pick')return {cats:[],tools:['wand']}; if(f)return {cats:[],tools:[],wandOk:true}; }\n"
    "  { const f=fairForce();")
rep("{ const L=tutLock(); if(L){ if(hit&&(!hit.cat||!L.cats.includes(hit.cat)))hit=null; if(!hit||W.tool==='wand'||W.tool==='laser'){ P.mode='none'; handVis(); return; } } }",
    "{ const L=tutLock(); if(L&&!(L.wandOk&&W.tool==='wand')){ if(hit&&(!hit.cat||!L.cats.includes(hit.cat)))hit=null; if(!hit||W.tool==='wand'||W.tool==='laser'){ P.mode='none'; handVis(); return; } } else if(L)hit=null; }")
rep("if(hintT>22&&!shopForce()&&!fairForce()){", "if(hintT>22&&!shopForce()&&!fairForce()&&!wandForce()){")
rep("function calmHold(){ return playerBusy()||", "function calmHold(){ return playerBusy()||!!wandForce()||")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tips.cur&&['flea','butt'].includes(tips.cur.kind))return;",
    "function startBlinkTut(c){ if(bt.c||intro.c||pl.a||firstAdopt()||tutLock())return; // never barge into another lesson")
rep("window.__wm={Snd,", "window.__wm={Snd,wandForce,")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
