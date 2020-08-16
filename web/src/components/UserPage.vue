<template lang="pug">
#user-page
  #head
    div
    i.ellipsis.horizontal.large.grey.icon

  .ui.unstackable.items
    .item
      i.child.massive.icon
      .content
        h2 Maggie Kao
        .averagedata
          .ui.circular.segment(:style='sysColor')
            h4.ui.header SYS
              .sub.header {{ avg_blood_pressure1 }}
          .ui.circular.segment(:style='diaColor')
            h4.ui.header DIA
              .sub.header {{ avg_blood_pressure2 }}
          .ui.circular.segment(style={ 'border-color': 'gray' })
            h4.ui.header PUL
              .sub.header {{ avg_blood_pressure3 }}

  .ui.ribbon.grey.label #[h3 血壓標準值]

  table.ui.unstackable.table
    thead
      tr
        th
        th Type
        th SYS
        th DIA
    tbody(v-for="row in rows")
      tr.title(@click="toggleDetail(row.id)")
        td #[i.square.icon(:class="row.color")]
        td {{ row.state }}
        td {{ row.sysBound }}
        td {{ row.diaBound }}
      tr.detail(v-if="row.showDetail", style={ 'backgound-color': 'gray' })
        td(colspan="4") {{ row.details }}

</template>

<script>

export default{

  data() { return {
    year: 2020,
    month: 0,
    avg_blood_pressure1: '',
    avg_blood_pressure2: '',
    avg_blood_pressure3: '',
    localData: [],
    rows: [
      { id: 0, color: 'red', state: '高血壓第二期', sysBound: '>160', diaBound: '>100', showDetail: false, details: '此時可能同時出現胸口疼痛、呼吸急促、後背疼痛、全身無力 、視力改變、說話困難等症狀，必須要立即撥打119求救，盡速就醫治療。' },
      { id: 1, color: 'orange', state: '高血壓第一期', sysBound: '141-160', diaBound: '91-100', showDetail: false, details: '第一期高血壓，建議應與醫師討論如何追蹤及是否治療。' },
      { id: 2, color: 'yellow', state: '偏高', sysBound: '121-140', diaBound: '81-90', showDetail: false, details: '高血壓前期，表示較有可能發展成為高血壓，建議應立即改善生活型態，並養成每天量血壓的習慣，尋求醫療人員評估後續血壓變化情形。' },
      { id: 3, color: 'green', state: '正常', sysBound: '91-120', diaBound: '61-80', showDetail: false, details: '血壓處於正常範圍，還是要繼續維持規律運動習慣、均衡營養的飲食，並且避免攝取過多反式脂肪與鹽類。' },
      { id: 4, color: 'blue', state: '低血壓', sysBound: '<90', diaBound: '<60', showDetail: false, details: '請注意是否為貧血所導致，建議可多加補充富含鐵質、葉酸、維生素 B12 的食物（如深綠色蔬菜等）。' },
    ],
  }},

  computed: {
    sysColor() {
      if (this.avg_blood_pressure1 > 160)
        return { 'border-color': '#db2828' }
      else if (this.avg_blood_pressure1 > 140 && this.avg_blood_pressure1 <= 160)
        return { 'border-color': '#f2711c' }
      else if (this.avg_blood_pressure1 > 120 && this.avg_blood_pressure1 <= 140)
        return { 'border-color': '#fbbd08' }
      else if (this.avg_blood_pressure1 > 90 && this.avg_blood_pressure1 <= 120)
        return { 'border-color': '#21ba45' }
      else
        return { 'border-color': '#2185d0' }
    },

    diaColor() {
      if (this.avg_blood_pressure2 > 100)
        return { 'border-color': '#db2828' }
      else if (this.avg_blood_pressure2 > 90 && this.avg_blood_pressure2 <= 100)
        return { 'border-color': '#f2711c' }
      else if (this.avg_blood_pressure2 > 80 && this.avg_blood_pressure2 <= 90)
        return { 'border-color': '#fbbd08' }
      else if (this.avg_blood_pressure2 > 60 && this.avg_blood_pressure2 <= 80)
        return { 'border-color': '#21ba45' }
      else
        return { 'border-color': '#2185d0' }
    },
  },

  mounted () {
    var today = new Date()
    this.year = today.getFullYear()
    this.month = today.getMonth() + 1    // 0~11 month
    this.getLocalData()
  },

  methods: {
    toggleDetail(id) {
      for(var i=0; i<5; i++){
        if (i == id)
          this.rows[i].showDetail = !this.rows[i].showDetail
        else
          this.rows[i].showDetail = false
      }
    },

    getLocalData() {
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

      this.countAverageData()
    },

    countAverageData() {
      var sum_pressure1 = 0
      var sum_pressure2 = 0
      var sum_pressure3 = 0
      for(var j=0; j<this.localData.length; j++){
        sum_pressure1 += parseInt(this.localData[j].blood_pressure1)
        sum_pressure2 += parseInt(this.localData[j].blood_pressure2)
        sum_pressure3 += parseInt(this.localData[j].blood_pressure3)
      }
      this.avg_blood_pressure1 = Math.floor(sum_pressure1 / this.localData.length)
      this.avg_blood_pressure2 = Math.floor(sum_pressure2 / this.localData.length)
      this.avg_blood_pressure3 = Math.floor(sum_pressure3 / this.localData.length)
    },
  },
}
</script>

<style lang="sass" scoped>
#user-page

  #head
    display: flex
    justify-content: space-between

  .items
    .item
      .content
        margin: 0em 1em
        .averagedata
          display: flex
          justify-content: space-between
          align-items: baseline
          .circular.segment
            padding: 0.75em 1em
            background-color: transparent
            margin: 0 0 2em 0
            border-width: 0.15rem
            border-style: dashed

  .table
    tbody
      .title
        font-weight: bold
      .detail
        background-color: #f9fafb
</style>
