"""Draw the app icons (img/icon-192.png, img/icon-512.png, img/icon-maskable-512.png): a cream cat face on a meadow-green tile."""
import pathlib
from PIL import Image, ImageDraw

root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'img'; out.mkdir(exist_ok=True)

def face(size=1024, pad=0.0):
    S = size; im = Image.new('RGBA', (S, S), (95, 179, 90, 255)); d = ImageDraw.Draw(im)
    d.ellipse([S*-.3, S*.72, S*1.3, S*1.5], fill=(79, 160, 74, 255))  # hill
    k = 1 - pad * 2; ox = oy = S * pad
    def P(x, y): return (ox + x * S * k, oy + y * S * k)
    def box(x0, y0, x1, y1): return [*P(x0, y0), *P(x1, y1)]
    cream, ink, pink = (255, 244, 223, 255), (74, 52, 38, 255), (255, 122, 162, 255)
    for sx in (1, -1):  # ears
        cx = .5 + .2 * sx
        d.polygon([P(cx - .14, .42), P(cx + .1 * sx, .14), P(cx + .14, .42)], fill=cream)
        d.polygon([P(cx - .07, .38), P(cx + .07 * sx, .22), P(cx + .07, .38)], fill=pink)
    d.ellipse(box(.2, .3, .8, .82), fill=cream)  # head
    for sx in (1, -1):  # eyes
        cx = .5 + .12 * sx
        d.ellipse(box(cx - .055, .48, cx + .055, .6), fill=ink)
        d.ellipse(box(cx - .02 + .015, .5, cx + .02 + .015, .54), fill=(255, 255, 255, 255))
    d.polygon([P(.47, .63), P(.53, .63), P(.5, .665)], fill=pink)  # nose
    for sx in (1, -1):  # whiskers
        for dy in (-.015, .02):
            d.line([P(.5 + .1 * sx, .66 + dy * .5), P(.5 + .27 * sx, .64 + dy * 2)], fill=ink, width=int(S * .008))
    return im

face().resize((512, 512), Image.LANCZOS).save(out / 'icon-512.png')
face().resize((192, 192), Image.LANCZOS).save(out / 'icon-192.png')
face(pad=.1).resize((512, 512), Image.LANCZOS).save(out / 'icon-maskable-512.png')  # face inside the safe zone
print('icons written')
