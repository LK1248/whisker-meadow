"""Lists candidate player-visible English strings in whisker-meadow.html (with ${...} turned into {0},{1}...).
Usage: python tools/i18n_extract.py OUT.txt   -> lines of "line<TAB>text". Used to build tools/i18n_strings.json."""
import re, sys

s = open('whisker-meadow.html', encoding='utf-8').read()
cands = {}
BAD = re.compile(r"[;=]|=>|&&|\|\||\bc\.|\bW\.|px\b|rgba|#[0-9a-fA-F]{3,6}\b|translate\(|\(\)|function|return|\bvar\(|\.\w+\(|^[a-z]+[A-Z]\w*$|^[a-z_]+$|viewBox|^M\d")


def add(t, ln):
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) < 2 or not re.search(r'[A-Za-z]{2}', t) or BAD.search(t):
        return
    cands.setdefault(t, ln)


def templates(src):
    i, n = 0, len(src)
    while True:
        i = src.find('`', i)
        if i < 0:
            return
        j, buf, args = i + 1, '', 0
        while j < n:
            ch = src[j]
            if ch == '\\':
                buf += src[j:j + 2]; j += 2; continue
            if ch == '`':
                break
            if src.startswith('${', j):
                k, d = j + 2, 1
                while k < n and d > 0:
                    if src[k] == '{': d += 1
                    elif src[k] == '}': d -= 1
                    elif src[k] == '`':
                        k = src.find('`', k + 1)
                    k += 1
                buf += '{%d}' % args; args += 1; j = k; continue
            buf += ch; j += 1
        yield i, buf
        i = j + 1


for pos, b in templates(s):
    ln = s.count('\n', 0, pos) + 1
    for part in re.split(r'<[^>]*>', b):
        add(part, ln)
for m in re.finditer(r"'((?:[^'\\\n]|\\.){2,200})'", s):
    t = m.group(1)
    if ' ' in t or re.match(r'^[A-Z][a-z]+!?$', t):
        add(t.replace("\\'", "'"), s.count('\n', 0, m.start()) + 1)
for m in re.finditer(r'"([^"\n]{2,200})"', s):
    t = m.group(1)
    if re.match(r'^[A-Z][^{}]*$', t) and ' ' in t:
        add(t, s.count('\n', 0, m.start()) + 1)
for m in re.finditer(r'>([^<>`]{2,400})<', s):
    add(m.group(1), s.count('\n', 0, m.start()) + 1)

lst = sorted(cands.items(), key=lambda x: x[1])
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(f'{ln}\t{t}' for t, ln in lst))
print(len(lst))
