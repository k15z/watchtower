<template>
  <v-container class="h-screen">
    <v-responsive class="align-center text-center fill-height">
      <v-img height="300" src="@/assets/logo.png" />

      <h1 class="text-h3 font-weight-bold">AdMob Watchtower</h1>
      <div class="text-body-1 font-weight-light mb-n1">A third-party app for bringing transparency to the AdMob network.
      </div>

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
            <v-btn to="/dashboard" color="red" min-width="228" rel="noopener noreferrer" size="large" variant="flat">
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
              <v-icon icon="mdi-cash-multiple" size="x-large"></v-icon>
            </td>
            <td>
              Use the Network eCPM report to compare your eCPM with peers to find issues as
              well as opportunities.
            </td>
          </tr>
          <tr>
            <td class="icon">
              <v-icon icon="mdi-table" size="x-large"></v-icon>
            </td>
            <td>
              Use the Data Explorer to navigate your AdMob data and gain new insights into
              your ad revenue.
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
                resulting in no valid impressions.</b> Watchtower can help you
              find anomalies in your eCPM across various breakdowns.</v-expansion-panel-text>
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
                region.</b> Watchtower
              can
              help you understand the current state of the market in that region for apps in your
              category.</v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
  <v-container class="pb-16">
    <v-row>
      <v-col>
        <h1 class="text-h5 font-weight-bold">Data Explorer</h1>
        Explore your realtime AdMob statistics with the built-in data explorer to see all your data in one place.
        <img style="max-width: 100%;" src="@/assets/overview.png" />
      </v-col>
    </v-row>
    <v-row class="pt-16">
      <v-col cols="auto" md="6" sm="12">
        <h1 class="text-h5 font-weight-bold">Network eCPM</h1>
        <p>
          Understand the state of the market by exploring eCPM breakdowns based on:
        </p>
        <ul class="pa-6">
          <li>Time</li>
          <li>Format</li>
          <li>Country</li>
          <li>App genre</li>
          <li>Personalization</li>
        </ul>
        Discover issues and find new opportunities with the Network eCPM report which provides you with the latest data
        from across our network.
      </v-col>
      <v-col cols="auto" md="6" sm="12">
        <div style="text-align:center;">
          <img style="max-width: 100%; border: 3px solid #ddd; border-radius: 10px;" src="@/assets/map.png" />
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-container class="pb-16">
    <v-row>
      <v-col cols="auto" md="6" sm="12">
        <h1 class="text-h5 font-weight-bold">Open Source</h1>
        <p>
          Explore the <a href="https://github.com/k15z/watchtower/">code base</a> on GitHub. Feel free to jump in and
          pick up an issue or two to work on - contributions are greatly appreciated. Or, if you want to build something
          on top of our platform, you can sign in and generate an API key to develop against the Watchtower API.
        </p>
      </v-col>
      <v-col cols="auto" md="6" sm="12">
        <h1 class="text-h5 font-weight-bold">Privacy Preserving</h1>
        <p>
          All of your data is anonymized and aggregated prior to being included in the Network eCPM report. We protect
          all your data, but we take special steps to protect sensitive attributes such as your identity, your apps,
          and your total revenue.
        </p>
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
  <v-overlay :model-value="state.is_validating" class="align-center justify-center">
    <v-progress-circular color="primary" indeterminate size="64"></v-progress-circular>
  </v-overlay>
  <v-overlay :model-value="state.show_app_preview" class="align-center justify-center" @afterLeave="state.show_app_preview=false">
    <v-card class="pa-4" max-width="480">
      <v-card-title>
        Coming Soon
      </v-card-title>
      <v-card-text>
        <p>
          We're hard at work building Watchtower for iOS and Android! Sign up here to get notified when
          the release is ready and to get early access to developer builds.
        </p>
        <p class="pt-4">
          <v-text-field v-model="state.email" label="Email address" type="email" placeholder="me@kevz.dev"></v-text-field>
        </p>
        <v-btn @click="subscribe" color="primary" block>Subscribe</v-btn>
      </v-card-text>
    </v-card>
  </v-overlay>
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
import { BASE_API_URL, helloWorld, sendMessage } from '../api'
import { store } from '../store'
import { event } from 'vue-gtag'

const state = reactive({
  email: '',
  is_validating: false,
  show_app_preview: false,
  is_signed_in: localStorage.getItem("token") ? true : false
})

function validateAuthorizationCode(code: string) {
  event("validation_start", {})
  state.is_validating = true
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
    state.is_validating = false
    if (resp.ok) {
      resp.json().then((res) => {
        event("validation_success", {})
        state.is_signed_in = true
        store.token = res.token
        localStorage.setItem("token", res.token)
        router.push('/dashboard')
      })
    } else {
      event("validation_fail", {})
      alert("Please try again using the Google Account linked to your AdMob profile.")
    }
  })
}

function launchAuthorizationFlow() {
  event("authorize_start", {})
  // @ts-ignore
  const client = google.accounts.oauth2.initCodeClient({
    client_id: '758313252344-959jdouposo1nd3mq7c01b6rbv0mf8hf.apps.googleusercontent.com',
    scope: 'https://www.googleapis.com/auth/admob.readonly https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    ux_mode: 'popup',
    callback: (authorization: any) => {
      event("authorize_received", {})
      validateAuthorizationCode(authorization.code)
    },
    error_callback: (error: any) => {
      event("authorize_failed", error)
    }
  })
  client.requestCode()

  // Call a random API to warm up the Lambda function
  helloWorld()
}

function getTheApp() {
  event("get_the_app", {})
  state.show_app_preview = true
}

function subscribe() {
  sendMessage(state.email, "Let me know when the app is ready!");
  state.email = '';
  state.show_app_preview = false
}
</script>
