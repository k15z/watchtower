<template>
    <v-container class="h-screen">
        <v-responsive class="align-center text-center fill-height">
            <div>
                <a href="/"><img style="width:6em;" src="/public/favicon.png" alt="Watchtower Logo" /></a>
                <h1 class="text-h5 font-weight-bold">Watchtower</h1>
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
            </div>
            <template v-if="loading">
                <v-progress-circular indeterminate size="64" color="red" />
            </template>
            <template v-if="!loading && !success">
                <v-btn @click="launchAuthorizationFlow" color="red" min-width="228" rel="noopener noreferrer" size="default"
                    variant="flat">
                    <v-icon icon="mdi-google" size="large" start />
                    Sign In With Google
                </v-btn>
            </template>
            <template v-if="!loading && success">
                <v-btn @click="openApp" color="red" min-width="228" rel="noopener noreferrer" size="default" variant="flat">
                    <v-icon icon="mdi-exit-to-app" size="large" start />
                    Launch The App
                </v-btn>
            </template>
        </v-responsive>
        <v-dialog v-model="showError" width="auto">
            <v-card>
                <v-card-text>
                    There was an error connecting to your AdMob account. Please make sure that the Google Account you
                    signed in with is associated with an AdMob account in good standing.
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" block @click="showError = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { event } from 'vue-gtag'
import { BASE_API_URL, helloWorld } from '../api'

const loading = ref(false)
const success = ref(false)
const showError = ref(false)

function validateAuthorizationCode(code: string) {
    event("validation_start", {})
    loading.value = true
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
        loading.value = false
        if (resp.ok) {
            resp.json().then((res) => {
                event("validation_success", {})
                localStorage.setItem("token", res.token)
                window.open("watchtower://connect?token=" + res.token, "_self")
            })
            success.value = true
        } else {
            event("validation_fail", {})
            showError.value = true
        }
    })
}

function openApp() {
    const token = localStorage.getItem("token")
    window.open("watchtower://connect?token=" + token, "_self")
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
</script>
