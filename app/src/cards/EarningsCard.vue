<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Estimated Earnings</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <apexchart width="100%" height="200px" type="bar" :options="options" :series="series"></apexchart>
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
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';

const options = {
    chart: {
        id: 'vuechart-example',
        toolbar: {
            show: false,
        },

    },
    grid: {
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        },  
    },
    xaxis: {
        categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
    },
    yaxis: {
        show: false,
    },
    tooltip: {
        enabled: false,
    }
}
const series = [{
    name: 'series-1',
    data: [30, 40, 45, 50, 49, 60, 70, 91]
}]
</script>
