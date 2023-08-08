<template>
    <ion-card>
        <ion-card-content>
            <ion-segment :scrollable="true" v-model="interval">
                <ion-segment-button value="day">
                    <ion-label>Today</ion-label>
                </ion-segment-button>
                <ion-segment-button value="week">
                    <ion-label>7 Days</ion-label>
                </ion-segment-button>
                <ion-segment-button value="month">
                    <ion-label>28 Days</ion-label>
                </ion-segment-button>
            </ion-segment>
            <div v-if="loading">
                <skeleton-loader></skeleton-loader>
            </div>
            <ion-grid v-if="!loading && data">
                <ion-row style="padding-top:12px;">
                    <ion-col>
                        <p class="label">Earnings</p>
                        <p class="primary">${{formatMoney(data.estimated_earnings.current)}}</p>
                        <ion-text :color="colorDifference(data.estimated_earnings)" class="secondary">${{formatMoney(data.estimated_earnings.previous)}} ({{percentDifference(data.estimated_earnings)}})</ion-text>
                    </ion-col>
                    <ion-col>
                        <p class="label">Impressions</p>
                        <p class="primary">{{data.impressions.current}}</p>
                        <ion-text :color="colorDifference(data.impressions)" class="secondary">{{data.impressions.previous}} ({{percentDifference(data.impressions)}})</ion-text>
                    </ion-col>
                </ion-row>
                <ion-row style="padding-top:12px;">
                    <ion-col>
                        <p class="label">Requests</p>
                        <p class="primary">{{data.ad_requests.current}}</p>
                        <ion-text :color="colorDifference(data.ad_requests)" class="secondary">{{data.ad_requests.previous}} ({{percentDifference(data.ad_requests)}})</ion-text>
                    </ion-col>
                    <ion-col>
                        <p class="label">eCPM</p>
                        <p class="primary">{{formatMoney(data.ecpm.current)}}</p>
                        <ion-text :color="colorDifference(data.ecpm)" class="secondary">{{formatMoney(data.ecpm.previous)}} ({{percentDifference(data.ecpm)}})</ion-text>
                    </ion-col>
                </ion-row>
            </ion-grid>
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-grid {
    --ion-grid-padding: 0px;
}

.label {
    font-weight: bold;
}

.primary {
    font-size: 2em;
    color: var(--ion-color-step-800)
}

ion-card-content {
    padding: 12px;
}
</style>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { IonCard, IonSegment, IonSegmentButton, IonLabel, IonCardContent, IonGrid, IonRow, IonCol, IonText } from '@ionic/vue';
import { fetchCard } from '@/api';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const interval = ref('day');
const loading = ref(true);
const data = ref({}) as any;

const fetchData = () => {
    data.value = {}
    loading.value = true
    fetchCard('ReportCardV1', { "date_filter": { "interval": interval.value } }).then((res: any) => {
        data.value = res
        loading.value = false
    });
}

const formatMoney = (amount: number) => {
    return amount.toFixed(2)
}

const percentDifference = (metric: any) => {
    const raw = ((metric.current - metric.previous) / metric.previous) * 100
    return (raw > 0 ? '+' : '-') + Math.abs(raw).toFixed(2) + '%'
}

const colorDifference = (metric: any) => {
    const raw = ((metric.current - metric.previous) / metric.previous) * 100
    return raw > 0 ? 'success' : 'danger'
}

watch(interval, fetchData)
fetchData()
</script>