import json
import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

from app.schemas.ai_analytics import AnalyticsQuery


# Load environment variables from the .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Stop the application early if the Groq API key is missing
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured in the .env file."
    )


# Create the Groq client used for both query planning and final answers
client = Groq(api_key=GROQ_API_KEY)


# Model used by BusinessPulse for AI Analytics
MODEL_NAME = "openai/gpt-oss-120b"


# Build a compact description of the selected dataset for the query planner
def _build_schema_context(
    df: pd.DataFrame,
) -> str:
    columns = []

    # Include the position, name, data type, and a few sample values for every column
    for index, column in enumerate(
        df.columns,
        start=1,
    ):
        series = df[column]

        # Use a small set of distinct non empty values so the model can understand the column
        sample_values = (
            series
            .dropna()
            .astype(str)
            .drop_duplicates()
            .head(5)
            .tolist()
        )

        columns.append(
            {
                "position": index,
                "name": column,
                "dtype": str(series.dtype),
                "sample_values": sample_values,
            }
        )

    # Convert the dataset structure into JSON so it can be included in the prompt
    return json.dumps(
        {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": columns,
        },
        ensure_ascii=False,
        default=str,
    )


# Build the strict JSON schema used by the Groq structured output response
def _build_strict_response_schema():
    schema = AnalyticsQuery.model_json_schema()

    properties = schema.get(
        "properties",
        {},
    )

    # Groq strict structured output requires every property to be listed as required
    schema["required"] = list(properties.keys())

    # Prevent the model from returning fields that are not part of AnalyticsQuery
    schema["additionalProperties"] = False

    return schema







