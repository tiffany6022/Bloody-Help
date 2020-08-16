<template lang="pug">
#chart-page
  .title
    .ui.ribbon.grey.label #[h3 圖表]
    select.ui.dropdown(v-model="month")
      option.item(v-for="mon in monthlist", :value="mon.id", :key="mon.id") {{ mon.text }}

  ve-line(:data="chartData", :mark-line="markLine", :colors="colors", :grid={ right: '8%' }, width="92vw", height="55vh")
</template>

<script>
import 'echarts/lib/component/title'
import 'echarts/lib/component/markLine'

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
  { text: 'Dec', id: 12 },
]

export default{
  data () {

    this.colors = ['#fbbd08', '#b5cc18', '#21ba45']
    this.markLine = {
      symbol: 'none',
      animation: false,
      data: [
        {
          name: '收縮壓臨界值',
          yAxis: 140,
          lineStyle: {
            color: 'crimson',
          }
        },
        {
          name: '舒張壓臨界值',
          yAxis: 90,
          lineStyle: {
            color: 'crimson',
          }
        },
      ]
    }

    return {
      year: 2020,
      month: 0,
      monthlist: months,
      chartData: {
        columns: ['日期', '收縮壓', '舒張壓', '心跳'],
        rows: []
      },

      localData: [],
    }
  },

  mounted () {
    var today = new Date()
    this.year = today.getFullYear()
    this.month = today.getMonth() + 1    // 0~11 month
  },

  watch: {
    'month' () {
      this.getLocalData()
    },
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
      this.localData.sort(function(a, b) {
        return a.day - b.day
      })
      for(var j=0; j<this.localData.length; j++){
        this.chartData.rows.push({
          '日期': this.month + '/' + this.localData[j].day,
          '收縮壓': this.localData[j].blood_pressure1,
          '舒張壓': this.localData[j].blood_pressure2,
          '心跳': this.localData[j].blood_pressure3,
        })
      }

    },
  },

}
</script>

<style lang="sass" scoped>
#chart-page
  .title
    display: flex
    justify-content: space-between
    margin-bottom: 2em
    .dropdown
      background-color: transparent
      border: 0px
      border-radius: .28571429rem
      font-size: medium
      .item
        font-size: 12px


</style>
