"""v39: title-screen music. Start the audio as the page loads; browsers that block autoplay get it on the first tap/click/key anywhere."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("$('#bPlay').onclick=()=>{", """// music on the title screen: plays at once where autoplay is allowed (e.g. installed app), otherwise from the first touch anywhere
Snd.init(); if(Snd.ac&&Snd.ac.state!=='running'){ const EV=['pointerdown','keydown','touchend'], wake=()=>{ Snd.ac.resume(); for(const ev of EV)removeEventListener(ev,wake,true); }; for(const ev of EV)addEventListener(ev,wake,true); }
$('#bPlay').onclick=()=>{""")
rep("window.__wm={", "window.__wm={Snd,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
