<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>Platform eCPM</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <table>
                <tr>
                    <td></td>
                    <td><ion-icon :icon="logoApple" size="large"></ion-icon></td>
                    <td><ion-icon :icon="logoAndroid" size="large"></ion-icon></td>
                </tr>
                <tr>
                    <td>Banner</td>
                    <td>$1.0</td>
                    <td>$1.1</td>
                </tr>
                <tr>
                    <td>Rewarded</td>
                    <td>$2.0</td>
                    <td>$3.1</td>
                </tr>
                <tr>
                    <td>App Open</td>
                    <td>$7.0</td>
                    <td>$10.1</td>
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
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent, IonGrid, IonRow, IonCol, IonIcon } from '@ionic/vue';
import { logoApple, logoAndroid } from 'ionicons/icons';
</script>
