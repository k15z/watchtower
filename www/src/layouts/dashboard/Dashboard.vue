<template>
  <v-app>
    <nav-bar />
    <app-bar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import AppBar from './AppBar.vue'
import NavBar from './NavBar.vue'
</script>
