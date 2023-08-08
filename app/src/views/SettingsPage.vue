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

      <ion-card v-if="Object.keys(profile).length">
        <ion-card-content>
          <ion-item lines="none">
            <ion-avatar slot="start">
              <img :src="profile.picture_url" />
            </ion-avatar>
            <ion-label>
              {{ profile.first_name }} {{ profile.last_name }}
              <br />
              {{ profile.email }}
            </ion-label>
          </ion-item>
        </ion-card-content>
      </ion-card>

      <div style="text-align:center;" class="ion-padding">
        <ion-button v-if="!authToken" @click="login" expand="full">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Login
        </ion-button>
        <ion-button v-if="authToken" @click="login" expand="full">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Reauthenticate
        </ion-button>
        <ion-button v-if="authToken" @click="logout" expand="full" color="danger">
          <ion-icon slot="start" :icon="logOutOutline"></ion-icon>
          Logout
        </ion-button>

        <ion-button href="https://admobwatchtower.com/privacy" target="_blank" expand="full" fill="clear">Privacy
          Policy</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>


<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonCard, IonCardContent, IonItem, IonAvatar, IonLabel } from '@ionic/vue';
import { authToken, store } from '@/state';
import { logInOutline, logOutOutline } from 'ionicons/icons';
import { fetchProfile } from '@/api'
import { watch, ref } from 'vue'
import { Capacitor } from '@capacitor/core';
import router from '@/router';

const loadData = () => {
  if (!authToken.value) {
    profile.value = {}
    return
  }
  fetchProfile().then((res) => {
    profile.value = res
  })
}

const profile = ref({})
watch(authToken, loadData)
loadData()

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

const logout = () => {
  authToken.value = ''
  store.clear()
}
</script>
