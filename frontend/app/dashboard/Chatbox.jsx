import React from "react";

function Chatbox({ questions, answers, updateAnswers }) {
    const [currentQuestion, setCurrentQuestion] = React.useState(0);

    function updateCurrentQuestion(idx) {
        setCurrentQuestion(idx > currentQuestion + 1 ? idx : currentQuestion + 1);
    }

  	return (
    	<section className="max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
			{/* Chat Bubble */}
            <ul className="space-y-5">
            {/* Chat */}
            { questions.map((question, index) => {
                return (
                    <>
                    <li key={"chat-" + index} className="max-w-lg flex gap-x-2 sm:gap-x-4">
                        {/* Card */}
                        <div className="bg-white border border-gray-200 rounded-2xl p-4 space-y-3 dark:bg-slate-900 dark:border-gray-700">
                            <p className="mb-1.5 text-sm text-gray-800 dark:text-white">
                                { question }
                            </p>
                        </div>
                        {/* End Card */}
                    </li>
                    <li className="max-w-lg ms-auto flex justify-end gap-x-2 sm:gap-x-4">
                        <div className="grow text-end space-y-3">
                        {/* Card */}
                        <div className="inline-block">
                        <ul class="flex flex-col sm:flex-row">
                            <li className="inline-flex items-center gap-x-2.5 py-3 px-4 text-sm font-medium bg-white border text-gray-800 -mt-px first:rounded-t-lg first:mt-0 last:rounded-b-lg sm:-ms-px sm:mt-0 sm:first:rounded-se-none sm:first:rounded-es-lg sm:last:rounded-es-none sm:last:rounded-se-lg dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                                <div className="relative flex items-start w-full">
                                    <div className="flex items-center h-5">
                                        <input id={"yes-chat-question-" + index} name={"chat-q-" + index} type="radio" className="border-gray-200 rounded-full disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800" checked={answers[index]} onClick={() => updateAnswers(index, true)} />
                                    </div>
                                    <label for={"yes-chat-question-" + index} className="ms-3 block w-full text-sm text-gray-600 dark:text-gray-500">
                                        Yes
                                    </label>
                                </div>
                            </li>
                            <li className="inline-flex items-center gap-x-2.5 py-3 px-4 text-sm font-medium bg-white border text-gray-800 -mt-px first:rounded-t-lg first:mt-0 last:rounded-b-lg sm:-ms-px sm:mt-0 sm:first:rounded-se-none sm:first:rounded-es-lg sm:last:rounded-es-none sm:last:rounded-se-lg dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                                <div className="relative flex items-start w-full">
                                    <div className="flex items-center h-5">
                                        <input id={"no-chat-question-" + index} name={"chat-q-" + index} type="radio" className="border-gray-200 rounded-full disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800" checked={!answers[index]} onClick={() => updateAnswers(index, false)} />
                                    </div>
                                    <label for={"no-chat-question-" + index} className="ms-3 block w-full text-sm text-gray-600 dark:text-gray-500">
                                        No
                                    </label>
                                </div>
                            </li>
                        </ul>
                        </div>
                        {/* End Card */}
                        </div>
                    </li>
                </>
                );
            })}
            {/* End Chat Bubble */}
            </ul>
            {/* End Chat Bubble */}
  		</section>
  	);
}

export default Chatbox;