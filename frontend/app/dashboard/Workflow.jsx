import React from "react";
import Chatbox from "./Chatbox";

function SingleBox({ title, description, guidance }) {
	return (
		<div className="flex flex-col bg-white border shadow-sm rounded-xl p-4 md:p-5 dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
			<h3 className="text-lg font-bold text-gray-800 dark:text-white">
				{ title }
			</h3>
			{/* <p className="mt-1 text-xs font-medium uppercase text-gray-500 dark:text-gray-500">
				Card subtitle
			</p> */}
			<p className="mt-2 text-gray-500 dark:text-gray-400">
				{ description }
			</p>
		</div>
	);

}

function Workflow() {
  	return (
    	<section className="max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
			<div className="grid grid-cols-4 gap-4">
				<SingleBox title="Step 1" description="This is the first step in the process." />
				<SingleBox title="Step 2" description="This is the second step in the process." />
				<SingleBox title="Step 3" description="This is the third step in the process." />
				<SingleBox title="Step 4" description="This is the fourth step in the process." />
			</div>
			<div id="chatbox">
				<Chatbox />
			</div>
  		</section>
  	);
}

export default Workflow;