<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Earnings By Day Of Week</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="300px" type="boxPlot" :options="options" :series="series">
            </apexchart>
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}

ion-card-content {
    padding: 12px;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';
import { fetchCard } from '@/api';

const options = ref({
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
    },
    dataLabels: {
        enabled: false
    },
    theme: {
        mode: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: '50%'
        },
        boxPlot: {
            colors: {
                upper: '#e9ecef',
                lower: '#f8f9fa'
            }
        }
    },
    stroke: {
        colors: ['#6c757d']
    },
    noData: {
        text: 'Loading...'
    },
})
const series = ref([
    {
        data: []
    }
]) as any;

fetchCard('EarningsByDayOfWeekV1', {}).then((res: any) => {
    series.value[0].data = res.rows.map((item: any) => {
        return {
            x: item.day_of_week,
            y: [item.min.toFixed(2), item.p25.toFixed(2), item.p50.toFixed(2), item.p75.toFixed(2), item.max.toFixed(2)]
        }
    })
})
</script>
