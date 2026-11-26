"""v159: tapping the locked laser points at the shop.
It used to show a small "laser -> bag" bubble under the shop for 2.6 s, easy to miss. Now it shows the regular hint:
the tapping hand on the shop button with a laser icon and its price, and the shop button pulses. The hint goes away
when the shop is opened (or after a few seconds) and can show again on the next tap. If another hint is already on
screen, the old small bubble is used instead."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function lockTip(){ let el=$('#lockTip');",
    "function lockTip(){ const b0=$('#bShop'); if(!curHint&&!lessonOn()&&$('#modal').hidden){ const price=($('[data-tool=\"laser\"] .lock')||{}).textContent||'';\n"
    "    curHint={id:'laserShop',el:'#bShop',g:'tap',when:()=>false,done:()=>W.laser||!$('#modal').hidden,redo:true,auto:4,again:true}; hintT=0; hintEl.className='g-tap';\n"
    "    hintEl.querySelector('.lab').innerHTML=hIco(IC.laser,26)+(price?`<span>${price}</span>`:''); hintEl.hidden=false; hintRetry.laserShop=0;\n"
    "    b0.classList.remove('nudge'); void b0.offsetWidth; b0.classList.add('nudge'); rec('lockTip','laser:hint'); return; }\n"
    "  let el=$('#lockTip');")
open(P, 'w', encoding='utf-8').write(s)
print('v159 applied')
