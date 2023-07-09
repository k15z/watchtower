<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-card>
          <v-card-text>
            Explore the average eCPM across the AdMob network and compare it to your eCPM to
            gain new insights, understand the state of the market, and identify new
            opportunities to grow your revenue.
          </v-card-text>
        </v-card>
        <br />
        <v-card>
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
        <v-card>
          <v-card-title>Country</v-card-title>
          <v-card-text>
            <v-skeleton-loader type="card-avatar"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>Custom Breakdowns</v-card-title>
          <v-card-text>
            <v-skeleton-loader type="table"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ecpmByBreakdowns } from '../api'
import { reactive } from 'vue'
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'
import HistoricalECPM from "../components/HistoricalECPM.vue"

const data = reactive({
  "serving": [],
  "platform": [],
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
