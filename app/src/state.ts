import { ref, reactive, watch } from 'vue';
import router from './router';
import { Storage } from '@ionic/storage';
import { App, URLOpenListenerEvent } from '@capacitor/app';
import { fetchProfile } from '@/api'

const store = new Storage();
const authToken = ref("");
const overviewCards = reactive([
    { "key": 'ReportCard', "options": {} },
    { "key": 'HeatMapImpressions', "options": { 'target': 'impressions' } },
    { "key": 'EarningsByDayOfWeek', "options": {} },
]) as any
const profile = ref({})

const loadProfile = () => {
    if (!authToken.value) {
        return;
    }
    fetchProfile().then((res) => {
        profile.value = res
    }).catch((err) => {
        alert("Unable to fetch profile.")
        authToken.value = ""
        store.set('authToken', '')
        router.push("/onboarding")
    })
}
watch(authToken, loadProfile)

store.create().then(async () => {
    App.addListener('appUrlOpen', function (event: URLOpenListenerEvent) {
        // Handle an authentication callback. After the user authenticates on the website, 
        // they are redirected to the app with: watchtower://connect?token=...
        const token = event.url.split('=').pop();
        authToken.value = token as string
        store.set('authToken', token)
        router.push('/')
    });

    authToken.value = await store.get('authToken')
    if (!authToken.value) {
        router.push('/onboarding')
    }
});


export { authToken, overviewCards, store, profile, loadProfile }
