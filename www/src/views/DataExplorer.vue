<template>
  <v-container fluid>
    <v-row>
      <v-col cols="auto" md="3" sm="6">
        <v-text-field v-model="inputs.start" type="date" label="Start"></v-text-field>
      </v-col>
      <v-col cols="auto" md="3" sm="6">
        <v-text-field v-model="inputs.end" type="date" label="End"></v-text-field>
      </v-col>
      <v-col cols="auto" md="6" sm="12">
        <v-select v-model="inputs.breakdowns" clearable label="Breakdowns"
          :items='["DATE", "AD_UNIT", "APP", "COUNTRY", "FORMAT", "PLATFORM", "MOBILE_OS_VERSION", "GMA_SDK_VERSION", "APP_VERSION_NAME"]'
          multiple></v-select>
      </v-col>
    </v-row>
    <v-data-table v-model:items-per-page="table.itemsPerPage" :headers="table.headers" :items="table.rows"
      class="elevation-1 pb-4" density="compact"></v-data-table>
    <v-alert class="mt-4" elevation="1" style="text-align:center; font-size: 0.85rem;">Missing something? Let me know what
      features you think we should add <router-link to="/dashboard/settings">here</router-link>!</v-alert>
  </v-container>
</template>

<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { VDataTable } from 'vuetify/labs/VDataTable'
import { realtimeQuery } from '../api'

const inputs = reactive({
  start: new Date((new Date()).getTime() - 24 * 60 * 60 * 28 * 1000).toLocaleDateString('en-CA'),
  end: new Date().toLocaleDateString('en-CA'),
  breakdowns: ["DATE", "AD_UNIT", "APP_VERSION_NAME"],
})

const table = reactive({
  itemsPerPage: 25,
  headers: [] as any,
  rows: [] as any,
})

function dateToYYYYMMDD(date: Date) {
  alert(date)
  return date.getFullYear() + "-" +
    (date.getMonth() + 1).toString().padStart(2, '0') + "-" +
    date.getDate().toString().padStart(2, '0')
}

function formatDate(datestr: string) {
  datestr = datestr.slice(0, 4) + "-" + datestr.slice(4, 6) + "-" + datestr.slice(6, 8)
  return datestr
}


function renderTable() {

  realtimeQuery(inputs.start, inputs.end, inputs.breakdowns).then(async (res) => {
    const dataset = await res.json()

    table.headers = []
    Object.keys(dataset[0].dimensionValues).forEach((key: any) => {
      let title = key
      if (key == "APP_VERSION_NAME") {
        title = "APP_VERSION"
      }
      table.headers.push({
        title: title, key: key
      })
    })
    Object.keys(dataset[0].metricValues).forEach((key: any) => {
      let title = key
      if (key == "ESTIMATED_EARNINGS") {
        title = "EARNINGS"
      }
      if (key == "MATCHED_REQUESTS") {
        title = "REQUESTS"
      }
      table.headers.push({
        title: title, key: key
      })
    })

    table.rows = []
    dataset.forEach((row: any) => {
      let result = {} as any
      Object.keys(row.dimensionValues).forEach((key: any) => {
        const obj = row.dimensionValues[key]
        result[key] = obj.displayLabel ? obj.displayLabel : obj.value;
      });
      Object.keys(row.metricValues).forEach((key: any) => {
        const obj = row.metricValues[key]
        result[key] = obj.integerValue ? obj.integerValue : obj.microsValue;
      });
      if ("DATE" in result) {
        result["DATE"] = formatDate(result["DATE"])
      }
      result["ESTIMATED_EARNINGS"] = "$" + result["ESTIMATED_EARNINGS"] / (1000.0 * 1000.0)
      table.rows.push(result)
    })
  })
}

watch(inputs, renderTable)
renderTable()
</script>
