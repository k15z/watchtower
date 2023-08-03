<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Explore</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Explore</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-searchbar v-model="query"></ion-searchbar>

      <ion-card @click="previewCard(card)" v-for="(card, key) in filteredCardDefinitions" :key="key">
        <ion-card-header>
          <ion-card-subtitle>{{ card.name }}</ion-card-subtitle>
        </ion-card-header>
        <ion-card-content>
          {{ card.description }}
        </ion-card-content>
      </ion-card>

      <ion-modal :is-open="showModal" @willDismiss="dismissModal">
        <ion-header>
          <ion-toolbar>
            <ion-buttons slot="start">
              <ion-button @click="dismissModal()">Close</ion-button>
            </ion-buttons>
            <ion-buttons slot="end">
              <ion-button :strong="true" @click="addCard(selectedCard)">Add</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding">
          <template v-if="selectedCard">
            <div>
              <h1 style="text-align: center;">{{ selectedCard.name }}</h1>
              <p style="text-align: justify;">{{ selectedCard.description }}</p>
            </div>
            <component style="margin:0px;" :is="selectedCard.component"></component>
          </template>
        </ion-content>
      </ion-modal>
    </ion-content>
  </ion-page>
</template>

<style scoped>
ion-card-header {
  padding-bottom: 0px;
}
</style>

<script setup lang="ts">
import { ref, shallowRef, computed } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonButton, IonButtons, IonModal, IonTitle, IonContent, IonSearchbar, IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';
import { cardDefinitions } from '@/cards';
import { overviewCards } from '@/state'

const query = ref("")
const filteredCardDefinitions = computed(() => {
  const filteredDefs = {} as any;
  Object.keys(cardDefinitions).map((key: string) => {
    if (
      cardDefinitions[key].name.toLowerCase().includes(query.value.toLowerCase()) ||
      cardDefinitions[key].description.toLowerCase().includes(query.value.toLowerCase())
    ) {
      filteredDefs[key] = cardDefinitions[key]
    }
  })
  return filteredDefs
})

const showModal = ref(false)
const selectedCard = shallowRef(undefined) as any

const dismissModal = () => {
  showModal.value = false
}

const previewCard = (card: any) => {
  showModal.value = true
  selectedCard.value = card
}

const addCard = (card: any) => {
  overviewCards.push({
    key: card.key,
    options: {}
  })
  showModal.value = false
}
</script>
