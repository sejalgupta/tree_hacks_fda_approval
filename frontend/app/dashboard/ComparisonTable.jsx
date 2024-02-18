import React from "react";

function ComparisonTable({ data, options, currentId, onChange }) {
	console.log({data, options, currentId, onChange});
  return (
    <section className="max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
      <div className="h-full max-w-full">
          <header className="px-5 py-4 border-b border-gray-100">
				<h2 className="font-semibold text-gray-800">Predicate Comparison</h2>
				<div className="flex items-center justify-between mt-2">
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
                  <table className="table-auto w-full">
                      <thead className="text-xs font-semibold uppercase text-gray-400 bg-gray-50">
                          <tr>
                              { data && data[0].map((item, index) => {
                                return (
                                  <th className="p-2 min-w-20" key={"header-" + index}>
                                      <div className="font-semibold text-left">{ item }</div>
                                  </th>
                                );
                              }) }
                          </tr>
                      </thead>
                      <tbody className="text-sm divide-y divide-gray-100">
                          { data && data.slice(1).map((row, i) => {
                            return (
                              <tr key={"row-" + i}>
                                { row.map((item, j) => {
                                  return (
                                    <td className="p-2" key={"cell-" + i + "-" + j}>
                                        <div className="text-left">{ item }</div>
                                    </td>
                                  );
                                }) }
                              </tr>
                            );
                          }) }
                      </tbody>
                  </table>
              </div>
          </div>
      </div>
  </section>
  );
}

export default ComparisonTable;