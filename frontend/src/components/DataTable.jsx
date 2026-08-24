function DataTable({ columns, rows }) {
  return (
    <div className="overflow-x-auto overflow-hidden rounded-lg border border-slate-200 bg-white">
      <table className="w-full text-xs">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200">
            {columns.map((column) => (
              <th
                key={column.key}
                className="px-3 py-2 text-left text-xs font-semibold text-slate-600 whitespace-nowrap"
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {/* Show a simple message when the table has no rows */}
          {rows.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                className="py-6 text-center text-xs text-slate-400"
              >
                No data available
              </td>
            </tr>
          ) : (
            rows.map((row, index) => (
              <tr
                key={index}
                className={`
                  transition-colors duration-150
                  border-b border-slate-100 last:border-b-0
                  hover:bg-blue-50
                  ${index % 2 === 0 ? "bg-white" : "bg-slate-50/50"}
                `}
              >
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={`px-3 py-2 text-slate-700 whitespace-nowrap ${
                      /* Keep numeric columns aligned to the right */
                      ["orders", "revenue", "amount"].includes(column.key)
                        ? "text-right font-medium"
                        : "text-left"
                    }`}
                  >
                    {column.render
                      ? column.render(row[column.key], row)
                      : row[column.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
