"""v124: during the petting grace the ring keeps the colour it had just before the finger lifted
(no flip to orange), so the lift reads as part of one continuous pet."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "const st=P.mode==='stroke'&&S.cat===c&&TG.c===c&&TG.shown>0.5?TG.st:null;"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "const st=P.mode==='stroke'&&S.cat===c?(c.beatSt=TG.c===c&&TG.shown>0.5?TG.st:null):petGrace(c)?c.beatSt:null; /* grace: keep the last colour */")
open(P, 'w', encoding='utf-8').write(s); print('ok')
