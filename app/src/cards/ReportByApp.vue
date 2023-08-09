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
            <div v-if="loading">
                <skeleton-loader></skeleton-loader>
            </div>
            <div v-if="!loading">
                <table>
                    <template v-for="row in rows">
                        <tr>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>
                        </tr>
                        <tr>
                            <td colspan="3">
                                <h1>
                                    {{ row.app_name }}
                                </h1>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <span class="label">Platform</span>
                            </td>
                            <td>
                                <span class="label">Earnings</span>
                            </td>
                            <td>
                                <span class="label">Impressions</span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <span class="primary">
                                    <ion-icon :icon="row.app_platform == 'Android' ? logoAndroid : logoApple"></ion-icon>

                                </span>
                            </td>
                            <td>
                                <span class="primary">${{ formatMoney(row.estimated_earnings) }}</span>
                            </td>
                            <td>
                                <span class="primary">{{ row.impressions }}</span>
                            </td>
                        </tr>
                    </template>
                </table>
            </div>
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

h2 {
    color: var(--ion-color-medium);
    font-weight: bold;
}

.primary {
    font-size: 2em;
    color: var(--ion-color-step-800)
}

ion-card-content {
    padding: 12px;
}

table {
    width: 100%;
}
</style>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { IonCard, IonSegment, IonSegmentButton, IonLabel, IonCardContent, IonIcon } from '@ionic/vue';
import { fetchCard } from '@/api';
import SkeletonLoader from '@/components/SkeletonLoader.vue';
import { logoApple, logoAndroid } from 'ionicons/icons';

const interval = ref('day');
const loading = ref(true);
const rows = ref([]) as any;

const fetchData = () => {
    rows.value = []
    loading.value = true
    fetchCard('ReportByAppV1', { "date_filter": { "interval": interval.value } }).then((res: any) => {
        rows.value = res.rows
        loading.value = false
    });
}

const formatMoney = (amount: number) => {
    return amount.toFixed(2)
}

watch(interval, fetchData)
fetchData()
</script>