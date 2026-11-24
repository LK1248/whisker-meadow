"""v88: the first cat-fair lesson is forced like the other lessons. While it is up, only a fair-ready cat can be tapped
(no stroking, tools, shop or dock), its name tag stays open, the guide moves to the fair badge, the hint never times
out, and no strays, families or other events arrive until the cat has gone to the fair."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("function shopForce(){",
    "function fairForce(){ if(!curHint||!W.started||W.stat.shows)return null; if(curHint.id==='show0')return 'hand'; if(curHint.id!=='show')return null; return W.cats.some(showReady)?'show':null; }\n"
    "function shopForce(){")
rep("  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};",
    "  if(tips.cur&&tips.cur.kind==='butt')return {cats:[tips.cur.c],tools:[],tapOnly:true};\n"
    "  { const f=fairForce(); if(f==='hand')return {cats:[],tools:['hand']}; if(f)return {cats:W.cats.filter(showReady),tools:[],tapOnly:true}; }")
rep("if(hintT>22&&!shopForce()){", "if(hintT>22&&!shopForce()&&!fairForce()){")
rep("{id:'show',when:()=>W.tool==='hand'&&W.cats.some(showReady),at:",
    "{id:'show',get el(){ return tag.c&&showReady(tag.c)&&!$('#tShow').hidden?'#tShow':null; },when:()=>W.tool==='hand'&&W.cats.some(showReady),at:")
rep("if(tag.t<=0&&!(tag.c.petT>0&&handOn(tag.c)))tag.c=null;",
    "if(tag.t<=0&&!(tag.c.petT>0&&handOn(tag.c))&&!(fairForce()==='show'&&showReady(tag.c)))tag.c=null;")
rep("$('#tStay').onclick=()=>{ const c=tag.c; if(!c)return;", "$('#tStay').onclick=()=>{ const c=tag.c; if(!c||fairForce())return;")
rep("function calmHold(){ return playerBusy()||", "function calmHold(){ return playerBusy()||!!fairForce()||")
rep("const HINT_HOLD=new Set(['feed',", "const HINT_HOLD=new Set(['show0','show','feed',")
rep("window.__wm={Snd,", "window.__wm={Snd,fairForce,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
