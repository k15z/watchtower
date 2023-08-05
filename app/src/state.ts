import { ref, reactive } from 'vue';
import { Storage } from '@ionic/storage';

const store = new Storage();
await store.create();

const authToken = ref(await store.get('authToken'));

const overviewCards = reactive([]) as any
if (authToken.value) {
    overviewCards.push(...[
        { "key": 'ReportCard', "options": {} },
        { "key": 'PlatformECPMCard', "options": {} },
    ])
} else {
    overviewCards.push(...[
        { "key": 'PlatformECPMCard', "options": {} },
    ])
}

export { authToken, overviewCards, store }