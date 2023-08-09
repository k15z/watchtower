import { ref, reactive } from 'vue';
import router from './router';
import { Storage } from '@ionic/storage';
import { App, URLOpenListenerEvent } from '@capacitor/app';

const store = new Storage();
const authToken = ref("");
const overviewCards = reactive([
    { "key": 'ReportCard', "options": {} },
    { "key": 'EarningsByDayOfWeek', "options": {} },
    { "key": 'ECPMByPlatform', "options": {} },
]) as any

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


export { authToken, overviewCards, store }
