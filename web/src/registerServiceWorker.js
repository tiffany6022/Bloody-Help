/* eslint-disable no-console */

if ('serviceWorker' in window.navigator) {
  window.navigator.serviceWorker.register(`${process.env.BASE_URL}sw.js`)
  .then(reg => {
    console.log(`SW is registered with scope: ${reg.scope}`)
  })
  .catch(err => {
    console.log('SW Error ', err)
  })
}

//  Step 4 code here //
// try edit the cached files and/or the `cachedFiles` list
const cachedFiles = [
  // './',
  './css/app.92b7e75c.css',
  './css/chunk-vendors.158b6d7d.css',
  // js
  './js/app.1a2ae9eb.js',
  './js/app.1a2ae9eb.js.map',
  './js/chunk-vendors.de92595b.js',
  './js/chunk-vendors.de92595b.js.map',
  // fonts
  './fonts/brand-icons.13db00b7.eot',
  './fonts/brand-icons.a046592b.woff',
  './fonts/brand-icons.c5ebe0b3.ttf',
  './fonts/brand-icons.e8c322de.woff2',
  './fonts/icons.0ab54153.woff2',
  './fonts/icons.8e3c7f55.eot',
  './fonts/icons.b87b9ba5.ttf',
  './fonts/icons.faff9214.woff',
  './fonts/lato-v14-latin-regular.62fb51e9.woff',
  './fonts/lato-v14-latin-regular.6a6d7150.eot',
  './fonts/lato-v14-latin-regular.da4b79be.ttf',
  './fonts/lato-v14-latin-regular.f1a4a058.woff2',
  './fonts/outline-icons.701ae6ab.eot',
  './fonts/outline-icons.ad97afd3.ttf',
  './fonts/outline-icons.cd6c777f.woff2',
  './fonts/outline-icons.ef60a4f6.woff',
  // img
  './img/brand-icons.a1a749e8.svg',
  './img/flags.9c74e172.png',
  './img/icons.962a1bf3.svg',
  './img/lato-v14-latin-regular.9087e4a6.svg',
  './img/outline-icons.82f60bd0.svg',
  // img/icons
  './img/icons/android-chrome-192x192.png',
  './img/icons/android-chrome-512x512.png',
  './img/icons/android-chrome-maskable-192x192.png',
  './img/icons/android-chrome-maskable-512x512.png',
  './img/icons/apple-touch-icon-120x120.png',
  './img/icons/apple-touch-icon-152x152.png',
  './img/icons/apple-touch-icon-180x180.png',
  './img/icons/apple-touch-icon-60x60.png',
  './img/icons/apple-touch-icon-76x76.png',
  './img/icons/apple-touch-icon.png',
  './img/icons/favicon-16x16.png',
  './img/icons/favicon-32x32.png',
  './img/icons/msapplication-icon-144x144.png',
  './img/icons/mstile-150x150.png',
  './img/icons/safari-pinned-tab.svg',
  //
  './favicon.ico',
  './index.html',
  './manifest.json',
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


/*
import { register } from 'register-service-worker'

if ( 'serviceWorker' in window.navigator ) {
  register(`${process.env.BASE_URL}sw.js`, {
    ready () {
      console.log(
        'App is being served from cache by a service worker.\n' +
        'For more details, visit https://goo.gl/AFskqB'
      )
    },
    registered () {
      console.log('Service worker has been registered.')
    },
    cached () {
      console.log('Content has been cached for offline use.')
    },
    updatefound () {
      console.log('New content is downloading.')
    },
    updated () {
      console.log('New content is available; please refresh.')
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
  }
*/
