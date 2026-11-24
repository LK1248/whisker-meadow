"""v107: Mochi starts a new game already in her petting-lesson pose (side-on to the opening camera, standing still),
so she doesn't swing round when the first lesson begins."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
old = "makeCat({name:'Mochi',sex:'f',trait:'cuddly',buttLike:true,coat:{base:'orange',pattern:'tabby',eye:0x8fd14f},x:-0.8,z:0.3,s:{aff:46,health:72,full:80,fun:75,groom:62}});"
if s.count(old) != 1: sys.exit('no match')
s = s.replace(old, "{ const m=makeCat({name:'Mochi',sex:'f',trait:'cuddly',buttLike:true,coat:{base:'orange',pattern:'tabby',eye:0x8fd14f},x:-0.8,z:0.3,s:{aff:46,health:72,full:80,fun:75,groom:62}});\n"
              "  if(m){ m.heading=0.55+Math.PI/2; m.g.rotation.y=m.heading; setState(m,'idle',8); } } // already in the petting-lesson pose (opening camera theta 0.55)")
open(P, 'w', encoding='utf-8').write(s); print('ok')
