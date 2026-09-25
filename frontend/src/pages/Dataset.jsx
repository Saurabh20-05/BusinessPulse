import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  uploadDataset,
  configureDataset,
  getMyDatasets,
  deleteDataset,
  previewDataset,
} from "../services/api";

import ColumnMapper from "../components/ColumnMapper";

function Dataset() {
  const { t } = useTranslation();

  const [file, setFile] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [mapping, setMapping] = useState({});
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [notification, setNotification] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [showPreview, setShowPreview] = useState(false);

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });

    setTimeout(() => {
      setNotification(null);
    }, 3000);
  };

  const handleDeleteDataset = async (datasetId, filename) => {
    const confirmed = window.confirm(t("deleteConfirmation", { filename }));

    if (!confirmed) {
      return;
    }

    try {
      await deleteDataset(datasetId);

      setDatasets((prev) =>
        prev.filter((dataset) => dataset.dataset_id !== datasetId),
      );

      if (selectedDataset === datasetId) {
        localStorage.removeItem("selected_dataset");
        setSelectedDataset(null);
      }

      showNotification(t("datasetDeleted"));
    } catch (error) {
      showNotification(
        error.response?.data?.detail || t("failedToDeleteDataset"),
        "error",
      );
    }
  };

  const handlePreviewDataset = async (datasetId) => {
    try {
      const response = await previewDataset(datasetId);

      setPreviewData(response.data);
      setShowPreview(true);
    } catch (error) {
      console.error("Failed to preview dataset:", error);

      showNotification(t("failedToLoadPreview"), "error");
    }
  };

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset");

    if (savedDataset) {
      setSelectedDataset(savedDataset);
    }

    const loadDatasets = async () => {
      try {
        const response = await getMyDatasets();
        setDatasets(response.data);
      } catch (error) {
        console.error("Failed to load datasets:", error);
      }
    };

    loadDatasets();
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      const response = await uploadDataset(file);

      setDataset(response.data);
      setFile(null);

      showNotification(t("datasetUploaded"));
    } catch (error) {
      console.error("Upload failed:", error);

      showNotification(
        error.response?.data?.detail || t("datasetUploadFailed"),
        "error",
      );
    }
  };

  const handleSaveMapping = async () => {
    if (!dataset) return;

    try {
      await configureDataset(dataset.dataset_id, mapping);

      showNotification(t("columnMappingSaved"));
    } catch (error) {
      console.error("Mapping failed:", error);

      showNotification(
        error.response?.data?.detail || t("failedToSaveMapping"),
        "error",
      );
    }
  };

  const handleSelectOlist = () => {
    localStorage.setItem("selected_dataset", "olist");
    setSelectedDataset("olist");

    showNotification(t("olistSelected"));
  };

  const handleSelectDataset = (datasetId, filename) => {
    setSelectedDataset(datasetId);
    localStorage.setItem("selected_dataset", datasetId);

    showNotification(t("datasetSelected", { filename }));
  };

  const selectedDatasetName =
    selectedDataset === "olist"
      ? "Olist Dataset"
      : datasets.find((item) => item.dataset_id === selectedDataset)
          ?.filename || "Custom Dataset";

  return (
    <div className="fade-in bg-slate-200 space-y-6 px-6 py-6 lg:px-8">
      {/* Notification */}
      {notification && (
        <div
          className={`fixed right-6 top-20 z-50 flex items-center gap-3 rounded-xl border px-4 py-3 text-sm font-medium shadow-lg ${
            notification.type === "error"
              ? "border-rose-200 bg-rose-50 text-rose-700"
              : "border-emerald-200 bg-emerald-50 text-emerald-700"
          }`}
        >
          <span>{notification.type === "error" ? "✕" : "✓"}</span>

          <span>{notification.message}</span>
        </div>
      )}

      {/* Page Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">
            {t("datasetPage")}
          </h1>

          <p className="mt-1 text-sm text-slate-500">{t("datasetSubtitle")}</p>
        </div>

        {selectedDataset && (
          <div className="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            {t("using")}: {selectedDatasetName}
          </div>
        )}
      </div>

      {/* Data Source Cards */}
      <div className="grid gap-5 lg:grid-cols-2">
        {/* Olist */}
        <div className="rounded-2xl border border-slate-300 bg-white p-6 shadow-card transition-shadow hover:shadow-lg">
          <div className="flex items-start gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-primary-50 text-2xl shadow-sm">
              📊
            </div>

            <div className="min-w-0">
              <h2 className="text-xl font-semibold text-slate-900">
                {t("builtInDataset")}
              </h2>

              <div className="mt-1.5 inline-flex items-center rounded-full bg-primary-50 px-3 py-1 text-xs font-medium text-primary-600">
                {t("builtInDataset")}
              </div>
            </div>
          </div>

          <p className="mt-5 max-w-xl text-sm leading-6 text-slate-500">
            {t("builtInDescription")}
          </p>

          <div className="mt-6 border-t border-slate-200 pt-5">
            <div className="flex items-center justify-between gap-4">
              <div className="inline-flex items-center rounded-lg bg-slate-100 px-3 py-2">
                <p className="text-sm font-medium text-slate-600">
                  {t("readyToAnalyze")}
                </p>
              </div>

              <button
                onClick={handleSelectOlist}
                className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-700"
              >
                {t("useOlistDataset")}
                <span className="text-base">→</span>
              </button>
            </div>
          </div>
        </div>

        {/* Custom Dataset */}
        <div className="rounded-2xl border border-slate-300 bg-white p-6 shadow-card transition-shadow hover:shadow-lg">
          <div className="flex items-start gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-violet-50 text-2xl shadow-sm">
              📁
            </div>

            <div className="min-w-0">
              <h2 className="text-xl font-semibold text-slate-900">
                {t("uploadDataset")}
              </h2>

              <div className="mt-1.5 inline-flex items-center rounded-full bg-violet-50 px-3 py-1 text-xs font-medium text-violet-600">
                {t("uploadOwnData")}
              </div>
            </div>
          </div>

          <p className="mt-5 max-w-xl text-sm leading-6 text-slate-500">
            {t("uploadDescription")}
          </p>

          <div className="mt-5 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full cursor-pointer text-sm text-slate-600 file:mr-4 file:cursor-pointer file:rounded-lg file:border-0 file:bg-white file:px-4 file:py-2 file:text-sm file:font-medium file:text-slate-700 file:shadow-sm"
            />

            {file && (
              <div className="mt-3 flex items-center justify-between rounded-lg bg-white px-3 py-2">
                <span className="truncate text-sm text-slate-600">
                  {file.name}
                </span>

                <span className="ml-3 text-xs font-medium text-emerald-600">
                  {t("ready")}
                </span>
              </div>
            )}
          </div>

          <div className="mt-5 flex justify-end">
            <button
              onClick={handleUpload}
              disabled={!file}
              className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {t("uploadCsv")}
              <span className="text-base">→</span>
            </button>
          </div>
        </div>
      </div>

      {/* Dataset Preview */}
      {dataset && (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-card">
          <div className="flex flex-col gap-2 border-b border-slate-200 px-6 py-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                {t("datasetPreview")}
              </h2>

              <p className="mt-1 text-sm text-slate-500">{dataset.filename}</p>
            </div>

            <div className="flex gap-2">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                {t("rows", { rows: dataset.rows })}
              </span>

              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                {t("columns", { count: dataset.columns.length })}
              </span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  {dataset.columns.map((column) => (
                    <th
                      key={column}
                      className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500"
                    >
                      {column}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {dataset.preview.map((row, index) => (
                  <tr
                    key={index}
                    className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                  >
                    {dataset.columns.map((column) => (
                      <td
                        key={column}
                        className="whitespace-nowrap px-5 py-3 text-slate-600"
                      >
                        {row[column]}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Column Mapping */}
      {dataset && (
        <div>
          <ColumnMapper
            columns={dataset.columns}
            onMappingChange={setMapping}
          />

          <div className="mt-4 flex justify-end">
            <button
              onClick={handleSaveMapping}
              className="rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-700"
            >
              {t("saveMapping")}
            </button>
          </div>
        </div>
      )}

      {/* Uploaded Datasets */}
      <div className="rounded-2xl border border-slate-300 bg-white shadow-card">
        <div className="border-b border-slate-200 px-6 py-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                {t("uploadedDatasets")}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {t("uploadedDatasetsDescription")}
              </p>
            </div>

            {datasets.length > 0 && (
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                {t("datasets", { count: datasets.length })}
              </span>
            )}
          </div>
        </div>

        {datasets.length === 0 ? (
          <div className="px-6 py-10 text-center">
            <p className="text-sm text-slate-500">{t("noUploadedDatasets")}</p>

            <p className="mt-1 text-xs text-slate-400">
              {t("uploadCsvToGetStarted")}
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {datasets.map((item) => {
              const isSelected = selectedDataset === item.dataset_id;

              return (
                <div
                  key={item.dataset_id}
                  className={`flex flex-col gap-4 px-6 py-4 transition sm:flex-row sm:items-center sm:justify-between ${
                    isSelected ? "bg-emerald-50/50" : "hover:bg-slate-50"
                  }`}
                >
                  <div className="flex min-w-0 items-center gap-4">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-lg">
                      📄
                    </div>

                    <div className="min-w-0">
                      <p className="truncate font-medium text-slate-900">
                        {item.filename}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {item.rows} rows · {item.columns.length} columns
                      </p>
                    </div>
                  </div>

                  <div className="flex shrink-0 gap-2">
                    <button
                      onClick={() =>
                        handleSelectDataset(item.dataset_id, item.filename)
                      }
                      className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                        isSelected
                          ? "border border-emerald-200 bg-emerald-50 text-emerald-700"
                          : "bg-primary-600 text-white hover:bg-primary-700"
                      }`}
                    >
                      {isSelected ? t("selected") : t("select")}
                    </button>

                    <button
                      onClick={() => handlePreviewDataset(item.dataset_id)}
                      className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                    >
                      {t("preview")}
                    </button>

                    <button
                      onClick={() =>
                        handleDeleteDataset(item.dataset_id, item.filename)
                      }
                      className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
                    >
                      {t("delete")}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {showPreview && previewData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-6">
          <div className="w-full max-w-6xl max-h-[85vh] overflow-hidden rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">
                  {previewData.filename}
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  {t("rows", { rows: previewData.rows })} ·{" "}
                  {t("columns", { count: previewData.columns.length })}
                </p>
              </div>

              <button
                onClick={() => {
                  setShowPreview(false);
                  setPreviewData(null);
                }}
                className="rounded-lg px-3 py-2 text-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-700"
              >
                ×
              </button>
            </div>

            <div className="max-h-[65vh] overflow-auto p-6">
              <table className="min-w-full border-collapse text-sm">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50">
                    {previewData.columns.map((column) => (
                      <th
                        key={column}
                        className="whitespace-nowrap px-4 py-3 text-left font-semibold text-slate-700"
                      >
                        {column}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {previewData.preview.map((row, rowIndex) => (
                    <tr key={rowIndex} className="border-b border-slate-100">
                      {previewData.columns.map((column) => (
                        <td
                          key={column}
                          className="whitespace-nowrap px-4 py-3 text-slate-600"
                        >
                          {row[column] ?? "-"}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex justify-end border-t border-slate-200 px-6 py-4">
              <button
                onClick={() => {
                  setShowPreview(false);
                  setPreviewData(null);
                }}
                className="rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-700"
              >
                {t("close")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dataset;
