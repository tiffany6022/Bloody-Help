const fs = require('fs')

module.exports = {
  publicPath: 'static',

  devServer: {
    host: 'merry.ee.ncku.edu.tw',
    port: 12233,
    https: {
      key: fs.readFileSync('/home/yichung/ssl/private.key'),
      cert: fs.readFileSync('/home/yichung/ssl/certificate.crt'),
    },
  },

  // pwa: {
  //   name: 'BPM_reader',
  //   appleMobileWebAppCapable: 'yes',
  //   appleMobileWebAppStatusBarStyle: 'black',
  //
  //   // configure the workbox plugin
  //   workboxPluginMode: 'InjectManifest',
  //   workboxOptions: {
  //     // swSrc is required in InjectManifest mode.
  //     swSrc: 'public/sw.js',
  //     // ...other Workbox options...
  //   },
  // }
}
