<template>
  <v-container>
    <v-row>
      <v-col>
        <country-e-c-p-m></country-e-c-p-m>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-card class="fill-height">
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
                  <td>{{ row.ecpm }}</td>
                  <td>{{ row.your_ecpm }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6">
        <v-card class="fill-height">
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
                  <td>{{ row.ecpm }}</td>
                  <td>{{ row.your_ecpm }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
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
        <v-alert style="text-align:center; font-size: 0.85rem;">Looking for something else? Let us know what breakdowns you'd like to see <router-link to="/dashboard/settings">here</router-link>!</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ecpmByBreakdowns } from '../api'
import { reactive } from 'vue'
import HistoricalECPM from "../components/HistoricalECPM.vue"
import CountryECPM from "../components/CountryECPM.vue"

const data = reactive({
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

</script>
