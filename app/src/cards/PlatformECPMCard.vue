<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Platform eCPM</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <div v-if="loading">
                <skeleton-loader></skeleton-loader>
            </div>
            <table v-if="!loading">
                <tr>
                    <td></td>
                    <td><ion-icon :icon="logoApple" size="large"></ion-icon></td>
                    <td><ion-icon :icon="logoAndroid" size="large"></ion-icon></td>
                </tr>
                <tr v-for="row in rows">
                    <td>{{ row.ad_format }}</td>
                    <td>{{ formatECPM(row.ios_ecpm) }}</td>
                    <td>{{ formatECPM(row.android_ecpm) }}</td>
                </tr>
            </table>
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}

table {
    width: 100%;
}

td {
    padding: 12px;
}

tr td:nth-child(2),
tr td:nth-child(3) {
    text-align: center;
}

ion-skeleton-text {
    margin-top: 24px;
}
</style>

<script setup lang="ts">
import { ref } from 'vue';
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent, IonIcon } from '@ionic/vue';
import { logoApple, logoAndroid } from 'ionicons/icons';
import { fetchCard } from '@/api';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const loading = ref(true);
const rows = ref([]) as any;

const formatECPM = (value: number) => {
    if (!value) {
        return "-"
    }
    return "$" + value.toFixed(2);
};

fetchCard('PlatformECPMV1', { "date_filter": { "interval": "day" } }).then((data: any) => {
    rows.value.push(...data.rows)
    loading.value = false
});
</script>
