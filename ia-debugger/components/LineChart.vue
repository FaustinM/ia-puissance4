<script>
// eslint-disable-next-line no-unused-vars
import { Line, mixins } from 'vue-chartjs'

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  mounted () {
    this.renderChart(this.chartData)
  }
}

</script>

<style scoped>

</style>
