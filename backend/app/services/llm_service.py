import time
import json


import os


from typing import Literal


import pandas as pd


from dotenv import load_dotenv


from groq import Groq


from pydantic import BaseModel, ConfigDict


from app.schemas.ai_analytics import AnalyticsQuery

# Load environment variables from the .env file


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Stop the application early if the Groq API key is missing


if not GROQ_API_KEY:

    raise RuntimeError("GROQ_API_KEY is not configured in the .env file.")


# Create the Groq client used for query planning and final answers


client = Groq(
    api_key=GROQ_API_KEY,
)


# Model used by BusinessPulse for AI Analytics


MODEL_NAME = "openai/gpt-oss-20b"


class AIAgentPlan(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
    )

    # The agent chooses which backend tool should handle the question

    tool: Literal[
        "metadata_tool",
        "analytics_tool",
        "forecast_tool",
        "rag_tool",
        "general_tool",
    ]

    # The agent creates the structured query required by the selected tool

    query: AnalyticsQuery


def _build_schema_context(
    df: pd.DataFrame,
) -> str:

    columns = []

    # Include the position, name, data type, and sample values for each column

    for index, column in enumerate(
        df.columns,
        start=1,
    ):

        series = df[column]

        sample_values = series.dropna().astype(str).drop_duplicates().head(5).tolist()

        columns.append(
            {
                "position": index,
                "name": column,
                "dtype": str(series.dtype),
                "sample_values": sample_values,
            }
        )

    # Convert the dataset structure into JSON for the agent prompt

    return json.dumps(
        {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": columns,
        },
        ensure_ascii=False,
        default=str,
    )


def _make_strict_schema(
    schema,
):

    # Groq strict structured output requires every object property to be required

    if isinstance(schema, dict):

        if schema.get("type") == "object":

            properties = schema.get(
                "properties",
                {},
            )

            schema["required"] = list(properties.keys())

            schema["additionalProperties"] = False

        # Apply the same rules to nested objects

        for value in schema.values():

            _make_strict_schema(value)

    elif isinstance(schema, list):

        for item in schema:

            _make_strict_schema(item)

    return schema


def _build_strict_agent_schema():

    # Build the Pydantic schema for the complete agent response

    schema = AIAgentPlan.model_json_schema()

    # Apply strict object rules to the agent and nested AnalyticsQuery schema

    return _make_strict_schema(schema)


