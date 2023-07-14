<template>
    <v-card class="fill-height">
        <v-card-text style="overflow-x: auto;">
            <div style="text-align:right;">
                <v-btn-toggle v-model="toggle" divided color="primary" mandatory style="height:1.7em;">
                    <v-btn @click="updateOverview" value="1-day">Today</v-btn>
                    <v-btn @click="updateOverview" value="7-day">Last 7 Days</v-btn>
                    <v-btn @click="updateOverview" value="28-day">Last 28 Days</v-btn>
                </v-btn-toggle>
            </div>
            <v-table class="stats">
                <thead>
                    <tr class="header">
                        <th>App</th>
                        <th>Earnings</th>
                        <th>Impressions</th>
                        <th>eCPM</th>
                        <th>Requests</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-if="Object.keys(overview.data).length == 0">
                        <tr v-if="overview.loading">
                            <td colspan="5" style="text-align: center; padding:1em">
                                <v-progress-circular indeterminate :width="3"></v-progress-circular>
                            </td>
                        </tr>
                        <tr v-if="!overview.loading">
                            <td colspan="5" style="text-align: center; padding:1em">
                                <template v-if="overview.error.length > 0">
                                    <div style="text-align: center; padding: 2em;" v-html="overview.error">
                                    </div>
                                </template>
                            </td>
                        </tr>
                    </template>
                    <template v-for="row in overview.data" v-bind:key="row">
                        <tr class="stats">
                            <td style="font-size:0.5em;">
                                <b>{{ row.name }}</b>
                                <br />
                                {{ row.platform }}
                            </td>
                            <td>
                                ${{ row.earnings }}
                                <span :class="{ 'loss': row.delta.earnings < 0 }" v-if="row.previous">${{
                                    row.previous.earnings
                                }} ({{
    row.delta.earnings }}%)</span>
                            </td>
                            <td>
                                {{ row.impressions }}
                                <span :class="{ 'loss': row.delta.impressions < 0 }" v-if="row.previous">{{
                                    row.previous.impressions }} ({{ row.delta.impressions }}%)</span>
                            </td>
                            <td>
                                ${{ row.eCPM }}
                                <span :class="{ 'loss': row.delta.eCPM < 0 }" v-if="row.previous">${{ row.previous.eCPM }}
                                    ({{
                                        row.delta.eCPM }}%)</span>

                            </td>
                            <td>
                                {{ row.requests }}
                                <span :class="{ 'loss': row.delta.requests < 0 }" v-if="row.previous">{{
                                    row.previous.requests
                                }} ({{
    row.delta.requests }}%)</span>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </v-table>
        </v-card-text>
    </v-card>
</template>

<style scoped>
.stats {
    margin-top: 12px;
    width: 100%;
    min-width: 600px;
    table-layout: fixed;
}

table tbody tr td {
    padding: 12px !important;
}

table .header th {
    font-size: 0.8em;
    padding-bottom: 12px;
}

table .stats {
    font-size: 2em;
}

table td span {
    display: block;
    color: green;
    font-size: 0.75rem;
}

table td span.loss {
    color: red;
}
</style>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { realtimeByApp } from "../api"

let toggle = ref("7-day")
let overview = reactive({
    data: [] as any,
    error: "",
    loading: true,
})

function formatStatistics(row: any) {
    let earnings = row['metricValues']['ESTIMATED_EARNINGS']['microsValue'] / (1000 * 1000)
    let impressions = row['metricValues']['IMPRESSIONS']['integerValue']
    let eCPM = parseInt(row['metricValues']['ESTIMATED_EARNINGS']['microsValue']) / (1000.0 * parseInt(row['metricValues']['IMPRESSIONS']['integerValue']))
    eCPM = isNaN(eCPM) ? 0.0 : eCPM
    let requests = row['metricValues']['AD_REQUESTS']['integerValue']
    return {
        "name": row['dimensionValues']['APP']['displayLabel'],
        "platform": row['dimensionValues']['PLATFORM']['value'],
        "earnings": Math.round(earnings * 1000) / 1000,
        "impressions": impressions,
        "eCPM": Math.round(eCPM * 100) / 100,
        "requests": requests,
    }
}

async function updateOverview() {
    overview.loading = true
    overview.data = []
    overview.error = ""

    // Load current interval
    const current = realtimeByApp(toggle.value, false)

    // Load previous interval (if applicable)
    let previous = null;
    if (toggle.value != "1-day") {
        previous = await realtimeByApp(toggle.value, true)
    }

    // Update UI with current data
    let response = await current
    if (!response.ok) {
        overview.loading = false
        overview.error = "Unable to fetch your data. Please make sure you're signed " +
            "into the Google Account that is associated with your AdMob account."
        return
    }
    let result = await response.json()
    overview.loading = false
    overview.data = result.map((row: any) => formatStatistics(row))
    if (result.length == 0) {
        overview.error = "You don't have any results for today yet."
    }

    // If previous interval data is set...
    if (previous) {
        const app_platform_to_data = {} as any;
        (await previous.json()).map((row: any) => {
            row = formatStatistics(row)
            app_platform_to_data[row.app + row.platform] = row
        })

        overview.data.forEach((element: any) => {
            let key = element.app + element.platform
            if (key in app_platform_to_data) {
                element.previous = app_platform_to_data[key]
                element.delta = {
                    earnings: Math.round(1000.0 * (element.earnings - element.previous.earnings) / element.previous.earnings) / 10.0,
                    impressions: Math.round(1000.0 * (element.impressions - element.previous.impressions) / element.previous.impressions) / 10.0,
                    eCPM: Math.round(1000.0 * (element.eCPM - element.previous.eCPM) / element.previous.eCPM) / 10.0,
                    requests: Math.round(1000.0 * (element.requests - element.previous.requests) / element.previous.requests) / 10.0,
                }
            }
        });
    }
}

updateOverview()

</script>
