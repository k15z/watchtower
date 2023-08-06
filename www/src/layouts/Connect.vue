<template>
    <v-container class="h-screen">
        <v-responsive class="align-center text-center fill-height">
            Connecting to app...
        </v-responsive>
    </v-container>
</template>

<script setup lang="ts">
// TODO: Replace with Google OAuth2 flow. Here's a temporary dummy user for testing:
window.open("watchtower://connect?token=aa8d6daa-a842-4acf-b948-957c6b4bb447", "_self")
</script>
