<template lang="pug">
#camera-page
  vue-web-cam(
    ref='webcam',
    width='100%',
    :device-id='deviceId',
    @cameras='onCameras',
  )
  .container
    #backhome(v-if='"running"==mode')
      button.icon.ui.button.circular.huge.item(@click='$emit("backhome")')
        i.icon.chevron.left
    #undo(v-if='"pause"==mode')
      button.icon.ui.button.circular.huge.item(@click='undo')
        i.icon.undo
    #shutter(v-if='"running"==mode')
      button.icon.ui.button.circular.massive.item(@click='capture')
        i.icon.circle
    #upload(v-if='"pause"==mode')
      button.icon.ui.button.circular.massive.item(@click='upload')
        i.icon.upload
    #change
      button.icon.ui.button.circular.huge.item(@click='changeCamera')
        i.icon.sync
</template>

<script>
import { WebCam } from "vue-web-cam"
import 'semantic-ui-offline/semantic.min.css'
const axios = require('axios')

export default{

  components: {
    'vue-web-cam': WebCam,
  },

  data(){ return {
    mode: 'running',
    devices: [],
    deviceId: null,
    img: null,
    cameraIndex: 0
  }},

  methods: {

    undo(){
      this.$refs.webcam.start()
      this.mode='running'
    },

    capture() {
      this.img = this.$refs.webcam.capture()
      this.$refs.webcam.pause()
      this.mode='pause'
    },

    upload() {
      console.log('uploading img...')
      var image = {
        base64: this.img,
        name: "123"
      }
      axios.post('/img', image)
      console.log(image.base64)
      this.$emit("backhome")
    },


    onCameras(cameras) {
	this.devices = cameras
	this.deviceId = cameras[0].deviceId
    },

    changeCamera() {
      this.cameraIndex = (this.cameraIndex+1) % this.devices.length
      this.deviceId = this.devices[this.cameraIndex].deviceId
    },

  }
}
</script>

<style lang="sass" scoped>
.container
  display: flex
  width: 100%
  justify-content: space-around
  bottom: 0
  position: absolute
  padding: 2em

#camera-page
  position: fixed
  top: 0
  left: 0
  width: 100vw
  height: 100vh
  background-color: white
  z-index: 102

</style>
