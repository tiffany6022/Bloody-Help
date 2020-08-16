<template lang="pug">
#app
  meta(name="viewport", content="width=device-width,initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0")
  #pages
    h2.ui.dividing.center.aligned.header(v-if="'home'==page") HomePage
    h2.ui.dividing.center.aligned.header(v-if="'chart'==page") ChartPage
    h2.ui.dividing.center.aligned.header(v-if="'user'==page") UserPage

    camera-page(v-if="'camera'==page", @backhome="page='home'")
    .ui.container
      home-page(v-if="'home'==page", @turnOnCamera="page='camera'")
      chart-page(v-if="'chart'==page")
      user-page(v-if="'user'==page")

  #footer
    .ui.bottom.fixed.icon.fixed.item.labeled.borderless.four.menu
      .item(@click="page='home'") #[i.home.icon(:style="homeIconStyle")]
      .item(@click="page='chart'") #[i.chart.line.icon(:style="chartIconStyle")]
      .item(@click="page='user'") #[i.user.icon(:style="userIconStyle")]

</template>

<script>
import 'semantic-ui-offline/semantic.min.css'

export default {
  components: {
    'home-page': require('./components/HomePage.vue').default,
    'chart-page': require('./components/ChartPage.vue').default,
    'user-page': require('./components/UserPage.vue').default,
    'camera-page': require('./components/Camera.vue').default,
  },

  computed: {
    homeIconStyle() { return {
      color: this.page == 'home' ? 'black' : 'lightgrey',
    }},
    chartIconStyle() { return {
      color: this.page == 'chart' ? 'black' : 'lightgrey',
    }},
    userIconStyle() { return {
      color: this.page == 'user' ? 'black' : 'lightgrey',
    }},
  },

  // created() {
  // },

  data(){ return {
    page: 'home',
  }},

  // methods: {
  // },

  // watch: {
  // }
}
</script>

<style lang="sass" scoped>
#app
  background-color: whitesmoke
  width: 100vw
  height: 100vh

  #pages
    background-color: whitesmoke
    .header
      padding: 2vh
      background-color: white

  #footer
    background-color: whitesmoke
    height: 5em
    .menu
      background-color: white

</style>
