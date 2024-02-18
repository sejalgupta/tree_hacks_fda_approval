import React from "react";
import Chatbox from "./Chatbox";
import WorkflowData from "../../components/workflowData";

function ClinicalTrials({ trials }) {
    const [currentIdx, setCurrentIdx] = React.useState(0);

  	return (
    	<section className="container mx-auto antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
            <div className="h-full max-w-full">
                <header className="px-5 py-4 border-b border-gray-100">
                        <h2 className="font-semibold text-gray-800">Similar Clinical Trials</h2>
                        <div className="flex items-center justify-between mt-2">
                            <ul class="flex flex-col sm:flex-row">
                            { trials && trials.map((option, index) => {
                                console.log({currentIdx, option});
                                return (
                                    <li className="inline-flex items-center gap-x-2.5 py-3 px-4 text-sm font-medium bg-white border text-gray-800 -mt-px first:rounded-t-lg first:mt-0 last:rounded-b-lg sm:-ms-px sm:mt-0 sm:first:rounded-se-none sm:first:rounded-es-lg sm:last:rounded-es-none sm:last:rounded-se-lg dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                                        <div className="relative flex items-start w-full">
                                            <div className="flex items-center h-5">
                                                <input id={"clinical-trials-" + index} name="hs-horizontal-list-group-item-radio" type="radio" className="border-gray-200 rounded-full disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800" checked={currentIdx === index} onClick={() => setCurrentIdx(index)} />
                                            </div>
                                            <label for={"clinical-trials-" + index} className="ms-3 block w-full text-sm text-gray-600 dark:text-gray-500">
                                                Clinical Trail { index }
                                            </label>
                                        </div>
                                    </li>
                                );
                            }) }
                        </ul>
                        </div>
                </header>
                <div className="p-3">
                    <div className="overflow-x-auto">
                        <Table data={trials[currentIdx]} />
                    </div>
                </div>
            </div>
        </section>
  	);
}

export default ClinicalTrials;