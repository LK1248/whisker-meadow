// Whisker Meadow thumbnail studio.
// Load inside the game page on its title screen (nothing is saved before Play):
//   const TS = await import('/tools/thumbstudio.js'); const url = await TS.shoot('boxDusk');
// Reuses the game's own cats, people and props, then re-lights them for stills: faceted standard
// materials, ACES tone mapping, soft shadows, 2x supersampling, and a 2D pass for bloom, vignette and tilt-shift.
const w = window.__wm, T = THREE;
export const SIZE = 1024, SS = 2;
let R = null;
const rnd = (() => { let a = 7; return (s) => { if (s !== undefined) a = s; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; })();
const rr = (a, b) => a + rnd() * (b - a);
const lin = (hex) => new T.Color(hex).convertSRGBToLinear();

function renderer() {
  if (R) return R;
  R = new T.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  R.setPixelRatio(1); R.setSize(SIZE * SS, SIZE * SS, false);
  R.shadowMap.enabled = true; R.shadowMap.type = T.PCFSoftShadowMap;
  R.outputEncoding = T.sRGBEncoding; R.toneMapping = T.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  return R;
}

// ---------- materials: the game's toon look -> faceted, lit low-poly ----------
const LOWSPH = new T.SphereGeometry(1, 16, 12), mats = new Map();
function std(hex, o = {}) {
  const key = hex + JSON.stringify(o); if (mats.has(key)) return mats.get(key);
  const m = new T.MeshStandardMaterial(Object.assign({ color: lin(hex), roughness: 0.78, metalness: 0, flatShading: true }, o));
  if (o.emissive !== undefined) m.emissive = lin(o.emissive);
  mats.set(key, m); return m;
}
export function upgrade(root, { facet = true, rough = 0.78, lowSph = true } = {}) {
  root.traverse((o) => {
    if (o.isSprite) { o.visible = false; return; }
    if (!o.isMesh) return; o.castShadow = true; o.receiveShadow = true;
    const m = o.material; if (!m || m.userData.ts) return;
    if (lowSph && o.geometry && o.geometry.type === 'SphereGeometry' && o.geometry.parameters.widthSegments >= 18) o.geometry = LOWSPH;
    if (m.isShaderMaterial) { o.visible = false; return; }
    if (m.map) { m.map.encoding = T.sRGBEncoding; m.needsUpdate = true; m.userData.ts = 1; return; }
    const basic = m.isMeshBasicMaterial;
    const n = basic ? new T.MeshBasicMaterial({ color: m.color.clone().convertSRGBToLinear(), transparent: m.transparent, opacity: m.opacity })
      : new T.MeshStandardMaterial({ color: m.color.clone().convertSRGBToLinear(), roughness: rough, metalness: 0, flatShading: facet, transparent: m.transparent, opacity: m.opacity, side: m.side });
    n.userData.ts = 1; o.material = n;
  });
  return root;
}

// ---------- game actors ----------
const COAT = (base, pattern = 'solid', eye = 0x8fd14f) => ({ base, pattern, eye });
export function cat(coat, o = {}) {
  const c = w.makeCat({ coat, age: o.age ?? 1, name: o.name || 'Studio' + rnd().toString(36).slice(2, 6), s: { groom: 100, trust: 90, aff: 90, health: 100 } });
  const i = w.W.cats.indexOf(c); if (i >= 0) w.W.cats.splice(i, 1);
  if (c.g.parent) c.g.parent.remove(c.g);
  pose(c, o.state || 'idle', o);
  if (o.head) c.head.scale.multiplyScalar(o.head); // bigger head reads better at thumbnail size
  upgrade(c.g, o);
  if (o.at) c.g.position.set(...o.at);
  if (o.yaw !== undefined) c.g.rotation.y = o.yaw;
  if (o.scale) c.g.scale.multiplyScalar(o.scale);
  return c;
}
function pose(c, st, o) {
  c.stT = 999; c.speed = o.speed || 0; if (o.flop) c.greetFlop = 1; Object.assign(c, o.set || {});
  const t0 = o.t || 1.3;
  for (let i = 0; i < 120; i++) { c.state = st; c.stT = 999; c.blink = 0; c.slowBlink = o.slowBlink || 0; Object.assign(c, o.set || {}); w.animateCat(c, 1 / 60, t0 + i / 600); }
  c.heading = o.yaw ?? c.heading;
}
export function person(o = {}) { const p = w.personMesh(o); upgrade(p.g); if (o.at) p.g.position.set(...o.at); if (o.yaw !== undefined) p.g.rotation.y = o.yaw; if (o.scale) p.g.scale.setScalar(o.scale); return p; }
export function item(kind, tier = 3) {
  const was = w.W.tier[kind]; w.W.tier[kind] = tier; const it = { kind, mesh: new T.Group(), portions: 6, cap: 6, dirt: 0 };
  try { w.buildItem(it); } finally { w.W.tier[kind] = was; } upgrade(it.mesh); return it.mesh;
}

// ---------- low-poly set pieces ----------
const box = (sx, sy, sz, hex, o = {}) => { const m = new T.Mesh(new T.BoxGeometry(sx, sy, sz), std(hex, o.m)); m.castShadow = m.receiveShadow = true; if (o.p) m.position.set(...o.p); if (o.r) m.rotation.set(...o.r); return m; };
const ico = (r, hex, det = 0, o = {}) => { const m = new T.Mesh(new T.IcosahedronGeometry(r, det), std(hex, o.m)); m.castShadow = m.receiveShadow = true; if (o.p) m.position.set(...o.p); if (o.s) m.scale.set(...o.s); return m; };
const cyl = (rt, rb, h, seg, hex, o = {}) => { const m = new T.Mesh(new T.CylinderGeometry(rt, rb, h, seg), std(hex, o.m)); m.castShadow = m.receiveShadow = true; if (o.p) m.position.set(...o.p); if (o.r) m.rotation.set(...o.r); return m; };

export function ground(size = 40, hexes = [0x7cc35e, 0x6fb853, 0x86cb66, 0x74bd58], seg = 34, bump = 0.12) {
  const g = new T.PlaneGeometry(size, size, seg, seg).toNonIndexed(); g.rotateX(-Math.PI / 2);
  const p = g.attributes.position; const cols = []; const keyed = new Map();
  for (let i = 0; i < p.count; i++) { const k = p.getX(i).toFixed(2) + ',' + p.getZ(i).toFixed(2); if (!keyed.has(k)) keyed.set(k, rr(-bump, bump)); p.setY(i, keyed.get(k)); }
  for (let f = 0; f < p.count / 3; f++) { const c = lin(hexes[Math.floor(rnd() * hexes.length)]); for (let k = 0; k < 3; k++) cols.push(c.r, c.g, c.b); }
  g.setAttribute('color', new T.Float32BufferAttribute(cols, 3)); g.computeVertexNormals();
  const m = new T.Mesh(g, new T.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 0.95 })); m.receiveShadow = true; return m;
}
export function tree(s = 1, hex = 0x5eae4f) {
  const g = new T.Group(); g.add(cyl(0.12, 0.18, 1.4, 6, 0x8a5a3b, { p: [0, 0.7, 0] }));
  g.add(ico(0.9, hex, 0, { p: [0, 1.9, 0] })); g.add(ico(0.62, hex, 0, { p: [0.45, 1.55, 0.2] })); g.add(ico(0.55, hex, 0, { p: [-0.42, 1.65, -0.15] }));
  g.scale.setScalar(s); return g;
}
export function pine(s = 1, hex = 0x3f8f5a) { const g = new T.Group(); g.add(cyl(0.1, 0.14, 0.6, 6, 0x7a4a2a, { p: [0, 0.3, 0] })); [[0.85, 1.0, 0.9], [0.65, 0.9, 1.5], [0.42, 0.8, 2.05]].forEach(([r, h, y]) => { const c = new T.Mesh(new T.ConeGeometry(r, h, 7), std(hex)); c.position.y = y; c.castShadow = true; g.add(c); }); g.scale.setScalar(s); return g; }
export function bush(s = 1, hex = 0x6fbf5a) { const g = new T.Group(); g.add(ico(0.5, hex, 0, { p: [0, 0.35, 0] })); g.add(ico(0.38, hex, 0, { p: [0.4, 0.26, 0.1] })); g.add(ico(0.34, hex, 0, { p: [-0.38, 0.24, -0.05] })); g.scale.setScalar(s); return g; }
export function flowers(n, area, cols = [0xffffff, 0xffd84d, 0xff9ec7, 0xb89cff, 0xff8a65], center = [0, 0], keepOut = 0) {
  const g = new T.Group();
  for (let i = 0; i < n; i++) { let x, z; do { x = center[0] + rr(-area, area); z = center[1] + rr(-area, area); } while (Math.hypot(x - center[0], z - center[1]) < keepOut);
    const f = new T.Group(); f.position.set(x, 0, z); f.add(cyl(0.012, 0.012, 0.22, 4, 0x5fa443, { p: [0, 0.11, 0] }));
    const head = ico(0.06, cols[Math.floor(rnd() * cols.length)], 0, { p: [0, 0.23, 0], s: [1, 0.6, 1] }); f.add(head); g.add(f); }
  return g;
}
export function grassTufts(n, area, center = [0, 0], keepOut = 0, hex = 0x5aa845) {
  const g = new T.Group(), geo = new T.ConeGeometry(0.05, 0.28, 3);
  for (let i = 0; i < n; i++) { let x, z; do { x = center[0] + rr(-area, area); z = center[1] + rr(-area, area); } while (Math.hypot(x - center[0], z - center[1]) < keepOut);
    for (let k = 0; k < 3; k++) { const b = new T.Mesh(geo, std(hex)); b.position.set(x + rr(-.06, .06), 0.12, z + rr(-.06, .06)); b.rotation.set(rr(-.3, .3), rr(0, 3), rr(-.3, .3)); b.castShadow = true; g.add(b); } }
  return g;
}
export function house() {
  const g = new T.Group();
  g.add(box(3.4, 2, 2.4, 0xfff1dc, { p: [0, 1, 0] }));
  const roof = new T.Mesh(new T.CylinderGeometry(1.6, 1.6, 3.9, 3, 1), std(0xd0583f)); roof.rotation.set(0, 0, Math.PI / 2); roof.rotation.x = Math.PI / 2; roof.rotation.z = Math.PI / 2; roof.scale.set(1, 1, 0.62); roof.position.y = 2.55; roof.castShadow = true;
  const r2 = new T.Mesh(new T.CylinderGeometry(1.75, 1.75, 3.9, 3, 1), std(0xd0583f)); r2.rotation.z = Math.PI / 2; r2.rotation.x = -Math.PI / 2; r2.scale.set(1, 1, 0.55); r2.position.y = 2.62; r2.castShadow = true; g.add(r2);
  g.add(box(0.35, 0.8, 0.35, 0xb58b63, { p: [1, 3.2, -0.4] }));
  g.add(box(0.72, 1.24, 0.06, 0x8a5a3b, { p: [0, 0.62, 1.21] }));
  for (const sx of [-1.05, 1.05]) { g.add(box(0.68, 0.58, 0.05, 0xffffff, { p: [sx, 1.25, 1.21] })); g.add(box(0.56, 0.46, 0.06, 0xffe7a8, { p: [sx, 1.25, 1.22], m: { emissive: 0xffc870, emissiveIntensity: 0.0 } })); g.add(box(0.7, 0.16, 0.2, 0xc99a6b, { p: [sx, 0.9, 1.3] }));
    for (let i = 0; i < 4; i++) g.add(ico(0.07, [0xff9ec7, 0xffd84d, 0xffffff, 0xff8a65][i], 0, { p: [sx - 0.24 + i * 0.16, 1.02, 1.3] })); }
  return g;
}
export function fenceRing(rad, n = 28, gap = null) {
  const g = new T.Group();
  for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; if (gap && Math.abs(Math.atan2(Math.sin(a - gap), Math.cos(a - gap))) < 0.25) continue;
    const x = Math.cos(a) * rad, z = Math.sin(a) * rad; g.add(box(0.12, 0.7, 0.12, 0xe2b67f, { p: [x, 0.35, z] }));
    const a2 = (i + 1) / n * Math.PI * 2; if (gap && Math.abs(Math.atan2(Math.sin(a2 - gap), Math.cos(a2 - gap))) < 0.25) continue;
    const x2 = Math.cos(a2) * rad, z2 = Math.sin(a2) * rad, L = Math.hypot(x2 - x, z2 - z);
    for (const y of [0.28, 0.55]) { const r = box(L, 0.07, 0.05, 0xf0cb93, { p: [(x + x2) / 2, y, (z + z2) / 2] }); r.rotation.y = -Math.atan2(z2 - z, x2 - x); g.add(r); } }
  return g;
}
export function bench(len = 1.4) { const g = new T.Group(); g.add(box(len, 0.08, 0.42, 0xc99a6b, { p: [0, 0.42, 0] })); g.add(box(len, 0.28, 0.06, 0xc99a6b, { p: [0, 0.7, -0.19] })); for (const sx of [-len / 2 + 0.1, len / 2 - 0.1]) g.add(box(0.08, 0.42, 0.38, 0x8a5a3b, { p: [sx, 0.21, 0] })); return g; }
export function cardboardBox(wd = 1.5, h = 0.9, d = 1.1) {
  const g = new T.Group(), c = 0xd9a56a, ci = 0xa8723f, t = 0.04;
  g.add(box(wd, t, d, ci, { p: [0, t / 2, 0] }));
  g.add(box(wd, h, t, c, { p: [0, h / 2, d / 2] })); g.add(box(wd, h, t, ci, { p: [0, h / 2, -d / 2] }));
  g.add(box(t, h, d, c, { p: [wd / 2, h / 2, 0] })); g.add(box(t, h, d, ci, { p: [-wd / 2, h / 2, 0] }));
  const flap = (x, z, rx, rz, sx, sz) => { const f = box(sx, t, sz, c, {}); const p = new T.Group(); p.position.set(x, h, z); f.position.set(rz ? sx / 2 * Math.sign(x) : 0, 0, rx ? sz / 2 * Math.sign(z) : 0); p.add(f); p.rotation.set(rx, 0, rz); g.add(p); };
  flap(0, -d / 2, -1.15, 0, wd, d * 0.48); flap(wd / 2, 0, 0, -1.9, wd * 0.42, d); flap(-wd / 2, 0, 0, 1.75, wd * 0.42, d);
  g.add(box(wd * 0.98, 0.012, 0.16, 0xc8b089, { p: [0, h * 0.55, d / 2 + 0.024], m: { roughness: 0.4 } }));
  return g;
}
export function blanket(wd = 1.7, d = 0.9, hex = 0xf3a3b8, sag = 0.22) {
  const g = new T.PlaneGeometry(wd, d, 22, 12).toNonIndexed(); g.rotateX(-Math.PI / 2); const p = g.attributes.position; const cache = new Map();
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), k = x.toFixed(3) + z.toFixed(3); if (!cache.has(k)) cache.set(k, Math.sin(x * 5.3) * 0.05 + Math.cos(z * 7 + x * 2) * 0.04 - Math.max(0, z / (d / 2)) ** 2 * sag + rr(-0.012, 0.012)); p.setY(i, cache.get(k)); }
  g.computeVertexNormals(); const m = new T.Mesh(g, std(hex, { roughness: 0.95, side: T.DoubleSide })); m.castShadow = m.receiveShadow = true; return m;
}
export function heart3d(s = 0.3, hex = 0xff6f96) {
  const sh = new T.Shape(); sh.moveTo(0, -0.6); sh.bezierCurveTo(-0.9, -0.05, -0.75, 0.75, 0, 0.35); sh.bezierCurveTo(0.75, 0.75, 0.9, -0.05, 0, -0.6);
  const g = new T.ExtrudeGeometry(sh, { depth: 0.28, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.1, bevelSegments: 2, curveSegments: 8 }); g.center();
  const m = new T.Mesh(g, new T.MeshStandardMaterial({ color: lin(hex), roughness: 0.35, metalness: 0, flatShading: true, emissive: lin(hex), emissiveIntensity: 0.15 })); m.scale.setScalar(s); m.castShadow = true; return m;
}
const glowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'); const gr = x.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.2, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 128, 128); const t = new T.CanvasTexture(c); return t; })();
export function glow(pos, size, hex, op = 1) { const s = new T.Sprite(new T.SpriteMaterial({ map: glowTex, color: lin(hex), transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false })); s.position.set(...pos); s.scale.setScalar(size); s.userData.keep = 1; return s; }
export function firefly(pos, s = 1) { const g = new T.Group(); const core = new T.Mesh(new T.SphereGeometry(0.022 * s, 6, 4), new T.MeshBasicMaterial({ color: lin(0xfff6a0) })); g.add(core); g.add(glow([0, 0, 0], 0.42 * s, 0xffe46a, 0.85)); g.position.set(...pos); return g; }
export function skyTex(stops) { const c = document.createElement('canvas'); c.width = 4; c.height = 512; const x = c.getContext('2d'); const gr = x.createLinearGradient(0, 0, 0, 512); stops.forEach(([o, col]) => gr.addColorStop(o, col)); x.fillStyle = gr; x.fillRect(0, 0, 4, 512); const t = new T.CanvasTexture(c); t.encoding = T.sRGBEncoding; return t; }
export function stars(n, rad, minY = 4) { const g = new T.Group(); for (let i = 0; i < n; i++) { const a = rr(0, Math.PI * 2), y = rr(minY, rad * 0.8); const s = glow([Math.cos(a) * rad, y, Math.sin(a) * rad], rr(0.15, 0.5), 0xfff4d6, rr(0.4, 1)); g.add(s); } return g; }

