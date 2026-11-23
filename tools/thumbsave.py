"""Move thumbnail renders POSTed to the sim receiver (tools/sim/out/th_*.json) into docs/thumbs3d/*.png."""
import base64, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src, dst = root / 'tools/sim/out', root / 'docs/thumbs3d'
dst.mkdir(parents=True, exist_ok=True)
for p in sorted(src.glob('th_*.json')):
    d = json.loads(p.read_text())
    (dst / (p.stem[3:] + '.png')).write_bytes(base64.b64decode(d['png'].split(',', 1)[1]))
    p.unlink(); print('saved', p.stem[3:] + '.png')
