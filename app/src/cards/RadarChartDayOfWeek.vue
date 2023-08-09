<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Earnings by Weekday</ion-card-subtitle>
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
import { IonCard, IonCardContent } from '@ionic/vue';

const chartOptions = {
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
        height: 350,
        type: 'radar',
        dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1
        }
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
        categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
};

const series = [{
    name: 'App 1',
    data: [80, 50, 30, 40, 100, 20],
}, {
    name: 'App 2',
    data: [20, 30, 40, 80, 20, 80],
}, {
    name: 'App 3',
    data: [44, 76, 78, 13, 43, 10],
}]
</script>
