<script>
// eslint-disable-next-line no-unused-vars
import { Doughnut, mixins } from 'vue-chartjs'

export default {
  extends: Doughnut,
  props: {
    chartdata: {
      type: Object,
      default: null
    }
  },
  mounted () {
    this.renderChart(this.chartdata, {
      borderWidth: '10px',
      hoverBackgroundColor: 'red',
      hoverBorderWidth: '10px'
    })
  }
}

</script>

<style scoped>

</style>
