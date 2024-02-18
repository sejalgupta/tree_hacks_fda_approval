'use client'

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
    const [description, setDescription] = React.useState<string>("The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app.");
    const [indication, setIndication] = React.useState<string>("The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old.");
    const [screenType, setScreenType] = React.useState(ScreenTypes.InputForm);
    const [subScreenType, setSubScreenType] = React.useState(SubScreenTypes.Comparison);
    const [comparisonData, setComparisonData] = React.useState<Record<string, String[][]>>({});
    const [comparisonOptions, setComparisonOptions] = React.useState<{"K": string, "Device Description": string, "Indications for use": string}[]>([]);
    const [comparisonId, setComparisonId] = React.useState<string>("");

    async function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
        setScreenType(ScreenTypes.Results);
        e.preventDefault();
        // TODO: Fetch data from /api/html-form and update comparisonData
        let formData = new FormData(e.target as HTMLFormElement);
        // formData.append('k-number-information', '');
        console.log(formData.entries());
        console.log({e});
        console.log(e.target);

        const response = await fetch(`api/handle-form`, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log({data});
        const k_number: string = data["k_number_information"][0]["K"];
        const info: Record<string, {"K": string, "Device Description": string, "Indications for use": string}> = {};
        for (const k of data["k_number_information"]) {
            info[k["K"]] = k;
        }
        const table: Record<string, string[][]> = {};
        table[k_number] = data["comparison_table"][0];
        
        setComparisonData(table);
        setComparisonOptions(data["k_number_information"]);
        setComparisonId(k_number);
        console.log({data});
        console.log({table});
        console.log({k_number});
    }

    async function handleChangeComparison(k_number: string) {
        if (!(k_number in comparisonData)) {
            // const form: HTMLFormElement = document.getElementById('comparison-form') as HTMLFormElement;
            let formData = new FormData();
            formData.append('device-description', description);
            formData.append('use-indication', indication);
            comparisonOptions.forEach((option) => {
                if (option["K"] === k_number) {
                    // formData.append('k-number-information', String(option));
                    console.log(option)
                    console.log(option["Device Description"])
                    formData.append('k-number', option["K"]);
                    formData.append('k-number-description', option["Device Description"]);
                    formData.append('k-number-use', option["Indications for use"]);
                }
            });
            // formData.append('k-number-information', String(comparisonOptions[k_number]));
            console.log(formData.entries());

            const response = await fetch(`api/handle-form`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            console.log(data);
            const comparison_table = comparisonData;
            comparison_table[k_number] = data["comparison_table"][0];
            setComparisonData(comparison_table);
        }
        setComparisonId(k_number);
    }

    return (
        <main className="container mx-auto my-20">
            {screenType === ScreenTypes.InputForm
                ? <IntroForm
                    onSubmit={handleFormSubmit}
                    description={description}
                    setDescription={setDescription}
                    indication={indication}
                    setIndication={setIndication}
                />
                : <ComparisonTable
                    key={comparisonId}
                    data={comparisonData[comparisonId]}
                    options={comparisonOptions}
                    currentId={comparisonId}
                    onChange={handleChangeComparison}
                />
            }
        </main>
    )
}
