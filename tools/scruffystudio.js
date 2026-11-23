// Side-by-side test renders of "neglected coat" looks (burrs vs. gentler ideas). Studio only, nothing here is in the game.
// In the game page's title screen: window.TS = await import('/tools/thumbstudio.js'); const S = await import('/tools/scruffystudio.js'); await S.sheet();
const TS = window.TS, T = THREE, { COAT, lin } = TS;
const L = (hex) => new T.MeshLambertMaterial({ color: hex });
const Lt = (hex, op) => new T.MeshLambertMaterial({ color: hex, transparent: true, opacity: op, depthWrite: false });
const SPH = new T.SphereGeometry(1, 10, 8), CONE = new T.ConeGeometry(1, 1, 6), CYL = new T.CylinderGeometry(1, 1, 1, 6), ICO = new T.IcosahedronGeometry(1, 0);
const mk = (geo, mat, p, s, r) => { const m = new T.Mesh(geo, mat); m.position.set(...p); m.scale.set(...s); if (r) m.rotation.set(...r); return m; };
const AX = [0.36, 0.33, 0.58];
const onBody = (dir, ax = AX) => { const d = new T.Vector3(...dir).normalize(); const t = 1 / Math.sqrt((d.x / ax[0]) ** 2 + (d.y / ax[1]) ** 2 + (d.z / ax[2]) ** 2); return d.multiplyScalar(t); };
const coatHex = (c) => '#' + c.bodyM.material.color.clone().convertLinearToSRGB().getHexString();
const mix = (a, b, k) => new T.Color(a).lerp(new T.Color(b), k).getHex();
const core = (c) => c.bodyM.parent;
const isEye = (c, o) => c.eyes.some((e) => e === o.parent);

// ---- looks ----
function burrs(c) { // the current game look
  [[0.55, 0.75, 0.2], [-0.5, 0.8, -0.25], [0.85, 0.25, -0.45], [-0.85, 0.3, 0.35], [0.15, 0.9, -0.6], [-0.2, 0.85, 0.55]].forEach((dir) => {
    const p = onBody(dir), g = new T.Group(); g.position.copy(p); g.scale.setScalar(1.3);
    g.add(mk(SPH, L(0x8f7436), [0, 0, 0], [0.055, 0.055, 0.055]));
    for (let i = 0; i < 5; i++) { const a = i * 1.26; g.add(mk(CONE, L(0x6b5326), [Math.cos(a) * 0.05, 0.02, Math.sin(a) * 0.05], [0.014, 0.05, 0.014], [Math.sin(a) * 1.2, 0, -Math.cos(a) * 1.2])); }
    g.add(mk(SPH, L(0x7fa54a), [0.05, 0.04, 0], [0.06, 0.012, 0.03], [0, 0, 0.5])); core(c).add(g); });
}
function dull(c, k = 0.3) { // flatter, greyer coat
  c.g.traverse((o) => { if (!o.isMesh || isEye(c, o) || !o.material.isMeshStandardMaterial) return; o.material = o.material.clone(); o.material.color.lerp(lin(0x8d8576), k); o.material.roughness = 1; });
}
function tufts(c, n = 1) { // bed-head: spikes of the cat's own fur
  const col = coatHex(c);
  const head = [[0, 0.27, -0.02, 0.25], [0.06, 0.26, -0.05, -0.35], [-0.07, 0.25, -0.04, 0.5]];
  head.slice(0, n === 1 ? 2 : 3).forEach(([x, y, z, r]) => c.head.add(mk(CONE, L(col), [x, y, z], [0.035, 0.11, 0.035], [-0.3, 0, r])));
  if (n > 1) [[0.4, 0.92, -0.2], [-0.35, 0.93, 0.15], [0.1, 0.98, -0.45]].forEach((d) => { const p = onBody(d); const g = new T.Group(); g.position.copy(p); g.lookAt(p.clone().multiplyScalar(2)); g.rotateX(Math.PI / 2);
    [[-0.02, 0.3], [0.02, -0.3]].forEach(([x, r]) => g.add(mk(CONE, L(col), [x, 0.03, 0], [0.03, 0.08, 0.03], [0, 0, r]))); core(c).add(g); });
  c.tail.forEach((m, i) => { if (i % 2) m.scale.multiplyScalar(1.3); });
}
function dusty(c) { // muddy socks + grubby belly
  const mud = 0x8a6a48;
  c.legs.forEach((Lg) => { const paw = Lg.children[1]; paw.material = paw.material.clone(); paw.material.color.lerp(lin(mud), 0.9);
    const shin = Lg.children[0], sl = new T.Mesh(shin.geometry, shin.material.clone()); sl.material.color.lerp(lin(mud), 0.75); sl.scale.set(shin.scale.x * 1.06, shin.scale.y * 0.32, shin.scale.z * 1.06); sl.position.y = -0.235; Lg.add(sl); });
  c.g.traverse((o) => { if (o.isMesh && o.userData.zone === 'belly' && o.material.isMeshStandardMaterial) { o.material = o.material.clone(); o.material.color.lerp(lin(mud), 0.35); } });
}
function leafTwig(c) { // a leaf caught on the head, a twig in the back fur
  const leaf = new T.Group(); leaf.position.set(0.2, 0.2, -0.02); leaf.rotation.set(0.3, -0.4, -0.7); leaf.scale.setScalar(1.25); c.head.add(leaf);
  leaf.add(mk(SPH, L(0xd9a23a), [0, 0, 0], [0.085, 0.012, 0.045])); leaf.add(mk(CYL, L(0x8a5a2b), [0.1, 0, 0], [0.006, 0.04, 0.006], [0, 0, Math.PI / 2]));
  const tw = new T.Group(); tw.position.copy(onBody([0.55, 0.85, -0.35])); tw.rotation.set(0.2, 0.7, 0.35); core(c).add(tw);
  tw.add(mk(CYL, L(0x7a5232), [0, 0, 0], [0.012, 0.22, 0.012], [0, 0, Math.PI / 2 - 0.15]));
  tw.add(mk(CYL, L(0x7a5232), [0.05, 0.03, 0], [0.008, 0.08, 0.008], [0, 0, 0.7]));
  tw.add(mk(SPH, L(0x6fa64a), [0.1, 0.055, 0], [0.03, 0.008, 0.017], [0, 0, 0.4]));
}
function dustPuff(c, scene) { // shown as a still; in game it would pop when the cat sits, lies down or shakes
  const p = c.g.position;
  [[0.38, 0.1, 0.2, 0.12], [0.48, 0.14, -0.05, 0.1], [-0.36, 0.09, 0.25, 0.1], [0.3, 0.22, 0.35, 0.07], [-0.44, 0.16, -0.1, 0.08], [0.56, 0.26, 0.12, 0.06]].forEach(([x, y, z, s]) =>
    scene.add(mk(ICO, Lt(0xe2d2b0, 0.42), [p.x + x * 1.15, y * 0.9 + 0.04, p.z + z * 1.3], [s * 1.5, s, s * 1.5])));
}
function matting(c) { // lumpy darker clumps on the flanks and haunches
  const col = mix(coatHex(c), 0x4a3a2c, 0.28);
  [[0.95, 0.2, -0.35], [0.9, 0.05, 0.25], [-0.95, 0.15, -0.3], [-0.9, 0.35, 0.3], [0.6, 0.35, -0.8], [0.7, -0.1, 0.55]].forEach((dir, i) => {
    const p = onBody(dir), g = new T.Group(); g.position.copy(p).multiplyScalar(0.97); core(c).add(g);
    [[0, 0, 0, 0.06], [0.03, 0.025, 0.035, 0.045], [-0.02, -0.03, 0.03, 0.04]].forEach(([x, y, z, s], j) => g.add(mk(ICO, L(col), [x, y, z], [s, s * 0.8, s * 1.1], [i, j, i * j]))); });
}

