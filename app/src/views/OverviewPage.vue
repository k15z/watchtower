<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Overview</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Overview</ion-title>
        </ion-toolbar>
      </ion-header>

      <template v-for="card in overviewCards">
        <component :is="cardDefinitions[card.key].component" :options="card.options"></component>
      </template>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { overviewCards } from '@/state'
import { cardDefinitions } from '@/cards';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
</script>
