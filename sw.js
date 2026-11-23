// Network-first service worker: always fresh when online, cached copy when offline.
// Three.js and the Google fonts are cached once (cache-first) so the game also starts offline.
const CACHE = 'whisker-meadow-v1';
const CDN = /cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com/;

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isCdn = CDN.test(url.host);
  if (url.origin !== location.origin && !isCdn) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    if (isCdn) {
      const hit = await cache.match(req);
      if (hit) return hit;
    }
    try {
      // revalidate game files every time so a new version shows up right away
      const res = await fetch(req, isCdn ? {} : { cache: 'no-cache' });
      if (res.ok || res.type === 'opaque') cache.put(req, res.clone());
      return res;
    } catch {
      const hit = await cache.match(req, { ignoreSearch: !isCdn });
      return hit || Response.error();
    }
  })());
});
