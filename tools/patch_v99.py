"""v99: the wand lesson's safety release comes after 30s (was 60s), so a player who isn't into it isn't held long."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "if(curHint.id==='wand2'&&W.tool==='wand'&&hintT<60)return 'sway';"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "if(curHint.id==='wand2'&&W.tool==='wand'&&hintT<30)return 'sway';")
open(P, 'w', encoding='utf-8').write(s); print('ok')
