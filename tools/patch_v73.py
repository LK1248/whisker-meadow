"""v73: no belly offer (flop) during the first petting lesson or any other lesson."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("if(r<0.28&&s.aff>=35&&c.state==='pet'){ setState(c,'flop',7);", "if(r<0.28&&s.aff>=35&&c.state==='pet'&&!lessonOn()){ setState(c,'flop',7);")
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep("if(r<0.43&&s.aff>35&&s.fun>30&&c.age>0.3){ setState(c,'flop'", "if(r<0.43&&s.aff>35&&s.fun>30&&c.age>0.3&&!(lessonOn()&&(c===intro.c||c===bt.c||c===pl.a||c===br.c))){ setState(c,'flop'")
open(P, 'w', encoding='utf-8').write(s); print('ok2')
