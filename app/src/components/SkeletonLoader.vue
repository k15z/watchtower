<template>
    <template v-for="index in rows" :key="index">
        <ion-skeleton-text :animated="true"></ion-skeleton-text>
    </template>
</template>

<style scoped>
ion-skeleton-text {
    margin-top: 12px;
    margin-bottom: 12px;
}
</style>

<script lang="ts" setup>
import { IonSkeletonText } from '@ionic/vue';

defineProps({
    rows: {
        type: Number,
        default: 3
    }
})
</script>
