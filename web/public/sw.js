
if (workbox) {
  console.log(`Workbox is loaded`)
}
else {
  console.log(`Workbox didn't load`)
}

workbox.core.setCacheNameDetails({
  prefix: 'bpm',
  suffix: 'v1.0.0'
})


var cacheFiles = [
  './css/app.c1577da7.css',
  './css/chunk-vendors.158b6d7d.css',
  './js/app.7f0b68fb.js',
  './js/chunk-vendors.8d4ff3ef.js',
  './index.html',
  './manifest.json',
]

// const precacheController = workbox.precaching.precacheAndRoute(cacheFiles)
//
// self.addEventListener('install', (event) => {
//   event.waitUntil(precacheController.install())
// })
//
// self.addEventListener('activate', (event) => {
//   event.waitUntil(precacheController.activate())
// })
//
// self.addEventListener('fetch', (event) => {
//   const cacheKey = precacheController.getCacheKeyForURL(event.request.url)
//   event.respondWith(caches.match(cacheKey).then(...))
// })

// workbox.precaching.precacheAndRoute(cacheFiles)

// workbox.precaching.precacheAndRoute(self.__precacheManifest || [])

// // 缓存web的css资源
// workbox.routing.registerRoute(
//   // Cache CSS files
//   /.*\.css/,
//   // 使用缓存，但尽快在后台更新
//   workbox.strategies.staleWhileRevalidate({
//     // 使用自定义缓存名称
//     cacheName: 'css-cache'
//   })
// );
//
// // 缓存web的js资源
// workbox.routing.registerRoute(
//   // 缓存JS文件
//   /.*\.js/,
//   // 使用缓存，但尽快在后台更新
//   workbox.strategies.staleWhileRevalidate({
//     // 使用自定义缓存名称
//     cacheName: 'js-cache'
//   })
// );
//
// // 缓存web的图片资源
// workbox.routing.registerRoute(
//   /\.(?:png|gif|jpg|jpeg|svg)$/,
//   workbox.strategies.staleWhileRevalidate({
//     cacheName: 'images',
//     plugins: [
//       new workbox.expiration.Plugin({
//         maxEntries: 60,
//         maxAgeSeconds: 30 * 24 * 60 * 60 // 设置缓存有效期为30天
//       })
//     ]
//     })
//   );

/*

// Step 4 code here //
// try edit the cached files and/or the `cachedFiles` list
const cachedFiles = [
  // './',
  './css/app.c1577da7.css',
  './css/chunk-vendors.158b6d7d.css',
  './js/app.7f0b68fb.js',
  './js/chunk-vendors.8d4ff3ef.js',
  './index.html',
  './manifest.json',
]

// edit this to force re-cache
const cacheKey = 'sw-v2'
console.log('sw')

// install, a good time to preload cache
self.addEventListener('install', event => {
  console.log(`${cacheKey} is installed`)
  event.waitUntil((async () => {
    const cache = await caches.open(cacheKey)
    return cache.addAll(cachedFiles)
  })())
})


// Step 5 code here //
// activate, a good time to clean old cache since the old service work stops now
self.addEventListener('activate', event => {
  console.log(`${cacheKey} is activated`)
  event.waitUntil((async () => {
    const keys = await caches.keys()
    return Promise.all(keys.filter(key => key != cacheKey).map(key => caches.delete(key)))
  })())
})


// Step 6 code here //
self.addEventListener('fetch', event => {
  event.respondWith((async () => {
    const response = await caches.match(event.request)
    if (response) {
      console.log(`Cache fetch: ${event.request.url}`)
      return response
    }
    console.log(`Network fetch: ${event.request.url}`)
    return fetch(event.request)
  })())
})

*/
