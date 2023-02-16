<template>
  <PaladiumErrorVue class="my-auto" :error="error.message" />
</template>

<script>
import PaladiumErrorVue from '@/components/PaladiumError'
export default {
  components: { PaladiumErrorVue },
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'Erreur inconnu :/'
    }
  },
  head () {
    let title
    switch (this.error.statusCode) {
      case 404:
        title = this.pageNotFound
        break
      default:
        title = this.otherError
        break
    }
    return {
      title
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
