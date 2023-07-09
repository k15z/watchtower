<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-card class="fill-height">
          <v-card-title>Platform and Format</v-card-title>
          <v-card-text>
            <v-skeleton-loader type="paragraph"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6">
        <v-card>
          <v-card-title>Serving Restriction</v-card-title>
          <v-card-text>
            <v-skeleton-loader></v-skeleton-loader>
          </v-card-text>
        </v-card>
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
          <v-card-title>Historical</v-card-title>
          <v-card-text>
            <v-skeleton-loader type="image"></v-skeleton-loader>
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
import { BASE_API_URL } from '../constants'
import { store } from '../store'
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'

function ecpmByBreakdowns(breakdowns: string) {
  return fetch(BASE_API_URL + "/network/ecpm?breakdowns=" + breakdowns, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Authorization': `Bearer ${store.token}`,
      'Content-Type': 'application/json'
    }
  })
}

ecpmByBreakdowns("platform,format").then((res) => {
  res.json().then((res) => {
    console.log(res)
  })
})

ecpmByBreakdowns("serving_restriction").then((res) => {
  res.json().then((res) => {
    console.log(res)
  })
})

ecpmByBreakdowns("country").then((res) => {
  res.json().then((res) => {
    console.log(res)
  })
})
</script>