const LOOKS = {
  'Now: burrs': (c) => burrs(c),
  'Groom < 40: dull + bed-head': (c) => { tufts(c, 1); TS.upgrade(c.g); dull(c, 0.3); },
  'Groom < 25: + dusty paws, leaf, twig, dust': (c, s) => { tufts(c, 2); dusty(c); leafTwig(c); TS.upgrade(c.g); dull(c, 0.42); dustPuff(c, s); },
  'Alt: matting': (c) => { matting(c); TS.upgrade(c.g); dull(c, 0.15); },
};
const COATS = [COAT('orange', 'tabby', 0x8fd14f), COAT('black', 'solid', 0xf2c14e), COAT('cream', 'calico', 0x6ec3f0)];

function shot(coat, look, seed) {
  TS.rnd(seed);
  const { scene } = TS.stage({ sky: TS.skyTex([[0, '#8fd0f2'], [0.7, '#d6f0fb'], [1, '#fff6e2']]), hemi: [0xfff6e8, 0x6d8f55, 0.7], sun: { hex: 0xfff0d0, i: 1.7, p: [4, 8, 6], shadow: 3 }, exposure: 0.95 });
  scene.add(TS.ground(30, [0x7cc35e, 0x6fb853, 0x86cb66, 0x74bd58], 30, 0.05));
  scene.add(TS.grassTufts(30, 3, [0, 0], 0.9));
  const c = TS.cat(coat, { age: 1, state: 'idle', at: [0, 0, 0], yaw: 0, head: 1.15 });
  scene.add(c.g); LOOKS[look](c, scene); TS.upgrade(c.g);
  return TS.render(scene, TS.camAt(30, [2.5, 1.9, 2.3], [0, 0.48, -0.05]), { bloom: 0.15, vignette: 0.2, sat: 1.12 });
}

export async function sheet() {
  const names = Object.keys(LOOKS), cell = 420, head = 56, pad = 8;
  const out = document.createElement('canvas'); out.width = names.length * (cell + pad) + pad; out.height = head + COATS.length * (cell + pad) + pad;
  const x = out.getContext('2d'); x.fillStyle = '#f5efe4'; x.fillRect(0, 0, out.width, out.height);
  x.fillStyle = '#3b2f2a'; x.font = 'bold 19px system-ui, sans-serif'; x.textAlign = 'center';
  names.forEach((n, i) => x.fillText(n, pad + i * (cell + pad) + cell / 2, head - 20));
  COATS.forEach((coat, r) => names.forEach((n, i) => { const img = shot(coat, n, 5 + r);
    x.drawImage(img, 90, 60, 860, 860, pad + i * (cell + pad), head + r * (cell + pad), cell, cell); }));
  const png = out.toDataURL('image/png');
  await fetch('http://127.0.0.1:8767/th_scruffy_compare', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ png }) });
  return 'ok';
}
