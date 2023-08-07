<template>
    <ion-card>
        <ion-card-content>
            <ion-segment :scrollable="true" v-model="target">
                <ion-segment-button value="estimated_earnings">
                    <ion-label>Earnings</ion-label>
                </ion-segment-button>
                <ion-segment-button value="impressions">
                    <ion-label>Impressions</ion-label>
                </ion-segment-button>
                <ion-segment-button value="ad_requests">
                    <ion-label>Requests</ion-label>
                </ion-segment-button>
            </ion-segment>
            <apexchart ref="chart" width="100%" height="300px" type="bar" :options="options" :series="selected_series">
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

.vue-apexcharts {
    margin-top: 12px;
}
</style>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { IonCard, IonCardContent, IonSegment, IonSegmentButton, IonLabel } from '@ionic/vue';
import { fetchCard } from '@/api';

const target = ref('estimated_earnings');
const loading = ref(true);
const chart = ref(null) as any;

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
    grid: {
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        },
    },
    noData: {
        text: 'Loading...'
    },
    xaxis: {
        categories: []
    },
    tooltip: {
        enabled: false,
    },
    legend: {
        show: false
    }
})
const series = ref({}) as any;
const selected_series = ref([]) as any;

watch(target, () => {
    if (!(target.value in series.value)) {
        return []
    }
    selected_series.value = [series.value[target.value]]
})


const fetchData = () => {
    loading.value = true
    fetchCard('TimeSeriesPlotV1', { "date_filter": { "interval": 'week' } }).then((res: any) => {
        loading.value = false

        let copy = JSON.parse(JSON.stringify(options.value))
        copy.xaxis.categories = res.rows.map((item: any) => item.date)
        options.value = copy;

        series.value['estimated_earnings'] = {
            name: 'estimated_earnings',
            data: res.rows.map((item: any) => item.estimated_earnings.toFixed(2))
        }
        series.value['impressions'] = {
            name: 'impressions',
            data: res.rows.map((item: any) => item.impressions)
        }
        series.value['ad_requests'] = {
            name: 'ad_requests',
            data: res.rows.map((item: any) => item.ad_requests)
        }

        selected_series.value = [series.value['estimated_earnings']]
    })
}

fetchData()
</script>
