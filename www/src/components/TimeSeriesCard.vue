<template>
    <v-card class="fill-height">
        <v-card-text>
            <apexchart ref="chartRef" width="100%" height="500px" type="line" :options="data.options" :series="data.series">
            </apexchart>
        </v-card-text>
    </v-card>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { realtimeQuery } from '../api'
import { onMounted } from 'vue';

const data = reactive({
    options: {},
    series: [] as any
})

function formatDate(datestr: string) {
    datestr = datestr.slice(0, 4) + "-" + datestr.slice(4, 6) + "-" + datestr.slice(6, 8)
    return datestr
}

function dateToYYYYMMDD(date: Date) {
    return date.getFullYear() + "-" +
        (date.getMonth() + 1).toString().padStart(2, '0') + "-" +
        date.getDate().toString().padStart(2, '0')
}

const end = new Date()
const start = new Date((new Date()).getTime() - 24 * 60 * 60 * 28 * 1000)
const chartRef = ref(null)

onMounted(() => {
    realtimeQuery(dateToYYYYMMDD(start), dateToYYYYMMDD(end), ["DATE"]).then(async (res) => {
        const dataset = await res.json()
        data.options = {
            chart: {
                id: 'realtime-timeseries'
            },
            stroke: {
                curve: 'smooth',
            },
            xaxis: {
                categories: dataset.map((x: any) => formatDate(x.dimensionValues.DATE.value))
            }
        }
        console.log(dataset)
        data.series = []
        data.series.push({
            name: "Earnings",
            data: dataset.map((x: any) => x.metricValues.ESTIMATED_EARNINGS.microsValue / (1000.0 * 1000.0)),
        })
        data.series.push({
            name: "Impressions",
            data: dataset.map((x: any) => x.metricValues.IMPRESSIONS.integerValue),
        })
        data.series.push({
            name: "Clicks",
            data: dataset.map((x: any) => x.metricValues.CLICKS.integerValue),
        })
        data.series.push({
            name: "Requests",
            data: dataset.map((x: any) => x.metricValues.AD_REQUESTS.integerValue),
        })
        setTimeout(() => {
            (chartRef.value as any).hideSeries("Impressions");
            (chartRef.value as any).hideSeries("Clicks");
            (chartRef.value as any).hideSeries("Requests");
        }, 100)
    })
})
</script>
