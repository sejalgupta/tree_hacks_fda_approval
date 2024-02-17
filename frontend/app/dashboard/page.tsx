'use client'

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
    const [comparisonData, setComparisonData] = React.useState<String[][][]>([[[]]]);
    const [comparisonOptions, setComparisonOptions] = React.useState<String[]>([]);
    const [comparisonIdx, setComparisonIdx] = React.useState<number>(0);

    async function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
        setScreenType(ScreenTypes.Results);
        e.preventDefault();
        // TODO: Fetch data from /api/html-form and update comparisonData
        let formData = new FormData(e.target as HTMLFormElement);
        console.log(formData.entries());
        console.log({e});
        console.log(e.target);

        const response = await fetch(`api/handle-form`, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log(data);
        setComparisonData(data["comparison_table"]);
        setComparisonOptions(data["k_numbers"]);
        setComparisonIdx(0);
    }

    return (
        <main className="container mx-auto my-20">
            {screenType === ScreenTypes.InputForm
                ? <IntroForm onSubmit={handleFormSubmit} />
                : <ComparisonTable data={comparisonData[comparisonIdx]} options={comparisonOptions} currentIdx={comparisonIdx} onChange={setComparisonIdx} />
            }
        </main>
    )
}
