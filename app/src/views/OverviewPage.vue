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

      <ion-reorder-group :disabled="!editable" @ionItemReorder="handleReorder($event)">
        <template v-for="(card, idx) in overviewCards">
          <div>
            <component :is="cardDefinitions[card.key].component" :options="card.options"></component>
            <div class="edit-menu" v-if="editable">
              <ion-button @click="deleteCard(idx)" color="danger" size="small">
                <ion-icon :icon="trashOutline"></ion-icon>
              </ion-button>
              <ion-reorder style="display:inline;">
                <ion-button color="light" size="small">
                  <ion-icon :icon="reorderThreeOutline"></ion-icon>
                </ion-button>
              </ion-reorder>
            </div>
          </div>
        </template>
      </ion-reorder-group>

      <ion-fab slot="fixed" vertical="top" horizontal="end" edge="true">
        <ion-fab-button @click="toggleEditable" size="small" color="dark">
          <ion-icon :icon="editable ? closeOutline : pencilOutline" size="small"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { overviewCards } from '@/state'
import { cardDefinitions } from '@/cards';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonReorder, IonButton, IonFab, IonIcon, IonFabButton, IonReorderGroup } from '@ionic/vue';
import { closeOutline, reorderThreeOutline, trashOutline, pencilOutline } from 'ionicons/icons';

const editable = ref(false)

const toggleEditable = async () => {
  editable.value = !editable.value
}

const deleteCard = (idx: number) => {
  overviewCards.splice(idx, 1)

}
const handleReorder = (event: CustomEvent) => {
  const swap = overviewCards[event.detail.from]
  overviewCards[event.detail.from] = overviewCards[event.detail.to]
  overviewCards[event.detail.to] = swap
  event.detail.complete(false);
};
</script>

<style scoped>
.edit-menu {
  text-align: right;
  margin-right: 16px;
  margin-top: -24px;
}

.edit-menu ion-button {
  font-size: 12px;
}
</style>