import EarningsCard from "./EarningsCard.vue";
import ReportCard from "./ReportCard.vue";
import ECPMSummaryCard from "./ECPMSummaryCard.vue";
import PlatformECPMCard from "./PlatformECPMCard.vue";
import ECPMMapCard from "./ECPMMapCard.vue"

const cardDefinitionsRaw = [
    {
        'key': 'EarningsCard',
        'name': 'Earnings Card',
        'description': 'A card that displays the last 7 days of earnings as a bar chart.',
        'component': EarningsCard,
    },
    {
        'key': 'ReportCard',
        'name': 'Report Card',
        'description': 'A card that displays the current report for a user-defined interval.',
        'component': ReportCard,
    },
    {
        'key': 'ECPMSummaryCard',
        'name': 'ECPM Summary Card',
        'description': 'A human-readible description of the network eCPM for the past week.',
        'component': ECPMSummaryCard,
    },
    {
        'key': 'PlatformECPMCard',
        'name': 'Platform ECPM Card',
        'description': 'Comparison of eCPM on different platforms.',
        'component': PlatformECPMCard,
    },
    {
        'key': 'ECPMMapCard',
        'name': 'ECPM Map Card',
        'description': 'Comparison of eCPM in different geographic regions.',
        'component': ECPMMapCard,
    }
]

const cardDefinitions: Record<string, any> = {}
cardDefinitionsRaw.forEach((cardDefinition: any) => {
    cardDefinitions[cardDefinition.key] = cardDefinition;
})

export { cardDefinitions, EarningsCard, ReportCard };