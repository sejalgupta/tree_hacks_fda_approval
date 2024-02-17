import Image from 'next/image'
import Link from 'next/link'
import ComparisonTable from './ComparisonTable'
import IntroForm from './IntroForm'
import React from 'react';

enum ScreenTypes {
    InputForm = 'inputForm',
    Results = 'results',
}

enum SubScreenTypes {
    Comparison = 'comparison',
    Workflow = 'workflow',
}

export default function PredicateComparison() {
    const [screenType, setScreenType] = React.useState(ScreenTypes.InputForm);
    const [subScreenType, setSubScreenType] = React.useState(SubScreenTypes.Comparison);
    const [comparisonData, setComparisonData] = React.useState<String[][]>([
        ["", "Header 1", "Header 2"],
        ["Row 1", "In the heart of the forest, a stream whispers its secrets to the wind, while sunlight filters through the leaves, painting patterns on the forest floor in dappled shades of green.", "The old oak tree stood tall, its branches reaching out like arms embracing the sky."],
        ["Row 2", "Lost in the labyrinth of city streets, strangers pass like ships in the night, each with a story untold, each with a destination yet to be discovered.", "Amidst the chaos of the bustling marketplace, a street performer captivates the crowd with his mesmerizing melodies, transporting them to a world of magic and wonder."],
        ["Row 3", "Beneath the starlit sky, waves crash against the rugged cliffs, their thunderous applause echoing through the silent night.", "The salty breeze carries whispers of tales from distant lands, mingling with the sounds of seagulls crying out over the restless sea."],
        ["Row 4", "Through the window, the first light of dawn paints the room in hues of gold and pink, awakening the world to a new day.", "In the cozy warmth of the kitchen, the aroma of freshly baked bread fills the air, evoking memories of simpler times."],
        ["Row 5", "Nestled in the embrace of rolling hills, a quaint village sleeps soundly under the stars, its secrets hidden within the whispers of the night.", "A solitary figure stands atop the mountain, gazing out over the vast expanse below, finding solace in the quiet majesty of nature."]
    ]);

    async function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
        setScreenType(ScreenTypes.Results);
        e.preventDefault();
        // TODO: Fetch data from /api/html-form and update comparisonData
        let formData = new FormData(e.target as HTMLFormElement);

        const response = await fetch(`api/handle-form`, {
            method: 'POST',
            body: formData,
        }
        );
        const data = await response.json();
        console.log(data);
    }

    return (
        <main className="container mx-auto my-20">
            {screenType === ScreenTypes.InputForm
                ? <IntroForm onSubmit={handleFormSubmit} />
                : <ComparisonTable data={comparisonData} />
            }
        </main>
    )
}
