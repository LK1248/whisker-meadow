"""v133: the day & night toggle leaves the main screen; it's now a row in How to play (settings), next to
Pointing hints."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

i = s.find('  <button class="hbtn pill icon" id="bDay"'); j = s.find('</button>', i)
if i < 0 or j < 0: sys.exit('bDay button not found')
s = s[:i] + s[j + len('</button>'):].lstrip('\n')
rep("$('#bDay').onclick=()=>{ W.dayOn=!W.dayOn; store.set('wm_daynight',W.dayOn); $('#bDay').classList.toggle('off',!W.dayOn); toast(W.dayOn?'Day & night: on':'Always daytime'); };\n$('#bDay').classList.toggle('off',!W.dayOn);\n", "")
rep('<div class="hrow"><span>Pointing hints</span>', '<div class="hrow"><span>Day &amp; night</span><button id="hDay">${W.dayOn?\'On\':\'Off\'}</button></div><div class="hrow"><span>Pointing hints</span>')
rep("  $('#hTog').onclick=()=>{", "  $('#hDay').onclick=()=>{ W.dayOn=!W.dayOn; store.set('wm_daynight',W.dayOn); $('#hDay').textContent=W.dayOn?'On':'Off'; };\n  $('#hTog').onclick=()=>{")
open(P, 'w', encoding='utf-8').write(s)
print('v133 applied')
