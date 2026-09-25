import { useState } from "react";
import { useTranslation } from "react-i18next";

function ColumnMapper({ columns, onMappingChange }) {
  const { t } = useTranslation();
  const fields = [
    { key: "date", label: t("date"), required: true },
    { key: "revenue", label: t("revenue"), required: false },
    { key: "orders", label: t("orders"), required: false },
    { key: "customers", label: t("customers"), required: false },
    { key: "category", label: t("category"), required: false },
    { key: "state", label: t("state"), required: false },
    { key: "payment_method", label: t("paymentMethod"), required: false },
    { key: "review_score", label: t("reviewScore"), required: false },
    { key: "price", label: t("price"), required: false },
  ];

  const [mapping, setMapping] = useState({});

  const handleChange = (field, column) => {
    const updatedMapping = {
      ...mapping,
      [field]: column,
    };

    setMapping(updatedMapping);
    onMappingChange(updatedMapping);
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-card">
      <h2 className="text-lg font-semibold text-slate-900">
        {t("mapColumns")}
      </h2>

      <p className="mt-1 text-sm text-slate-500">
        {t("mapColumnsDescription")}
      </p>

      <div className="mt-5 space-y-4">
        {fields.map((field) => (
          <div
            key={field.key}
            className="flex items-center justify-between gap-4"
          >
            <label className="text-sm font-medium text-slate-700">
              {field.label}
              {field.required && <span className="ml-1 text-red-500">*</span>}
            </label>

            <select
              value={mapping[field.key] || ""}
              onChange={(e) => handleChange(field.key, e.target.value)}
              className="w-64 rounded-lg border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">{t("selectColumn")}</option>

              {columns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ColumnMapper;
