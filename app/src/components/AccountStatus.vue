<template>
    <ion-card color="warning" v-if="Object.values(profile).length > 0 && profile.status != 'FINISHED_BACKFILL'">
        <ion-card-content>
            Your account is still being prepared which may take a few minutes. Your results will be incomplete in 
            the meantime.
        </ion-card-content>
    </ion-card>
</template>

<script setup lang="ts">
import { profile } from '@/state'
import { IonCard, IonCardContent } from "@ionic/vue";
</script>
