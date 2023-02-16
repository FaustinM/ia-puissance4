<template>
  <v-layout
    column
    justify-center
    align-center
    @drop.prevent="onDrop($event)"
    @dragover.prevent="resetDrag()"
    @dragenter.prevent="resetDrag()"
    @dragleave.prevent="dragover = false"
    @dragend.prevent="dragover = false"
  >
    <!--    <v-flex>
      <v-container>
        <v-row>
          <v-col md="6">
            <PaladiumStatusOfMinecraft />
          </v-col>
          <v-col md="6">
            <PaladiumStatusOfMinecraft />
          </v-col>
        </v-row>
      </v-container>
    </v-flex>-->
    <v-col v-if="games.length === 0" class="text-center" cols="8">
      <v-icon class="ma-5" :color="dragover ? 'primary' : 'grey'" size="150">
        mdi-cloud-upload
      </v-icon>
      <h1 :class="dragover ? ['primary--text'] : ['grey--text']">
        Vous pouvez upload un fichier de log !
      </h1>
    </v-col>
    <v-col v-else>
      <v-row align="center">
        <v-col md="6">
          <v-card>
            <pie-chart class="ma-5" :chartdata="pieChartData" />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="ma-5">
            <v-subheader>Nb de parties par paquet</v-subheader>
            <v-card-text>
              <v-row>
                <v-col class="pr-4">
                  <v-slider
                    v-model.lazy="gameNbPacket"
                    class="align-center"
                    :max="games.length/2"
                    :min="0"
                    hide-details
                  >
                    <template #append>
                      <v-text-field
                        v-model.lazy="gameNbPacket"
                        class="mt-0 pt-0"
                        hide-details
                        single-line
                        type="number"
                        style="width: 60px"
                      />
                    </template>
                  </v-slider>
                </v-col>
              </v-row>
            </v-card-text>
            <line-chart class="ma-5" :chart-data="lineChartData" />
          </v-card>
          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-title>Moyenne de tour</v-list-item-title>
                <v-list-item-subtitle v-text="averageRound" />
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Somme des rewards</v-list-item-title>
                <v-list-item-subtitle v-text="sumReward" />
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Nombre partie</v-list-item-title>
                <v-list-item-subtitle v-text="games.length" />
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
      <v-divider class="my-5" />
      <v-card>
        <v-subheader>Choix de la partie</v-subheader>

        <v-card-text>
          <v-row>
            <v-col class="pr-4">
              <v-slider
                v-model="gameId"
                class="align-center"
                :max="games.length - 1"
                :min="0"
                hide-details
              >
                <template #append>
                  <v-text-field
                    v-model="gameId"
                    class="mt-0 pt-0"
                    hide-details
                    single-line
                    type="number"
                    style="width: 60px"
                  />
                </template>
              </v-slider>
            </v-col>
          </v-row>
        </v-card-text>
        <Connect4 v-if="games[gameId]" class="ma-5" :grid="games[gameId].grid" />
      </v-card>
      <v-row v-if="games[gameId]">
        <v-col md="6">
          <v-card>
            <v-card-subtitle>Gagnant</v-card-subtitle>
            <v-card-title v-text="games[gameId].isFinish" />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card>
            <v-card-subtitle>Reward</v-card-subtitle>
            <v-card-title v-text="games[gameId].reward" />
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </v-layout>
</template>

<script>
// import PaladiumStatusOfMinecraft from '@/components/PaladiumStatusOfMinecraft'

export default {
  data () {
    return {
      dragover: false,
      gameId: 0,
      gameNbPacket: 0,
      games: []
    }
  },
  computed: {
    pieChartData () {
      return {
        labels: ['Victoire', 'Défaite', 'Égalité'],
        datasets: [{
          label: 'First dataset',
          backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
          data: [this.nbVictory, this.nbDefeat, this.nbAllLoose]
        }]
      }
    },
    lineChartData () {
      return {
        labels: this.splitedArray.map((d, i) => `Parties ${i * 100} à ${i * 100 + d.length}`),
        datasets: [{
          label: 'Victoire',
          borderColor: '#41B883',
          data: this.nbVictoryPacket
        }, {
          label: 'Défaite',
          borderColor: '#E46651',
          data: this.nbDefeatPacket
        }, {
          label: 'Égalité',
          borderColor: '#00D8FF',
          data: this.nbEqualityPacket
        }]
      }
    },
    nbVictoryPacket () {
      return this.splitedArray.map(d => ((d.filter(e => e.isFinish === 2).length / d.length) * 100).toFixed(2))
    },
    nbDefeatPacket () {
      return this.splitedArray.map(d => ((d.filter(e => e.isFinish === 1).length / d.length) * 100).toFixed(2))
    },
    nbEqualityPacket () {
      return this.splitedArray.map(d => ((d.filter(e => e.isFinish === 0).length / d.length) * 100).toFixed(2))
    },
    nbVictory () {
      return this.games.filter(d => d.isFinish === 2).length
    },
    nbDefeat () {
      return this.games.filter(d => d.isFinish === 1).length
    },
    nbAllLoose () {
      return this.games.filter(d => d.isFinish === 3).length
    },
    averageRound () {
      return this.games.reduce((r, c) => r + c.turns, 0) / this.games.length
    },
    sumReward () {
      return this.games.reduce((r, c) => r + c.reward, 0)
    },
    sumTurns () {
      return this.games.reduce((r, c) => r + c.turns, 0)
    },
    averageColumn () {
      return this.games
        .map(d => d.grid)
        .map(d => d.map(e => e.reduce((r, c) => c === 2 ? r + 1 : r, 0)))
        .reduce((r, c) => r.map((a, i) => a + c[i]) || c)
        .map(d => this.sumTurns ? (d / this.sumTurns).toFixed(2) : d)
    },
    splitedArray () {
      return this.gameNbPacket
        ? this.games.reduce((acc, curr, i) => {
          if (!(i % this.gameNbPacket)) {
            acc.push(this.games.slice(i, i + this.gameNbPacket))
          }
          return acc
        }, [])
        : []
    }
  },
  methods: {
    async onDrop (e) {
      this.dragover = false
      if (e.dataTransfer.files.length === 1) {
        this.games = (await e.dataTransfer.files[0].text()).split('\n').filter(d => !!d).map(d => JSON.parse(d))
        this.gameNbPacket = this.games.length > 10000 ? 1000 : 100
      }
      console.log(this.averageColumn)
    },
    resetDrag () {
      this.games = []
      this.dragover = true
    }
  }
}
</script>
