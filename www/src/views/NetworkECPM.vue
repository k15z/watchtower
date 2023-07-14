<template>
  <v-container>
    <v-row>
      <v-col>
        <country-e-c-p-m></country-e-c-p-m>
      </v-col>
    </v-row>
    <v-row>
      <v-col xs="12" md="6">
        <v-card>
          <template v-if="data.genre.length == 0">
            <v-skeleton-loader type="table-row"></v-skeleton-loader>
          </template>
          <template v-if="data.genre.length > 0">
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">Serving Restriction</th>
                    <th class="text-left">Network eCPM</th>
                    <th class="text-left">Your eCPM</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in data.serving">
                    <td>{{ row.serving_restriction }}</td>
                    <td>${{ row.ecpm }}</td>
                    <td>${{ row.your_ecpm ? row.your_ecpm : '-' }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </template>
        </v-card>
        <v-card class="mt-4">
          <template v-if="data.genre.length == 0">
            <v-skeleton-loader type="table-tbody"></v-skeleton-loader>
          </template>
          <template v-if="data.genre.length > 0">
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">App Genre</th>
                    <th class="text-left">Network eCPM</th>
                    <th class="text-left">Your eCPM</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in data.genre">
                    <td>{{ row.genre }}</td>
                    <td>${{ row.ecpm }}</td>
                    <td>${{ row.your_ecpm ? row.your_ecpm : '-' }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </template>
        </v-card>
      </v-col>
      <v-col xs="12" md="6">
        <v-card class="fill-height">
          <template v-if="data.platform.length == 0">
            <v-skeleton-loader type="table"></v-skeleton-loader>
          </template>
          <template v-if="data.platform.length > 0">
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">Platform</th>
                    <th class="text-left">Format</th>
                    <th class="text-left">Network eCPM</th>
                    <th class="text-left">Your eCPM</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in data.platform">
                    <td>{{ row.platform }}</td>
                    <td>{{ row.format }}</td>
                    <td>${{ row.ecpm }}</td>
                    <td>${{ row.your_ecpm ? row.your_ecpm : '-' }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </template>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <historical-e-c-p-m></historical-e-c-p-m>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-alert style="text-align:center; font-size: 0.85rem;">Looking for something else? Let us know what breakdowns
          you'd like to see <router-link to="/dashboard/settings">here</router-link>!</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ecpmByBreakdowns } from '../api'
import { reactive } from 'vue'
import HistoricalECPM from "../components/HistoricalECPM.vue"
import CountryECPM from "../components/CountryECPM.vue"
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader';

const data = reactive({
  "genre": [] as any,
  "serving": [] as any,
  "platform": [] as any,
})


ecpmByBreakdowns("platform,format").then((res) => {
  res.json().then((res) => {
    data.platform = res
  })
})

ecpmByBreakdowns("serving_restriction").then((res) => {
  res.json().then((res) => {
    data.serving = res
  })
})

ecpmByBreakdowns("genre").then((res) => {
  res.json().then((res) => {
    data.genre = res
  })
})

</script>
