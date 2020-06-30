<template lang="pug">
#chart-page
  .title
    .ui.ribbon.grey.label #[h3 圖表]
    i.redo.alternate.large.icon(@click="getLocalData")
  ve-line(:data="chartData", width="90vw", height="55vh")
</template>

<script>
import 'echarts/lib/component/title'

export default{
  data () { return {
    year: 2020,
    month: 0,
    chartData: {
      columns: ['日期', '收縮壓', '舒張壓', '血糖', '血脂'],
      rows: []
    },

    localData: [],
  }},

  mounted () {
    var today = new Date()
    this.year = today.getFullYear()
    this.month = today.getMonth() + 1    // 0~11 month

    this.getLocalData()
  },

  methods: {
    getLocalData() {

      // get localStorage and save in localData
      this.localData = []
      for(var i=0; i<window.localStorage.length; i++){
        var month = (this.month < 10 ? '0' : '') + this.month
        if (window.localStorage.key(i).substring(0,7) == `${this.year}-${month}`){  //2020-06
          var day = window.localStorage.key(i).substring(8,10)
          day = day < 10 ? day.substring(1,2) : day
          day = this.month + '/' + day
          var healthData = JSON.parse(window.localStorage.getItem(window.localStorage.key(i)))
          healthData['day'] = day
          this.localData.push(healthData)
        }
      }

      this.makeChart()

    },

    makeChart() {

      // save in chartData
      this.chartData.rows = []
      for(var j=0; j<this.localData.length; j++){
        this.chartData.rows.push({
          '日期': this.localData[j].day,
          '收縮壓': this.localData[j].blood_pressure1,
          '舒張壓': this.localData[j].blood_pressure2,
          '血糖': this.localData[j].blood_pressure3,
          '血脂': this.localData[j].blood_pressure4
        })
      }

    },
  },

  // watch: {
  //   'localData' () {
  //     this.chartData.rows = []
  //     for(var i=0; i<this.localData.length; i++){
  //       this.chartData.rows.push({
  //         '日期': this.localData[i].day,
  //         '收縮壓': this.localData[i].blood_pressure1,
  //         '舒張壓': this.localData[i].blood_pressure2,
  //         '血糖': this.localData[i].blood_pressure3,
  //         '血脂': this.localData[i].blood_pressure4
  //       })
  //     }
  //   },
  // },

}
</script>

<style lang="sass" scoped>
#chart-page
  .title
    display: flex
    justify-content: space-between
    align-items: center
    margin-bottom: 2em

</style>
