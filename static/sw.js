const CACHE_NAME = 'django-pwa-v1';
const ASSETS = [
  '/',
  '/static/base.css',
  '/static/manifest.json',
  '/static/chat/css/lobby.css',
  '/static/chat/css/room.css',
  '/static/chat/js/goban/goban.js',
  '/static/chat/js/util/logging.js',
  '/static/chat/js/chat.js',
  '/static/chat/js/elements.js',
  '/static/chat/js/lobby.js',
  '/static/chat/js/room.js',
  '/static/chat/js/userlist.js',
  '/static/chat/js/websocket.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

self.addEventListener('install', event => {
  console.log('Service Worker installed.');
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  // APIリクエストはキャッシュしない
  //console.log('Fetch:', event.request.url);
  if (event.request.url.includes('/api/')) {
    return;
  }
  // HTMLはネットワーク優先（ログイン後の表示崩れ対策(chrome)）
  if (event.request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});

self.addEventListener("push", (event) => {
  console.log("Push received:", event);

  let data = { title: "通知", body: "メッセージがあります" };

  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data.body = event.data.text();
    }
  }

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: "/static/icons/icon-192.png",
      badge: "/static/icons/icon-192.png",
      data: data.url || "/chat/lobby/"
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const url = event.notification.data || "/chat/lobby/";

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true })
      .then((clientList) => {
        for (const client of clientList) {
          if (client.url.includes(url) && "focus" in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow(url);
        }
      })
  );
});