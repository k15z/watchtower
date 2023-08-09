<template>
    <img @click="onClick" src="/public/favicon.png" alt="Watchtower Logo" />
</template>

<script setup lang="ts">
const emit = defineEmits(['easter-egg'])

let counter = 0;
const onClick = () => {
  counter += 1;
  if (counter == 5) {
    emit('easter-egg')
  }
}
</script>
