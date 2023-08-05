<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Earnings By Day Of Week</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            Plot with confidence intervals of earnings by day of week.
        </ion-card-content>
    </ion-card>
</template>

<style scoped>
ion-card-header {
    padding-bottom: 0px;
}
</style>

<script setup lang="ts">
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';
</script>
