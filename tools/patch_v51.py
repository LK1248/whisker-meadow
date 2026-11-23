"""v51:
- Hint bubbles show icons instead of words (feed, shop item, play, scoop, carry, fair, roof, more room, ...).
- A slow-blinking cat turns its body part of the way toward the camera, so the blink is seen face-on.
- New brush icon everywhere (dock tool, hints, brush lesson, flea tip): a grooming brush with a head, bristles and a handle."""
import re, sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- brush icon ----
BRUSH_IN = ('<g transform="rotate(-35 12 12)"><rect x="2.5" y="6.5" width="12.5" height="6.2" rx="2.6" fill="currentColor"/>'
            '<path d="M4.6 13.6v3.4M7.3 13.6v3.4M10 13.6v3.4M12.7 13.6v3.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>'
            '<path d="M15 9.6h6.8" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/></g>')
m = re.search(r'(data-tool="brush" aria-label="Brush">)<svg.*?</svg>', s); assert m
s = s[:m.start()] + m.group(1) + f'<svg viewBox="0 0 24 24">{BRUSH_IN}</svg>' + s[m.end():]
m = re.search(r"BRUSH_HINT='<svg.*?</svg>';", s); assert m
s = s[:m.start()] + f"BRUSH_HINT='<svg viewBox=\"0 0 24 24\" width=\"30\" height=\"30\" style=\"color:#4a3426\">{BRUSH_IN}</svg>';" + s[m.end():]
m = re.search(r"const BRUSH_ICON='<svg.*?</svg>';", s); assert m
s = s[:m.start()] + f"const BRUSH_ICON='<svg viewBox=\"0 0 24 24\" width=\"34\" height=\"34\" style=\"color:#4a3426\">{BRUSH_IN}</svg>';" + s[m.end():]
m = re.search(r'<g transform="translate\(92 6\) scale\(2\)" fill="none" stroke="#8a6a52".*?</g>', s); assert m
s = s[:m.start()] + f'<g transform="translate(92 6) scale(2)" color="#8a6a52">{BRUSH_IN}</g>' + s[m.end():]

# ---- hint icons ----
rep("const GUIDE_LABEL={", """// hint bubble icons (wordless)
const hIco=(inner,w=30)=>`<svg viewBox="0 0 24 24" width="${w}" height="${w}" style="vertical-align:middle">${inner}</svg>`;
const sized=(svg,w,h)=>svg.replace('<svg ',`<svg width="${w}" height="${h}" style="vertical-align:middle" `);
const toolIco=t=>{ const e=$(`[data-tool=${t}] svg`); return e?sized(e.outerHTML.replace(/ width="[^"]*"| height="[^"]*"/g,''),30,30).replace('style="','style="color:#4a3426;'):''; };
const H_HEART='<path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z" fill="#ff6f99"/>';
const H_LOOK='<circle cx="10" cy="10" r="6" fill="#fff6ea" stroke="#4a3426" stroke-width="2.4"/><path d="M14.5 14.5L20 20" stroke="#4a3426" stroke-width="3" stroke-linecap="round"/>';
const H_EYES='<svg viewBox="0 0 72 30" width="54" height="23" style="vertical-align:middle"><g fill="none" stroke="#4a3426" stroke-width="5" stroke-linecap="round"><path d="M6 10q12 12 24 0"/><path d="M42 10q12 12 24 0"/></g></svg>';
const H_BAG='<path d="M4 9h16l-1.5 11h-13z" fill="#ff8fb1"/><path d="M8 9V7a4 4 0 0 1 8 0v2" fill="none" stroke="#4a3426" stroke-width="2.2"/>';
const H_SWAY='<span style="font-size:24px;vertical-align:middle"> ⇆</span>';
const GUIDE_LABEL={""")
H = {
 "label:'Stroke gently'": "label:()=>sized(HOURGLASS,22,26)+hIco(H_HEART,26)",
 "label:()=>'Find '+(W.runaway?W.runaway.c.name:'')": "label:()=>hIco(H_LOOK)+sized(PAWS_SVG,34,26)",
 "label:'Pick a cat'": "label:()=>sized(FAM_SVG,40,30)+hIco(H_HEART,24)",
 "label:'Feed'": "label:()=>hIco(IC.food)",
 "label:'Blink back!'": "label:()=>H_EYES+hIco(H_HEART,24)",
 "label:'Hold to carry'": "label:()=>`<svg viewBox=\"0 0 64 50\" width=\"42\" height=\"33\" style=\"vertical-align:middle\">${catFace(22,'#f3a64a').replace('translate(22,25)','translate(22,30)')}<path d=\"M50 42V12m-8 8l8-8 8 8\" fill=\"none\" stroke=\"#4a3426\" stroke-width=\"4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>`",
 "label:'Scoop'": "label:()=>hIco(IC.litter)",
 "label:()=>GUIDE_LABEL[guidePick('shop')]||'Shop'": "label:()=>hIco(IC[guidePick('shop')]||H_BAG)",
 "label:'Play'": "label:()=>toolIco('wand')",
 "label:'Drag · Flick · Hold'": "label:()=>toolIco('wand')+H_SWAY",
 "label:'Pet'": "label:()=>toolIco('hand')",
 "label:'Cat fair!'": "label:()=>fairBadge(0,30)",
 "label:'Rain roof'": "label:()=>hIco(IC.shelter)",
 "label:'More room'": "label:()=>hIco(IC.expand)",
}
for a, b in H.items(): rep(a, b)
# icon-only bubbles: a little tighter
rep("#hint .lab{position:absolute;left:0;top:-70px;", "#hint .lab{position:absolute;left:0;top:-70px;display:flex;align-items:center;gap:4px;line-height:0;")

# ---- slow blink: turn toward the camera ----
rep("const yaw=angDiff(c.heading,Math.atan2(camera.position.x-p.x,camera.position.z-p.z)); hy=clamp(yaw,-1.1,1.1);",
    "const yaw=angDiff(c.heading,Math.atan2(camera.position.x-p.x,camera.position.z-p.z));\n"
    "    // turn the body part way round, so the blink reads face-on (the head does the rest)\n"
    "    if(['idle','watch','shelter'].includes(c.state)&&!(c.hopT>0)){ const ex=yaw-clamp(yaw,-0.35,0.35); c.heading+=ex*Math.min(1,dt*2.2); }\n"
    "    hy=clamp(angDiff(c.heading,Math.atan2(camera.position.x-p.x,camera.position.z-p.z)),-1.1,1.1);")
rep("window.__wm={Snd,", "window.__wm={Snd,HINTS,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
