import EarningsCard from "./EarningsCard.vue";
import ReportCard from "./ReportCard.vue";
import ECPMSummaryCard from "./ECPMSummaryCard.vue";
import PlatformECPMCard from "./PlatformECPMCard.vue";
import ECPMMapCard from "./ECPMMapCard.vue"
import EarningsByApp from "./EarningsByApp.vue"


enum Tag {
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
        'key': 'EarningsCard',
        'name': '7-Day Earnings Card',
        'description': 'This displays a bar chart containing the earnings over the past 7 days (not including today).',
        'component': EarningsCard,
        'tags': [Tag.Graphical]
    },
    {
        'key': 'ReportCard',
        'name': 'Report Card',
        'description': 'This displays the earnings, impressions, requests, and eCPM for the most recent 1, 7, or 28 days.',
        'component': ReportCard,
        'tags': [Tag.Interactive, Tag.Numerical]
    },
    {
        'key': 'ECPMSummaryCard',
        'name': 'ECPM Summary Card',
        'description': 'This displays a text-based summary of the eCPM of the entire network over the past week compared to the previous week.',
        'component': ECPMSummaryCard,
        'tags': [Tag.Public, Tag.Textual]
    },
    {
        'key': 'PlatformECPMCard',
        'name': 'Platform ECPM Card',
        'description': 'This displays a breakdown of the current network eCPM across different platforms and for different ad formats.',
        'component': PlatformECPMCard,
        'tags': [Tag.Public, Tag.Textual],
    },
    {
        'key': 'ECPMMapCard',
        'name': 'ECPM Map Card',
        'description': 'This displays a map showing the current eCPM in different countries around the world.',
        'component': ECPMMapCard,
        'tags': [Tag.Public, Tag.Graphical],
    },
    {
        'key': '1DayEarningsByApp',
        'name': 'Today\'s Earnings By App',
        'description': 'This displays your earnings so far for today broken down by app.',
        'component': EarningsByApp,
        'tags': [Tag.Numerical],
        'options': {'interval': 'today'}
    },
    {
        'key': '7DayEarningsByApp',
        'name': '7-Day Earnings By App',
        'description': 'This displays your total earnings over the past week broken down by app.',
        'component': EarningsByApp,
        'tags': [Tag.Numerical],
        'options': {'interval': 'week'}
    },
]

const cardDefinitions: Record<string, any> = {}
cardDefinitionsRaw.forEach((cardDefinition: any) => {
    cardDefinitions[cardDefinition.key] = cardDefinition;
})

export { cardDefinitions, EarningsCard, ReportCard };