def _build_agent_prompt(
    schema_context: str,
) -> str:

    return f"""



You are the AI Agent for BusinessPulse.

First determine whether the question is about BusinessPulse data or is a general question.

Routing precedence:
- If the user does not clearly refer to the selected dataset, its values, its structure, business analytics, forecasts, or an uploaded knowledge document, use general_tool.
- Do not treat a question as a dataset question merely because a dataset is selected.
- Questions such as "What is Python?", "What is machine learning?", "Who are you?", greetings, arithmetic, coding help, and general factual questions must use general_tool.
- Questions explicitly referring to rows, columns, dataset values,
  historical metrics, calculations, forecasts, or uploaded documents
  must use the appropriate BusinessPulse tool.

- Questions asking for the meaning, definition, purpose, or business
  interpretation of a dataset field or metric must use rag_tool.








Your job is to understand the user's question, choose exactly one BusinessPulse



backend tool, and create exactly one AIAgentPlan containing one AnalyticsQuery.







You are NOT responsible for calculating numeric results.







The selected backend tool performs the actual calculation or retrieval.







DATASET INFORMATION:



{schema_context}











\\==================================================



AVAILABLE TOOLS



\\==================================================







Choose exactly ONE:







1\\. metadata_tool



2\\. analytics_tool



3\\. forecast_tool



4\\. rag_tool



5\\. general_tool


        ==================================================
        FIELD MEANING / BUSINESS DEFINITION QUESTIONS
        ==================================================

        Use rag_tool when the user asks what a dataset field, column,
        metric, or business concept means or represents.

        These are knowledge questions, not dataframe structure questions.

        Examples:

        "What does the profit field represent?"

        "What does revenue mean in this dataset?"

        "What is the purpose of customer_segment?"

        "What does shipping_days represent?"

        "What does review_score mean?"

        "What is the business meaning of the profit column?"

        "Explain the customer_segment field."

        "What does the sales_channel field represent?"

        "What is the meaning of order_status?"

        "Explain what profit represents."

        Even if the field name exists as an actual dataset column,
        use rag_tool when the user is asking for its meaning,
        definition, purpose, or business interpretation.

        Do NOT use metadata_tool for these questions.

        Metadata questions ask about the dataframe itself, such as:

        "What are the column names?"

        "What is the data type of profit?"

        "How many values are in profit?"

        "How many missing values are in profit?"

        Those remain metadata_tool questions.

        For field meaning questions use exactly:

        tool = "rag_tool"
        query_type = "rag"
        operation = "knowledge_search"
        visualization = "text"

        field = null
        group_by = null
        filters = []
        limit = null
        sort = null
        row_number = null
        column_number = null
        prediction_type = null
        horizon = null
        forecast_offset = null
        model_name = null
        direct_answer = null
        direct_result = null








\\==================================================

1\\. metadata_tool



\\==================================================







Use metadata_tool for questions about the selected dataset itself.







This includes:







\\- dataset structure



\\- columns



\\- rows



\\- column names



\\- column positions



\\- data types



\\- missing values



\\- unique values



\\- raw cell values



\\- general dataset summary







Examples:







"What are the columns?"







"What are the data types?"







"How many rows are there?"







"What is the 6th column?"







"What is the value in row 14 column 6?"







"How many missing values are there?"







"What does this dataset contain?"







Use:







query_type = "metadata"







Allowed operations:







\\- columns



\\- row_count



\\- column_name



\\- column_values



\\- cell_value



\\- data_types



\\- missing_values



\\- unique_values



\\- summary







Row and column numbers are 1-based.







Do NOT use metadata_tool when the user explicitly asks what an uploaded



PDF, report, document, or knowledge base says.











\\==================================================



2\\. analytics_tool



\\==================================================







Use analytics_tool for calculations performed on historical dataset data.







Examples:







"What is the total revenue?"







"What is the average revenue?"







"How many orders are there?"







"Show revenue by state."







"Which category generated the most revenue?"







"Which column has the highest average value?"







Use:







query_type = "analytics"







Allowed operations:







\\- count



\\- sum



\\- average



\\- min



\\- max



\\- highest_average



\\- lowest_average



\\- group_by



\\- top_n







Use exact dataset column names.







Do not calculate the result yourself.











\\==================================================



HIGHEST AVERAGE



\\==================================================







Use:







operation = "highest_average"







when the user asks:







"Which column has the highest average value?"







"Which numeric column has the highest average?"







"Which field has the largest average?"







"Which column has the greatest average?"







For highest_average:







query_type = "analytics"



operation = "highest_average"



field = null







The backend compares all numeric columns.







Do not select a numeric field yourself.











\\==================================================



LOWEST AVERAGE



\\==================================================







Use:







operation = "lowest_average"







when the user asks:







"Which column has the lowest average value?"







"Which numeric column has the lowest average?"







"Which field has the smallest average?"







"Which column has the least average?"







For lowest_average:







query_type = "analytics"



operation = "lowest_average"



field = null







The backend compares all numeric columns.







Do not select a numeric field yourself.











\\==================================================



NORMAL AVERAGE



\\==================================================







Use:







operation = "average"







when the user asks for the average of one specific field.







Example:







"What is the average revenue?"







"What is the average payment value?"







For average:







field = the requested numeric dataset column.







Do not use average when the user asks which column has the highest or lowest



average.











\\==================================================



OTHER ANALYTICS OPERATIONS



\\==================================================







Use count for questions such as:







"How many orders are there?"







"How many records are there?"







Use sum for:







"What is the total revenue?"







"What are the total sales?"







Use min for:







"What is the minimum revenue?"







Use max for:







"What is the maximum revenue?"







Use group_by for:







"Show revenue by state."







"Show revenue by category."







For group_by:







field = numeric column being aggregated







group_by = grouping column







Use top_n for:







"Which category generated the most revenue?"







"Top 5 states by revenue."







For top_n:







field = numeric column being aggregated







group_by = grouping column







limit = requested number







sort = "desc" for highest values







sort = "asc" for lowest values











\\==================================================



3\\. forecast_tool



\\==================================================







Use forecast_tool for future predictions and future forecast periods.







Examples:







"What will revenue be next month?"







"What will orders be for the next 3 months?"







"What will revenue be 2 months after?"







"Which future month has the highest predicted revenue?"







"What month is the next revenue forecast?"







Use:







query_type = "forecast"







Allowed operations:







\\- forecast



\\- forecast_total



\\- forecast_average



\\- forecast_min



\\- forecast_max



\\- forecast_highest_month



\\- forecast_lowest_month



\\- forecast_month







Allowed prediction types:







\\- revenue



\\- orders



\\- customers







BusinessPulse supports a maximum of 4 future months.







Default models:







revenue:



linear







orders:



random_forest







customers:



polynomial







Do not invent another model.











\\==================================================



FORECAST HORIZON VS FORECAST OFFSET



\\==================================================







horizon means how many future forecast points should be returned.







Example:







"What will revenue be for the next 2 months?"







Use:







horizon = 2



forecast_offset = null







forecast_offset means a specific future forecast point.







Example:







"What will revenue be 2 months after?"







Use:







horizon = 1



forecast_offset = 2







Therefore:







"next 2 months"







means:







horizon = 2



forecast_offset = null







"2 months after"







means:







horizon = 1



forecast_offset = 2







Never confuse these.











\\==================================================



FORECAST EXAMPLES



\\==================================================







"What will revenue be next month?"







query_type = "forecast"



operation = "forecast"



prediction_type = "revenue"



horizon = 1



forecast_offset = null







"What will revenue be 2 months after?"







query_type = "forecast"



operation = "forecast"



prediction_type = "revenue"



horizon = 1



forecast_offset = 2







"What will revenue be 3 months after?"







query_type = "forecast"



operation = "forecast"



prediction_type = "revenue"



horizon = 1



forecast_offset = 3







"What will orders be 2 months after?"







query_type = "forecast"



operation = "forecast"



prediction_type = "orders"



horizon = 1



forecast_offset = 2







"What will customer count be 3 months after?"







query_type = "forecast"



operation = "forecast"



prediction_type = "customers"



horizon = 1



forecast_offset = 3







"What will revenue be for the next 2 months?"







query_type = "forecast"



operation = "forecast"



prediction_type = "revenue"



horizon = 2



forecast_offset = null







"What will revenue be for the next 4 months?"







query_type = "forecast"



operation = "forecast"



prediction_type = "revenue"



horizon = 4



forecast_offset = null







If the user asks for a forecast without specifying a horizon:







horizon = 4



forecast_offset = null







Never use:







horizon > 4







forecast_offset > 4











\\==================================================



FORECAST MONTH QUESTIONS



\\==================================================







Use:







query_type = "forecast"



operation = "forecast_month"







when the user asks for the month, year, date, or time period associated



with a future forecast point.







Examples:







"What month will be 2 months after?"







prediction_type = null



horizon = 1



forecast_offset = 2







"What is the month and year 2 months after?"







prediction_type = null



horizon = 1



forecast_offset = 2







"What month will the revenue forecast be 2 months after?"







prediction_type = "revenue"



horizon = 1



forecast_offset = 2







"What month is the next revenue forecast?"







prediction_type = "revenue"



horizon = 1



forecast_offset = 1







"What is the date of the third forecast month?"







prediction_type = null



horizon = 1



forecast_offset = 3







A future month, year, or date question does not require a numeric dataset field.







Never use sum, average, min, max, group_by, or top_n for these questions.







Never select a date column as a numeric field.







The forecast backend determines the actual month and year.











\\==================================================



FORECAST TOTAL



\\==================================================







Use:







operation = "forecast_total"







when the user asks for the total across multiple forecast months.







Example:







"What is the total predicted revenue for the next 4 months?"







query_type = "forecast"



operation = "forecast_total"



prediction_type = "revenue"



horizon = 4



forecast_offset = null







For:







"What is the total revenue 2 months after?"







this means one specific forecast point.







Use:







operation = "forecast"



horizon = 1



forecast_offset = 2







Do not use forecast_total for a single forecast point.











\\==================================================



FORECAST AVERAGE



\\==================================================







Use:







operation = "forecast_average"







when the user asks for the average across multiple forecast months.







Example:







"What is the average predicted revenue for the next 4 months?"







query_type = "forecast"



operation = "forecast_average"



prediction_type = "revenue"



horizon = 4



forecast_offset = null











\\==================================================



FORECAST MINIMUM AND MAXIMUM



\\==================================================







Use:







operation = "forecast_min"







for the minimum predicted value across a forecast range.







Use:







operation = "forecast_max"







for the maximum predicted value across a forecast range.







Example:







"What is the minimum predicted revenue for the next 4 months?"







query_type = "forecast"



operation = "forecast_min"



prediction_type = "revenue"



horizon = 4



forecast_offset = null







"What is the maximum predicted revenue for the next 4 months?"







query_type = "forecast"



operation = "forecast_max"



prediction_type = "revenue"



horizon = 4



forecast_offset = null







If minimum or maximum refers to one specific forecast point, use:







operation = "forecast"



forecast_offset = N











\\==================================================



HIGHEST AND LOWEST FORECAST MONTH



\\==================================================







Use:







operation = "forecast_highest_month"







when the user asks which future month has the highest predicted value.







Use:







operation = "forecast_lowest_month"







when the user asks which future month has the lowest predicted value.







Example:







"Which future month has the highest predicted revenue?"







query_type = "forecast"



operation = "forecast_highest_month"



prediction_type = "revenue"



horizon = 4



forecast_offset = null







"Which future month has the lowest predicted revenue?"







query_type = "forecast"



operation = "forecast_lowest_month"



prediction_type = "revenue"



horizon = 4



forecast_offset = null











\\==================================================



4\\. rag_tool



\\==================================================







Use rag_tool when the user explicitly wants information from an uploaded:







\\- PDF



\\- report



\\- document



\\- documentation



\\- knowledge document



\\- knowledge base







Examples:







"What does the uploaded PDF say about this dataset?"







"What is the purpose of this dataset according to the document?"







"What information is mentioned about customer satisfaction?"







"What does the knowledge document say about missing values?"







"Explain the business use of this dataset from the uploaded document."







"According to the uploaded report, what are the important fields?"







"Tell me about this dataset according to the PDF."







"Explain the information given in the uploaded document."







Use:







query_type = "rag"



operation = "knowledge_search"



visualization = "text"







For RAG:







prediction_type = null



field = null



group_by = null



filters = []



limit = null



sort = null



row_number = null



column_number = null



horizon = null



forecast_offset = null



model_name = null



direct_answer = null



direct_result = null







The original user question will be passed to the retrieval system.







The retrieval system searches knowledge documents belonging to the authenticated



user and selected dataset.







Do not invent information that is not present in the retrieved document.











\\==================================================



5\\. general_tool



\\==================================================







Use general_tool for questions that are NOT related to BusinessPulse.







A question is general when it is unrelated to:







\\- the selected dataset



\\- dataset structure



\\- dataset values



\\- dataset metadata



\\- historical dataset analytics



\\- business calculations



\\- business insights



\\- future forecasts



\\- uploaded PDFs



\\- uploaded reports



\\- uploaded documentation



\\- uploaded knowledge documents



\\- the BusinessPulse knowledge base







Examples:







"Hi"







"Hello"







"Hey"







"How are you?"







"What's your name?"







"Who are you?"







"Tell me a joke"







"Tell me a story"







"What is Python?"







"What is Java?"







"What is C++?"







"What is 2 + 2?"







"Who is Elon Musk?"







"What is the capital of India?"







"What's the weather?"







"Write some code"







"Help me with my homework"







"I am bored"







"Good morning"







"Good night"







"Thanks"







"Thank you"







For ALL unrelated questions use exactly:







tool = "general_tool"







query_type = "general"







operation = "general"







visualization = "text"







field = null







group_by = null







filters = []







limit = null







sort = null







direct_answer = null







direct_result = null







row_number = null







column_number = null







prediction_type = null







horizon = null







forecast_offset = null







model_name = null







Do NOT send general questions to metadata_tool.







Do NOT send general questions to analytics_tool.







Do NOT send general questions to forecast_tool.







Do NOT send general questions to rag_tool.







Only use a BusinessPulse dataset tool when the question clearly refers to the



selected dataset, its historical data, its structure, its values, its



business calculations, its forecasts, or its uploaded knowledge documents.







Otherwise use general_tool.











\\==================================================



FILTERS



\\==================================================







For analytics questions, use filters when the user specifies conditions.







Supported operators:







\\- eq



\\- neq



\\- gt



\\- gte



\\- lt



\\- lte



\\- contains



\\- in







Only use fields that actually exist in the dataset.







If no filters are needed:







filters = []











\\==================================================



VISUALIZATION



\\==================================================







Use "text" for a simple direct answer.







Use "kpi" for one important aggregate value.







Use "table" for:







\\- columns



\\- multiple values



\\- grouped results



\\- multiple forecast months



\\- unique values







Use "chart" when the user explicitly asks for:







\\- a chart



\\- a graph



\\- a trend



\\- a visual comparison







For forecast_month:







visualization = "text"







For a single forecast point:







visualization = "text"







For multiple forecast months:







visualization = "table"







For rag_tool:







visualization = "text"







For highest_average:







visualization = "text"







For lowest_average:







visualization = "text"







For general_tool:







visualization = "text"







Do not use a chart when a simple answer is sufficient.











\\==================================================



FIELD SELECTION



\\==================================================







Use exact dataset column names.







Never invent column names.







If the user uses a natural-language concept such as:







"revenue"



"sales"



"order value"



"payment amount"







map it to the closest appropriate actual dataset column when the mapping is



clear.







For highest_average and lowest_average:







field = null







because the backend compares all numeric columns.







For average, sum, min, and max:







field must identify the specific numeric column.











\\==================================================



DIRECT ANSWERS



\\==================================================







direct_answer and direct_result are helper fields.







For metadata, analytics, forecast, and RAG queries:







direct_answer = null







direct_result = null







Do not use these fields instead of executing the selected backend tool.







For general_tool:







direct_answer = null







direct_result = null











\\==================================================



FINAL RULES



\\==================================================







1\\. Return exactly one AIAgentPlan.







2\\. Choose exactly one backend tool.







3\\. Include exactly one AnalyticsQuery.







4\\. Every schema field must be present.







5\\. Use null for irrelevant optional fields.







6\\. Use [] for filters when there are no filters.







7\\. Do not calculate numeric results yourself.







8\\. Do not invent dataset values.







9\\. Do not invent column names.







10\\. Only use operations defined in the AnalyticsQuery schema.







11\\. Metadata questions use metadata_tool.







12\\. Historical calculations use analytics_tool.







13\\. Future predictions and future date or month questions use forecast_tool.







14\\. Explicit questions about uploaded PDFs, reports, documentation,



    knowledge documents, or knowledge bases use rag_tool.







15\\. Questions unrelated to the selected dataset, BusinessPulse analytics,



    forecasting, or uploaded knowledge documents use general_tool.







16\\. RAG questions use:







    query_type = "rag"



    operation = "knowledge_search"



    visualization = "text"







17\\. General questions use:







    query_type = "general"



    operation = "general"



    visualization = "text"







18\\. Do not use rag_tool for direct dataframe questions such as columns,



    rows, data types, missing values, or raw cells.







19\\. Do not use metadata_tool, analytics_tool, or forecast_tool when the user



    explicitly asks what an uploaded document or PDF says.







20\\. Row and column positions are 1-based.







21\\. Forecast horizon cannot exceed 4.







22\\. Forecast offset cannot exceed 4.







23\\. "N months after" means:







    horizon = 1



    forecast_offset = N







24\\. "next N months" means:







    horizon = N



    forecast_offset = null







25\\. Never aggregate a date column just because the user asks for a future



    month or year.







26\\. Do not explain your reasoning.







27\\. Return only the structured AIAgentPlan object.



"""


