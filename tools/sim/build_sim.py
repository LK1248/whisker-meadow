"""Build tools/sim/sim.html: the game with its own save key, no render loop, and the bot harness injected. The shipped game is untouched."""
import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
s = (root / 'whisker-meadow.html').read_text(encoding='utf-8')
def rep(old, new):
    global s
    if s.count(old) != 1: sys.exit(f'match count {s.count(old)} != 1 for: {old[:70]}')
    s = s.replace(old, new)
rep("const SAVE='wm_save_v3';", "const SAVE='wm_sim_v1'; try{localStorage.removeItem(SAVE);}catch(e){}")
rep("function frame(now){\n  requestAnimationFrame(frame);", "function frame(now){ if(window.__SIMOFF)return;\n  requestAnimationFrame(frame);")
rep("function saveGame(){ if(!W.started)return;", "function saveGame(){ return; if(!W.started)return;")
bot = (root / 'tools/sim/bot.js').read_text(encoding='utf-8')
end = s.rstrip().rfind('})();')
if end < 0: sys.exit('closure end not found')
s = s[:end] + 'window.__SIMOFF=true;\n' + bot + '\n' + s[end:]
(root / 'tools/sim/sim.html').write_text(s, encoding='utf-8')
print('sim.html written')
