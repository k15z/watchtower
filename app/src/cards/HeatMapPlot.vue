<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>
                Historical {{ formatTarget(options.target) }}
            </ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="250px" type="heatmap" :options="chartOptions" :series="series">
            </apexchart>
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}

ion-card-content {
    padding-top: 0;
    padding-left: 0;
    padding-right: 0;
}
</style>

<script setup lang="ts">
import { IonCard, IonCardContent, IonCardHeader, IonCardSubtitle } from '@ionic/vue';
import { fetchCard } from '@/api';
import {ref} from 'vue'

let props = defineProps(['options']);

function formatTarget(target: string) {
    if (target == 'ecpm') {
        return 'eCPM'
    }
    return target.charAt(0).toUpperCase() + target.slice(1)
}

let chartOptions = {
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
        background: '#fff0',
    },
    theme: {
        mode: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    },
    dataLabels: {
        enabled: false
    },
    colors: ["#008FFB"]
};
let series = ref([]) as any

fetchCard('HeatMapPlotV1', {'target': props.options.target}).then((res: any) => {
    series.value.length = 0
    series.value.push(...res.rows)
})
</script>
