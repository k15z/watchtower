<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>
                Historical {{ formatTarget(options.target) }}
            </ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="300px" type="heatmap" :options="chartOptions" :series="series">
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

defineProps(['options'])

function formatTarget(target: string) {
    if (target == 'ecpm') {
        return 'eCPM'
    }
    return target.charAt(0).toUpperCase() + target.slice(1)
}

function generateData(count: number, yrange: any) {
    let i = 0;
    let series = [];
    while (i < count) {
        let x = 'w' + (i + 1).toString();
        let y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

        series.push({
            x: x,
            y: y
        });
        i++;
    }
    return series;
}

let chartOptions = {
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
    },
    theme: {
        mode: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    },
    dataLabels: {
        enabled: false
    },
    colors: ["#008FFB"]
};
let series = [{
    name: 'Monday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Tuesday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Wednesday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Thursday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Friday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Saturday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
},
{
    name: 'Sunday',
    data: generateData(10, {
        min: 0,
        max: 90
    })
}]
</script>
