import React from "react";

function Chatbox() {
    const questions = [];
  	return (
    	<section className="max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
			{/* Chat Bubble */}
            <ul className="space-y-5">
            {/* Chat */}
            <li className="max-w-lg flex gap-x-2 sm:gap-x-4">
                {/* Card */}
                <div className="bg-white border border-gray-200 rounded-2xl p-4 space-y-3 dark:bg-slate-900 dark:border-gray-700">
                <h2 className="font-medium text-gray-800 dark:text-white">
                    How can we help?
                </h2>
                <div className="space-y-1.5">
                    <p className="mb-1.5 text-sm text-gray-800 dark:text-white">
                    You can ask questions like:
                    </p>
                    <ul className="list-disc list-outside space-y-1.5 ps-3.5">
                    <li className="text-sm text-gray-800 dark:text-white">
                        What's Preline UI?
                    </li>

                    <li className="text-sm text-gray-800 dark:text-white">
                        How many Starter Pages & Examples are there?
                    </li>

                    <li className="text-sm text-gray-800 dark:text-white">
                        Is there a PRO version?
                    </li>
                    </ul>
                </div>
                </div>
                {/* End Card */}
            </li>
            {/* End Chat */}

            {/* Chat */}
            <li className="max-w-lg ms-auto flex justify-end gap-x-2 sm:gap-x-4">
                <div className="grow text-end space-y-3">
                {/* Card */}
                <div className="inline-block bg-blue-600 rounded-2xl p-4 shadow-sm">
                    <p className="text-sm text-white">
                    what's preline ui?
                    </p>
                </div>
                {/* End Card */}
                </div>
            </li>
            {/* End Chat */}

            {/* Chat Bubble */}
            <li className="max-w-lg flex gap-x-2 sm:gap-x-4">
                {/* Card */}
                <div className="bg-white border border-gray-200 rounded-2xl p-4 space-y-3 dark:bg-slate-900 dark:border-gray-700">
                <p className="text-sm text-gray-800 dark:text-white">
                    Preline UI is an open-source set of prebuilt UI components based on the utility-first Tailwind CSS framework.
                </p>
                <div className="space-y-1.5">
                    <p className="text-sm text-gray-800 dark:text-white">
                    Here're some links to get started
                    </p>
                    <ul>
                    <li>
                        <a className="text-sm text-blue-600 decoration-2 hover:underline font-medium dark:text-blue-500 dark:hover:text-blue-400 dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600" href="../docs/index.html">
                        Installation Guide
                        </a>
                    </li>
                    <li>
                        <a className="text-sm text-blue-600 decoration-2 hover:underline font-medium dark:text-blue-500 dark:hover:text-blue-400 dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600" href="../docs/frameworks.html">
                        Framework Guides
                        </a>
                    </li>
                    </ul>
                </div>
                </div>
                {/* End Card */}
            </li>
            {/* End Chat Bubble */}
            </ul>
            {/* End Chat Bubble */}
  		</section>
  	);
}

export default Chatbox;