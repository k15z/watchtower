/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import router from '../router'
import vue3GoogleLogin from 'vue3-google-login'
import VueApexCharts from "vue3-apexcharts";

// Types
import type { App } from 'vue'

export function registerPlugins (app: App) {
  loadFonts()
  app
    .use(vuetify)
    .use(router)
    .use(VueApexCharts)
    .use(vue3GoogleLogin, {
      clientId: '758313252344-959jdouposo1nd3mq7c01b6rbv0mf8hf.apps.googleusercontent.com'
    })
}