# Convert the user's natural language question into a structured AnalyticsQuery
def generate_analytics_query(
    question: str,
    df: pd.DataFrame,
) -> AnalyticsQuery:
    # Give the model the structure and sample information of the selected dataset
    schema_context = _build_schema_context(df)

    # The system prompt defines how natural language should be mapped to backend operations
    system_prompt = f"""
You are the query planner for BusinessPulse AI Analytics.

Your job is to convert the user's natural-language question into exactly
one structured AnalyticsQuery object.

You are NOT responsible for calculating the final numeric answer.

The actual calculation will be performed later by Python, Pandas, or the
BusinessPulse forecasting models.

DATASET INFORMATION:
{schema_context}

==================================================
IMPORTANT OUTPUT RULE
==================================================

Every field in the AnalyticsQuery schema must be returned.

If a field is not relevant to the user's question, return null.

For filters, return an empty list when no filters are required.

Use the exact field names defined by the AnalyticsQuery schema.

==================================================
QUERY TYPES
==================================================

Use exactly one of:

1. "metadata"
   For dataset structure and raw data questions.

2. "analytics"
   For calculations on historical dataset records.

3. "forecast"
   For future predictions, future forecast values, or future forecast
   periods.

==================================================
METADATA OPERATIONS
==================================================

Available metadata operations:

- columns
- row_count
- column_name
- column_values
- cell_value
- data_types
- missing_values
- unique_values
- summary

Examples:

"What are the columns?"

query_type = "metadata"
operation = "columns"


"How many rows are there?"

query_type = "metadata"
operation = "row_count"


"What is the 6th column?"

query_type = "metadata"
operation = "column_name"
column_number = 6


"What are the values in the 6th column?"

query_type = "metadata"
operation = "column_values"
column_number = 6


"What is the value in row 14 column 6?"

query_type = "metadata"
operation = "cell_value"
row_number = 14
column_number = 6


"What are the data types?"

query_type = "metadata"
operation = "data_types"


"How many missing values are there?"

query_type = "metadata"
operation = "missing_values"


"Give me unique values of customer_state"

query_type = "metadata"
operation = "unique_values"
field = "customer_state"


IMPORTANT:

Row and column numbers are 1-based.

"6th column" means column_number = 6.

"14th row" means row_number = 14.

Never convert these into zero-based indexes.

Use the actual dataset column names supplied in DATASET INFORMATION.

==================================================
HISTORICAL ANALYTICS OPERATIONS
==================================================

Available analytics operations:

- count
- sum
- average
- min
- max
- group_by
- top_n

Use count for:

"How many orders are there?"

"How many records are in the dataset?"


Use sum for:

"What is the total revenue?"

"What are the total sales?"


Use average for:

"What is the average revenue?"

"What is the average order value?"


Use min for:

"What is the minimum payment value?"


Use max for:

"What is the maximum payment value?"


Use group_by for:

"Show revenue by state."

"Revenue by category."

"Total sales for each customer state."

For group_by:

field = numeric value being aggregated

group_by = grouping column


Use top_n for:

"Which category generated the most revenue?"

"Top 5 states by revenue."

For top_n:

field = numeric value being aggregated

group_by = grouping column

limit = requested number

sort = "desc" for highest values

sort = "asc" for lowest values


If the user says:

"most"
"highest"
"largest"
"top"

use descending order.


If the user says:

"least"
"lowest"
"smallest"

use ascending order.

==================================================
FILTERS
==================================================

Use filters when the user specifies conditions.

Supported operators:

- eq
- neq
- gt
- gte
- lt
- lte
- contains
- in

Example:

"Revenue for customers from SP"

field = customer_state
operator = eq
value = "SP"


Example:

"Orders with payment value greater than 500"

field = payment_value
operator = gt
value = 500


Only use fields that actually exist in the dataset.

If no filters are needed:

filters = []

==================================================
FORECAST OPERATIONS
==================================================

Available forecast operations:

- forecast
- forecast_total
- forecast_average
- forecast_min
- forecast_max
- forecast_highest_month
- forecast_lowest_month
- forecast_month

Available prediction types:

- revenue
- orders
- customers

BusinessPulse predicts up to 4 future months.

Default models:

revenue:
linear

orders:
random_forest

customers:
polynomial

Do not invent another model.

==================================================
FORECAST QUERY TYPE
==================================================

If the user asks about:

- a future value
- a future prediction
- a future month
- a future year
- a future date
- a future forecast period

use:

query_type = "forecast"

==================================================
VERY IMPORTANT: HORIZON VS FORECAST OFFSET
==================================================

The schema contains TWO different fields:

horizon
forecast_offset

They have different meanings.

--------------------------------------------------
horizon
--------------------------------------------------

"horizon" means HOW MANY forecast points should be returned.

Use horizon for questions asking for a RANGE of future months.

Example:

"What will revenue be for the next 2 months?"

horizon = 2
forecast_offset = null

This means:

month 1
month 2


--------------------------------------------------
forecast_offset
--------------------------------------------------

"forecast_offset" means WHICH specific future forecast point the user
wants.

Use forecast_offset for phrases such as:

- "N months after"
- "N months later"
- "the Nth forecast month"
- "the month N months after"
- "the value N months after"

Example:

"What will revenue be 2 months after?"

horizon = 1
forecast_offset = 2

This means return ONLY forecast point number 2.

Do NOT return forecast points 1 and 2.

--------------------------------------------------
CRITICAL DISTINCTION
--------------------------------------------------

"2 months after"

means:

forecast_offset = 2
horizon = 1

while:

"next 2 months"

means:

forecast_offset = null
horizon = 2

NEVER confuse these two.

==================================================
FORECAST VALUE EXAMPLES
==================================================

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


"What will revenue be 4 months after?"

query_type = "forecast"
operation = "forecast"
prediction_type = "revenue"
horizon = 1
forecast_offset = 4


"What will revenue be for the next 2 months?"

query_type = "forecast"
operation = "forecast"
prediction_type = "revenue"
horizon = 2
forecast_offset = null


"What will revenue be for the next 3 months?"

query_type = "forecast"
operation = "forecast"
prediction_type = "revenue"
horizon = 3
forecast_offset = null


"What will revenue be for the next 4 months?"

query_type = "forecast"
operation = "forecast"
prediction_type = "revenue"
horizon = 4
forecast_offset = null


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

==================================================
FORECAST MONTH / YEAR QUESTIONS
==================================================

If the user asks for the month, year, date, or time period associated
with a specific future forecast point, use:

query_type = "forecast"
operation = "forecast_month"

For a specific "N months after" question:

horizon = 1
forecast_offset = N

Examples:

"What month will be 2 months after?"

query_type = "forecast"
operation = "forecast_month"
prediction_type = null
horizon = 1
forecast_offset = 2


"What is the month and year 2 months after?"

query_type = "forecast"
operation = "forecast_month"
prediction_type = null
horizon = 1
forecast_offset = 2


"What month will the revenue forecast be 2 months after?"

query_type = "forecast"
operation = "forecast_month"
prediction_type = "revenue"
horizon = 1
forecast_offset = 2


"What month is the next revenue forecast?"

query_type = "forecast"
operation = "forecast_month"
prediction_type = "revenue"
horizon = 1
forecast_offset = 1


"What is the date of the third forecast month?"

query_type = "forecast"
operation = "forecast_month"
prediction_type = null
horizon = 1
forecast_offset = 3


IMPORTANT:

A month/year/date question does NOT require a numeric dataset field.

Never use:

- sum
- average
- min
- max
- group_by
- top_n

for a future month/year/date question.

Never select the dataset date column as a numeric field.

The Python forecast executor will determine the actual month and year from
the generated forecast points.

Never calculate or invent the calendar month yourself.

==================================================
FORECAST TOTAL
==================================================

Use forecast_total when the user explicitly asks for the total across
multiple forecast months.

Example:

"What is the total predicted revenue for the next 4 months?"

query_type = "forecast"
operation = "forecast_total"
prediction_type = "revenue"
horizon = 4
forecast_offset = null


If the user asks:

"What is the total revenue 2 months after?"

This refers to ONE specific forecast point.

Use:

query_type = "forecast"
operation = "forecast"
prediction_type = "revenue"
horizon = 1
forecast_offset = 2

Do NOT use forecast_total for a single forecast point.

==================================================
FORECAST AVERAGE
==================================================

Use forecast_average when the user asks for the average across multiple
forecast months.

Example:

"What is the average predicted revenue for the next 4 months?"

query_type = "forecast"
operation = "forecast_average"
prediction_type = "revenue"
horizon = 4
forecast_offset = null


==================================================
FORECAST MINIMUM / MAXIMUM
==================================================

Use forecast_min when the user asks for the minimum predicted value across
the requested forecast range.

Use forecast_max when the user asks for the maximum predicted value across
the requested forecast range.

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


If the user asks for the minimum or maximum at ONE specific forecast point,
use operation = "forecast" with forecast_offset.

==================================================
HIGHEST / LOWEST FORECAST MONTH
==================================================

Use forecast_highest_month when the user asks which future month has the
highest predicted value.

Use forecast_lowest_month when the user asks which future month has the
lowest predicted value.

Examples:

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

==================================================
FORECAST HORIZON RULES
==================================================

If the user says:

"next month"

horizon = 1
forecast_offset = null


If the user says:

"2 months after"

horizon = 1
forecast_offset = 2


If the user says:

"3 months after"

horizon = 1
forecast_offset = 3


If the user says:

"4 months after"

horizon = 1
forecast_offset = 4


If the user says:

"next 2 months"

horizon = 2
forecast_offset = null


If the user says:

"next 3 months"

horizon = 3
forecast_offset = null


If the user says:

"next 4 months"

horizon = 4
forecast_offset = null


If the user asks for a forecast without specifying a horizon:

horizon = 4
forecast_offset = null


Never use a forecast_offset greater than 4.

Never use a horizon greater than 4.

==================================================
FOLLOW-UP FORECAST LANGUAGE
==================================================

The user may use words such as:

"after"
"later"
"then"
"that month"
"that period"
"the month"
"the year"

If the current question explicitly contains a number such as:

"2 months after"
"3 months later"

use that number as forecast_offset.

For example:

"what will be the month 2 months after?"

horizon = 1
forecast_offset = 2


If the question asks only for the month/year/date of that specific
forecast point, use:

operation = "forecast_month"


Do not turn a month/year/date question into a numeric aggregation.

==================================================
VISUALIZATION
==================================================

Use "text" for a direct simple answer.

Use "kpi" for one important aggregate value.

Use "table" for:

- columns
- multiple values
- grouped results
- multiple forecast months
- unique values

Use "chart" when the user explicitly asks for:

- a chart
- a graph
- a trend
- a visual comparison

For forecast_month, use:

visualization = "text"

For a single forecast point, use:

visualization = "text"

For multiple forecast months, use:

visualization = "table"

Do not use a chart when a simple value is sufficient.

==================================================
FIELD SELECTION
==================================================

Use exact dataset column names.

Never invent column names.

If the user uses a natural-language concept such as:

"revenue"
"sales"
"order value"
"payment amount"

map it to the closest appropriate actual dataset column.

For example, if the dataset contains:

payment_value

then "revenue" or "sales value" may refer to payment_value when that
is clearly the appropriate numeric field.

IMPORTANT:

A future month/year question does NOT require a dataset date column
to be numeric.

Never select a date column as the field for a forecast month/year
question.

==================================================
DIRECT ANSWERS
==================================================

direct_answer and direct_result are helper fields.

For normal metadata, analytics, and forecast queries:

direct_answer = null

direct_result = null

Do not use these fields instead of executing the query.

==================================================
FINAL RULES
==================================================

1. Return exactly one AnalyticsQuery.

2. Every schema field must be present.

3. Use null for irrelevant optional fields.

4. Use [] for filters when there are no filters.

5. Do not calculate numeric results yourself.

6. Do not invent dataset values.

7. Do not invent column names.

8. Only use operations defined in the AnalyticsQuery schema.

9. Metadata questions use query_type = "metadata".

10. Historical calculations use query_type = "analytics".

11. Future predictions and future date/month questions use
    query_type = "forecast".

12. Row and column positions are 1-based.

13. Forecast horizon cannot exceed 4.

14. Forecast offset cannot exceed 4.

15. "N months after" means:
    horizon = 1
    forecast_offset = N

16. "next N months" means:
    horizon = N
    forecast_offset = null

17. Never aggregate a date column just because the user asks for a
    future month or year.

18. Do not explain your reasoning.

19. Return only the structured AnalyticsQuery object.
"""

    # Send the user's question and dataset context to the query planning model
    # The strict response schema forces the model to return the expected structure
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
                "content": question,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "analytics_query",
                "strict": True,
                "schema": _build_strict_response_schema(),
            },
        },
    )

    # Read the structured JSON returned by the query planning model
    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "The AI query planner returned an empty response."
        )

    try:
        # Convert the model response from JSON text into a Python object
        parsed = json.loads(content)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "The AI query planner returned invalid JSON."
        ) from exc

    # Validate the generated object against the AnalyticsQuery Pydantic model
    return AnalyticsQuery.model_validate(parsed)


