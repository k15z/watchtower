<template>
  <ion-page>
    <div id="container">
      <watchtower-logo style="width:6em;" @easter-egg="easterEgg"></watchtower-logo>
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
import { authToken, store } from '@/state';
import router from '@/router';
import WatchtowerLogo from '@/components/WatchtowerLogo.vue';

const login = () => {
  window.open("https://admobwatchtower.com/connect")
}

const easterEgg = () => {
  // Log in with a test account.
  store.set('authToken', "d537a8df-51a5-4ab3-84d8-7eaa1fcae5f7")
  authToken.value = "d537a8df-51a5-4ab3-84d8-7eaa1fcae5f7"
  router.push('/')
}
</script>
