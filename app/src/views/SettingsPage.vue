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
        <ion-button @click="restoreDefaults" expand="full" color="secondary">
          <ion-icon slot="start" :icon="refreshOutline"></ion-icon>
          Restore Default Cards
        </ion-button>
        <ion-button v-if="!authToken" @click="login" expand="full">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Login
        </ion-button>
        <ion-button v-if="authToken" @click="login" expand="full" color="primary">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Reauthenticate
        </ion-button>
        <ion-button v-if="authToken" @click="logout" expand="full" color="warning">
          <ion-icon slot="start" :icon="logOutOutline"></ion-icon>
          Logout
        </ion-button>
        <ion-button v-if="authToken" @click="callDeleteAccount" expand="full" color="danger">
          <ion-icon slot="start" :icon="trashOutline"></ion-icon>
          Delete Account
        </ion-button>

        <ion-button href="https://admobwatchtower.com/privacy" target="_blank" expand="full" fill="clear">Privacy
          Policy</ion-button>

        <watchtower-logo style="width:2em" @easter-egg="easterEgg"></watchtower-logo>
      </div>
    </ion-content>
  </ion-page>
</template>


<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonCard, IonCardContent, IonItem, IonAvatar, IonLabel, alertController } from '@ionic/vue';
import { authToken, store, overviewCards, profile } from '@/state';
import { cardDefinitions } from '@/cards';
import { logInOutline, logOutOutline, refreshOutline, trashOutline } from 'ionicons/icons';
import router from '@/router';
import { deleteAccount } from '@/api';
import WatchtowerLogo from '@/components/WatchtowerLogo.vue';

const login = () => {
  window.open("https://admobwatchtower.com/connect")
}

const restoreDefaults = () => {
  overviewCards.length = 0
  overviewCards.push(...[
    { "key": 'ReportCard' },
    { "key": 'HeatMapImpressions' },
    { "key": 'EarningsByDayOfWeek' },
  ])
  router.push("/")
}

const logout = () => {
  authToken.value = ''
  store.clear()
  router.push("/onboarding")
}

const callDeleteAccount = async () => {
  const alert = await alertController.create({
    header: 'Are you sure?',
    message: 'Your account data will be deleted and may not be recoverable.',
    buttons: [
      {
        text: 'Cancel',
      },
      {
        text: 'Delete',
        handler: async () => {
          logout()
          deleteAccount()
        }
      }
    ],
  });
  await alert.present();
}

function shuffle(a: any[]) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const easterEgg = () => {
  alert("🥚🐣🐥")
  const kitchenSink: any = [];
  Object.values(cardDefinitions).forEach((card: any) => {
    kitchenSink.push({ "key": card.key, "options": card.options ? card.options : {} })
  })
  overviewCards.length = 0
  overviewCards.push(...kitchenSink)
  shuffle(overviewCards)
  router.push("/")
}
</script>
