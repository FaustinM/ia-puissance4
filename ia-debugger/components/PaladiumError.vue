<template>
  <v-card
    class="mx-auto"
    max-width="600"
  >
    <v-list-item>
      <v-list-item-avatar>
        <v-icon size="35" dark color="red">
          mdi-alert-circle
        </v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Une erreur s'est produite :/
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider />
    <v-card-text>
      Désolé pour cette erreur... Si vous ne comprenez pas d'où viens l'erreur, je vous invite à contacter un Développeur.
    </v-card-text>
    <v-divider />

    <v-tooltip bottom>
      <template #activator="{ on, attrs }">
        <v-list-item v-bind="attrs" @click="copyError" v-on="on">
          <v-list-item-avatar>
            <v-icon>
              mdi-tray-alert
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-subtitle>Code d'erreur</v-list-item-subtitle>
            <v-list-item-title v-text="error" />
          </v-list-item-content>
        </v-list-item>
      </template>
      <span>Vous pouvez copier l'erreur en cliquant dessus !</span>
    </v-tooltip>
    <v-divider />
    <v-card-actions>
      <v-spacer />
      <NuxtLink to="/">
        <v-btn color="primary" text>
          Accueil
        </v-btn>
      </NuxtLink>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'PaladiumErrorVue',
  props: {
    error: {
      type: [String, Object],
      require: true,
      default: 'Erreur inconnu :/'
    }
  },
  methods: {
    copyError () {
      navigator.clipboard.writeText(this.error)
    }
  }
}
</script>

<style scoped>

</style>
