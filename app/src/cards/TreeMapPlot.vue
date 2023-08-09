<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Top Countries by {{formatTarget(options.target)}}</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart ref="chart" width="100%" height="300px" type="treemap" :options="chartOptions" :series="series">
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

defineProps(['options'])

function formatTarget(target: string) {
    if (target == 'ecpm') {
        return 'eCPM'
    }
    return target.charAt(0).toUpperCase() + target.slice(1)
}

const chartOptions = {
    chart: {
        toolbar: {
            show: false,
        },
        parentHeightOffset: 0,
        height: 350,
    },
};

const series = [
    {
        data: [
            {
                x: 'United States',
                y: 218
            },
            {
                x: 'Canada',
                y: 149
            },
            {
                x: 'Australia',
                y: 184
            },
            {
                x: 'United Kingdom',
                y: 55
            },
            {
                x: 'India',
                y: 84
            },
        ]
    }
]
</script>
