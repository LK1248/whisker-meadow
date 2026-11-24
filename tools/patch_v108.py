"""v108: the blink-back badge is called 'Slow Blink + Boop' (it shows in the badge list and its pop-up toast)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "['blink','Slow Blink','Blinked back',"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "['blink','Slow Blink + Boop','Blinked back',")
open(P, 'w', encoding='utf-8').write(s); print('ok')
