import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  BarChart3,
  Database,
  FileText,
  Loader2,
  Send,
  Upload,
  User,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  getMyDatasets,
  askAIAnalytics,
  uploadKnowledgeDocument,
  getKnowledgeStatus,
} from "../services/api";

/* Format numeric results so large values are easier to read */
function formatNumber(value) {
  if (typeof value !== "number") {
    return String(value);
  }

  return value.toLocaleString(undefined, {
    maximumFractionDigits: 2,
  });
}

/* Clean the final AI response before showing it in the chat */
function cleanAnswer(answer) {
  if (!answer) {
    return "";
  }

  return answer.replace(/\*\*/g, "").trim();
}

/* Build a readable answer from structured chart data */
function buildStructuredAnswer(answer, visualization, chartData) {
  if (
    !chartData ||
    !Array.isArray(chartData.data) ||
    chartData.data.length === 0
  ) {
    return answer;
  }

  if (
    !chartData.x_key ||
    !Array.isArray(chartData.series) ||
    chartData.series.length === 0
  ) {
    return answer;
  }

  const xKey = chartData.x_key;
  const series = chartData.series[0];
  const yKey = series.data_key;

  if (!yKey) {
    return answer;
  }

  if (visualization === "chart") {
    if (chartData.chart_type === "line") {
      return (
        "Here is the forecast for the requested period:\n\n" +
        chartData.data
          .map((item) => {
            const label = item[xKey];
            const value = item[yKey];

            return `${label} — ${formatNumber(value)}`;
          })
          .join("\n")
      );
    }

    return (
      "Here are the results grouped by " +
      `${xKey.replace(/_/g, " ")}:\n\n` +
      chartData.data
        .map((item) => {
          const label = item[xKey];
          const value = item[yKey];

          return `${label} — ${formatNumber(value)}`;
        })
        .join("\n")
    );
  }

  return answer;
}

