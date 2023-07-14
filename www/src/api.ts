import { store } from './store'

const BASE_API_URL = "http://localhost:8000"
//const BASE_API_URL = "https://5l40l9u6y0.execute-api.us-east-1.amazonaws.com/api"

function helloWorld() {
    // Used to warm up a Lambda instance
    return fetch(BASE_API_URL + "/hello", {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

function ecpmByBreakdowns(breakdowns: string) {
    return fetch(BASE_API_URL + "/network/ecpm?breakdowns=" + breakdowns, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${store.token}`,
            'Content-Type': 'application/json'
        }
    })
}

function realtimeByApp(period: string, previous: boolean) {
    if (previous) {
        period += "&previous=true"
    }
    return fetch(BASE_API_URL + "/realtime/by_app?period=" + period, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${store.token}`,
            'Content-Type': 'application/json'
        }
    })
}

function realtimeQuery(start: string, end: string, breakdowns: string[]) {
    return fetch(BASE_API_URL + "/realtime/query?start=" + start + "&end=" + end + "&breakdowns=" + breakdowns.join(","), {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${store.token}`,
            'Content-Type': 'application/json'
        }
    })
}

export { BASE_API_URL, helloWorld, ecpmByBreakdowns, realtimeByApp, realtimeQuery }