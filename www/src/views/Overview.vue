<template>
  <v-container>
    <template v-if="store.profile.status == 'STARTED_BACKFILL'">
      <v-row>
        <v-col>
          <v-alert color="warning" variant="tonal">
            Your account is still being prepared which can take up to 10 minutes to complete. You can still explore your
            data but some results may be missing or inaccurate until this is complete.
          </v-alert>
        </v-col>
      </v-row>
    </template>
    <template v-if="store.profile.status == 'ERROR'">
      <v-row>
        <v-col>
          <v-alert color="error" variant="tonal">
            Your account is in an error state. This is most likely because you revoked access to the AdMob API. To fix
            this, please sign out and reconnect your account to AdMob.
          </v-alert>
        </v-col>
      </v-row>
    </template>
    <v-row>
      <v-col>
        <overview-card></overview-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <time-series-card></time-series-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { store } from "../store"
import OverviewCard from '@/components/OverviewCard.vue'
import TimeSeriesCard from "@/components/TimeSeriesCard.vue";
</script>
