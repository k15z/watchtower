<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="fill-height">
          <v-card-title>
            Developers
          </v-card-title>
          <v-card-text>
            <v-container class="pa-0">
              <v-row no-gutters>
                <v-col>
                  <p class="pb-4">
                    Developers can interact with Watchtower via the REST API which allows you to
                    fetch both your raw AdMob data and the network eCPM comparison report. If you
                    plan on querying the API frequently, please consider donating to support this
                    project; otherwise, I reserve the right to apply rate limiting at any time in
                    order to manage server costs.
                  </p>
                  <v-row>
                    <v-col>
                      <v-btn block color="info" @click="generateAPIKey">Generate API Key</v-btn>
                    </v-col>
                    <v-col><v-btn block color="red" @click="revokeAPIKeys">Revoke API Keys</v-btn></v-col>
                  </v-row>
                  <v-alert v-if="data.developer_message" class="mt-4" style="text-align:center; font-size: 0.85rem;">
                    {{ data.developer_message }}
                  </v-alert>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-card class="fill-height">
          <v-card-title>
            Donate
          </v-card-title>
          <v-card-text>
            <p>
              If you found Watchtower useful, please consider donating to support this project. Your
              contributions help cover server costs and fund the developments of new features such as
              detection alerts and automated insights.
            </p>
            <br />
            <div class="pa-4" style="text-align: center;">
              <form action="https://www.paypal.com/donate" method="post" target="_top">
                <input type="hidden" name="business" value="CF7PFGT4B5FNC" />
                <input type="hidden" name="no_recurring" value="0" />
                <input type="hidden" name="currency_code" value="USD" />
                <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0"
                  name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
                <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
              </form>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <v-card-title>
            Contact Me
          </v-card-title>
          <v-card-text>
            <p class="pb-4">
              Feel free to reach out if you run into any issues, have any feature suggestions,
              or just want to chat!
            </p>
            <v-text-field v-model="data.email" label="Email" placeholder="hello@kevz.dev" type="email"></v-text-field>
            <v-textarea v-model="data.message" label="Message" placeholder="Say hello!"></v-textarea>
            <v-btn @click="sendMessage" block>Submit</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <div class="pt-4" style="text-align: right;">
      <v-btn @click="signOut" color="outline" class="mr-4">Sign Out</v-btn>
      <v-btn @click="deleteAccount" color="red">Delete Account</v-btn>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import router from "../router"
import { store } from "@/store"
import { BASE_API_URL } from "@/api";
import { reactive } from 'vue'

const data = reactive({
  "developer_message": "",
  email: '',
  message: '',
})

function generateAPIKey() {
  return fetch(BASE_API_URL + "/account/api_keys", {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Authorization': `Bearer ${store.token}`,
      'Content-Type': 'application/json'
    }
  }).then(async (res) => {
    data.developer_message = "API Key: " + (await res.text())
  })
}

function revokeAPIKeys() {
  return fetch(BASE_API_URL + "/account/api_keys", {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Authorization': `Bearer ${store.token}`,
      'Content-Type': 'application/json'
    }
  }).then(async (res) => {
    data.developer_message = "Success! All API keys have been revoked."
  })
}

function sendMessage() {
  return fetch(BASE_API_URL + "/account/message", {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Authorization': `Bearer ${store.token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: data.email,
      message: data.message
    })
  }).then(async (res) => {
    data.email = ''
    data.message = ''
  })
}

function deleteAccount() {
  return fetch(BASE_API_URL + "/account", {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Authorization': `Bearer ${store.token}`,
      'Content-Type': 'application/json'
    },
  }).then(async (res) => {
    localStorage.clear()
    router.push("/")
  })
}

function signOut() {
  localStorage.clear()
  router.push("/")
}
</script>
