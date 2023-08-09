<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Median Earnings by Day of Week</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="300px" type="radar" :options="chartOptions" :series="series">
            </apexchart>
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}

ion-card-content {
    padding-top: 12px;
}
</style>

<script setup lang="ts">
import { IonCard, IonCardContent, IonCardHeader, IonCardSubtitle } from '@ionic/vue';
import { fetchCard } from '@/api';
import { ref } from 'vue'

const chartOptions = ref({
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
        dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1
        },
        background: '#fff0',
    },
    theme: {
        mode: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    },
    stroke: {
        width: 2
    },
    fill: {
        opacity: 0.1
    },
    markers: {
        size: 0
    },
    xaxis: {
        categories: []
    },
    noData: {
        text: 'Loading...'
    },
    yaxis: {
        labels: {
        }
    }
});

const series = ref([{
    data: [],
}])

fetchCard('EarningsByDayOfWeekV1', {}).then((res: any) => {
    const deepCopy = JSON.parse(JSON.stringify(chartOptions.value))
    deepCopy.xaxis.categories = res.rows.map((item: any) => item.day_of_week)
    deepCopy.yaxis.labels.formatter = (x: number) => {
        return x.toFixed(2)
    }
    chartOptions.value = deepCopy

    series.value[0].data = res.rows.map((item: any) => item.p50)
})
</script>