// ---------- staging helpers ----------
export function stage({ sky, fog, hemi = [0xfff6e8, 0x6d8f55, 0.6], sun = { hex: 0xfff0d0, i: 1.6, p: [6, 10, 5], shadow: 9 }, exposure = 0.95 }) {
  const scene = new T.Scene(); scene.background = sky; if (fog) scene.fog = new T.Fog(lin(fog[0]), fog[1], fog[2]);
  const h = new T.HemisphereLight(lin(hemi[0]), lin(hemi[1]), hemi[2]); scene.add(h);
  let d = null; if (sun) { d = new T.DirectionalLight(lin(sun.hex), sun.i); d.position.set(...sun.p); d.castShadow = true; d.shadow.mapSize.set(4096, 4096); const s = sun.shadow; Object.assign(d.shadow.camera, { left: -s, right: s, top: s, bottom: -s, near: 0.5, far: 60 }); d.shadow.bias = -0.0004; d.shadow.normalBias = 0.02; d.shadow.radius = 3; scene.add(d); scene.add(d.target); if (sun.target) d.target.position.set(...sun.target); }
  renderer().toneMappingExposure = exposure; return { scene, sun: d, hemi: h };
}
export function point(scene, pos, hex, i = 1.5, dist = 8, shadow = false) { const l = new T.PointLight(lin(hex), i, dist, 2); l.position.set(...pos); if (shadow) { l.castShadow = true; l.shadow.mapSize.set(1024, 1024); l.shadow.bias = -0.002; } scene.add(l); return l; }

