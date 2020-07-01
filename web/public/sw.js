
// importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js')
//
// if (workbox) {
//   console.log(`Workbox is loaded`)
//   // workbox.precaching.precacheAndRoute(self.__precacheManifest)
// }
// else {
//   console.log(`Workbox didn't load`)
// }

// Step 4 code here //
// try edit the cached files and/or the `cachedFiles` list
const cachedFiles = [
  './',
  './js/app.js',
  './js/chunk-vendors.js',
  './fonts/icons.0ab54153.woff2',
  './fonts/lato-v14-latin-regular.f1a4a058.woff2',
  './index.html',
  './manifest.json',
]

// edit this to force re-cache
const cacheKey = 'demo-sw-v3'

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


