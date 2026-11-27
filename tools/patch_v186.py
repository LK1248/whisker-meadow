"""v186: the "Fewer helpers" shop item is gone. Letting a helper go gave no money back, and helpers already just stop
working when wages can't be paid, so it mostly invited a regretted choice."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
lines = [l for l in s.split('\n') if l.startswith("  {id:'fire',name:()=>'Fewer helpers'")]
if len(lines) != 1: sys.exit(f'fire item lines: {len(lines)}')
s = s.replace(lines[0] + '\n', '', 1)
for old, new in [("SHOP.filter(it=>it.id!=='fire'||paidN()).map(", "SHOP.map("),
                 (":it.id==='fire'?'Let one go':`$${cost}`", ":`$${cost}`")]:
    if s.count(old) != 1: sys.exit('no match: ' + old)
    s = s.replace(old, new)
if "'fire'" in s: sys.exit('leftover fire reference')
open(P, 'w', encoding='utf-8').write(s)
print('v186 applied')