// 2D finishing: downsample (SSAA), bloom, vignette, tilt-shift, color grade
export function finish(src, { bloom = 0.22, bloomBlur = 18, vignette = 0.3, tilt = 0, tiltBand = [0.42, 0.7], warm = 0, sat = 1.16, contrast = 1.06 } = {}) {
  const c = document.createElement('canvas'); c.width = c.height = SIZE; const x = c.getContext('2d'); x.imageSmoothingQuality = 'high';
  x.filter = `saturate(${sat}) contrast(${contrast})`; x.drawImage(src, 0, 0, SIZE, SIZE); x.filter = 'none';
  if (tilt) { const b = document.createElement('canvas'); b.width = b.height = SIZE; const bx = b.getContext('2d'); bx.filter = `blur(${tilt}px)`; bx.drawImage(c, 0, 0); bx.filter = 'none';
    const m = document.createElement('canvas'); m.width = m.height = SIZE; const mx = m.getContext('2d'); const gr = mx.createLinearGradient(0, 0, 0, SIZE);
    gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(tiltBand[0] - 0.12, 'rgba(0,0,0,1)'); gr.addColorStop(tiltBand[0], 'rgba(0,0,0,0)'); gr.addColorStop(tiltBand[1], 'rgba(0,0,0,0)'); gr.addColorStop(Math.min(1, tiltBand[1] + 0.15), 'rgba(0,0,0,1)'); gr.addColorStop(1, 'rgba(0,0,0,1)');
    mx.fillStyle = gr; mx.fillRect(0, 0, SIZE, SIZE); mx.globalCompositeOperation = 'source-in'; mx.drawImage(b, 0, 0); x.drawImage(m, 0, 0); }
  if (bloom) { const b = document.createElement('canvas'); b.width = b.height = SIZE / 2; const bx = b.getContext('2d'); bx.filter = `brightness(0.8) contrast(3) blur(${bloomBlur / 2}px)`; bx.drawImage(c, 0, 0, SIZE / 2, SIZE / 2);
    x.globalAlpha = bloom; x.globalCompositeOperation = 'screen'; x.drawImage(b, 0, 0, SIZE, SIZE); x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1; }
  if (warm) { x.globalCompositeOperation = 'soft-light'; x.fillStyle = warm > 0 ? `rgba(255,170,90,${warm})` : `rgba(90,130,255,${-warm})`; x.fillRect(0, 0, SIZE, SIZE); x.globalCompositeOperation = 'source-over'; }
  if (vignette) { const gr = x.createRadialGradient(SIZE / 2, SIZE / 2, SIZE * 0.32, SIZE / 2, SIZE / 2, SIZE * 0.75); gr.addColorStop(0, 'rgba(20,10,30,0)'); gr.addColorStop(1, `rgba(20,10,30,${vignette})`); x.fillStyle = gr; x.fillRect(0, 0, SIZE, SIZE); }
  return c;
}
export function render(scene, cam, post) { const r = renderer(); cam.aspect = 1; cam.updateProjectionMatrix(); r.render(scene, cam); return finish(r.domElement, post); }
export const camAt = (fov, pos, look) => { const c = new T.PerspectiveCamera(fov, 1, 0.1, 200); c.position.set(...pos); c.lookAt(...look); return c; };

export { COAT, rnd, rr, lin, box, ico, cyl };
