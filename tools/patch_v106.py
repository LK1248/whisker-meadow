"""v106: 'trust' is gone; Love is the one bond stat. Love used to be stored as s.trust with s.aff as an alias for it, so
this is a rename that keeps play the same: love lives in s.aff, every trust read/write now uses it, a cat's
starting love is c.love0, and the score/summary read love. Old saves (s.trust, trust0) load into love."""
import re, sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# 1) cat creation: default stats, starting love, and the old alias -> a one-time migration of old saves
rep("s:Object.assign({trust:30,aff:25,health:65,", "s:Object.assign({aff:30,health:65,")
rep("cat.trust0=cat.s.trust; if(!o.loading", "if(!o.loading")
rep("const love='trust' in os&&'aff' in os?Math.max(os.trust,os.aff):'trust' in os?os.trust:'aff' in os?os.aff:30;\n"
    "    delete st.aff; st.trust=love; Object.defineProperty(st,'aff',{get(){ return this.trust; },set(v){ this.trust=v; },enumerable:false,configurable:true}); }",
    "const love='trust' in os&&'aff' in os?Math.max(os.trust,os.aff):'trust' in os?os.trust:'aff' in os?os.aff:30; // old saves kept love under 'trust'\n"
    "    delete st.trust; st.aff=love; cat.love0=love; }")

# 2) literal stat blocks: {trust:A,aff:B,...} -> {aff:max-ish,...}
rep("s:{trust:55,aff:50,", "s:{aff:55,")
rep("s:{trust:rand(15,25),aff:rand(15,25),", "s:{aff:rand(15,25),", count=2)
rep("s:{trust:rand(25,40),aff:rand(25,40),", "s:{aff:rand(25,40),")
rep("s:{trust:rand(10,20),aff:rand(10,20),", "s:{aff:rand(10,20),")
rep("Object.assign(c.s,{trust:95,aff:95,", "Object.assign(c.s,{aff:95,")
rep("s:{trust:46,aff:42,", "s:{aff:46,")
rep("s:{trust:22,aff:18,", "s:{aff:22,")
rep("s:{trust:45,aff:40,", "s:{aff:45,")

# 3) starting love (Most Improved, patient adopter) and save/load
rep("c.trust0", "c.love0", count=s.count("c.trust0"))
rep("trust0:c.love0,", "love0:c.love0,")
rep("trust0:s.trust0??c.s.trust,", "love0:s.love0??s.trust0??c.s.aff,")

# 4) score and end-of-game summary
rep("avg('trust')*2", "avg('aff')*2")
rep("trust:Math.round(avg('trust')),", "love:Math.round(avg('aff')),")
rep("['Love',r.trust]", "['Love',r.love]")

# 5) every remaining stat read/write: <x>.trust -> <x>.aff
s, n = re.subn(r"\b(s|c\.s|x\.s|y\.s|a\.s|b\.s|cat\.s)\.trust\b", r"\1.aff", s)
print('renamed stat refs:', n)

# 6) names, comments and help text
rep("trustIco", "loveIco", count=s.count("trustIco"))
rep("// kittens learn to trust faster", "// kittens warm up faster")
rep("belly rubs (only with high trust)", "belly rubs (only with high love)")
rep("you earn their trust, keep them", "you win their love, keep them")
rep("if it doesn't trust you yet, it scratches", "if it isn't fond of you yet, it scratches")

left = [m.start() for m in re.finditer('trust', s)]
for i in left: print('LEFT:', s[max(0,i-60):i+40].replace('\n',' '))
open(P, 'w', encoding='utf-8').write(s); print('ok')
