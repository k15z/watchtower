import ReportCard from "./ReportCard.vue";
import ReportByApp from "./ReportByApp.vue"
import ReportByAppVersion from "./ReportByAppVersion.vue"

import ECPMSummaryCard from "./ECPMSummaryCard.vue";
import ECPMByPlatform from "./ECPMByPlatform.vue";
import ECPMMapCard from "./ECPMMapCard.vue"
import ECPMByGenre from "./ECPMByGenre.vue"

import TimeSeriesPlot from "./TimeSeriesPlot.vue";
import EarningsByDayOfWeek from "./EarningsByDayOfWeek.vue"
import TreeMapPlot from "./TreeMapPlot.vue";
import HeatMapPlot from "./HeatMapPlot.vue";
import RadarChartDayOfWeek from "./RadarChartDayOfWeek.vue";

export enum Tag {
    Public = "Public",
    Interactive = "Interactive",
    Textual = "Textual",
    Numerical = "Numerical",
    Graphical = "Graphical",
}

interface CardDefinition {
    // Used to load the component
    key: string;
    component: any;
    options?: any;

    // Used to explain the card in the Explore UI
    name: string;
    description: string;
    tags?: Tag[];
}

const cardDefinitionsRaw: CardDefinition[] = [
    {
        'key': 'ReportCard',
        'name': 'Report Card',
        'description': 'This displays the earnings, impressions, requests, and eCPM for the most recent 1, 7, or 28 days.',
        'component': ReportCard,
        'tags': [Tag.Interactive, Tag.Numerical]
    },
    {
        'key': 'ReportByApp',
        'name': 'Report By App',
        'description': 'This displays your earnings and impressions broken down by apps for the most recent 1, 7, or 28 days.',
        'component': ReportByApp,
        'tags': [Tag.Interactive, Tag.Numerical],
    },
    {
        'key': 'ReportByAppVersion',
        'name': 'Report By App Version',
        'description': 'This displays your earnings and impressions for a specific app broken down by app version for the most recent 1, 7, or 28 days.',
        'component': ReportByAppVersion,
        'tags': [Tag.Interactive, Tag.Numerical],
    },
    {
        'key': 'TimeSeriesPlot',
        'name': '7-Day Time Series',
        'description': 'This displays a bar chart containing the earnings, impressions, and requests for the past 7 days.',
        'component': TimeSeriesPlot,
        'tags': [Tag.Interactive, Tag.Graphical]
    },
    {
        'key': 'EarningsByDayOfWeek',
        'name': 'Box Plot: Earnings By Weekday',
        'description': 'This displays a boxplot showing average earnings on each day of the week to let you explore weekly seasonal patterns.',
        'component': EarningsByDayOfWeek,
        'tags': [Tag.Graphical]
    },
    {
        'key': 'RadarChartDayOfWeek',
        'name': 'Radar Chart: Earnings By App and Weekday',
        'description': 'This displays a radar chart showing average earnings on each day of the week for each app.',
        'component': RadarChartDayOfWeek,
        'tags': [Tag.Graphical]
    },
    {
        'key': 'ECPMByPlatform',
        'name': 'ECPM By Platform',
        'description': 'This displays a breakdown of the current network eCPM across different platforms and for different ad formats.',
        'component': ECPMByPlatform,
        'tags': [Tag.Public, Tag.Numerical],
    },
    {
        'key': 'ECPMByGenre',
        'name': 'ECPM By Genre',
        'description': 'This displays a bar plot showing the eCPM for each genre to let you explore which genres are most valuable.',
        'component': ECPMByGenre,
        'tags': [Tag.Public, Tag.Graphical],
    },
    {
        'key': 'ECPMSummaryCard',
        'name': 'ECPM Summary Card',
        'description': 'This displays a text-based summary of the eCPM of the entire network over the past week compared to the previous week.',
        'component': ECPMSummaryCard,
        'tags': [Tag.Public, Tag.Textual]
    },
    {
        'key': 'ECPMMapCard',
        'name': 'ECPM Map Card',
        'description': 'This displays a map showing the current eCPM in different countries around the world.',
        'component': ECPMMapCard,
        'tags': [Tag.Public, Tag.Graphical],
    },
    {
        'key': 'TreeMapECPM',
        'name': 'Tree Map: Top Countries by eCPM',
        'description': 'This displays a tree map showing the top performing countries by eCPM.',
        'component': TreeMapPlot,
        'options': {'target': 'ecpm'},
        'tags': [Tag.Numerical, Tag.Graphical],
    },
    {
        'key': 'TreeMapEarnings',
        'name': 'Tree Map: Top Countries by Earnings',
        'description': 'This displays a tree map showing the top performing countries by eCPM.',
        'component': TreeMapPlot,
        'options': {'target': 'earnings'},
        'tags': [Tag.Numerical, Tag.Graphical],
    },
    {
        'key': 'HeatMapECPM',
        'name': 'Heat Map: Historical eCPM',
        'description': 'This displays a heat map showing the historical network eCPM.',
        'component': HeatMapPlot,
        'options': {'target': 'ecpm'},
        'tags': [Tag.Public, Tag.Graphical],
    },
    {
        'key': 'HeatMapEarnings',
        'name': 'Heat Map: Historical Earnings',
        'description': 'This displays a heat map showing your historical earnings.',
        'component': HeatMapPlot,
        'options': {'target': 'earnings'},
        'tags': [Tag.Graphical],
    },
    {
        'key': 'HeatMapImpressions',
        'name': 'Heat Map: Historical Impressions',
        'description': 'This displays a heat map showing your historical impressions.',
        'component': HeatMapPlot,
        'options': {'target': 'impressions'},
        'tags': [Tag.Graphical],
    },
]

const cardDefinitions: Record<string, any> = {}
cardDefinitionsRaw.forEach((cardDefinition: any) => {
    if (cardDefinition.key in cardDefinitions) {
        throw new Error(`Duplicate card definition for ${cardDefinition.key}`);
    }
    cardDefinitions[cardDefinition.key] = cardDefinition;
})

export { cardDefinitions };