def generate_agent_plan(
    question: str,
    df: pd.DataFrame,
) -> AIAgentPlan:

    start_time = time.perf_counter()

    schema_context = _build_schema_context(df)

    system_prompt = _build_agent_prompt(schema_context)

    # Ask the model for a strict structured agent plan

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ai_agent_plan",
                "strict": True,
                "schema": _build_strict_agent_schema(),
            },
        },
    )

    planner_time = time.perf_counter() - start_time

    print(f"[AI TIMING] Planner: {planner_time:.2f}s")

    # Read the structured JSON returned by the agent

    content = response.choices[0].message.content

    if not content:

        raise ValueError("The AI Agent returned an empty response.")

    try:

        # Convert the model response from JSON text into a Python object

        parsed = json.loads(content)

    except json.JSONDecodeError as exc:

        raise ValueError("The AI Agent returned invalid JSON.") from exc

    # Validate the complete plan against the Pydantic schema

    return AIAgentPlan.model_validate(parsed)


def generate_analytics_query(
    question: str,
    df: pd.DataFrame,
) -> AnalyticsQuery:

    # Keep the older function available for existing code

    plan = generate_agent_plan(
        question,
        df,
    )

    return plan.query


def _get_result_data(result):
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _format_value(value):
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,}"
    return str(value)


