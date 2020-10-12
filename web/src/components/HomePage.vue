<template lang="pug">
#main-page
  #month
    .ui.ribbon.grey.label #[h3 日期]
    select.ui.dropdown(v-model="month")
      option.item(v-for="mon in monthlist", :value="mon.id", :key="mon.id") {{ mon.text }}

  .ui.secondary.compact.menu
    .item(v-for="day in daylist", :class="{ active: day.date == date }", @click="date = day.date; jump(day.date)", :id="'d'+day.date")
      h4.header {{ day.date }}
      p {{ day.week }}

  #faceIcon
    .ui.ribbon.grey.label #[h3 數值]
    #icons(:data-tooltip="status_word", data-position="top right")
      i.frown.large.icon(:class="{ red: 'high' == health_status, outline: 'high' != health_status }")
      i.meh.outline.large.icon(:class="{ yellow: 'elevated' == health_status, outline: 'elevated' != health_status }")
      i.smile.outline.large.icon(:class="{ green: 'normal' == health_status, outline: 'normal' != health_status }")

  .ui.vertical.big.segments
    .ui.inverted.active.dimmer(v-if='loading')
      .ui.text.loader(v-if='loading') loading
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.yellow.icon] 收縮壓(SYS)
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure1")]
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.olive.icon] 舒張壓(DIA)
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure2")]
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.green.icon] 心跳(PUL)
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure3")]


  .container
    // #camera
    //   button.icon.ui.button.circular.massive.item(@click='$emit("turnOnCamera")')
    //     i.file.image.icon
    #image
      button.icon.ui.button.circular.massive.item(@click='handleFile')
        i.icon.camera
</template>

<script>
const axios = require('axios')
const months = [
  { text: 'Jan', id: 1 },
  { text: 'Feb', id: 2 },
  { text: 'Mar', id: 3 },
  { text: 'Apr', id: 4 },
  { text: 'May', id: 5 },
  { text: 'Jun', id: 6 },
  { text: 'Jul', id: 7 },
  { text: 'Aug', id: 8 },
  { text: 'Sep', id: 9 },
  { text: 'Oct', id: 10 },
  { text: 'Nov', id: 11 },
  { text: 'Dec', id: 12 }
]

export default {
  data() {
    return {
      year: 2020,
      month: 0,
      date: 0,
      daylist: [],
      monthlist: months,
      blood_pressure1: '',
      blood_pressure2: '',
      blood_pressure3: '',
      health_status: 'none',
      img: '',
      loading: false
    }
  },

  computed: {
    status_word() {
      if (this.health_status == 'normal') {
        return '血壓處於正常範圍'
      } else if (this.health_status == 'elevated') {
        return '高血壓前期，需要盡早開始控制血壓'
      } else if (this.health_status == 'high') {
        return '建議應與醫師討論如何追蹤及是否治療'
      } else {
        return '請填入血壓值'
      }
    }
  },

  mounted() {
    var today = new Date()
    this.year = today.getFullYear()
    this.month = today.getMonth() + 1 // 0~11 month
    this.date = today.getDate()
  },

  updated() {
    this.jump(this.date)
  },

  watch: {
    date() {
      this.getLocalData()
    },

    month() {
      this.daylist = []
      var d = new Date(this.year, this.month, 0)
      var days = d.getDate() // how many days in this month
      for (var i = 1; i <= days; i++) {
        var w = new Date(this.year, this.month - 1, i)
        var week = w.getDay() // 0~6(SUN~SAT)
        if (week == 0) {
          week = 'SUN'
        } else if (week == 1) {
          week = 'MON'
        } else if (week == 2) {
          week = 'TUE'
        } else if (week == 3) {
          week = 'WED'
        } else if (week == 4) {
          week = 'THU'
        } else if (week == 5) {
          week = 'FRI'
        } else if (week == 6) {
          week = 'SAT'
        }
        this.daylist.push({
          date: i,
          week: week
        })
      }
      this.getLocalData()
    },

    blood_pressure1() {
      this.setStorage()
    },
    blood_pressure2() {
      this.setStorage()
    },
    blood_pressure3() {
      this.setStorage()
    }
  },

  methods: {
    async handleFile() {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => {
          this.upload(reader.result)
        }

        const input = document.createElement('input')
        input.type = 'file'

        input.onchange = () => {
          const file = input.files[0]
          if (!file.type.match(/image.*/)) return reject()

          reader.readAsDataURL(file)
          resolve(input.files[0])
        }

        input.click()
      })
    },

    async upload(base64data) {
      this.loading = true

      var image = {
        base64: base64data,
        name: 'imageName'
      }

      this.blood_pressure1 = '...'
      this.blood_pressure2 = '...'
      this.blood_pressure3 = '...'

      axios.post('/img', image).then(res => {
        this.blood_pressure1 = res.data.SYS
        this.blood_pressure2 = res.data.DIA
        this.blood_pressure3 = res.data.PUL

        this.loading = false
      })
    },

    getLocalData() {
      var dateString = this.getDateString()
      var healthData = JSON.parse(window.localStorage.getItem(dateString))
      if (healthData) {
        console.log('have localStorage!')
        this.blood_pressure1 = healthData.blood_pressure1
        this.blood_pressure2 = healthData.blood_pressure2
        this.blood_pressure3 = healthData.blood_pressure3
        this.assessStatus()
      } else {
        this.blood_pressure1 = ''
        this.blood_pressure2 = ''
        this.blood_pressure3 = ''
        this.health_status = 'none'
      }
    },

    setStorage() {
      var healthData = {
        blood_pressure1: this.blood_pressure1,
        blood_pressure2: this.blood_pressure2,
        blood_pressure3: this.blood_pressure3
      }
      if (
        healthData.blood_pressure1 ||
        healthData.blood_pressure2 ||
        healthData.blood_pressure3
      ) {
        var dateString = this.getDateString()
        window.localStorage.setItem(dateString, JSON.stringify(healthData))
      }
      this.assessStatus()
    },

    getDateString() {
      var month = (this.month < 10 ? '0' : '') + this.month
      var date = (this.date < 10 ? '0' : '') + this.date
      var dateString = this.year + '-' + month + '-' + date
      return dateString
    },

    jump(date) {
      document.getElementById('d' + date).scrollIntoView({ inline: 'center' })
    },

    assessStatus() {
      if (this.blood_pressure1 && this.blood_pressure2) {
        if (this.blood_pressure1 < 120 && this.blood_pressure2 < 80) {
          this.health_status = 'normal'
        } else if (this.blood_pressure1 < 140 && this.blood_pressure2 < 90) {
          this.health_status = 'elevated'
        } else {
          this.health_status = 'high'
        }
      } else {
        this.health_status = 'none'
      }
    }
  }
}
</script>

<style lang="sass" scoped>
#main-page

  #month
    display: flex
    justify-content: space-between
    .dropdown
      background-color: transparent
      border: 0px
      border-radius: .28571429rem
      font-size: medium
      .item
        font-size: 12px

  #faceIcon
    display: flex
    justify-content: space-between
    align-items: flex-end

  .secondary.menu
    display: inline-flex
    overflow: auto
    height: 12vh
    width: 95vw

  ::-webkit-scrollbar
      height: 0px
      width: 0px

  .vertical.segments
    margin: 2rem 1rem 1rem 1rem
    border-radius: 1rem
    background-color: white

    .horizontal.segments
      .segment
        border-left: 0px
        padding: 0.8em 1em

  .input
    width: 4.2em
    height: 1.8em
    input
      text-align: center
      padding: 0.6em

  .container
    display: flex
    justify-content: space-around
    width: 100%
</style>
