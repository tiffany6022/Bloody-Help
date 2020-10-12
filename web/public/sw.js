const cachedFiles = [
'./sw.js',
'./.sw.js.swp',
'./favicon.ico',
'./robots.txt',
'./manifest.json',
// img
'./img/flags.9c74e172.png',
'./img/lato-v14-latin-regular.9087e4a6.svg',
'./img/outline-icons.82f60bd0.svg',
'./img/icons.962a1bf3.svg',
'./img/brand-icons.a1a749e8.svg',
// img/icons
'./img/icons/android-chrome-192x192.png',
'./img/icons/msapplication-icon-144x144.png',
'./img/icons/apple-touch-icon-120x120.png',
'./img/icons/apple-touch-icon-180x180.png',
'./img/icons/android-chrome-512x512.png',
'./img/icons/favicon-32x32.png',
'./img/icons/android-chrome-maskable-192x192.png',
'./img/icons/apple-touch-icon.png',
'./img/icons/apple-touch-icon-152x152.png',
'./img/icons/apple-touch-icon-60x60.png',
'./img/icons/safari-pinned-tab.svg',
'./img/icons/mstile-150x150.png',
'./img/icons/apple-touch-icon-76x76.png',
'./img/icons/favicon-16x16.png',
'./img/icons/android-chrome-maskable-512x512.png',
// fonts
'./fonts/lato-v14-latin-regular.62fb51e9.woff',
'./fonts/brand-icons.e8c322de.woff2',
'./fonts/outline-icons.ef60a4f6.woff',
'./fonts/icons.b87b9ba5.ttf',
'./fonts/lato-v14-latin-regular.6a6d7150.eot',
'./fonts/outline-icons.ad97afd3.ttf',
'./fonts/lato-v14-latin-regular.da4b79be.ttf',
'./fonts/icons.8e3c7f55.eot',
'./fonts/icons.0ab54153.woff2',
'./fonts/brand-icons.c5ebe0b3.ttf',
'./fonts/outline-icons.701ae6ab.eot',
'./fonts/icons.faff9214.woff',
'./fonts/brand-icons.13db00b7.eot',
'./fonts/outline-icons.cd6c777f.woff2',
'./fonts/lato-v14-latin-regular.f1a4a058.woff2',
'./fonts/brand-icons.a046592b.woff',
// ./js
// './js/appe6c2da6f.js',
'./js/app.e6c2da6f.js.map',
// './js/chunk-vendors01efc803.js',
'./js/chunk-vendors.01efc803.js.map',
'./index.html',
]

// edit this to force re-cache
const cacheKey = 'sw-v8'
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

