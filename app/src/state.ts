import { ref, reactive } from 'vue';
import { Storage } from '@ionic/storage';
import { App, URLOpenListenerEvent } from '@capacitor/app';

const store = new Storage();
const authToken = ref("");
const overviewCards = reactive([]) as any

store.create().then(async () => {
    authToken.value = await store.get('authToken')
    if (authToken.value) {
        overviewCards.push(...[
            { "key": 'ReportCard', "options": {} },
            { "key": 'PlatformECPMCard', "options": {} },
        ])
    } else {
        overviewCards.push(...[
            { "key": 'PlatformECPMCard', "options": {} },
            { "key": 'ECPMByGenre', "options": {} },
        ])
    }

    App.addListener('appUrlOpen', function (event: URLOpenListenerEvent) {
        // Handle an authentication callback. After the user authenticates on the website, 
        // they are redirected to the app with: watchtower://connect?token=...
        const token = event.url.split('=').pop();
        console.log("Received authentication token: " + token)
        authToken.value = token as string
        store.set('authToken', token)
    });
});


export { authToken, overviewCards, store }
