"""v134: windows are easier to close (shop, sanctuary, help...).
- They sit lower: a strip at the top (12% of the screen) always shows the meadow; tapping it closes the window.
- The X is pinned: it stays at the top-right while the content scrolls.
- Swipe down: drag the window down from its top (when not scrolled) and let go past ~90px or with a flick
  to close it; a small grab bar on top shows it can be pulled. Only for windows that have an X (not cards that
  need their button, not while the shop lesson holds it open)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#modal{position:fixed;inset:0;background:rgba(60,40,30,.35);display:grid;place-items:center;z-index:20;padding:16px}",
    "#modal{position:fixed;inset:0;background:rgba(60,40,30,.35);display:grid;grid-template-columns:minmax(0,1fr);place-items:center;z-index:20;padding:max(16px,12vh) 16px 16px}")
rep("#modal .box{background:var(--cream);", "#modal .box{box-sizing:border-box;background:var(--cream);")
rep("#modal .x{position:absolute;right:14px;top:14px;width:40px;height:40px;border-radius:50%;background:#f3e7d6;font:700 20px var(--display)}",
    "#modal .x{position:sticky;float:right;top:0;margin:-6px -4px 0 10px;z-index:3;width:40px;height:40px;border-radius:50%;background:#f3e7d6;font:700 20px var(--display);box-shadow:0 2px 8px rgba(60,40,30,.18)}\n"
    "#mbox:has(> .x)::before{content:'';display:block;width:44px;height:5px;border-radius:3px;background:#e2d2bd;margin:-10px auto 10px}#mbox.drag{animation:none;transition:none}#mbox.snap{transition:transform .2s ease-out}")
rep("$('#modal').addEventListener('pointerdown',e=>{ if(e.target.id==='modal')userClose(); });",
    """$('#modal').addEventListener('pointerdown',e=>{ if(e.target.id==='modal')userClose(); });
{ const mb=$('#mbox'); let sy=null, dy=0, t0=0, on=false;
  const can=()=>!!mb.querySelector(':scope > .x')&&!(shopForce()&&mb.querySelector('[data-buy]'));
  mb.addEventListener('touchstart',e=>{ if(e.touches.length!==1||!can()||mb.scrollTop>2){ sy=null; return; } sy=e.touches[0].clientY; dy=0; t0=performance.now(); on=false; },{passive:true});
  mb.addEventListener('touchmove',e=>{ if(sy==null)return; dy=e.touches[0].clientY-sy; if(!on){ if(dy>8&&mb.scrollTop<=0){ on=true; mb.classList.add('drag'); mb.classList.remove('snap'); } else if(dy<-4){ sy=null; return; } else return; }
    e.preventDefault(); mb.style.transform=`translateY(${Math.max(0,dy)}px)`; },{passive:false});
  const end=()=>{ if(sy==null)return; sy=null; if(!on)return; on=false; mb.classList.remove('drag'); const fast=dy/Math.max(1,performance.now()-t0)>0.6;
    if(dy>90||(fast&&dy>30)){ mb.style.transform=''; rec('swipeClose',''); userClose(); } else { mb.classList.add('snap'); mb.style.transform=''; } };
  mb.addEventListener('touchend',end); mb.addEventListener('touchcancel',end); }""")
open(P, 'w', encoding='utf-8').write(s)
print('v134 applied')
