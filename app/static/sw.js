/**
 * Service Worker - Su, Tarım & Hayvancılık Dijital Gazetesi
 * Çevrimdışı (offline) okuma ve statik varlık önbellekleme yöneticisi.
 */

const CACHE_NAME = 'suhaber-portal-v1';
const STATIC_ASSETS = [
  './index.html',
  './tarim.html',
  './hayvancilik.html',
  './yasal.html',
  './assets/css/portal.css',
  './assets/icons/icon.svg',
  './manifest.json'
];

// Install: Cache critical shell assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('Service worker cache.addAll partial warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Network-first for HTML pages (to get fresh news), Cache-first for CSS/JS/images
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET and foreign analytics/tracking
  if (req.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  // HTML navigation requests: Network first, fallback to cached offline page
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, responseClone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(req).then((cached) => {
            return cached || caches.match('./index.html');
          });
        })
    );
    return;
  }

  // Static assets (CSS, JS, SVG, Images): Stale-while-revalidate
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetchPromise = fetch(req).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, responseClone));
        }
        return networkResponse;
      }).catch(() => {/* ignore offline fetch failures */});

      return cached || fetchPromise;
    })
  );
});
