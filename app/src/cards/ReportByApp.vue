<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Earnings By App ({{ props.options.interval }})</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <table>
                <tr>
                    <td></td>
                    <td>Earnings</td>
                    <td>Impressions</td>
                </tr>
                <tr>
                    <td>AO3 Disco</td>
                    <td>$1.0</td>
                    <td>1000</td>
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

tr td:nth-child(2), tr td:nth-child(3) {
    text-align:center;
}
</style>

<script setup lang="ts">
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';
const props = defineProps(['options'])
</script>
