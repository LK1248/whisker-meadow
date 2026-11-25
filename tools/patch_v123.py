"""v123: the petting grace after a lifted finger lasts 1 second (was 0.5)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "PG_T=0.5; // pet grace: focus outlives a lifted finger by half a second"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "PG_T=1; // pet grace: focus outlives a lifted finger by a second")
open(P, 'w', encoding='utf-8').write(s); print('ok')