def _deterministic_answer(query: AnalyticsQuery, result):
    data = _get_result_data(result)

    if data is None:
        return None

    if query.query_type == "metadata":
        if query.operation == "row_count":
            return f"There are {_format_value(data)} rows in the dataset."

        if query.operation == "columns":
            if isinstance(data, list):
                return f"The dataset has {len(data):,} columns."
            return None

        if query.operation == "column_name" and isinstance(data, dict):
            position = data.get("position")
            name = data.get("name")
            dtype = data.get("dtype")

            if position is not None and name is not None:
                if dtype:
                    return (
                        f"Column {position} is '{name}' and its data type is {dtype}."
                    )
                return f"Column {position} is '{name}'."

        if query.operation == "cell_value" and isinstance(data, dict):
            row_number = data.get("row_number")
            column_number = data.get("column_number")
            value = data.get("value")

            if row_number is not None and column_number is not None:
                return (
                    f"The value at row {row_number}, column "
                    f"{column_number} is {_format_value(value)}."
                )

        if query.operation == "missing_values":
            if isinstance(data, dict):
                total_missing = data.get("total_missing")
                if total_missing is not None:
                    return (
                        f"There are {_format_value(total_missing)} missing values "
                        f"in the dataset."
                    )

        return None

    if query.query_type == "analytics":
        if query.operation == "count":
            if query.field:
                return (
                    f"There are {_format_value(data)} non-empty values "
                    f"in '{query.field}'."
                )
            return f"There are {_format_value(data)} records in the dataset."

        if query.operation == "sum" and query.field:
            return f"The total {query.field} is {_format_value(data)}."

        if query.operation == "average" and query.field:
            return f"The average {query.field} is {_format_value(data)}."

        if query.operation == "min" and query.field:
            return f"The minimum {query.field} is {_format_value(data)}."

        if query.operation == "max" and query.field:
            return f"The maximum {query.field} is {_format_value(data)}."

        if query.operation in {"highest_average", "lowest_average"}:
            if isinstance(data, dict):
                column = data.get("column")
                average = data.get("average")

                if column is not None and average is not None:
                    if query.operation == "highest_average":
                        return (
                            f"'{column}' has the highest average, "
                            f"at {_format_value(average)}."
                        )

                    return (
                        f"'{column}' has the lowest average, "
                        f"at {_format_value(average)}."
                    )

        if query.operation in {"group_by", "top_n"} and isinstance(data, list):
            if not data:
                return "No matching results were found."

            group_field = query.group_by or "category"
            value_field = query.field or "value"

            lines = []
            for item in data:
                if not isinstance(item, dict):
                    continue

                group_value = item.get(group_field)
                metric_value = item.get(value_field)

                if group_value is not None and metric_value is not None:
                    lines.append(f"{group_value}: {_format_value(metric_value)}")

            if lines:
                if query.operation == "top_n":
                    return "Top results:\n" + "\n".join(lines)
                return "Results:\n" + "\n".join(lines)

    if query.query_type == "forecast" and isinstance(data, dict):
        prediction_type = data.get("prediction_type") or "value"

        if query.operation == "forecast_month":
            month = data.get("month")
            if month:
                return f"The forecast month is {month}."

        if query.operation == "forecast_total":
            total = data.get("total")
            if total is not None:
                return (
                    f"The total predicted {prediction_type} is "
                    f"{_format_value(total)}."
                )

        if query.operation == "forecast_average":
            average = data.get("average")
            if average is not None:
                return (
                    f"The average predicted {prediction_type} is "
                    f"{_format_value(average)}."
                )

        if query.operation in {"forecast_min", "forecast_max"}:
            value = data.get("value")
            month = data.get("month")

            if value is not None:
                label = "minimum" if query.operation == "forecast_min" else "maximum"
                answer = (
                    f"The {label} predicted {prediction_type} is "
                    f"{_format_value(value)}"
                )
                if month:
                    answer += f" in {month}"
                return answer + "."

        if query.operation in {
            "forecast_highest_month",
            "forecast_lowest_month",
        }:
            month = data.get("month")
            value = data.get("value")

            if month:
                label = (
                    "highest"
                    if query.operation == "forecast_highest_month"
                    else "lowest"
                )
                answer = f"{month} has the {label} predicted {prediction_type}"
                if value is not None:
                    answer += f" of {_format_value(value)}"
                return answer + "."

        if query.operation == "forecast":
            predicted = data.get("predicted")

            if isinstance(predicted, list) and predicted:
                points = []

                for point in predicted:
                    if not isinstance(point, dict):
                        continue

                    month = point.get("month")
                    value = point.get("value")

                    if month is not None and value is not None:
                        points.append(f"{month}: {_format_value(value)}")

                if len(points) == 1:
                    return (
                        f"The predicted {prediction_type} for "
                        f"{points[0].replace(':', ' is', 1)}."
                    )

                if points:
                    return f"Predicted {prediction_type}:\n" + "\n".join(points)

    return None


