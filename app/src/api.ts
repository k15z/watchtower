import { authToken } from '@/state'
import { Capacitor } from '@capacitor/core';

// const BASE_API_URL = ""
let BASE_API_URL = "https://5l40l9u6y0.execute-api.us-east-1.amazonaws.com/api"
if (Capacitor.getPlatform() == 'web') {
    BASE_API_URL = "http://localhost:8000"
}

export const deleteAccount = async () => {
    return fetch(BASE_API_URL + "/account", {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${authToken.value}`,
            'Content-Type': 'application/json'
        },
    })
}

export const fetchProfile = async () => {
    let response = await fetch(BASE_API_URL + "/account", {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${authToken.value}`,
            'Content-Type': 'application/json'
        }
    })
    if (response.status !== 200) {
        throw new Error("Failed to fetch profile")
    }
    return await response.json()
}

export const fetchCard = async (name: string, options: any) => {
    let response = await fetch(BASE_API_URL + "/card", {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${authToken.value}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            options: options
        })
    })
    return await response.json()
}
