<template>
  <v-container class="h-screen">
    <v-responsive class="align-center text-center fill-height">
      <v-img height="300" src="@/assets/logo.png" />

      <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

      <h1 class="text-h2 font-weight-bold">AdMob Watchtower</h1>

      <div class="py-14" />

      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <v-btn href="#anchor" min-width="164" rel="noopener noreferrer" variant="text">
            <v-icon icon="mdi-puzzle" size="medium" start />

            How It Works
          </v-btn>
        </v-col>

        <v-col cols="auto">
          <template v-if="!state.is_signed_in">
            <v-btn @click="launchAuthorizationFlow" color="red" min-width="228" rel="noopener noreferrer" size="large"
              variant="flat">
              <v-icon icon="mdi-google" size="large" start />

              Sign In With Google
            </v-btn>
          </template>
          <template v-if="state.is_signed_in">
            <v-btn :to="'dashboard'" color="red" min-width="228" rel="noopener noreferrer" size="large" variant="flat">
              <v-icon icon="mdi-view-dashboard" size="large" start />

              Go To Dashboard
            </v-btn>

          </template>
        </v-col>

        <v-col cols="auto">
          <v-btn @click="getTheApp" min-width="164" rel="noopener noreferrer" variant="text">
            <v-icon icon="mdi-cellphone" size="medium" start />

            Get The App
          </v-btn>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
  <div id="anchor" style="background-color: #D85140; height:24px;"></div>
  <v-container class="pt-16 pb-16">
    <v-row justify="center">
      <v-col cols="auto" md="6" sm="12" xs="12">
        <h1 class="text-h5 font-weight-bold">How It Works</h1>
        <table class="features">
          <tr>
            <td class="icon">
              <v-icon icon="mdi-lock-check-outline" size="x-large"></v-icon>
            </td>
            <td>
              Share your AdMob data safely by logging in with your Google Account.
            </td>
          </tr>
          <tr>
            <td class="icon">
              <v-icon icon="mdi-account-group" size="x-large"></v-icon>
            </td>
            <td>
              Benchmark your eCPM with similar apps in your category to find opportunities.
            </td>
          </tr>
          <tr>
            <td class="icon">
              <v-icon icon="mdi-bell-badge" size="x-large"></v-icon>
            </td>
            <td>
              Use alerting to automatically spot potential issues with your AdMob setup.
            </td>
          </tr>
        </table>
      </v-col>
      <v-col cols="auto" md="6" sm="12" xs="12">
        <h1 class="text-h5 font-weight-bold">Use Cases</h1>
        <br />
        <v-expansion-panels variant="accordion">
          <v-expansion-panel>
            <v-expansion-panel-title>Detect issues in new releases</v-expansion-panel-title>
            <v-expansion-panel-text><b>Suppose you accidentally released a new version of the app
                with
                test
                ads instead of real ads,
                resulting in no valid impressions.</b> Watchtower can automatically alert you
              when
              it
              detects anomalies in your eCPM across various breakdowns.</v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>Troubleshoot unusual eCPM values</v-expansion-panel-title>
            <v-expansion-panel-text><b>Suppose your eCPM is much lower this week compared to the
                previous
                week.</b> Watchtower can
              help
              you identify whether the issue is specific to you or whether it's a larger trend
              affecting
              others as well.</v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>Explore the AdMob network</v-expansion-panel-title>
            <v-expansion-panel-text><b>Suppose you're considering rolling out your app to a new
                geographic
                region which would require additional work.</b> Watchtower
              can
              help you understand the current state of the market in that region for apps in your
              category.</v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
  <v-container>
    <table class="footer">
      <tr>
        <td>
          Copyright 2023, <a class="text-decoration-none" href="https://kevz.dev/">Kevin Alex Zhang</a>
        </td>
        <td class="text-end">
          <a class="text-decoration-none" href="privacy">Privacy Policy</a>
          <a class="text-decoration-none" href="terms">Terms of Service</a>
        </td>
      </tr>
    </table>
  </v-container>
</template>

<style scoped>
table.features {
  padding-top: 12px;
}

table.features td {
  padding: 24px;
}

table.features td.icon {
  font-size: 2rem;
}

table.footer {
  width: 100%;
  font-size: 0.8rem;
}

table.footer a {
  color: #D85140;
}

table.footer .text-end a {
  padding-left: 12px;
}

table.footer a:hover {
  color: #B83120;
}
</style>

<script lang="ts" setup>
import { reactive } from 'vue'
import router from '../router'
import { BASE_API_URL } from '../api'
import { store } from '../store'

const state = reactive({
  is_signed_in: localStorage.getItem("token") ? true : false
})

function validateAuthorizationCode(code: string) {
  fetch(BASE_API_URL + "/authorize", {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'auth_code': code
    })
  }).then((resp) => {
    if (resp.ok) {
      resp.json().then((res) => {
        state.is_signed_in = true
        store.token = res.token
        localStorage.setItem("token", res.token)
        router.push('/dashboard')
      })
    } else {
      alert("Please try again using the Google Account linked to your AdMob profile.")
    }
    console.log(resp)
  })
}

function launchAuthorizationFlow() {
  // @ts-ignore
  const client = google.accounts.oauth2.initCodeClient({
    client_id: '758313252344-959jdouposo1nd3mq7c01b6rbv0mf8hf.apps.googleusercontent.com',
    scope: 'https://www.googleapis.com/auth/admob.readonly https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    ux_mode: 'popup',
    callback: (authorization: any) => {
      validateAuthorizationCode(authorization.code)
    }
  })
  client.requestCode()
}

function getTheApp() {
  alert("Coming soon!")
}
</script>
../api