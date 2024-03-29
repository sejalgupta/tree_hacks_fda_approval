import React from "react";
import Chatbox from "./Chatbox";
import WorkflowData from "../../components/workflowData";

function SingleBox({ title, description, guidance_text, guidance_link, display }) {
	const truncuate_style = {
		"overflow": "hidden",
		"text-overflow": "ellipsis",
		"display": "-webkit-box",
		"-webkit-line-clamp": "4", /* number of lines to show */
				"line-clamp": "4",
		"-webkit-box-orient": "vertical",
	}
	
	return (
		<div className={"hs-tooltip [--trigger:click] sm:[--placement:right] rounded-xl" + (display ? " border-t-4 border-t-blue-600" : " opacity-30")}>
		  <div className="hs-tooltip-toggle max-w-xs p-4 flex items-center gap-x-3 bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
		
			{/* User Content */}
			<div className={"bg-white rounded-xl dark:bg-slate-900"} style={{minHeight: "120px"}}>
				<h2 className="text-lg font-semibold text-gray-800 dark:text-white" style={{fontSize: "1.2em", wordBreak: "break-word"}}>
					{ title }
				</h2>
				{/* <p className="mt-1 text-xs font-medium uppercase text-gray-500 dark:text-gray-500">
					Card subtitle
				</p> */}
				{/* <p className="mt-2 text-gray-500 dark:text-gray-400" style={truncuate_style}>
					{ description }
				</p> */}
			</div>
			{/* End User Content */}
		
			{/* Popover Content */}
			<div className="hs-tooltip-content hs-tooltip-shown:opacity-100 hs-tooltip-shown:visible hidden opacity-0 transition-opacity absolute invisible z-10 max-w-xs w-full bg-white border border-gray-100 text-start rounded-xl shadow-md after:absolute after:top-0 after:-start-4 after:w-4 after:h-full dark:bg-gray-800 dark:border-gray-700" role="tooltip">
			  {/* Header */}
			  <div className="py-3 px-4 border-b border-gray-200 dark:border-gray-700">
				<div className="flex items-center gap-x-3">
				  <div className="grow">
					<h3 className="text-lg font-semibold text-gray-800 dark:text-white">
					  { title }
					</h3>
				  </div>
				</div>
			  </div>
			  {/* End Header */}
		
			  {/* List */}
			  <p className="p-4">
				{ description }
			  </p>
			  {/* End List */}
		
			  {/* Footer */}
			  <p>{guidance_text}</p>
			  { guidance_text && 
			  	
					<div className="py-2 px-4 flex justify-between items-center bg-gray-100 dark:bg-gray-800">
						Helpful links: <a href={guidance_link} className="text-blue-600 dark:text-blue-400 hover:underline" target="_blank">{guidance_text}</a>
					</div>
				}
			  {/* End Footer */}
			</div>
			{/* End Popover Content */}
		  </div>
		</div>
	);

}

function Workflow() {
	const defaultAnswer = [];
	WorkflowData.conditions.forEach((condition, index) => {
		defaultAnswer.push(true);
	});
	const [questionAnswers, setQuestionAnswers] = React.useState(defaultAnswer);

	function updateAnswers(index, value) {
		console.log("Updating answers " + index + " to " + value);
		let newAnswers = [...questionAnswers];
		newAnswers[index] = value;
		setQuestionAnswers(newAnswers);
	}

  	return (
    	<section className="mx-3 max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
			<h1 className="text-2xl font-semibold text-gray-800 text-center mb-6">Your 510(k) application workflow</h1>
			<div className="grid grid-cols-3">
				<div className="grid grid-cols-3 gap-5 col-span-2">
					{ Object.entries(WorkflowData.steps).map(([step, info], index) => {
						const display = info.condition == null ? true : questionAnswers[info.condition];
						return (
							<SingleBox 
								key={"single-box-" + index + "-" + display ? "true" : "false"}
								title={step}
								description={info.description}
								guidance_text={info.guidance != null ? info.guidance.name : ""}
								guidance_link={info.guidance != null ? info.guidance.link : ""} 
								display={info.condition == null ? true : questionAnswers[info.condition]}
							/>
						);
					})}
				</div>
				<div id="chatbox" className="rounded-lg border-gray-300">
					<Chatbox questions={WorkflowData.conditions} answers={questionAnswers} updateAnswers={updateAnswers} />
				</div>
			</div>
  		</section>
  	);
}

export default Workflow;