def generate_final_answer(
    question: str,
    query: AnalyticsQuery,
    result,
) -> str:

    start_time = time.perf_counter()
    deterministic_answer = _deterministic_answer(query, result)

    if deterministic_answer is not None:
        return deterministic_answer

    result_context = json.dumps(
        result,
        ensure_ascii=False,
        default=str,
    )

    if query.query_type == "general":
        system_prompt = """
You are a general-purpose AI assistant.

Answer the user's question directly using your general knowledge.

Rules:
1. Do not mention BusinessPulse, datasets, backend tools, query planners, or internal processing.
2. Do not pretend the question is a BusinessPulse analytics question.
3. Answer the actual question, not a different question.
4. Be concise, clear, and natural.
5. For definitions, explain the concept simply.
6. For programming questions, give technically correct explanations.
7. For calculations, calculate the answer correctly.
8. If the user asks for code, provide useful code and a short explanation when appropriate.
9. Never output a BusinessPulse greeting as the answer to a general question.
"""

        user_prompt = f"""
User question:
{question}

Return only the final natural-language answer.
"""
    else:
        system_prompt = """
You are the final answer generator for BusinessPulse AI Analytics.

Answer the user's question using ONLY the result supplied by the BusinessPulse backend.

For analytics and forecast questions, the result was calculated by the backend.
For RAG questions, the result contains information retrieved from uploaded knowledge documents.

Rules:
1. Never invent numbers.
2. Never modify numbers.
3. Never perform a new calculation that is not directly represented in the supplied result.
4. Do not repeat the user's question.
5. Do not mention the LLM, query planner, prompts, or internal processing.
6. Keep the answer concise and natural.
7. For multiple values, present them clearly.
8. For grouped results, preserve every supplied category and value without changing them.
9. For forecast results, preserve the supplied month and value exactly.
10. For forecast_month, answer only with the month, year, or date supplied by the backend.
11. For RAG results, answer only from the retrieved knowledge.
12. If the retrieved knowledge is insufficient, say so clearly.
13. If the result is empty or null, say that no matching information was found.
14. Never replace a backend value with an estimated or remembered value.
"""

        user_prompt = f"""
User question:
{question}

Structured query:
{query.model_dump_json()}

Backend result:
{result_context}

Return only the final natural-language answer.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    final_answer_time = time.perf_counter() - start_time

    print(f"[AI TIMING] Final answer: {final_answer_time:.2f}s")

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("The AI answer generator returned an empty response.")

    return answer.strip()
