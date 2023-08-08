<template>
    <ion-page>
        <div id="container">
            <img style="width:6em;" src="/public/favicon.png" alt="Watchtower Logo" />
            <h1>Watchtower</h1>
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <ion-button @click="login" expand="full" color="danger">
                <ion-icon slot="start" :icon="logInOutline"></ion-icon>
                Connect To AdMob
            </ion-button>
        </div>
    </ion-page>
</template>

<style scoped>
#container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}
</style>

<script setup lang="ts">
import { IonPage, IonButton, IonIcon } from '@ionic/vue';
import { logInOutline } from 'ionicons/icons';
import { Capacitor } from '@capacitor/core';
import { authToken, store } from '@/state';
import router from '@/router';

const login = () => {
  if (Capacitor.getPlatform() == 'web') {
    // Live-reload + debug mode with test account.
    store.set('authToken', "8449ee12-ecf8-445f-b721-cb2022b28ff0")
    authToken.value = "8449ee12-ecf8-445f-b721-cb2022b28ff0"
    router.push('/')
  } else {
    window.open("https://admobwatchtower.com/connect")
  }
}
</script>
