import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  BarChart3,
  Database,
  Loader2,
  Send,
  User,
} from "lucide-react";

import {
  getMyDatasets,
  askAIAnalytics,
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

  return answer
    .replace(/\*\*/g, "")
    .replace(/\n+/g, " ")
    .trim();
}


function AIAnalytics() {
  const { t } = useTranslation();

  /* Store the currently selected dataset and its display information */
  const [selectedDataset, setSelectedDataset] = useState("");
  const [datasetInfo, setDatasetInfo] = useState(null);

  /* Store the current question and the complete chat history */
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  /* Track dataset loading and question processing states */
  const [loading, setLoading] = useState(true);
  const [asking, setAsking] = useState(false);

  /* Store errors that need to be displayed to the user */
  const [error, setError] = useState("");

  /* Reference to the chat container so new messages can scroll into view */
  const chatRef = useRef(null);


  /* Load the dataset selected by the user when the page opens */
  useEffect(() => {
    loadSelectedDataset();
  }, []);


  /* Automatically scroll to the latest message while the chat changes */
  useEffect(() => {
    if (!chatRef.current) {
      return;
    }

    requestAnimationFrame(() => {
      chatRef.current.scrollTop =
        chatRef.current.scrollHeight;
    });
  }, [messages, asking]);


  /* Find the dataset selected on the Dataset page */
  const loadSelectedDataset = async () => {
    try {
      setLoading(true);
      setError("");

      /* The selected dataset ID is shared through localStorage */
      const datasetId =
        localStorage.getItem("selected_dataset") || "";

      /* Stop here when the user has not selected a dataset */
      if (!datasetId) {
        setSelectedDataset("");
        setDatasetInfo(null);
        return;
      }

      setSelectedDataset(datasetId);

      /* Olist is the built in dataset and does not need an API lookup */
      if (datasetId === "olist") {
        setDatasetInfo({
          dataset_id: "olist",
          filename: "Olist Dataset",
        });

        return;
      }

      /* Load user uploaded datasets from the backend */
      const response = await getMyDatasets();

      const datasets = response.data || [];

      /* Find the dataset matching the ID stored in localStorage */
      const selected = datasets.find(
        (dataset) =>
          dataset.dataset_id === datasetId
      );

      /* Show an error if the previously selected dataset is no longer available */
      if (!selected) {
        setDatasetInfo(null);
        setError(t("datasetUnavailable"));
        return;
      }

      setDatasetInfo(selected);
    } catch (err) {
      /* Prefer the backend error message and fall back to the translated message */
      setError(
        err?.response?.data?.detail ||
          t("unableToLoadDataset")
      );
    } finally {
      setLoading(false);
    }
  };


  /* Send the user's question to the AI Analytics backend */
  const handleAsk = async (event) => {
    event?.preventDefault();

    const trimmedQuestion = question.trim();

    /* Do not send empty questions or start another request while one is running */
    if (
      !trimmedQuestion ||
      !selectedDataset ||
      asking
    ) {
      return;
    }

    /* Clear the input immediately after the question is submitted */
    setQuestion("");

    /* Add the user's question to the chat before waiting for the API response */
    const userMessage = {
      id: Date.now(),
      role: "user",
      question: trimmedQuestion,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setAsking(true);
    setError("");

    try {
      /* Send the selected dataset and question to the AI Analytics API */
      const response = await askAIAnalytics(
        selectedDataset,
        trimmedQuestion
      );

      /* Store the answer and calculated backend result as an assistant message */
      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        answer: cleanAnswer(response.answer),
        result: response.result,
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);
    } catch (err) {
      /* Display the backend error when the request cannot be processed */
      setError(
        err?.response?.data?.detail ||
          t("unableToProcessQuestion")
      );
    } finally {
      setAsking(false);
    }
  };


  /* Put an example question into the input field */
  const handleExampleClick = (value) => {
    setQuestion(value);
  };


  /* Render backend results according to their returned data type */
  const renderResult = (result) => {
    /* Do not render a result when the backend returned nothing */
    if (
      result === null ||
      result === undefined
    ) {
      return null;
    }

    /* Display a single numeric result as a large value */
    if (typeof result === "number") {
      return (
        <div className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
            {t("result")}
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {formatNumber(result)}
          </p>
        </div>
      );
    }

    /* Display a single string result as text */
    if (typeof result === "string") {
      return (
        <div className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
            {t("result")}
          </p>

          <p className="mt-2 text-xl font-semibold text-slate-800">
            {result}
          </p>
        </div>
      );
    }

    /* Display array results as a list of result cards */
    if (Array.isArray(result)) {
      /* Show a message when the query returned no matching records */
      if (result.length === 0) {
        return (
          <div className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5">
            <p className="text-sm text-slate-500">
              {t("noMatchingData")}
            </p>
          </div>
        );
      }

      return (
        <div className="w-full space-y-3">
          {result.map((item, index) => {
            /* Handle array items that are simple values instead of objects */
            if (
              typeof item !== "object" ||
              item === null
            ) {
              return (
                <div
                  key={index}
                  className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                    {t("result")}
                  </p>

                  <p className="mt-3 text-2xl font-bold text-slate-800">
                    {String(item)}
                  </p>
                </div>
              );
            }

            const entries = Object.entries(item);

            /* Use the first text or boolean field as the main label */
            const labelEntry = entries.find(
              ([, value]) =>
                typeof value === "string" ||
                typeof value === "boolean"
            );

            /* Use the first numeric field as the main displayed value */
            const valueEntry = entries.find(
              ([, value]) =>
                typeof value === "number"
            );

            const label = labelEntry
              ? String(labelEntry[1])
              : `${t("result")} ${index + 1}`;

            /* Show the numeric value when available
               otherwise display the remaining object values */
            const value = valueEntry
              ? formatNumber(valueEntry[1])
              : entries
                  .filter(
                    ([key]) =>
                      key !== labelEntry?.[0]
                  )
                  .map(([, value]) =>
                    String(value)
                  )
                  .join(" · ");

            return (
              <div
                key={index}
                className="w-full rounded-lg border border-slate-200 bg-slate-50 p-5"
              >
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                  {t("result")}
                </p>

                <p className="mt-3 text-lg font-semibold text-slate-800">
                  {label}
                </p>

                <p className="mt-2 text-2xl font-bold text-slate-800">
                  {value}
                </p>
              </div>
            );
          })}
        </div>
      );
    }

    return null;
  };


  return (
    <div className="h-[calc(100vh-74px)] w-full overflow-hidden bg-slate-200">
      <div className="flex h-full w-full flex-col overflow-hidden">
        <div className="flex min-h-0 h-full w-full flex-col">

          {/* Page heading and short description */}
          <div className="shrink-0 px-6 pt-5 pb-4">
            <h1 className="text-2xl font-bold text-slate-800">
              {t("aiAnalytics")}
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              {t("querySelectedDataset")}
            </p>
          </div>


          {/* Show which dataset will be used for the current questions */}
          <div className="shrink-0 px-6 pb-4">
            <div className="w-full rounded-xl border border-slate-200 bg-white shadow-sm">
              <div className="flex items-center gap-4 px-5 py-4">

                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
                  <Database size={19} />
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                    {t("dataSource")}
                  </p>

                  {/* Show a loading indicator until the selected dataset is resolved */}
                  {loading ? (
                    <div className="mt-1 flex items-center gap-2 text-sm text-slate-500">
                      <Loader2
                        size={15}
                        className="animate-spin"
                      />
                      {t("loadingDataset")}
                    </div>
                  ) : (
                    <p className="mt-1 truncate text-sm font-semibold text-slate-700">
                      {datasetInfo?.filename ||
                        t("noDatasetSelected")}
                    </p>
                  )}
                </div>

                {datasetInfo && (
                  <div className="hidden shrink-0 rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500 sm:block">
                    {t("selectedFromDataset")}
                  </div>
                )}
              </div>

              {/* Tell the user when a dataset must be selected before asking questions */}
              {!loading && !selectedDataset && (
                <div className="border-t border-slate-100 px-5 py-3 text-sm text-amber-700">
                  {t("selectDatasetFirst")}
                </div>
              )}
            </div>
          </div>


          {/* Main chat area containing questions and calculated results */}
          <div className="min-h-0 flex-1 px-6 pb-4">
            <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

              {/* Header for the analytics conversation */}
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
                  /* Empty state shown before the first question is submitted */
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

                      {/* Provide a few ready to use questions for the user */}
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
                            onClick={() =>
                              handleExampleClick(item)
                            }
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

                      /* Render user questions on the right side of the conversation */
                      if (message.role === "user") {
                        return (
                          <div
                            key={message.id}
                            className="flex justify-end"
                          >
                            <div className="max-w-3xl rounded-xl bg-primary-600 px-5 py-3 text-sm leading-6 text-white">
                              <div className="flex items-start gap-2">
                                <User
                                  size={16}
                                  className="mt-1 shrink-0"
                                />

                                <p>
                                  {message.question}
                                </p>
                              </div>
                            </div>
                          </div>
                        );
                      }

                      /* Render BusinessPulse answers and their calculated results */
                      return (
                        <div
                          key={message.id}
                          className="w-full"
                        >
                          <div className="mb-2 flex items-center gap-2">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
                              <BarChart3 size={16} />
                            </div>

                            <span className="text-sm font-semibold text-slate-700">
                              BusinessPulse
                            </span>
                          </div>

                          {message.answer && (
                            <p className="mb-4 text-sm leading-6 text-slate-700">
                              {message.answer}
                            </p>
                          )}

                          {renderResult(
                            message.result
                          )}
                        </div>
                      );
                    })}

                    {/* Show a loading state while the backend processes the question */}
                    {asking && (
                      <div className="flex items-center gap-3 text-sm text-slate-500">
                        <Loader2
                          size={17}
                          className="animate-spin"
                        />
                        {t("processingQuestion")}
                      </div>
                    )}
                  </div>
                )}
              </div>


              {/* Display API errors above the question input */}
              {error && (
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
                    onChange={(event) =>
                      setQuestion(event.target.value)
                    }
                    placeholder={
                      selectedDataset
                        ? t("askQuestionPlaceholder")
                        : t("selectDatasetPlaceholder")
                    }
                    disabled={
                      !selectedDataset || asking
                    }
                    className="h-12 min-w-0 flex-1 rounded-lg border border-slate-300 bg-white px-4 text-sm text-slate-700 outline-none transition focus:border-primary-500 focus:ring-1 focus:ring-primary-500 disabled:cursor-not-allowed disabled:bg-slate-100"
                  />

                  <button
                    type="submit"
                    disabled={
                      asking ||
                      !selectedDataset ||
                      !question.trim()
                    }
                    className="flex h-12 shrink-0 items-center gap-2 rounded-lg bg-primary-600 px-6 text-sm font-semibold text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {/* Replace the send icon with a spinner while the request is running */}
                    {asking ? (
                      <Loader2
                        size={17}
                        className="animate-spin"
                      />
                    ) : (
                      <Send size={17} />
                    )}

                    {asking
                      ? t("processing")
                      : t("ask")}
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIAnalytics;