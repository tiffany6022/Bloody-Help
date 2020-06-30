<template lang="pug">
#main-page
  .ui.ribbon.grey.label #[h3 日期]
  .ui.secondary.compact.menu
    .item(v-for="day in daylist", :class="{ active: day.date == date }", @click="date = day.date")
      h4.header {{ day.date }}
      p {{ day.week }}

  .ui.ribbon.grey.label #[h3 數值]
  .ui.vertical.big.segments
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.yellow.icon] 收縮壓
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure1")]
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.olive.icon] 舒張壓
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure2")]
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.green.icon] 血糖
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure3")]
    .ui.horizontal.segments
      .ui.segment #[i.heartbeat.large.teal.icon] 血脂
      .ui.right.aligned.segment
        .ui.input #[input(type="text", placeholder="請輸入", v-model="blood_pressure4")]

</template>

<script>

export default{

  data() { return {
    year: 2020,
    month: 0,
    date: 0,
    daylist: [],
    blood_pressure1: '',
    blood_pressure2: '',
    blood_pressure3: '',
    blood_pressure4: '',
  }},

  mounted () {
    var today = new Date()
    this.year = today.getFullYear()
    this.month = today.getMonth() + 1    // 0~11 month
    this.date = today.getDate()
  },

  watch: {
    'date' () {
      var dateString = this.getDateString()
      var healthData = JSON.parse(window.localStorage.getItem(dateString))
      if (healthData) {
        console.log("have localStorage!")
        this.blood_pressure1 = healthData.blood_pressure1
        this.blood_pressure2 = healthData.blood_pressure2
        this.blood_pressure3 = healthData.blood_pressure3
        this.blood_pressure4 = healthData.blood_pressure4
      }
      else {
        this.blood_pressure1 = ''
        this.blood_pressure2 = ''
        this.blood_pressure3 = ''
        this.blood_pressure4 = ''
      }
    },

    'month' () {
      this.daylist = []
      var d = new Date(this.year, this.month, 0)
      var days = d.getDate() // how many days in this month
      for(var i=1; i<=days; i++){
        var w = new Date(this.year, this.month-1, i)
        var week = w.getDay() // 星期幾：0~6(SUN~SAT)
        if (week == 0){ week = "SUN" }
        else if (week == 1){ week = "MON" }
        else if (week == 2){ week = "TUE" }
        else if (week == 3){ week = "WED" }
        else if (week == 4){ week = "THU" }
        else if (week == 5){ week = "FRI" }
        else if (week == 6){ week = "SAT" }
        this.daylist.push({
          date: i,
          week: week
        })
      }
    },

    'blood_pressure1' () {
      this.setStorage()
    },
    'blood_pressure2' () {
      this.setStorage()
    },
    'blood_pressure3' () {
      this.setStorage()
    },
    'blood_pressure4' () {
      this.setStorage()
    },
  },

  methods: {

    setStorage() {
      var healthData = {
        blood_pressure1: this.blood_pressure1,
        blood_pressure2: this.blood_pressure2,
        blood_pressure3: this.blood_pressure3,
        blood_pressure4: this.blood_pressure4,
      }
      var dateString = this.getDateString()
      window.localStorage.setItem(dateString, JSON.stringify(healthData))
    },

    getDateString() {
      var month = (this.month < 10 ? '0' : '') + this.month
      var date = (this.date < 10 ? '0' : '') + this.date
      var dateString = this.year + '-' + month + '-' + date
      return dateString
    },

  },

}
</script>

<style lang="sass" scoped>
#main-page

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

</style>
