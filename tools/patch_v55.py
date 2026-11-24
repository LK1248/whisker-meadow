"""v55: a subtler groomed coat.
The old gloss added a crisp white highlight spot plus a lobe, which read as wet (seal-like), especially on dark cats.
Now it's a soft, wide sheen tinted by the coat's own colour, plus a faint velvety rim at the silhouette,
so a well-groomed cat looks soft and clean rather than slick. The stars and chime on reaching 85 groom stay."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("// glossy coat: the same toon material plus a specular highlight (a crisp stepped spot and a soft lobe around it)",
    "// groomed coat: the same toon material plus a soft sheen (a wide, coat-tinted lobe and a faint velvety rim; no crisp highlight, so it never looks wet)")
rep("    ' vec3 hv=normalize(directLight.direction+geometry.viewDir); float nh=max(dot(geometry.normal,hv),0.0); float sp=pow(nh,90.0); float soft=pow(nh,16.0);'+\n"
    "    ' reflectedLight.directDiffuse += directLight.color*(smoothstep(0.3,0.5,sp)*0.5+soft*0.12);')); };",
    "    ' vec3 hv=normalize(directLight.direction+geometry.viewDir); float nh=max(dot(geometry.normal,hv),0.0); float nl=max(dot(geometry.normal,directLight.direction),0.0);'+\n"
    "    ' float rim=pow(1.0-max(dot(geometry.normal,geometry.viewDir),0.0),3.0); vec3 tint=mix(vec3(0.5),material.diffuseColor,0.55);'+\n"
    "    ' reflectedLight.directDiffuse += directLight.color*tint*(pow(nh,8.0)*0.1+rim*nl*0.16);')); };")
open(P, 'w', encoding='utf-8').write(s); print('ok')
