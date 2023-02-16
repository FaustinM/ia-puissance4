<template>
  <table>
    <tbody>
      <td v-for="(column, index) in grid" :key="index">
        <tr v-for="(line, indexL) in column" :key="indexL" :class="line === 1 ? 'red' : line === 2 ? 'yellow' : ''" v-text="line" />
      </td>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'Connect4',
  props: {
    grid: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
tr {
  font-size: xxx-large;
}

tr, td {
  margin: 0;
  border-width: 0;
  text-align: center;
  vertical-align: center;
}

table {
  height: 100%;
  width: 100%;
}
</style>
