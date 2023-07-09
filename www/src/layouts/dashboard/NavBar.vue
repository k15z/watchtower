<template>
    <v-navigation-drawer :permanent="true" :rail="$vuetify.display.mobile">
        <v-list>
            <v-list-item :prepend-avatar="store.profile.picture_url" :title="store.profile.first_name"
                :subtitle="store.profile.email">
            </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
            <v-list-item to="/dashboard/overview" prepend-icon="mdi-view-dashboard" title="Overview"></v-list-item>
            <v-list-item to="/dashboard/data" prepend-icon="mdi-table" title="Data Explorer"></v-list-item>
            <v-list-item to="/dashboard/ecpm" prepend-icon="mdi-cash-multiple" title="Network eCPM"></v-list-item>
        </v-list>

        <template v-slot:append>
            <v-list density="compact">
                <v-list-item to="/dashboard/settings" prepend-icon="mdi-cog" title="Settings"></v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>

<script lang="ts" setup>
import { BASE_API_URL } from '../../api'
import { store } from '../../store'
import router from '../../router'

fetch(BASE_API_URL + "/account", {
    method: 'GET',
    mode: 'cors',
    headers: {
        'Authorization': `Bearer ${store.token}`,
        'Content-Type': 'application/json'
    }
}).then((res) => {
    if (res.ok) {
        res.json().then((res: any) => {
            store.profile.status = res.status;
            store.profile.first_name = res.first_name;
            store.profile.last_name = res.last_name;
            store.profile.picture_url = res.picture_url;
            store.profile.email = res.email;
        })
    } else {
        router.push('/')
    }
})
</script>
../../api