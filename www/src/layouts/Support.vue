<template>
    <v-container class="h-screen">
        <div class="pa-4">
            <h1 class="text-center">Support Center</h1>
        </div>
        <v-card>
            <v-card-title>
                Contact Us
            </v-card-title>
            <v-card-text>
                <p class="pb-4">
                    Feel free to reach out if you run into any issues, have any feature suggestions,
                    or just want to chat!
                </p>
                <v-text-field v-model="data.email" label="Email" placeholder="hello@kevz.dev" type="email"></v-text-field>
                <v-textarea v-model="data.message" label="Message" placeholder="Say hello!"></v-textarea>
                <v-btn @click="callSendMessage" block>Submit</v-btn>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup lang="ts">
import { sendMessage } from '../api'
import { reactive } from 'vue'

const data = reactive({
    email: '',
    message: '',
})

function callSendMessage() {
    sendMessage(data.email, data.message).then(async (res) => {
        data.email = ''
        data.message = ''
    })
}
</script>
