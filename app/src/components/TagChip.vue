<template>
    <ion-chip :color="tagToColor[tag]" @click.stop="explainTag(tag)" :outline="true">{{ tag
    }}</ion-chip>
</template>

<script setup lang="ts">
import { Tag } from '@/cards';
import { IonChip, alertController } from '@ionic/vue';

const props = defineProps(["tag"])

const tagToColor: Record<Tag, string> = {
    "Public": "success",
    "Numerical": "primary",
    "Interactive": "secondary",
    "Graphical": "warning",
    "Textual": "tertiary",
}

const tagToMessage: Record<Tag, string> = {
    "Public": "Public cards does not require access to your AdMob account and only display anonymized data.",
    "Numerical": "Numerical cards typically contain tables or grids showing various breakdowns of your data.",
    "Interactive": "Interactive cards typically contain elements such as selection menus to choose what is displayed.",
    "Graphical": "Graphical cards typically contain charts and are often used to display time series.",
    "Textual": "Textual cards are focused on displaying text-based content suck as summaries and instructions.",
}

const explainTag = async (tag: Tag) => {
    const alert = await alertController.create({
        header: tag + " Cards",
        message: tagToMessage[tag],
        buttons: ['OK'],
    });
    await alert.present();
}
</script>