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
          <p>
            {{ card.description }}
          </p>
          <div>
            <tag-chip :tag="tag" v-for="tag in card.tags"></tag-chip>
          </div>
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
              <p style="text-align: left;">{{ selectedCard.description }}</p>
              <div style="padding-bottom:1em;">
                <tag-chip :tag="tag" v-for="tag in selectedCard.tags"></tag-chip>
              </div>
            </div>
            <template v-if="selectedCard.tags.indexOf('Public') < 0 && !authToken">
              <ion-card style="margin:0px;" color="danger">
                <ion-card-content>
                  This card contains data that requires access to your AdMob account. You can connect
                  your account in the Settings tab.
                </ion-card-content>
              </ion-card>
            </template>
            <template v-if="!(selectedCard.tags.indexOf('Public') < 0 && !authToken)">
              <component style="margin:0px;" :is="selectedCard.component" :options="selectedCard.options"></component>
            </template>
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

ion-chip {
  margin-left: 0;
  font-size: 0.8em;
}
</style>

<script setup lang="ts">
import { ref, shallowRef, computed } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonButton, IonButtons, IonModal, IonChip, IonTitle, IonContent, IonSearchbar, IonCard, IonCardHeader, IonCardSubtitle, IonCardContent, alertController } from '@ionic/vue';
import { Tag, cardDefinitions } from '@/cards';
import { overviewCards } from '@/state'
import { authToken } from '@/state';
import TagChip from '@/components/TagChip.vue';

const query = ref("")
const filteredCardDefinitions = computed(() => {
  const filteredDefs = {} as any;
  Object.keys(cardDefinitions).map((key: string) => {
    if (
      cardDefinitions[key].name.toLowerCase().includes(query.value.toLowerCase()) ||
      cardDefinitions[key].tags.join(" ").toLowerCase().includes(query.value.toLowerCase()) ||
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
    options: card.options || {}
  })
  showModal.value = false
}
</script>