function AIAnalytics() {
  const { t } = useTranslation();

  /* Store the currently selected dataset and its display information */
  const [selectedDataset, setSelectedDataset] = useState("");
  const [datasetInfo, setDatasetInfo] = useState(null);

  /* Store the current question and complete chat history */
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  /* Track dataset loading and question processing states */
  const [loading, setLoading] = useState(true);
  const [asking, setAsking] = useState(false);

  /* Track PDF upload state and the selected knowledge file */
  const [knowledgeFile, setKnowledgeFile] = useState(null);
  const [uploadingKnowledge, setUploadingKnowledge] = useState(false);
  const [knowledgeUploaded, setKnowledgeUploaded] = useState(false);
  const [uploadedKnowledgeName, setUploadedKnowledgeName] = useState("");

  /* Store errors that need to be displayed to the user */
  const [error, setError] = useState("");

  /* Reference to the chat container so new messages stay visible */
  const chatRef = useRef(null);

  /* Load the selected dataset when the page opens */
  useEffect(() => {
    loadSelectedDataset();
  }, []);

  /* Scroll to the latest message whenever the conversation changes */
  useEffect(() => {
    if (!chatRef.current) {
      return;
    }

    requestAnimationFrame(() => {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    });
  }, [messages, asking]);

  /*
   * Load the knowledge document already stored for the selected dataset
   */
  const loadKnowledgeStatus = async (datasetId) => {
    if (!datasetId) {
      setKnowledgeUploaded(false);
      setUploadedKnowledgeName("");
      return;
    }

    try {
      const response = await getKnowledgeStatus(datasetId);

      setKnowledgeUploaded(Boolean(response.uploaded));

      setUploadedKnowledgeName(response.filename || "");
    } catch (err) {
      setKnowledgeUploaded(false);
      setUploadedKnowledgeName("");
    }
  };

  // /* Find the dataset selected on the Dataset page */
  // const loadSelectedDataset = async () => {
  //   try {
  //     setLoading(true);
  //     setError("");

  //     /* The selected dataset ID is shared through localStorage */
  //     const datasetId = localStorage.getItem("selected_dataset") || "";

  //     /* Stop here when no dataset has been selected */
  //     if (!datasetId) {
  //       setSelectedDataset("");
  //       setDatasetInfo(null);
  //       return;
  //     }

  //     setSelectedDataset(datasetId);

  //     /* Olist is the built in dataset and does not need an API lookup */
  //     if (datasetId === "olist") {
  //       setDatasetInfo({
  //         dataset_id: "olist",
  //         filename: "Olist Dataset",
  //       });

  //       return;
  //     }

  //     /* Load user uploaded datasets from the backend */
  //     const response = await getMyDatasets();

  //     const datasets = response.data || [];

  //     /* Find the dataset matching the selected ID */
  //     const selected = datasets.find(
  //       (dataset) => dataset.dataset_id === datasetId,
  //     );

  //     /* Tell the user if the selected dataset no longer exists */
  //     if (!selected) {
  //       setDatasetInfo(null);
  //       setError(t("datasetUnavailable"));
  //       return;
  //     }

  //     setDatasetInfo(selected);
  //   } catch (err) {
  //     /* Use the backend message when available */
  //     setError(err?.response?.data?.detail || t("unableToLoadDataset"));
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  /*
   * Find the dataset selected on the Dataset page
   */
  const loadSelectedDataset = async () => {
    try {
      setLoading(true);
      setError("");

      /*
       * The selected dataset ID is shared through localStorage
       */
      const datasetId = localStorage.getItem("selected_dataset") || "";

      /*
       * Stop here when no dataset has been selected
       */
      if (!datasetId) {
        setSelectedDataset("");
        setDatasetInfo(null);
        setKnowledgeUploaded(false);
        setUploadedKnowledgeName("");
        return;
      }

      setSelectedDataset(datasetId);

      /*
       * Load the knowledge document status from the backend
       */
      await loadKnowledgeStatus(datasetId);

      /*
       * Olist is the built in dataset and does not need an API lookup
       */
      if (datasetId === "olist") {
        setDatasetInfo({
          dataset_id: "olist",
          filename: "Olist Dataset",
        });

        return;
      }

      /*
       * Load user uploaded datasets from the backend
       */
      const response = await getMyDatasets();

      const datasets = response.data || [];

      /*
       * Find the dataset matching the selected ID
       */
      const selected = datasets.find(
        (dataset) => dataset.dataset_id === datasetId,
      );

      /*
       * Tell the user if the selected dataset no longer exists
       */
      if (!selected) {
        setDatasetInfo(null);
        setKnowledgeUploaded(false);
        setUploadedKnowledgeName("");
        setError(t("datasetUnavailable"));
        return;
      }

      setDatasetInfo(selected);
    } catch (err) {
      /*
       * Use the backend message when available
       */
      setError(err?.response?.data?.detail || t("unableToLoadDataset"));
    } finally {
      setLoading(false);
    }
  };

  /* Upload the selected PDF as a knowledge source for the current dataset */
  // const handleKnowledgeUpload = async () => {
  //   if (!knowledgeFile || !selectedDataset || uploadingKnowledge) {
  //     return;
  //   }

  //   setUploadingKnowledge(true);
  //   setError("");

  //   try {
  //     /* Send the PDF and selected dataset to the knowledge API */
  //     await uploadKnowledgeDocument(selectedDataset, knowledgeFile);

  //     setKnowledgeUploaded(true);
  //     setUploadedKnowledgeName(knowledgeFile.name);

  //     /* Clear the selected file after a successful upload */
  //     setKnowledgeFile(null);

  //     /* Reset the browser file input */
  //     const fileInput = document.getElementById("knowledge-file-input");

  //     if (fileInput) {
  //       fileInput.value = "";
  //     }
  //   } catch (err) {
  //     const detail = err?.response?.data?.detail || "";

  //     if (
  //       detail.toLowerCase().includes("already been uploaded") ||
  //       detail.toLowerCase().includes("already uploaded")
  //     ) {
  //       setKnowledgeUploaded(true);

  //       if (knowledgeFile) {
  //         setUploadedKnowledgeName(knowledgeFile.name);
  //       }

  //       setKnowledgeFile(null);
  //       setError("");

  //       const fileInput = document.getElementById("knowledge-file-input");

  //       if (fileInput) {
  //         fileInput.value = "";
  //       }

  //       return;
  //     }

  //     setError(detail || "Unable to upload the knowledge document.");
  //   } finally {
  //     setUploadingKnowledge(false);
  //   }
  // };

  /*
   * Upload the selected PDF as a knowledge source for the current dataset
   */
  const handleKnowledgeUpload = async () => {
    if (!knowledgeFile || !selectedDataset || uploadingKnowledge) {
      return;
    }

    setUploadingKnowledge(true);
    setError("");

    try {
      /*
       * Send the PDF and selected dataset to the knowledge API
       */
      const response = await uploadKnowledgeDocument(
        selectedDataset,
        knowledgeFile,
      );

      setKnowledgeUploaded(true);

      setUploadedKnowledgeName(response?.filename || knowledgeFile.name);

      /*
       * Clear the selected file after a successful upload
       */
      setKnowledgeFile(null);

      /*
       * Reset the browser file input
       */
      const fileInput = document.getElementById("knowledge-file-input");

      if (fileInput) {
        fileInput.value = "";
      }
    } catch (err) {
      const detail = err?.response?.data?.detail || "";

      /*
       * If the document already exists, load the
       * actual stored document information
       */
      if (
        detail.toLowerCase().includes("already been uploaded") ||
        detail.toLowerCase().includes("already uploaded")
      ) {
        await loadKnowledgeStatus(selectedDataset);

        setKnowledgeFile(null);

        const fileInput = document.getElementById("knowledge-file-input");

        if (fileInput) {
          fileInput.value = "";
        }

        setError(
          detail ||
            "This PDF has already been uploaded for the selected dataset.",
        );

        return;
      }

      setError(detail || "Unable to upload the knowledge document.");
    } finally {
      setUploadingKnowledge(false);
    }
  };

  /* Send the user's question to the AI Analytics backend */
  const handleAsk = async (event) => {
    event?.preventDefault();

    const trimmedQuestion = question.trim();

    /* Ignore empty questions or another request while processing */
    if (!trimmedQuestion || !selectedDataset || asking) {
      return;
    }

    /* Clear the input after submitting the question */
    setQuestion("");

    /* Add the question to the conversation immediately */
    const userMessage = {
      id: Date.now(),
      role: "user",
      question: trimmedQuestion,
    };

    setMessages((current) => [...current, userMessage]);

    setAsking(true);
    setError("");

    try {
      /* Send the dataset and question to the backend */
      const response = await askAIAnalytics(selectedDataset, trimmedQuestion);

      const visualization = response.visualization;

      const chartData = response.chart_data;

      /* Use structured chart data to create a readable answer */
      const answer = buildStructuredAnswer(
        cleanAnswer(response.answer),
        visualization,
        chartData,
      );

      /* Store the complete structured backend response */
      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        answer,
        result: response.result,
        query: response.query,
        visualization,
        tableData: response.table_data,
        chartData,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch (err) {
      /* Display the backend error when the request fails */
      setError(err?.response?.data?.detail || t("unableToProcessQuestion"));
    } finally {
      setAsking(false);
    }
  };

  /* Put an example question into the input field */
  const handleExampleClick = (value) => {
    setQuestion(value);
  };

  /* Render a structured table returned by the backend */
  const renderTable = (tableData) => {
    if (
      !tableData ||
      !Array.isArray(tableData.columns) ||
      !Array.isArray(tableData.rows)
    ) {
      return null;
    }

    /* Show a message when the table has no rows */
    if (tableData.rows.length === 0) {
      return (
        <div className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5">
          <p className="text-sm text-slate-500">{t("noMatchingData")}</p>
        </div>
      );
    }

    return (
      <div className="w-full overflow-hidden rounded-lg border border-slate-200 bg-white">
        <div className="max-h-[420px] overflow-auto">
          <table className="w-full min-w-max border-collapse text-sm">
            <thead className="sticky top-0 bg-slate-100">
              <tr>
                {tableData.columns.map((column) => (
                  <th
                    key={column}
                    className="border-b border-slate-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500"
                  >
                    {column}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {tableData.rows.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className="border-b border-slate-100 last:border-b-0 hover:bg-slate-50"
                >
                  {tableData.columns.map((column) => (
                    <td key={column} className="px-4 py-3 text-slate-700">
                      {typeof row[column] === "number"
                        ? formatNumber(row[column])
                        : String(row[column] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  /* Render a compact bar or line chart returned by the backend */
  const renderChart = (chartData) => {
    if (
      !chartData ||
      !Array.isArray(chartData.data) ||
      !chartData.data.length ||
      !chartData.x_key ||
      !Array.isArray(chartData.series) ||
      !chartData.series.length
    ) {
      return null;
    }

    const chartType = chartData.chart_type;

    return (
      <div className="w-full max-w-3xl rounded-lg border border-slate-200 bg-white p-3">
        <div className="h-[220px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            {chartType === "line" ? (
              <LineChart
                data={chartData.data}
                margin={{
                  top: 8,
                  right: 12,
                  left: 0,
                  bottom: 8,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey={chartData.x_key} tick={{ fontSize: 11 }} />

                <YAxis
                  tick={{ fontSize: 11 }}
                  tickFormatter={(value) => formatNumber(value)}
                />

                <Tooltip
                  formatter={(value) =>
                    typeof value === "number" ? formatNumber(value) : value
                  }
                />

                <Legend />

                {chartData.series.map((series) => (
                  <Line
                    key={series.data_key}
                    type="monotone"
                    dataKey={series.data_key}
                    name={series.label || series.data_key}
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />
                ))}
              </LineChart>
            ) : (
              <BarChart
                data={chartData.data}
                margin={{
                  top: 8,
                  right: 12,
                  left: 0,
                  bottom: 8,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey={chartData.x_key} tick={{ fontSize: 11 }} />

                <YAxis
                  tick={{ fontSize: 11 }}
                  tickFormatter={(value) => formatNumber(value)}
                />

                <Tooltip
                  formatter={(value) =>
                    typeof value === "number" ? formatNumber(value) : value
                  }
                />

                <Legend />

                {chartData.series.map((series) => (
                  <Bar
                    key={series.data_key}
                    dataKey={series.data_key}
                    name={series.label || series.data_key}
                  />
                ))}
              </BarChart>
            )}
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderResult = (result) => {
    if (result === null || result === undefined) {
      return null;
    }

    // Simple values are already shown by the AI answer
    if (typeof result === "number" || typeof result === "string") {
      return null;
    }

    // Render array results
    if (Array.isArray(result)) {
      if (result.length === 0) {
        return (
          <div className="w-full max-w-3xl rounded-lg border border-slate-200 bg-slate-50 p-5">
            <p className="text-sm text-slate-500">{t("noMatchingData")}</p>
          </div>
        );
      }

      return (
        <div className="w-full max-w-3xl rounded-lg border border-slate-200 bg-slate-50 p-4">
          <div className="space-y-3">
            {result.map((item, index) => {
              if (typeof item !== "object" || item === null) {
                return (
                  <div
                    key={index}
                    className="flex items-center justify-between gap-4 border-b border-slate-200 pb-2 last:border-b-0 last:pb-0"
                  >
                    <span className="text-sm text-slate-500">{index + 1}</span>

                    <span className="text-sm font-semibold text-slate-800">
                      {typeof item === "number"
                        ? formatNumber(item)
                        : String(item)}
                    </span>
                  </div>
                );
              }

              return (
                <div
                  key={index}
                  className="grid grid-cols-1 gap-3 border-b border-slate-200 pb-3 last:border-b-0 last:pb-0 sm:grid-cols-2"
                >
                  {Object.entries(item).map(([key, value]) => (
                    <div key={key} className="min-w-0">
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                        {key.replace(/_/g, " ")}
                      </p>

                      <p className="mt-1 break-words text-sm font-semibold text-slate-800">
                        {typeof value === "number"
                          ? formatNumber(value)
                          : typeof value === "object" && value !== null
                            ? JSON.stringify(value)
                            : String(value ?? "")}
                      </p>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    // Render structured object results
    if (typeof result === "object") {
      const entries = Object.entries(result);

      return (
        <div className="w-full max-w-3xl rounded-lg border border-slate-200 bg-slate-50 p-4">
          <div className="space-y-3">
            {entries.map(([key, value]) => {
              // Forecast prediction details are already included in the answer
              if (key === "predicted" && Array.isArray(value)) {
                return null;
              }

              // Raw RAG chunks should not be displayed to the user
              if (key === "chunks") {
                return null;
              }

              return (
                <div
                  key={key}
                  className="flex flex-wrap items-start justify-between gap-4 border-b border-slate-200 pb-2 last:border-b-0 last:pb-0"
                >
                  <span className="text-sm font-medium capitalize text-slate-500">
                    {key.replace(/_/g, " ")}
                  </span>

                  <span className="max-w-[70%] break-words text-right text-sm font-semibold text-slate-800">
                    {typeof value === "number"
                      ? formatNumber(value)
                      : Array.isArray(value)
                        ? value
                            .map((item) => {
                              if (typeof item === "object" && item !== null) {
                                return Object.entries(item)
                                  .map(
                                    ([itemKey, itemValue]) =>
                                      `${itemKey.replace(/_/g, " ")}: ${
                                        typeof itemValue === "number"
                                          ? formatNumber(itemValue)
                                          : String(itemValue ?? "")
                                      }`,
                                  )
                                  .join(", ");
                              }

                              return String(item);
                            })
                            .join(" | ")
                        : typeof value === "object" && value !== null
                          ? JSON.stringify(value)
                          : String(value ?? "")}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="h-[calc(100vh-74px)] w-full overflow-hidden bg-slate-200">
      <div className="flex h-full w-full flex-col overflow-hidden">
        {/* Page heading and short description */}
        <div className="shrink-0 px-6 pb-4 pt-5">
          <h1 className="text-2xl font-bold text-slate-800">
            {t("aiAnalytics")}
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            {t("querySelectedDataset")}
          </p>
        </div>

        {/* Main workspace with controls on the left and chat on the right */}
        <div className="min-h-0 flex-1 px-6 pb-5">
          <div className="grid h-full min-h-0 grid-cols-1 gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
            {/* Left side contains dataset and knowledge controls */}
            <div className="min-h-0 overflow-y-auto">
              <div className="space-y-4">
                {/* Selected dataset card */}
                <div className="min-w-0 w-full overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
                  <div className="px-5 py-4">
                    <div className="flex items-start gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
                        <Database size={19} />
                      </div>

                      <div className="min-w-0 flex-1">
                        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                          {t("dataSource")}
                        </p>

                        {loading ? (
                          <div className="mt-2 flex items-center gap-2 text-sm text-slate-500">
                            <Loader2 size={15} className="animate-spin" />

                            {t("loadingDataset")}
                          </div>
                        ) : (
                          <p className="mt-2 break-words text-sm font-semibold text-slate-700">
                            {datasetInfo?.filename || t("noDatasetSelected")}
                          </p>
                        )}
                      </div>
                    </div>

                    {datasetInfo && (
                      <div className="mt-4 rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">
                        {t("selectedFromDataset")}
                      </div>
                    )}
                  </div>

                  {!loading && !selectedDataset && (
                    <div className="border-t border-slate-100 px-5 py-3 text-sm text-amber-700">
                      {t("selectDatasetFirst")}
                    </div>
                  )}
                </div>

                {/* Knowledge document upload card */}
                <div className="w-full rounded-xl border border-slate-200 bg-white shadow-sm">
                  <div className="px-5 py-4">
                    <div className="flex items-start gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
                        <FileText size={19} />
                      </div>

                      <div className="min-w-0">
                        <p className="text-sm font-semibold text-slate-800">
                          Knowledge Document
                        </p>

                        <p className="mt-1 text-xs leading-5 text-slate-500">
                          Upload a PDF to ask questions about its contents
                        </p>
                      </div>
                    </div>

                    <div className="mt-4 space-y-3">
                      {knowledgeUploaded && (
                        <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3">
                          <div className="flex items-start gap-2">
                            <span className="mt-0.5 shrink-0 text-emerald-600">
                              ✓
                            </span>

                            <div className="min-w-0">
                              <p className="text-sm font-semibold text-emerald-700">
                                Knowledge document already uploaded
                              </p>

                              {uploadedKnowledgeName && (
                                <p className="mt-1 min-w-0 break-all text-xs leading-5 text-emerald-700">
                                  {uploadedKnowledgeName}
                                </p>
                              )}
                            </div>
                          </div>
                        </div>
                      )}

                      <input
                        id="knowledge-file-input"
                        type="file"
                        accept="application/pdf,.pdf"
                        onChange={(event) => {
                          const file = event.target.files?.[0] || null;

                          setKnowledgeFile(file);
                          setError("");
                        }}
                        disabled={!selectedDataset || uploadingKnowledge}
                        className="block min-w-0 max-w-full w-full overflow-hidden text-sm text-slate-500 file:mr-3 file:rounded-md file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-xs file:font-semibold file:text-slate-700 hover:file:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
                      />

                      <button
                        type="button"
                        onClick={handleKnowledgeUpload}
                        disabled={
                          !knowledgeFile ||
                          !selectedDataset ||
                          uploadingKnowledge
                        }
                        className="flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-slate-800 px-4 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        {uploadingKnowledge ? (
                          <Loader2 size={16} className="animate-spin" />
                        ) : (
                          <Upload size={16} />
                        )}

                        {uploadingKnowledge
                          ? "Uploading..."
                          : knowledgeUploaded
                            ? "Replace PDF"
                            : "Upload PDF"}
                      </button>

                      {knowledgeFile && (
                        <div className="min-w-0 overflow-hidden border-t border-slate-100 pt-3 text-xs text-slate-500">
                          <span className="break-all">
                            Selected: {knowledgeFile.name}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Display errors from dataset or PDF operations */}
                {error && !asking && (
                  <div className="rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700">
                    {error}
                  </div>
                )}
              </div>
            </div>

            {/* Right side contains the complete AI Analytics chat */}
            <div className="min-h-0">
              <div className="flex h-full min-h-[520px] flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
                {/* Analytics conversation header */}
                <div className="shrink-0 border-b border-slate-200 px-5 py-4">
                  <h2 className="text-base font-semibold text-slate-800">
                    {t("dataAnalysis")}
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    {t("askQuestionsSelectedDataset")}
                  </p>
                </div>

                {/* Scrollable conversation area */}
                <div
                  ref={chatRef}
                  className="min-h-0 flex-1 overflow-y-auto px-5 py-6"
                >
                  {messages.length === 0 ? (
                    <div className="flex min-h-full items-center justify-center">
                      <div className="max-w-2xl text-center">
                        <div className="mb-4 flex justify-center">
                          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
                            <BarChart3 size={22} />
                          </div>
                        </div>

                        <h3 className="text-lg font-semibold text-slate-800">
                          {t("startWithQuestion")}
                        </h3>

                        <p className="mt-2 text-sm text-slate-500">
                          {t("askAboutData")}
                        </p>

                        <div className="mt-5 flex flex-wrap justify-center gap-2">
                          {[
                            t("howManyRecords"),
                            t("totalRevenueQuestion"),
                            t("averageRevenueQuestion"),
                            t("topCategoryQuestion"),
                          ].map((item) => (
                            <button
                              key={item}
                              type="button"
                              disabled={!selectedDataset}
                              onClick={() => handleExampleClick(item)}
                              className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600 transition hover:border-slate-300 hover:bg-white disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              {item}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-8">
                      {messages.map((message) => {
                        {
                          /* Render user questions on the right */
                        }
                        if (message.role === "user") {
                          return (
                            <div key={message.id} className="flex justify-end">
                              <div className="max-w-3xl rounded-xl bg-primary-600 px-5 py-3 text-sm leading-6 text-white">
                                <div className="flex items-start gap-2">
                                  <User size={16} className="mt-1 shrink-0" />

                                  <p>{message.question}</p>
                                </div>
                              </div>
                            </div>
                          );
                        }

                        {
                          /* Render BusinessPulse responses */
                        }
                        return (
                          <div key={message.id} className="w-full">
                            <div className="mb-2 flex items-center gap-2">
                              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
                                <BarChart3 size={16} />
                              </div>

                              <span className="text-sm font-semibold text-slate-700">
                                BusinessPulse
                              </span>
                            </div>

                            {/* Show the final natural-language answer */}
                            {message.answer && (
                              <div className="mb-4 max-w-3xl whitespace-pre-line text-sm leading-6 text-slate-700">
                                {message.answer}
                              </div>
                            )}

                            {/* Tables are shown below the answer */}
                            {message.tableData && (
                              <div className="mb-4">
                                {renderTable(message.tableData)}
                              </div>
                            )}

                            {/* Charts are shown below the answer */}
                            {message.chartData && (
                              <div className="mb-4">
                                {renderChart(message.chartData)}
                              </div>
                            )}

                            {/* Only show structured results when there is no table or chart */}
                            {!message.tableData &&
                              !message.chartData &&
                              message.query?.query_type !== "rag" &&
                              message.result &&
                              typeof message.result === "object" &&
                              renderResult(message.result)}
                          </div>
                        );
                      })}

                      {/* Show processing state while the backend works */}
                      {asking && (
                        <div className="flex items-center gap-3 text-sm text-slate-500">
                          <Loader2 size={17} className="animate-spin" />

                          {t("processingQuestion")}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Display API errors above the input */}
                {error && asking === false && (
                  <div className="shrink-0 border-t border-rose-100 bg-rose-50 px-5 py-3 text-sm text-rose-700">
                    {error}
                  </div>
                )}

                {/* Question input and submit button */}
                <div className="shrink-0 border-t border-slate-200 bg-white p-3">
                  <form
                    onSubmit={handleAsk}
                    className="flex w-full items-center gap-3"
                  >
                    <input
                      type="text"
                      value={question}
                      onChange={(event) => setQuestion(event.target.value)}
                      placeholder={
                        selectedDataset
                          ? t("askQuestionPlaceholder")
                          : t("selectDatasetPlaceholder")
                      }
                      disabled={!selectedDataset || asking}
                      className="h-12 min-w-0 flex-1 rounded-lg border border-slate-300 bg-white px-4 text-sm text-slate-700 outline-none transition focus:border-primary-500 focus:ring-1 focus:ring-primary-500 disabled:cursor-not-allowed disabled:bg-slate-100"
                    />

                    <button
                      type="submit"
                      disabled={asking || !selectedDataset || !question.trim()}
                      className="flex h-12 shrink-0 items-center gap-2 rounded-lg bg-primary-600 px-6 text-sm font-semibold text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {asking ? (
                        <Loader2 size={17} className="animate-spin" />
                      ) : (
                        <Send size={17} />
                      )}

                      {asking ? t("processing") : t("ask")}
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIAnalytics;
