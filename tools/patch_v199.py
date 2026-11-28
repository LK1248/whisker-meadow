"""v199: calmer fair results. Trophy cards no longer pop up as each cat comes home from the fair.
Results collect and show at most once every 90 s of play. When more than one is waiting, a single card shows them all
(photo, ribbon, name, category and prize for each cat) with the total and one Collect button. It waits on the same
things as other cards (lessons, petting, other cards, the 4 s gap). The very first ribbon still shows right away.
Prize money is still added when the cat comes home, as before."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# CSS for the montage
rep(".fairpic .fb{position:absolute;left:6px;top:4px;width:78px;height:78px}",
    ".fairpic .fb{position:absolute;left:6px;top:4px;width:78px;height:78px}\n"
    ".awards{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:2px 0 6px}\n"
    ".awards .aw{position:relative;background:#fff8ef;border-radius:16px;padding:6px 6px 8px;text-align:center;box-shadow:0 2px 6px rgba(60,40,30,.1)}\n"
    ".awards .aw img{width:100%;border-radius:12px;display:block}\n"
    ".awards .aw .fb{position:absolute;left:2px;top:2px;width:46px;height:46px}\n"
    ".awards .aw b{display:block;font:700 17px var(--display);margin-top:4px}\n"
    ".awards .aw span{display:block;font:600 14px var(--display);color:var(--pinkd)}\n"
    ".awards .aw i{display:block;font:700 20px var(--display);font-style:normal;color:var(--leafd)}\n"
    ".awards.c3{grid-template-columns:1fr 1fr 1fr;gap:7px}.awards.c3 .aw{padding:4px 4px 6px}.awards.c3 .aw .fb{width:34px;height:34px}\n"
    ".awards.c3 .aw b{font-size:14px}.awards.c3 .aw span{font-size:11px;line-height:1.15}.awards.c3 .aw i{font-size:16px}")

# returnFromShow: queue the result instead of opening a card
a = s.index("  const col=['','#ffcf3f','#c9d3de','#e1a06a'][place], lbl=place+['','st','nd','rd'][place];\n  const shot=fairShot(c,place);\n  showCard(")
end_mark = "  $('#collect').onclick=closeModal; });\n}\n"
b = s.index(end_mark, a) + len(end_mark)
old_card = s[a:b]
rep(old_card,
    "  AW.list.push({name:c.name,cat,place,prize,shiny,shot:fairShot(c,place)});\n"
    "  if(W.ribbons===1)AW.at=0; /* the very first ribbon shows right away */ else if(AW.list.length===1)AW.at=Math.max(AW.at,W.time+20); /* give other cats a moment to come home too */\n"
    "}\n"
    "// fair results: collected and shown together, at most once every AW_GAP seconds\n"
    "const AW={list:[],at:0,queued:false}, AW_GAP=90;\n"
    "function ribbonSVG(place,cls,sz){ const col=['','#ffcf3f','#c9d3de','#e1a06a'][place], lbl=place+['','st','nd','rd'][place];\n"
    "  return `<svg ${cls?`class=\"${cls}\"`:''} viewBox=\"0 0 100 100\" width=\"${sz}\" height=\"${sz}\"><path d=\"M34 52L20 96l16-8 10 12 8-40zM66 52l14 44-16-8-10 12-8-40z\" fill=\"#5b8def\"/><circle cx=\"50\" cy=\"38\" r=\"30\" fill=\"${col}\" stroke=\"rgba(0,0,0,.12)\" stroke-width=\"4\"/><text x=\"50\" y=\"47\" text-anchor=\"middle\" font-family=\"Fredoka,sans-serif\" font-weight=\"700\" font-size=\"26\" fill=\"#4a3426\">${lbl}</text></svg>`; }\n"
    "const SHINE='<div class=\"shine\"><i></i><i></i><i></i><i></i><i></i></div>';\n"
    "function awardCard(){ AW.queued=false; const L=AW.list.splice(0); if(!L.length){ cardOpen=false; return; } AW.at=W.time+AW_GAP;\n"
    "  if(L.length===1){ const a=L[0], shot=a.shot;\n"
    "    openModal(`<div class=\"${shot?'fairpic':'center'}\">${shot?`<img src=\"${shot}\" alt=\"\">`:''}${shot&&a.shiny?SHINE:''}${ribbonSVG(a.place,shot?'fb':'',shot?78:120)}</div>\n"
    "    <h3 class=\"center\" style=\"margin:0\">${a.name}</h3><div class=\"center\" style=\"font:600 19px var(--display);color:var(--pinkd)\">${a.cat}</div><div class=\"prize\">+$${a.prize}</div><button class=\"big\" id=\"collect\">Collect</button>`,true); }\n"
    "  else { const tot=L.reduce((t,a)=>t+a.prize,0);\n"
    "    openModal(`<div class=\"awards ${L.length>=3?'c3':''}\">${L.map(a=>`<div class=\"aw\">${a.shot?`<img src=\"${a.shot}\" alt=\"\">`:''}${ribbonSVG(a.place,'fb',46)}<b>${a.name}</b><span>${a.cat}</span><i>+$${a.prize}</i></div>`).join('')}</div>\n"
    "    <div class=\"prize\">+$${tot}</div><button class=\"big\" id=\"collect\">Collect</button>`,true); }\n"
    "  $('#collect').onclick=()=>{ Snd.coin(); closeModal(); }; }\n"
    "function awardTick(){ if(AW.list.length&&!AW.queued&&W.time>=AW.at&&!W.paused){ AW.queued=true; showCard(awardCard); } }\n")

# check every frame, next to the card queue
rep("  if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused&&uiGapOk()&&!petRecent()){ const fn=cardQ.shift();",
    "  awardTick();\n  if(cardQ.length&&$('#modal').hidden&&!cam.meet&&!W.paused&&uiGapOk()&&!petRecent()){ const fn=cardQ.shift();")
rep("window.__wm={i18nMiss:T.miss,", "window.__wm={AW,cardQ,uiGapOk,petRecent,i18nMiss:T.miss,")
open(P, 'w', encoding='utf-8').write(s)
print('v199 applied')
