const cacheName = 'artisanget-v1';

// function precache() {
//     return caches.open('my-cache').then(function (cache){
//         return cache.addAll([
//             '{% url "home" %}',
//             '{% url "about" %}',
//             '{% url "contact" %}',
//             '{% url "dashboard" %}',
//             '{% url "profile" %}',
//         ]);
//     });
// }
{% load static %}
const staticAssets = [
    '{% static "css/style.css" %}',
    '{% static "css/bootstrap.min.css" %}',
    '{% static "css/bootstrap.css" %}',
    '{% static "js/main.js" %}',
    '{% static "js/JiSlider.js" %}',
    '{% static "js/jquery-2.2.3.min.js" %}',
    '{% static "js/move-top.js" %}',
    '{% static "js/easing.js" %}',
    '{% static "js/SmoothScroll.min.js" %}',
    '{% static "js/bootstrap.js" %}',
    '{% static "js/numscroller-1.0.js" %}',
    '{% static "assets/css/black-dashboard.css" %}',
    '{% static "assets/css/nucleo-icons.css" %}',
    '{% static "assets/js/core/bootstrap.min.js" %}',
    "{% static 'assets/js/core/popper.min.js' %}",
    "{% static 'assets/js/core/jquery.min.js' %}",
    "{% static 'assets/js/black-dashboard.min.js' %}"
];

self.addEventListener('install', async e => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', e => {
  self.clients.claim();
});

self.addEventListener('fetch', async e => {
  const req = e.request;
  const url = new URL(req.url);

  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}