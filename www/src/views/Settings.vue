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
                      <v-btn block color="info">Generate API Key</v-btn>
                    </v-col>
                    <v-col><v-btn block color="red">Revoke API Keys</v-btn></v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card>
          <v-card-title>
            Featured Apps
          </v-card-title>
          <v-card-text>
            <p>
              If you opt-in, your app icon and description may be shown on the home page along with
              a link to download your app.
            </p>
            <v-checkbox label="Allow apps to be featured"></v-checkbox>
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
            If you found Watchtower useful, please consider donating to support this project. Your
            contributions help cover server costs and fund the developments of new features such as
            detection alerts and automated insights.
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
            <v-text-field label="Email" placeholder="hello@kevz.dev" type="email"></v-text-field>
            <v-textarea label="Message" placeholder="Say hello!"></v-textarea>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <div class="pt-4" style="text-align: right;">
      <v-btn @click="signOut" color="outline" class="mr-4">Sign Out</v-btn>
      <v-btn color="red">Delete Account</v-btn>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import router from "../router"
function signOut() {
  localStorage.clear()
  router.push("/")
}
</script>
