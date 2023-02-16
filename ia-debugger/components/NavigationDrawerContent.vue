<template>
  <div>
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            IA Debugger
          </v-list-item-title>
          <v-list-item-subtitle>by Faustin for NSI</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-divider />
    <v-list>
      <v-list-item to="/" router exact>
        <v-list-item-action><v-icon>mdi-home</v-icon></v-list-item-action>
        <v-list-item-content><v-list-item-title>Accueil</v-list-item-title></v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'NavigationDrawerContent',
  data () {
    return {
    }
  }
}
</script>

<style scoped>

</style>
