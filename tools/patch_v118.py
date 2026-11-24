"""v118: scritches. Stroking the face (head, cheek, chin) allows hand speeds up to 35% faster before the cat finds
it too fast; small quick movements around the face read as scratches, not long strokes. Back/rump/belly unchanged."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("  const tf=tolFast(c);\n  if(x>tf){ // too fast",
    "  const tf=tolFast(c)+(['head','cheek','chin'].includes(zone)?Math.log(1.35):0); // face scritches may be 35% quicker\n  if(x>tf){ // too fast")
open(P, 'w', encoding='utf-8').write(s); print('ok')
