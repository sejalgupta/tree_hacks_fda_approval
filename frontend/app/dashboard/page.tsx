'use client'

import ComparisonTable from './ComparisonTable'
import IntroForm from './IntroForm'
import Workflow from './Workflow'
import ClinicalTrials from './ClinicalTrials'
import TrialVisualization from './TrialVisualization'
import Table from './Table'
import React from 'react';

enum ScreenTypes {
    InputForm = 'inputForm',
    Results = 'results',
}

enum SubScreenTypes {
    Comparison = 'comparison',
    Workflow = 'workflow',
    PredicateVisualization = 'predicateVisualization',
    ClinicalTrials = 'clinicalTrials',
    MyTrials = 'myTrials',
}

// const BACKEND_BASE: string = "https://fda-approval-service.onrender.com/";
// const BACKEND_BASE: string = "http://localhost:3000/";
const BACKEND_BASE:string = "https://5ba3-68-65-175-99.ngrok-free.app";

export default function PredicateComparison() {
    const [description, setDescription] = React.useState<string>("The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app.");
    const [indication, setIndication] = React.useState<string>("The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old.");
    const [screenType, setScreenType] = React.useState(ScreenTypes.InputForm);
    const [subScreenType, setSubScreenType] = React.useState(SubScreenTypes.Comparison);
    const [comparisonData, setComparisonData] = React.useState<Record<string, String[][]>>({});
    const [comparisonOptions, setComparisonOptions] = React.useState<{"K": string, "Device Description": string, "Indications for use": string}[]>([]);
    const [comparisonId, setComparisonId] = React.useState<string>("");
    const [clinicalTrials, setClinicalTrials] = React.useState<String[][][]>();
    const [myTrial, setMyTrial] = React.useState<String[][]>();

    async function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
        setScreenType(ScreenTypes.Results);
        e.preventDefault();
        // TODO: Fetch data from /api/html-form and update comparisonData
        let formData = new FormData(e.target as HTMLFormElement);
        // formData.append('k-number-information', '');
        console.log(formData.entries());
        console.log({e});
        console.log(e.target);

        const response = await fetch(`${BACKEND_BASE}api/handle-form`, {
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

    async function handleClinicalTrials() {
        setSubScreenType(SubScreenTypes.ClinicalTrials);
        let formData = new FormData();
        formData.append('device-description', description);
        const response = await fetch(`${BACKEND_BASE}api/similar-trials`, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log({data});
        const trails = data["all-trials"];
        console.log({trails});
        setClinicalTrials(trails);
        console.log({clinicalTrials});
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

            const response = await fetch(`${BACKEND_BASE}api/handle-form`, {
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

    async function generateTrial() {
        let formData = new FormData();
        formData.append('device-description', description);
        formData.append('use-indication', indication);
        formData.append('all-trials', JSON.stringify(clinicalTrials));
        const response = await fetch(`${BACKEND_BASE}api/generate-trial`, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        const trial = data["trial-info"];
        console.log({data});
        console.log({trial});
        setMyTrial(trial);
        setSubScreenType(SubScreenTypes.MyTrials);
        console.log({myTrial});
    }

    function getResultScreen() {
        switch (subScreenType) {
            case SubScreenTypes.Comparison:
                return <>
                    <ComparisonTable
                        key={comparisonId}
                        data={comparisonData[comparisonId]}
                        options={comparisonOptions}
                        currentId={comparisonId}
                        onChange={handleChangeComparison}
                    />
                    <div className='container mx-auto flex flex-justify'>
                        <button
                            type="button"
                            onClick={() => setSubScreenType(SubScreenTypes.PredicateVisualization)}
                            className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-blue-600 text-blue-600 hover:border-blue-500 hover:text-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                        >
                            {"Visualize"}
                        </button>
                        <button
                            type="button"
                            onClick={() => setSubScreenType(SubScreenTypes.Workflow)}
                            className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-blue-600 text-blue-600 hover:border-blue-500 hover:text-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                        >
                            {"Next>"}
                        </button>
                    </div>
                </>;
            case SubScreenTypes.Workflow:
                return <>
                    <Workflow />
                    <div className='container mx-auto flex flex-justify'>
                        <button
                            type="button"
                            onClick={handleClinicalTrials}
                            className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-blue-600 text-blue-600 hover:border-blue-500 hover:text-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                        >
                            {"Find Clinical Trials"}
                        </button>
                    </div>
                    {/* <button onClick={handleClinicalTrials}>Find Clinical Trials</button> */}
                </>;
            case SubScreenTypes.ClinicalTrials:
                return <>
                    <ClinicalTrials trials={clinicalTrials} key={clinicalTrials?.length} />
                    <div className='container mx-auto text-center'>
                        <button
                            type="button"
                            onClick={generateTrial}
                            className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-blue-600 text-blue-600 hover:border-blue-500 hover:text-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                        >
                            {"Find Clinical Trials"}
                        </button>
                    </div>
                </>;
            case SubScreenTypes.MyTrials:
                return myTrial && <Table data={myTrial} />;
            case SubScreenTypes.PredicateVisualization:
                return <TrialVisualization deviceDescription={description} useIndication={indication} />;
        }
    }

    return (
        <main className="my-20">
            {
                screenType === ScreenTypes.InputForm
                ? <IntroForm
                    onSubmit={handleFormSubmit}
                    description={description}
                    setDescription={setDescription}
                    indication={indication}
                    setIndication={setIndication}
                />
                : getResultScreen()
            }
        </main>
    )
}
