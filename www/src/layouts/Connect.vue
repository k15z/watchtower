<template>
    <v-container class="h-screen">
        <v-responsive class="align-center text-center fill-height">
            <div>
                <h1 class="text-h5 font-weight-bold">AdMob Watchtower</h1>
                <br />
                <div class="text-body-1 font-weight-light mb-n1">
                    <span>Sign in with your Google Account to continue.</span>
                </div>
                <br />
            </div>
            <v-btn @click="launchAuthorizationFlow" color="red" min-width="228" rel="noopener noreferrer" size="large"
                variant="flat">
                <v-icon icon="mdi-google" size="large" start />

                Sign In With Google
            </v-btn>
        </v-responsive>
    </v-container>
</template>

<script setup lang="ts">
import { event } from 'vue-gtag'
import { BASE_API_URL, helloWorld } from '../api'

function validateAuthorizationCode(code: string) {
    event("validation_start", {})
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
                event("validation_success", {})
                localStorage.setItem("token", res.token)
                window.open("watchtower://connect?token=" + res.token, "_self")
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
</script>
