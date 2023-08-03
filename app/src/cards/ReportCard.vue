<template>
    <ion-card>
        <ion-card-content>
            <ion-segment :scrollable="true" value="day">
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
            <ion-grid>
                <ion-row style="padding-top:12px;">
                    <ion-col>
                        <p class="label">Earnings</p>
                        <p class="primary">$0.30</p>
                        <p class="secondary">$0.20 (+20%)</p>
                    </ion-col>
                    <ion-col>
                        <p class="label">Impressions</p>
                        <p class="primary">$0.30</p>
                        <p class="secondary">$0.20 (+20%)</p>
                    </ion-col>
                </ion-row>
                <ion-row style="padding-top:12px;">
                    <ion-col>
                        <p class="label">Requests</p>
                        <p class="primary">$0.30</p>
                        <p class="secondary">$0.20 (+20%)</p>
                    </ion-col>
                    <ion-col>
                        <p class="label">eCPM</p>
                        <p class="primary">$0.30</p>
                        <p class="secondary">$0.20 (+20%)</p>
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
}

.secondary {
    font-size: 0.8em;
}

ion-card-content {
    padding: 12px;
}
</style>

<script setup lang="ts">
import { IonCard, IonSegment, IonSegmentButton, IonLabel, IonCardContent, IonGrid, IonRow, IonCol } from '@ionic/vue';
const props = defineProps(['options'])
</script>