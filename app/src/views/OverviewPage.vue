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

      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content></ion-refresher-content>
      </ion-refresher>

      <account-status></account-status>

      <ion-reorder-group :key="componentKey" :disabled="!editable" @ionItemReorder="handleReorder($event)">
        <template v-for="(card, idx) in overviewCards" :key="card.key">
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
        <ion-fab-button @click="toggleEditable" size="small" color="medium">
          <ion-icon :icon="editable ? closeOutline : pencilOutline" size="small"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { authToken, overviewCards, loadProfile } from '@/state'
import AccountStatus from '@/components/AccountStatus.vue';
import { cardDefinitions } from '@/cards';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonReorder, IonButton, IonFab, IonIcon, IonFabButton, IonReorderGroup, IonRefresher, IonRefresherContent } from '@ionic/vue';
import { closeOutline, reorderThreeOutline, trashOutline, pencilOutline } from 'ionicons/icons';

const editable = ref(false)
const componentKey = ref(0)

const toggleEditable = async () => {
  editable.value = !editable.value
}

const deleteCard = (idx: number) => {
  overviewCards.splice(idx, 1)

}
const handleReorder = (event: CustomEvent) => {
  event.detail.complete(overviewCards);
};

const handleRefresh = (event: any) => {
  componentKey.value += 1
  event.target.complete();
  loadProfile()
}

watch(authToken, () => {
  componentKey.value += 1
})

onBeforeRouteLeave((to: any, from: any, next: any) => {
  editable.value = false
  next()
})
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