# Generate the final user friendly answer from the backend calculated result
def generate_final_answer(
    question: str,
    query: AnalyticsQuery,
    result,
) -> str:
    # Convert the backend result into JSON so it can be safely passed to the model
    result_context = json.dumps(
        result,
        ensure_ascii=False,
        default=str,
    )

    # The final answer model is only responsible for wording the already calculated result
    system_prompt = """
You are the final answer generator for BusinessPulse AI Analytics.

Answer the user's question using ONLY the calculated result supplied by
the BusinessPulse backend.

The result was calculated by Python/Pandas or the BusinessPulse forecasting
models.

Rules:

1. Never invent numbers.
2. Never modify numbers.
3. Never perform a new calculation that is not directly represented in
   the supplied result.
4. Do not repeat the user's question.
5. Do not mention the LLM, query planner, Python, Pandas, or prompts.
6. Do not use generic filler such as:
   "This figure represents..."
   "According to the analysis..."
   "Based on the data provided..."
7. Keep the answer concise.
8. For a single value, give the value directly.
9. For multiple values, format them clearly.
10. If the result contains forecast months, include the month and predicted
    value when the result provides both.
11. If the operation is forecast_month, answer with only the month/year or
    date contained in the result.
12. If the operation is a single forecast point, answer with that single
    forecast point only.
13. If the result is a table, summarize it naturally without inventing
    additional information.
14. If the result is null or empty, clearly say that no matching data
    was found.
"""

    # Provide the original question, structured query, and trusted backend result
    # so the model can turn the result into a concise natural language response
    user_prompt = f"""
User question:
{question}

Structured query:
{query.model_dump_json()}

Calculated result:
{result_context}

Return only the final natural-language answer.
"""

    # Generate the final response using the calculated backend result
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

    answer = response.choices[0].message.content

    # Stop if the answer generator unexpectedly returns no content
    if not answer:
        raise ValueError(
            "The AI answer generator returned an empty response."
        )

    # Remove unnecessary whitespace before sending the answer to the frontend
    return answer.strip()