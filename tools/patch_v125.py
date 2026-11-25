"""v125: an always-on play log (for now) to help debug lessons and ease of use. It records, on the device only:
lesson / tip / hint / modal / tool state changes, taps on the meadow (what they hit, and whether a lesson blocked
them), finger lifts, UI button clicks, toasts, lesson skips, full petting rings and too-fast hourglasses.
Kept in localStorage (last 5000 events, across sessions and new games). Help → 'Play log' copies or shares it."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

REC = r"""
/* ---------- play log (always on for now): what the player did and what the game was asking for ---------- */
const REC={k:'wm_rec',max:5000,L:[],sig:'',dirty:0,t0:Date.now()};
try{ REC.L=JSON.parse(localStorage.getItem(REC.k)||'[]'); if(!Array.isArray(REC.L))REC.L=[]; }catch(e){ REC.L=[]; }
function rec(ev,d){ try{ REC.L.push([Math.round((Date.now()-REC.t0)/100)/10,Math.round((W.time||0)*10)/10,ev,d==null?'':String(d)]); if(REC.L.length>REC.max)REC.L.splice(0,REC.L.length-REC.max); REC.dirty=1; }catch(e){} }
function recSave(){ if(!REC.dirty)return; REC.dirty=0; try{ localStorage.setItem(REC.k,JSON.stringify(REC.L)); }catch(e){} }
setInterval(recSave,4000); addEventListener('pagehide',recSave); document.addEventListener('visibilitychange',()=>{ rec(document.hidden?'hidden':'visible'); if(document.hidden)recSave(); });
rec('session',`${new Date().toISOString()} ${innerWidth}x${innerHeight} ${matchMedia('(pointer:coarse)').matches?'touch':'mouse'}`);
function recLesson(){ if(!W.started)return 'menu'; const p=[];
  if(intro.c)p.push('pet:'+intro.c.name); if(bt.c)p.push('blink:'+bt.c.name); if(pl.a)p.push('pair:'+pl.stage); if(br.c)p.push('brush:'+br.c.name);
  if(firstAdopt())p.push('adopt'+(W.pickHome?':pick':'')); { const g=shopForce(); if(g)p.push('shop:'+g); } if(tips.cur)p.push('tip:'+tips.cur.kind);
  { const f=wandForce(); if(f)p.push('wand:'+f); } { const f=fairForce(); if(f)p.push('fair:'+f); } return p.join(',')||'free'; }
function recTick(){ try{ const m=$('#modal'), sig=[recLesson(),'tool='+W.tool,'hint='+(curHint&&!hintEl.hidden?curHint.id:'-'),'modal='+(m.hidden?'-':((($('#mbox h3')||{}).textContent)||'?').slice(0,30)),W.paused?'paused':''].join(' | ');
  if(sig!==REC.sig){ REC.sig=sig; rec('state',sig); } }catch(e){} }
const recXY=e=>`@${Math.round(e.clientX/innerWidth*100)},${Math.round(e.clientY/innerHeight*100)}`;
canvas.addEventListener('pointerdown',e=>{ if(!W.started||W.paused)return; const L=tutLock();
  rec('down',`${P.mode||'-'}${P.mode==='catPending'&&P.cat?':'+P.cat.name+'/'+(P.zone||''):''}${P.mode==='item'&&P.item?':'+P.item.kind:''} tool=${W.tool}${L&&P.mode==='none'?' BLOCKED':''} ${recXY(e)}`); });
addEventListener('pointerup',e=>{ if(!W.started||e.target!==canvas)return; rec('up',`${P.mode||'-'}${P.moved?' moved':''}${P.mode==='stroke'&&S.cat?' '+S.cat.name:''} ${Math.round(performance.now()-(P.t0||0))}ms`); },true);
document.addEventListener('click',e=>{ const b=e.target.closest&&e.target.closest('button,summary,.tool'); if(!b)return; rec('click',b.id||(b.dataset&&b.dataset.tool)||b.getAttribute('aria-label')||(b.textContent||'').trim().slice(0,24)); if(b.id==='hLog')recExport(b,false); if(b.id==='hLogShare')recExport(b,true); },true);
function recText(){ recSave(); return 'Whisker Meadow play log  (wall s since session start | game time | event | detail)\n'+REC.L.map(r=>r.join('\t')).join('\n'); }
async function recExport(b,share){ const t=recText();
  if(share&&navigator.share){ try{ await navigator.share({title:'Whisker Meadow play log',text:t}); b.textContent='✓'; return; }catch(e){} }
  try{ await navigator.clipboard.writeText(t); b.textContent='✓ Copied'; return; }catch(e){}
  openModal(`<h3>Play log</h3><textarea readonly style="width:100%;height:50vh;font:11px monospace">${t.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</textarea>`); }
"""
rep("function frame(now){", REC.lstrip('\n') + "function frame(now){ recTick();")
rep("function toast(html,cls='',ms=2600){ ", "function toast(html,cls='',ms=2600){ rec('toast',String(html).replace(/<[^>]+>/g,'').slice(0,60)); ")
rep("function skipLesson(){ ", "function skipLesson(){ rec('skip',recLesson()); ")
rep("function floatHourglass(x,y,fast){", "function floatHourglass(x,y,fast){ rec('tooFast',fast?'hard':'');")
rep("function onStroke(c,zone,frantic,good){", "function onStroke(c,zone,frantic,good){ rec('stroke',`${c.name} ${zone}${frantic?' frantic':''}${good?' ring':''}`);")
rep('<div class="hrow"><span>Pointing hints</span><button id="hTog">${W.hints?\'On\':\'Off\'}</button></div>',
    '<div class="hrow"><span>Pointing hints</span><button id="hTog">${W.hints?\'On\':\'Off\'}</button></div>'
    '<div class="hrow"><span>Play log</span><span><button id="hLog">Copy</button>${navigator.share?\' <button id="hLogShare">Share</button>\':\'\'}</span></div>')
open(P, 'w', encoding='utf-8').write(s); print('ok')
