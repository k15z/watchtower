<template>
    <ion-card>
        <ion-card-header>
            <ion-card-subtitle>eCPM Map</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
            <div style="height:300px; width:100%">
                <l-map ref="map" :zoom="3" :center="[39.8282, -98.5796]" :use-global-leaflet="false"
                    :options="{ attributionControl: false }">
                    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
                        name="OpenStreetMap"></l-tile-layer>
                </l-map>
            </div>
        </ion-card-content>
    </ion-card>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardContent } from '@ionic/vue';

import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

const map = ref(null) as any
onMounted(() => {
    setInterval(() => {
        if (map.value?.leafletObject) {
            map.value.leafletObject?.invalidateSize();
        }
    }, 1000)
})
</script>
  
<style></style>
