"""v100: fix v97's slip. An inline // comment in startBlinkTut swallowed the rest of its line, so the slow-blink lesson
showed its overlay but never actually started: no lock, no hold on the cat, panning and taps all still worked, and the
bubble never cleared."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "if(bt.c||intro.c||pl.a||firstAdopt()||tutLock())return; // never barge into another lesson Object.assign(bt,"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "if(bt.c||intro.c||pl.a||firstAdopt()||tutLock())return; /* never barge into another lesson */ Object.assign(bt,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
