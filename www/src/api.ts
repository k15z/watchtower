import { store } from './store'

//const BASE_API_URL = "https://5l40l9u6y0.execute-api.us-east-1.amazonaws.com/api"
const BASE_API_URL = "http://127.0.0.1:8000"

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

export { BASE_API_URL, ecpmByBreakdowns }