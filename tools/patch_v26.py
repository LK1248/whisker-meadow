"""v26: playful cats sometimes slip out to explore, whatever their trust."""
import sys
P='whisker-meadow.html'; s=open(P,encoding='utf-8').read()
old="const cand=active().filter(c=>c.s.trust<22&&!c.carried"
if s.count(old)!=1: sys.exit('no match')
s=s.replace(old,"const cand=active().filter(c=>(c.s.trust<22||(c.trait==='playful'&&c.age>=0.5&&Math.random()<0.5))&&!c.carried")
open(P,'w',encoding='utf-8').write(s); print('ok')
