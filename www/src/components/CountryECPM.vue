<template>
    <v-card>
        <v-card-text>
            <div style="height:480px;width:100%;">
                <l-map :use-global-leaflet="false" ref="map" :zoom="1.5" :center="[23.41322, -40.219482]">
                    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
                        name="OpenStreetMap"></l-tile-layer>
                    <l-geo-json :geojson="settings.geojson" :options-onEachFeature="onEachFeature"
                        :options="settings.options"></l-geo-json>
                </l-map>
            </div>
        </v-card-text>
    </v-card>
</template>

  
<style></style>

<script lang="ts" setup>
import { reactive } from 'vue'
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { ecpmByBreakdowns } from '../api'
import countryGeoJSON from "@/assets/countries.geo.json"
import countryCodeMap from "@/assets/countryCodeMap.json"

function getColor(ecpm: number) {
    if (ecpm > 10.0) {
        return '#094F29'
    }
    if (ecpm > 5.0) {
        return '#0A6921'
    }
    if (ecpm > 2.0) {
        return '#1A8828'
    }
    if (ecpm > 1.0) {
        return '#429B46'
    }
    if (ecpm > 0.5) {
        return '#64AD62'
    }
    return '#94C58C'
}

function onEachFeature(feature: any, layer: any) {
    const defaultStyle = {
        fillColor: getColor(feature.properties.ecpm),
        weight: 1,
        color: 'white',
        dashArray: '3',
    }
    const hoverStyle = {
        weight: 4,
    }

    layer.on({
        mouseover: (e: any) => {
            const layer = e.target;
            layer.setStyle(hoverStyle);
            layer.bringToFront();
            settings.country = e.target.feature.id
        },
        mouseout: (e: any) => {
            const layer = e.target;
            layer.setStyle(defaultStyle)
        },
    });
    layer.setStyle(defaultStyle)
    layer.bindTooltip(`
            <b>Country:</b> ${feature.id}<br/>
            <b>eCPM:</b> ${feature.properties.ecpm}
            `)
}

const settings = reactive({
    country: "",
    options: {
        onEachFeature: onEachFeature
    },
    geojson: null as any
})

ecpmByBreakdowns("country").then((res) => {
    res.json().then((res) => {
        const countryToECPM = {} as any
        res.forEach((x: any) => {
            countryToECPM[x.country] = x
        })

        const filtered_features = [] as any
        countryGeoJSON.features.forEach((feature: any) => {
            // @ts-expect-error
            feature.properties.alpha2 = countryCodeMap[feature.id]
            if (feature.properties.alpha2 in countryToECPM) {
                filtered_features.push(feature)
                feature.properties.ecpm = countryToECPM[feature.properties.alpha2].ecpm
            }
        })
        countryGeoJSON.features = filtered_features
        settings.geojson = countryGeoJSON
    })
})
</script>
