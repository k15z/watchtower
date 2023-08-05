<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Settings</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Settings</ion-title>
        </ion-toolbar>
      </ion-header>

      <div id="container">
        <ion-button v-if="!authToken" @click="login" size="small" fill="outline">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Login
        </ion-button>
        <ion-button v-if="authToken" @click="logout" size="small" fill="outline">
          <ion-icon slot="start" :icon="logOutOutline"></ion-icon>
          Logout
        </ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<style scoped>
#container {
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}
</style>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon } from '@ionic/vue';
import { authToken, store } from '@/state';
import { logInOutline, logOutOutline } from 'ionicons/icons';


const login = () => {
  authToken.value = 'aa8d6daa-a842-4acf-b948-957c6b4bb447'
  store.set('authToken', 'aa8d6daa-a842-4acf-b948-957c6b4bb447')
}

const logout = () => {
  authToken.value = null
  store.clear()
}
</script>
