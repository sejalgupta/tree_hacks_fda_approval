import React from "react";

function Table({ data }) {

  	return (
    	<table className="table-auto w-full bg-white shadow-md rounded-lg">
            <thead className="text-xs font-semibold uppercase bg-gray-50">
                <tr>
                    { data && data[0].map((item, index) => {
                    return (
                        <th className="p-2 min-w-20" key={"header-" + index}>
                            <div className="font-semibold text-center">{ item }</div>
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
  	);
}

export default Table;