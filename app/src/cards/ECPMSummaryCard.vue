<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>eCPM Report</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            Based on an anonymized dataset with approximately 71,400 impressions, the average eCPM has increased around 2%
            compared to the previous week. Looking at region, it appears that Europe is an outlier where the eCPM actually
            increased by 30%. Looking at platform, it appears that ANDROID is an outlier where the eCPM actually increased
            by 12%. Looking at privacy/personalization settings, there are no clear trends in eCPM. Looking at app
            genre/category, it appears that Trivia is an outlier where the eCPM actually increased by 12%.
        </ion-card-content>
</ion-card></template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}
</style>

<script setup lang="ts">
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';
</script>
