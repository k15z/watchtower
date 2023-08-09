<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>eCPM By App Genre</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="300px" type="bar" :options="options" :series="series">
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
        background: '#fff0',
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
        name: 'eCPM',
        data: []
    }
]) as any;

fetchCard('ECPMByGenreV1', {"ad_format": "BANNER"}).then((res: any) => {
    series.value[0].data = res.rows.map((item: any) => {
        return {
            x: item.app_genre,
            y: item.ecpm
        }
    })
})
</script>
