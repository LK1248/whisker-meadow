"""v105: the Keep button on a cat's card only appears once the player knows about adoptions: from the first family's
visit onward (a family is here, or a cat has already found a home). A cat already marked Keep still shows it."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "const st=$('#tStay'); st.hidden=!(c.age>=1);"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "const st=$('#tStay'); st.hidden=!(c.age>=1&&(W.homes.length>0||!!W.family||c.forever));")
open(P, 'w', encoding='utf-8').write(s); print('ok')
