<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="tab1" href="/tabs/overview">
          <ion-icon aria-hidden="true" :icon="barChartOutline" />
          <ion-label>Overview</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="tab2" href="/tabs/explore">
          <ion-icon aria-hidden="true" :icon="albumsOutline" />
          <ion-label>Explore</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="tab3" href="/tabs/settings">
          <ion-icon aria-hidden="true" :icon="settingsOutline" />
          <ion-label>Settings</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { settingsOutline, albumsOutline, barChartOutline } from 'ionicons/icons';
</script>
