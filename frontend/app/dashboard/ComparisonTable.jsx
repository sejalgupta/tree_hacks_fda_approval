import React from "react";

function ComparisonTable({ data }) {
  return (
    <section className="max-w-full antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
      <div className="h-full max-w-full">
          <header className="px-5 py-4 border-b border-gray-100">
              <h2 className="font-semibold text-gray-800">Predicate Comparison</h2>
          </header>
          <div className="p-3">
              <div className="overflow-x-auto">
                  <table className="table-auto w-full">
                      <thead className="text-xs font-semibold uppercase text-gray-400 bg-gray-50">
                          <tr>
                              { data[0].map((item, index) => {
                                return (
                                  <th className="p-2 min-w-20" key={"header-" + index}>
                                      <div className="font-semibold text-left">{ item }</div>
                                  </th>
                                );
                              }) }
                          </tr>
                      </thead>
                      <tbody className="text-sm divide-y divide-gray-100">
                          { data.slice(1).map((row, i) => {
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
                          {/* <tr>
                              <td className="p-2 whitespace-nowrap">
                                  <div className="flex items-center">
                                      <div className="w-10 h-10 flex-shrink-0 mr-2 sm:mr-3"></div>
                                      <div className="font-medium text-gray-800">Alex Shatov</div>
                                  </div>
                              </td>
                              <td className="p-2 whitespace-nowrap">
                                  <div className="text-left">alexshatov@gmail.com</div>
                              </td>
                              <td className="p-2 whitespace-nowrap">
                                  <div className="text-left font-medium text-green-500">$2,890.66</div>
                              </td>
                              <td className="p-2 whitespace-nowrap">
                                  <div className="text-lg text-center">🇺🇸</div>
                              </td>
                          </tr> */}
                      </tbody>
                  </table>
              </div>
          </div>
      </div>
  </section>
  );
}

export default ComparisonTable;