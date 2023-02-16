<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" app>
      <NavigationDrawerContent />
    </v-navigation-drawer>
    <v-app-bar
      app
      color="primary"
      dark
      fixed
    >
      <v-row>
        <v-col cols="3" class="d-flex flex-row align-center">
          <v-app-bar-nav-icon class="mr-2" @click.stop="drawer = !drawer" />
          <v-toolbar-title class="">
            <span class="hidden-sm-and-down">IA Debugger</span>
          </v-toolbar-title>
        </v-col>
      </v-row>
    </v-app-bar>
    <v-main>
      <v-container id="page-container">
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavigationDrawerContent from '../components/NavigationDrawerContent.vue'
export default {
  components: {
    NavigationDrawerContent
  },
  data () {
    return {
      drawer: false
    }
  }
}
</script>

<style>
#page-container {
  height: 100%;
}
</style>
