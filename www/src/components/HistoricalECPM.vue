<template>
  <v-card>
    <v-card-text>
      <apexchart width="100%" height="400" type="line" :options="chart.options" :series="chart.series"></apexchart>
    </v-card-text>
  </v-card>
</template>
  
<script lang="ts" setup>
import { ecpmByBreakdowns } from '../api'
import { reactive } from 'vue'

let chart = reactive({
  options: {},
  series: [] as any,
})

ecpmByBreakdowns("week,format").then((res) => {
  res.json().then((res) => {
    chart.options = {
      chart: {
        id: "vuechart-example",
        toolbar: { show: false }
      },
      title: {
        text: "Historical eCPM"
      },
      stroke: {
        curve: 'smooth',
      },
      xaxis: {
        labels: {
          rotate: -45,
          rotateAlways: true,
        },
        categories: res.week,
      },
    }
    res.series.forEach((x: any) => {
      chart.series.push({
        name: x.breakdown,
        data: x.data,
      })
    });
  })
})
</script>
