import React from "react";
import Table from "./Table";

function ComparisonTable({ data, options, currentId, onChange }) {
	console.log({data, options, currentId, onChange});
  return (
    <section className="container mx-auto antialiased bg-gray-100 text-gray-600 p-4">
      <div className="h-full max-w-full">
          <header className="px-5 py-4 border-b border-gray-100 text-center">
				<h1 className="text-2xl font-semibold text-gray-800">Predicate Comparison</h1>
				<div className="flex items-center justify-center mt-2">
					<ul class="flex flex-col sm:flex-row">
					{ options && options.map((option, index) => {
						console.log({currentId, option});
						return (
							<li className="inline-flex items-center gap-x-2.5 py-3 px-4 text-sm font-medium bg-white border text-gray-800 -mt-px first:rounded-t-lg first:mt-0 last:rounded-b-lg sm:-ms-px sm:mt-0 sm:first:rounded-se-none sm:first:rounded-es-lg sm:last:rounded-es-none sm:last:rounded-se-lg dark:bg-gray-800 dark:border-gray-700 dark:text-white">
								<div className="relative flex items-start w-full">
									<div className="flex items-center h-5">
										<input id={"hs-horizontal-list-group-item-radio-" + index} name="hs-horizontal-list-group-item-radio" type="radio" className="border-gray-200 rounded-full disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800" checked={currentId === option["K"]} onClick={() => onChange(option["K"])} />
									</div>
									<label for={"hs-horizontal-list-group-item-radio-" + index} className="ms-3 block w-full text-sm text-gray-600 dark:text-gray-500">
										{ option["K"] }
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
                  <Table data={data} />
              </div>
          </div>
      </div>
  </section>
  );
}

export default ComparisonTable;