# BusinessPulse

### Business Analytics & Forecasting Platform

BusinessPulse is a full-stack **business analytics, forecasting, and AI Analytics platform** that turns e-commerce and business data into actionable information. It combines historical analytics, KPI monitoring, data-quality checks, automated business insights, machine-learning forecasting, natural-language question answering, and Retrieval-Augmented Generation (RAG) over uploaded PDF knowledge documents.

The platform supports the built-in **Olist Brazilian E-Commerce dataset** as well as **user-uploaded CSV datasets**. Users can upload data, preview it, map source columns to standardized fields, save and select datasets, explore charts and KPIs, inspect common quality issues, generate forecasts, and ask questions about data through the AI Analytics interface.

The application uses **React, Vite, Tailwind CSS, Axios, Recharts, FastAPI, Python, Pandas, NumPy, Scikit-learn, MongoDB, GridFS, JWT authentication, the Groq API, and Sentence Transformers**. The backend is organized into routes, Pydantic schemas, services, repositories, utilities, database access, machine-learning modules, and AI/RAG services.

------------------------------------------------------------------------

## 🚀 Key Features

### 📊 Historical Analytics

Analyze historical business performance through interactive
visualizations.

-   Monthly revenue trends
-   Monthly order trends
-   Revenue by product category
-   Top-performing categories
-   Payment method distribution
-   Customers by state
-   Review score distribution
-   Product price distribution
-   Revenue vs. orders analysis
-   Correlation heatmap
-   Historical business trends
-   Interactive charts and tables

------------------------------------------------------------------------

### 📈 Current Dashboard

Monitor important business KPIs through a centralized dashboard.

#### Key Performance Indicators

-   Total Revenue
-   Total Orders
-   Total Customers
-   Total Products
-   Average Review Score
-   Average Payment Value
-   Top-Selling Category
-   Top Seller
-   Most Used Payment Method

#### Additional Insights

-   Recent orders
-   Top categories
-   Business performance summaries
-   Interactive KPI cards
-   Charts and data tables

------------------------------------------------------------------------

### 🧹 Data Quality

Review the selected dataset for common data-quality issues before
relying on its results.

-   Overall data quality score
-   Missing value checks
-   Duplicate row checks
-   Invalid date checks
-   Negative value checks
-   Column-level quality details
-   Quality status for each check
-   Dataset-specific quality analysis

------------------------------------------------------------------------

### 💡 Business Insights

BusinessPulse generates automated, human-readable observations from the
selected business dataset.

Insights can highlight:

-   Business performance patterns
-   Revenue trends
-   Order trends
-   Category performance
-   Customer-related patterns
-   Review-related observations
-   Important business changes
-   Dataset-aware business observations

------------------------------------------------------------------------

### 🤖 AI Analytics

Ask questions about a selected dataset in natural language instead of
manually writing queries.

-   Natural-language question answering for dataset metadata and
    business analytics
-   AI-based routing to the appropriate tool for each question
-   Metadata questions such as row counts, column names, data types, and
    missing values
-   Analytical operations such as sums, averages, counts, minimums,
    maximums, grouping, and top-performing values
-   Forecast questions routed to the forecasting service
-   Retrieval-Augmented Generation (RAG) over uploaded knowledge PDFs
-   General questions handled separately from dataset-specific queries
-   Final answers generated from backend results
-   Dataset-scoped knowledge retrieval
-   PDF text extraction, chunking, embeddings, and retrieval
-   Duplicate PDF upload protection for the selected dataset

#### AI Analytics Tool Routing

The AI Planner in `llm_service.py` selects the appropriate tool based on the user's question.

| Tool | Purpose | Example question |
|---|---|---|
| `metadata_tool` | Inspects dataset structure and values. | “How many rows are there?” |
| `analytics_tool` | Calculates metrics from existing data. | “What is the total revenue?” |
| `forecast_tool` | Requests future business predictions. | “Forecast revenue for the next few months.” |
| `rag_tool` | Retrieves relevant information from uploaded knowledge documents. | “What does this field mean according to my PDF?” |
| `general_tool` | Handles questions unrelated to the selected dataset. | “What is Python?” |

#### AI Analytics Request Flow

``` text
React AI Analytics page
        ↓
POST /ai-analytics/ask
        ↓
FastAPI route and dataset loading
        ↓
AI Planner selects a tool and creates a structured plan
        ↓
Backend executes the calculation, forecast, or retrieval
        ↓
Final answer generation
        ↓
Response displayed in the React interface
```

The LLM plans and routes the question; backend services perform data
calculations, forecasting, and knowledge retrieval. This separates
planning from execution and keeps numeric answers grounded in actual
backend operations.

#### AI Analytics Implementation Details

The AI Analytics page sends the selected `dataset_id` and user's question to `POST /ai-analytics/ask`. The FastAPI route authenticates the request, loads the selected dataset for the current user, asks the planner for a structured plan, executes the selected tool (except for the separate general-question path), and builds a response for the frontend.

**Planner and answer generation**

- `generate_agent_plan()` in `services/llm_service.py` interprets the question and produces a structured plan, rather than directly performing all numeric calculations.
- The plan is validated using Pydantic schemas and a structured JSON format before execution.
- `execute_agent_plan()` in `services/ai_query_service.py` dispatches the plan to the appropriate backend operation.
- `generate_final_answer()` turns the backend result into a natural-language answer for the user.
- The API response can include the question, parsed query/plan, answer, result, visualization type, and optional table/chart data for rendering in React.
- General questions are handled separately from dataset-specific execution.
- The route includes timing logs for dataset loading, tool execution, and total request duration, which help with debugging slow queries.

**Tool responsibilities**

| Tool | Role | Example |
|---|---|---|
| `metadata_tool` | Inspects dataset structure, row/column information, data types, values, and missing values. | “How many rows are there?” |
| `analytics_tool` | Computes dataset operations such as counts, sums, averages, minima/maxima, grouping, filters, and top-N results. | “What is the total revenue?” |
| `forecast_tool` | Routes a supported future-prediction question to the forecasting service. | “Forecast revenue for the next few months.” |
| `rag_tool` | Retrieves relevant text from PDF knowledge documents associated with the user and selected dataset. | “What does this field mean according to my document?” |
| `general_tool` | Handles general questions that do not need an operation on the selected dataset. | “What is Python?” |

The system is designed so that the LLM identifies intent and selects a tool, while deterministic backend code performs data calculations and existing ML services generate forecasts. For simple questions such as row counts, the implementation can return a deterministic answer without depending on a second LLM answer-generation call.

Key files:

- `frontend/src/pages/AIAnalytics.jsx` — question input, dataset selection, knowledge PDF upload, and answer display.
- `backend/app/routes/ai_analytics.py` — `POST /ai-analytics/ask` orchestration.
- `backend/app/services/llm_service.py` — structured plan generation and final answer generation.
- `backend/app/services/ai_query_service.py` — tool execution, analytics operations, forecasting/RAG dispatch, and result formatting.
- `backend/app/schemas/ai_analytics.py` — structured request, plan/query, and response models.
- `backend/app/routes/knowledge.py` and `backend/app/services/knowledge_service.py` — PDF knowledge ingestion.

#### Knowledge PDF Workflow

```text
PDF upload
    ↓
Knowledge API and service
    ↓
PDF text extraction and chunking
    ↓
Text embeddings
    ↓
PDF file and chunk metadata stored in MongoDB/GridFS
    ↓
Question-time retrieval of relevant chunks for the same user and dataset
    ↓
Relevant text passed to answer generation
```

The implementation accepts **PDF files**. It uses `pypdf` to extract selectable text, then normalizes whitespace and splits the text into **1,200-character chunks with 200 characters of overlap**. Embeddings are produced by Sentence Transformers using **`all-MiniLM-L6-v2`** with normalized embeddings. The PDF itself is stored in the MongoDB GridFS `knowledge_files` bucket; document metadata and text chunks with embeddings are stored in MongoDB collections.

At query time, the question is embedded using the same model. Retrieval only searches chunks associated with the authenticated user's `user_id` and selected `dataset_id`. Because the vectors are normalized, the implementation uses their dot product as cosine similarity, ranks matching chunks in application code, and returns the **top three** relevant chunks by default. Duplicate PDF contents are detected using a SHA-256 file hash within the same user/dataset scope.

Limitations to be aware of: scanned/image-only PDFs may not yield text because OCR is not part of this pipeline. The current retrieval code loads matching chunks from MongoDB and ranks them in Python; it does not use a dedicated MongoDB vector-search index.

------------------------------------------------------------------------

### 🌍 Multilingual Interface

The frontend is configured with `i18next` and `react-i18next` and includes locale files for:

- English (`en`)
- Hindi (`hi`)
- German (`de`)
- Spanish (`es`)
- French (`fr`)

The translation files provide a localization foundation for the interface. This is frontend localization; it does not mean uploaded dataset values or user-provided documents are automatically translated.

------------------------------------------------------------------------

### 👤 Profile

The profile area provides account and dataset information in one place.

-   User name and email
-   Account status
-   Uploaded dataset count
-   Currently selected dataset
-   Quick access to Dashboard
-   Quick access to Insights
-   Quick access to Dataset Management

------------------------------------------------------------------------

### 🔮 Forecast & Predictions

Predict future business performance and customer satisfaction using
multiple machine-learning models.

The forecast page offers three targets:

-   **Revenue** — monthly revenue totals.
-   **Orders** — monthly order counts.
-   **Customer satisfaction** — monthly average customer review score.

**Important implementation detail:** the API internally uses `prediction_type="customers"` for the third target, but the active frontend labels it **Customer Satisfaction Forecast** and describes it as the average review-score forecast. It should not be described as predicting the number of customers.

#### Machine Learning Models

-   Linear Regression
-   Polynomial Regression
-   Random Forest Regression

#### Forecasting Capabilities

-   User-selectable prediction target and regression model
-   Monthly historical series and four future monthly predictions
-   Historical-versus-predicted line chart
-   Selected model displayed with forecast results
-   Model performance cards for MAE, RMSE, and R²
-   Non-negative clipping for revenue/order-style forecasts
-   Customer-satisfaction predictions constrained to the 1–5 review-score range
-   Basic input check requiring at least two monthly observations

#### Evaluation Metrics

-   **Mean Absolute Error (MAE)** — average absolute difference between actual and fitted historical values.
-   **Root Mean Squared Error (RMSE)** — gives a larger penalty to larger prediction errors.
-   **R² Score** — coefficient of determination for the fitted historical series.

**Evaluation caveat:** the current model code calculates these metrics against predictions on the same historical observations used to fit the model. They are in-sample fit metrics, not metrics from an independent chronological test set. A holdout period or rolling time-series validation would be needed to estimate out-of-sample forecasting performance more reliably.

------------------------------------------------------------------------

## 📂 Custom Dataset Management

BusinessPulse is not limited to the built-in Olist dataset.

Users can upload their own CSV business or sales data and configure it
for analysis.

### Custom Dataset Workflow

``` text
Upload CSV
    ↓
Validate File
    ↓
Preview Dataset
    ↓
Map Columns
    ↓
Normalize Data
    ↓
Save Dataset
    ↓
Select Dataset
    ↓
Data Quality
    ↓
Historical Analytics
    ↓
Current KPIs
    ↓
Business Insights
    ↓
Forecasting
```

### Dataset Features

-   CSV file upload
-   File validation
-   Dataset preview
-   Column mapping
-   Data normalization
-   Dataset selection
-   Dataset deletion
-   Multiple uploaded datasets
-   User-specific dataset access
-   Built-in Olist dataset
-   Custom dataset analysis
-   Dataset-aware forecasting where the required normalized fields are available
-   Data quality analysis
-   Business insights
-   Use of the selected dataset in AI Analytics

Each authenticated user can access their own uploaded datasets.

------------------------------------------------------------------------

# 🏗️ System Architecture

BusinessPulse follows a layered full-stack architecture that separates
presentation, API handling, business logic, data access, persistence,
and machine learning.

``` text
                         ┌──────────────────────┐
                         │      React UI        │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                               Axios / API
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         │        Routes        │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      Services        │
                         │    Business Logic    │
                         └──────┬─────────┬─────┘
                                │         │
                    ┌───────────▼───┐ ┌──▼──────────────┐
                    │ Repositories  │ │ Machine         │
                    │  Data Access  │ │ Learning Models │
                    └───────┬───────┘ └─────────────────┘
                            │
                    ┌───────▼────────┐
                    │    MongoDB     │
                    │   Persistence  │
                    └────────────────┘

              CSV / Olist Data
                     │
                     ▼
              Data Processing
```

------------------------------------------------------------------------

# 🔄 Backend Architecture

The backend follows a modular layered architecture:

``` text
Client
  │
  ▼
Routes
  │
  ▼
Services
  │
  ├──────────────► Machine Learning
  │
  ▼
Repositories
  │
  ▼
Database / Data Sources
```

## Routes

The route layer handles HTTP requests and API endpoints.

``` text
routes/
├── auth.py
├── current.py
├── data_quality.py
├── dataset.py
├── forecast.py
├── historical.py
├── insights.py
├── ai_analytics.py
└── knowledge.py
```

Responsibilities:

-   Receive HTTP requests
-   Validate request data
-   Authenticate users
-   Invoke services
-   Return API responses

------------------------------------------------------------------------

## Services

The service layer contains business logic.

``` text
services/
├── auth_service.py
├── category_service.py
├── customer_service.py
├── data_quality_service.py
├── dataset_data_service.py
├── dataset_service.py
├── forecast_service.py
├── heatmap_service.py
├── insights_service.py
├── kpi_service.py
├── order_service.py
├── payment_service.py
├── price_service.py
├── revenue_service.py
└── review_service.py
```

Each service focuses on a specific business responsibility, improving
maintainability and separation of concerns.

------------------------------------------------------------------------

## Repositories

The repository layer isolates data-access operations from business
logic.

``` text
repositories/
├── dataset_repository.py
├── sales_repository.py
└── user_repository.py
```

Responsibilities include:

-   User data access
-   Dataset persistence
-   Dataset retrieval
-   Dataset deletion
-   Business data access

------------------------------------------------------------------------

## Schemas

Pydantic schemas provide structured request and response models.

They help provide:

-   Input validation
-   Response validation
-   Consistent API contracts
-   Structured data models
-   Type-safe request and response handling

------------------------------------------------------------------------

## Database

MongoDB is used for application-level persistence.

The database layer manages:

-   User records
-   Uploaded datasets
-   Dataset metadata
-   Normalized dataset information
-   User-specific dataset records

------------------------------------------------------------------------

# 🔐 Authentication & Authorization

BusinessPulse implements JWT-based authentication and protected
resources.

### Authentication Features

-   User registration
-   User login
-   Password hashing
-   JWT access tokens
-   Authenticated API requests
-   Protected frontend routes
-   Protected backend routes

### Frontend Protection

``` text
ProtectedRoute.jsx
PublicRoute.jsx
```

Protected pages require authentication before access.

### Backend Protection

Protected FastAPI routes validate the authenticated user before allowing
access to application resources.

------------------------------------------------------------------------

# 🔑 JWT Authentication Flow

``` text
User
 │
 ▼
Login / Signup
 │
 ▼
Authentication API
 │
 ▼
JWT Token
 │
 ▼
Frontend
 │
 ▼
Axios Interceptor
 │
 ▼
Authorization: Bearer <JWT>
 │
 ▼
Protected FastAPI Route
 │
 ▼
Authentication Validation
 │
 ▼
Service Layer
```

The Axios interceptor automatically attaches the JWT access token to
protected API requests.

------------------------------------------------------------------------

# 🛡️ User Data Isolation

Uploaded datasets are associated with the authenticated user.

``` text
User A
 │
 ├── Dataset A1
 └── Dataset A2

User B
 │
 ├── Dataset B1
 └── Dataset B2
```

A user can only access, select, or delete datasets belonging to their
account.

This prevents unauthorized cross-user dataset access.

------------------------------------------------------------------------

# 🧠 Machine Learning Architecture

Forecasting logic is separated into a dedicated machine-learning module.

``` text
ml/
├── forecast_models.py
├── linear_forecast.py
├── polynomial_forecast.py
└── random_forest_forecast.py
```

The forecasting workflow is:

``` text
Forecast API
     │
     ▼
Forecast Service
     │
     ▼
Forecast Models
     │
     ├── Linear Regression
     ├── Polynomial Regression
     └── Random Forest Regression
```

------------------------------------------------------------------------

### Forecast Series and Model Behavior

The forecasting service prepares a monthly series before fitting a selected model:

| Forecast target | Built-in Olist series | Required normalized fields for custom CSVs |
|---|---|---|
| Revenue | Sum of item totals by order month (with fallback based on order timestamp and price where applicable). | `date` and `revenue` |
| Orders | Number of unique orders by purchase month. | `date` and `orders` |
| Customer satisfaction | Mean `review_score` by order purchase month. | `date` and `review_score` |

The active frontend lets the user select one of the three targets and one of the three models: `linear`, `polynomial`, and `random_forest`. All three models can be used for a selected target.

The models use the sequential monthly position as the predictor input. Linear Regression fits a straight-line trend. Polynomial Regression expands the input with a degree-two polynomial feature before fitting Linear Regression. Random Forest Regression uses `RandomForestRegressor` with 100 trees and `random_state=42`. Each generates the next four monthly predictions. The code clips negative forecast outputs to zero and additionally constrains customer-satisfaction predictions to the review-score scale of 1 to 5.

The reported metrics are computed on fitted historical values. They are useful for understanding in-sample fit, but because no separate chronological test set is used by this code path, they should not be represented as independent out-of-sample forecast accuracy.

------------------------------------------------------------------------

## Linear Regression

Used for modeling approximately linear historical business trends and generating future predictions.

------------------------------------------------------------------------

## Polynomial Regression

Used to model non-linear relationships in historical business trends.

------------------------------------------------------------------------

## Random Forest Regression

Used to model more complex non-linear relationships and business
patterns.

------------------------------------------------------------------------

# 🗃️ Data Sources

BusinessPulse supports:

### Built-in Dataset

The platform includes the **Olist Brazilian E-Commerce Public Dataset**.

The dataset contains information related to:

-   Customers
-   Orders
-   Order Items
-   Payments
-   Products
-   Reviews
-   Sellers

### Custom Dataset

Users can upload their own CSV files and map their columns to
BusinessPulse fields.

------------------------------------------------------------------------

# ⚙️ Data Processing Pipeline

``` text
CSV Dataset
     │
     ▼
File Validation
     │
     ▼
Dataset Preview
     │
     ▼
Column Mapping
     │
     ▼
Data Normalization
     │
     ▼
Data Quality Analysis
     │
     ▼
Business Metrics
     │
     ├── Historical Analytics
     ├── Current KPIs
     └── Forecasting
```

The data-processing layer handles tasks such as:

-   Loading CSV data
-   Validating uploaded files
-   Mapping user-defined columns
-   Renaming fields into standardized fields
-   Data transformation
-   Data quality analysis
-   Preparing business metrics
-   Preparing business insights
-   Preparing forecasting data

------------------------------------------------------------------------

# 🌐 API Architecture

BusinessPulse exposes its functionality through REST APIs built using
FastAPI.

``` text
React Frontend
      │
      ▼
Axios API Client
      │
      ▼
FastAPI
      │
      ├── Authentication
      ├── Dataset Management
      ├── Historical Analytics
      ├── Current Dashboard
      └── Forecasting
             │
             ▼
          Services
```

------------------------------------------------------------------------

# 📚 API Documentation

FastAPI automatically generates API documentation using
**Swagger/OpenAPI**.

The documentation allows developers to:

-   View available endpoints
-   Inspect request parameters
-   Inspect response schemas
-   Test APIs directly
-   Understand API contracts

When the backend is running, open:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🖥️ Frontend Architecture

The frontend is developed using React with a component-based
architecture.

``` text
frontend/
└── src/
    ├── components/
    ├── pages/
    ├── services/
    ├── App.jsx
    ├── index.css
    └── main.jsx
```

### Reusable Components

The frontend contains reusable components for:

-   Navigation
-   Sidebar
-   Tabs
-   Page headers
-   Charts
-   Tables
-   KPI cards
-   Tooltips
-   Loaders
-   Route protection
-   Dataset mapping

This reduces duplication and improves maintainability.

------------------------------------------------------------------------

# 📄 Application Pages

### Home

Provides an overview of the BusinessPulse platform and its capabilities.

### Login

Handles user authentication.

### Signup

Allows users to create an account.

### Dataset

Provides:

-   Olist dataset selection
-   CSV upload
-   Dataset preview
-   Column mapping
-   Uploaded dataset management
-   Dataset selection
-   Dataset deletion

### Dashboard

Acts as the main analytics area.

It contains:

-   Historical Analytics
-   Current Dashboard
-   Forecast & Predictions

### Historical Analytics

Provides detailed analysis of historical business performance.

### Current Dashboard

Displays business KPIs, recent orders, categories, and operational
metrics.

### Data Quality

Reviews the selected dataset for missing values, duplicate rows, invalid
dates, negative values, and column-level quality issues.

### Business Insights

Provides automated business observations based on the selected dataset
and its performance metrics.

### Profile

Displays account information, uploaded dataset count, the currently
selected dataset, and quick access to key areas of the platform.

### AI Analytics

Provides a natural-language interface for asking dataset questions,
running backend analytics, requesting forecasts, and retrieving
information from uploaded knowledge PDFs. The AI Planner routes each
question to metadata, analytics, forecast, RAG, or general handling.

### Forecast Predictions

Displays machine-learning-based predictions for future business trends
and customer satisfaction.

------------------------------------------------------------------------

# 📊 Dashboard Visualizations

BusinessPulse uses interactive visualizations to make business data
easier to understand.

The platform includes:

-   Line charts
-   Bar charts
-   Pie charts
-   Scatter charts
-   Correlation heatmaps
-   KPI cards
-   Data tables
-   Historical vs. predicted charts
-   Data quality summaries
-   Business insight cards

------------------------------------------------------------------------

# 🧩 SOLID Principles

The backend is structured around the **SOLID principles** to improve
maintainability, modularity, and separation of responsibilities.

### Single Responsibility Principle

Each layer has a focused responsibility:

``` text
Routes        → HTTP/API handling
Services      → Business logic
Repositories  → Data access
Schemas       → Data validation
ML            → Forecasting
Utils         → Shared functionality
Database      → Persistence
```

### Open/Closed Principle

New business services, endpoints, and forecasting models can be added
without significantly modifying unrelated modules.

### Liskov Substitution Principle

Forecasting components are structured so that different prediction
models can participate in the forecasting workflow.

### Interface Segregation Principle

The application is divided into focused modules rather than large,
tightly coupled interfaces.

### Dependency Inversion Principle

Business logic is separated from lower-level data-access and
implementation details through service and repository layers.

------------------------------------------------------------------------

# 🛡️ Error Handling

The backend provides centralized exception handling through:

``` text
app/exceptions.py
```

This helps maintain consistent API error responses and keeps business
logic separated from HTTP-specific error handling.

The frontend also provides user-facing notifications for operations such
as:

-   Dataset upload
-   Dataset deletion
-   Dataset selection
-   Column mapping
-   Authentication failures

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Frontend

-   React
-   Vite
-   React Router
-   Axios
-   Tailwind CSS
-   Recharts
-   Lucide React

## Backend

-   Python
-   FastAPI
-   Uvicorn
-   Pandas
-   NumPy
-   Pydantic
-   Scikit-Learn

## Database and File Storage

-   MongoDB
-   PyMongo asynchronous client
-   MongoDB GridFS for uploaded CSV and PDF file storage

## AI Analytics and RAG

-   Groq API
-   `openai/gpt-oss-20b` model
-   Structured LLM planning and tool routing
-   `pypdf` for PDF text extraction
-   Sentence Transformers with `all-MiniLM-L6-v2` embeddings
-   Application-level cosine-similarity ranking of document chunks

## Frontend Localization

-   `i18next`
-   `react-i18next`
-   Locale files for English, Hindi, German, Spanish, and French

## Authentication & Security

-   JWT
-   Password hashing
-   Authorization
-   Protected frontend routes
-   Protected backend routes
-   Axios interceptors
-   User-specific dataset access

## Machine Learning

-   Linear Regression
-   Polynomial Regression
-   Random Forest Regression
-   Mean Absolute Error (MAE)
-   Root Mean Squared Error (RMSE)
-   R² Score

## API Documentation

-   Swagger UI
-   OpenAPI

## Dataset

-   Olist Brazilian E-Commerce Public Dataset

------------------------------------------------------------------------

# 📁 Project Structure

The key project folders and implementation files are summarized below. Some helper or generated files are omitted for readability.

```text
BusinessPulse/
├── backend/
│   ├── app/
│   │   ├── data/                         # Built-in Olist CSV tables
│   │   ├── database/
│   │   │   └── mongodb.py                # MongoDB client, collections, GridFS buckets
│   │   ├── ml/
│   │   │   ├── forecast_models.py         # Monthly target-series preparation and metrics
│   │   │   ├── linear_forecast.py         # Linear Regression
│   │   │   ├── polynomial_forecast.py     # Polynomial Regression, degree 2
│   │   │   └── random_forest_forecast.py  # Random Forest Regression
│   │   ├── repositories/
│   │   │   ├── dataset_repository.py      # Dataset persistence and user-scoped access
│   │   │   ├── sales_repository.py        # Business/sales data access
│   │   │   └── user_repository.py         # User record access
│   │   ├── routes/
│   │   │   ├── auth.py                   # Signup/login
│   │   │   ├── dataset.py                # CSV upload, mapping and dataset management
│   │   │   ├── current.py                # Current KPI dashboard
│   │   │   ├── historical.py             # Historical analytics
│   │   │   ├── data_quality.py           # Quality checks
│   │   │   ├── insights.py               # Business insights
│   │   │   ├── forecast.py               # Forecast API endpoints
│   │   │   ├── ai_analytics.py           # Natural-language analytics endpoint
│   │   │   └── knowledge.py              # PDF knowledge-base endpoints
│   │   ├── schemas/                      # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── dataset_service.py
│   │   │   ├── dataset_data_service.py
│   │   │   ├── kpi_service.py
│   │   │   ├── data_quality_service.py
│   │   │   ├── insights_service.py
│   │   │   ├── forecast_service.py
│   │   │   ├── llm_service.py            # AI plan + final answer
│   │   │   ├── ai_query_service.py       # Executes planned AI operations
│   │   │   ├── knowledge_service.py      # PDF ingestion and duplicate detection
│   │   │   ├── pdf_processor.py          # PDF extraction and chunking
│   │   │   ├── embedding_service.py      # Sentence Transformer embeddings
│   │   │   └── retrieval_service.py     # User/dataset-scoped semantic retrieval
│   │   ├── utils/
│   │   │   ├── auth.py                   # Authenticated-user dependency
│   │   │   ├── security.py               # Password hashing and JWT functions
│   │   │   ├── data_loader.py            # Built-in/custom dataset loading
│   │   │   └── data_validation.py        # CSV/data validation helpers
│   │   ├── exceptions.py                 # Centralized API exception handling
│   │   └── main.py                       # FastAPI app and router registration
│   ├── requirements.txt
│   └── .env                              # Local secrets; do not commit
│
├── frontend/
│   ├── src/
│   │   ├── components/                   # Reusable charts, tables, cards, routes, UI
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Dataset.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CurrentDashboard.jsx
│   │   │   ├── HistoricalAnalytics.jsx
│   │   │   ├── DataQuality.jsx
│   │   │   ├── Insights.jsx
│   │   │   ├── ForecastPredictions.jsx
│   │   │   ├── AIAnalytics.jsx
│   │   │   └── Profile.jsx
│   │   ├── services/api.js               # Axios client and API functions
│   │   ├── locales/                      # English, Hindi, German, Spanish, French
│   │   ├── i18n.js                       # i18next configuration
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

------------------------------------------------------------------------

------------------------------------------------------------------------

# 🌐 Deployment

The deployment configuration documented for BusinessPulse is:

- **Frontend:** Vercel
- **Backend:** Render
- **Database and file storage:** MongoDB, including GridFS buckets
- **Source repository:** GitHub

For a deployed environment, configure backend secrets in the hosting provider's environment-variable settings. Configure the frontend's `VITE_API_URL` to point to the deployed backend and ensure the backend's CORS policy allows the deployed frontend origin. The Render service must be able to connect to the configured MongoDB database.

**Security:** never commit `.env` files, MongoDB connection strings, JWT secrets, or Groq API keys. Keep secrets in the local environment or hosting provider's secret configuration. If a credential has already been included in a shared archive or repository, rotate it.

------------------------------------------------------------------------

# 🚀 Installation & Setup

## Prerequisites

- Python compatible with the pinned backend dependencies
- Node.js and npm
- A MongoDB instance or MongoDB Atlas database
- A Groq API key for AI Analytics

## 1. Clone the repository

```bash
git clone https://github.com/Saurabh20-05/BusinessPulse.git
cd BusinessPulse
```

## 2. Configure backend environment variables

Create `backend/.env` locally. Use your own values; do not copy credentials from another environment or commit this file.

```dotenv
MONGODB_URL=your_mongodb_connection_string
MONGODB_DATABASE=businesspulse
JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GROQ_API_KEY=your_groq_api_key
```

The code reads `MONGODB_URL`, `GROQ_API_KEY`, and `JWT_SECRET_KEY`. `MONGODB_DATABASE` defaults to `businesspulse`; the JWT algorithm and token lifetime also have code defaults, but they may be set explicitly as shown.

## 3. Install and start the backend

```bash
cd backend
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install the backend dependencies and the multipart support used by file uploads:

```bash
python -m pip install -r requirements.txt
python -m pip install python-multipart
```

Then start FastAPI from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The local API runs at `http://127.0.0.1:8000` and Swagger UI is available at `http://127.0.0.1:8000/docs`.

**Dependency-file note for the supplied archive:** `backend/requirements.txt` is encoded as UTF-16 and does not list `python-multipart`. If pip reports null characters or malformed requirement lines, convert the file to UTF-8 before installing. The project dependencies also include `fastapi`, `uvicorn`, `python-dotenv`, `PyJWT`, `numpy`, `pandas`, `pwdlib[argon2]`, `pydantic`, `pymongo`, `scikit-learn`, `groq`, `pypdf`, and `sentence-transformers`.

## 4. Configure and start the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

The frontend uses `VITE_API_URL` for the backend base URL and falls back to `http://127.0.0.1:8000` if it is not configured. To set it explicitly, create `frontend/.env.local`:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

Start the Vite development server:

```bash
npm run dev
```

Open the local URL printed by Vite in the terminal.

------------------------------------------------------------------------

# 📚 API Documentation

FastAPI generates interactive API documentation from the registered routes and Pydantic models.

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **OpenAPI schema:** `http://127.0.0.1:8000/openapi.json`

The backend includes route groups for authentication, dataset management, current dashboard KPIs, historical analytics, data quality, business insights, forecasting, AI Analytics, and PDF knowledge documents. Swagger UI can be used to inspect endpoint contracts and manually try API requests during development.

------------------------------------------------------------------------

# 🔁 Complete Application Workflow

```text
User
 │
 ├── Signup / Login ──> Authentication API ──> JWT access token
 │                                             │
 │                                             ▼
 │                                      Axios bearer token
 │
 ▼
React frontend ──> FastAPI routes ──> authenticated user / selected dataset
                                       │
             ┌─────────────────────────┼──────────────────────────┐
             ▼                         ▼                          ▼
      Dataset management       KPI / historical analytics       Data quality
             │                         │                          │
             └─────────────────────────┼──────────────────────────┘
                                       ▼
                              Business insights / forecasting
                                       │
                                       ▼
                                 React visualizations

AI Analytics path:
Question -> planner -> structured tool plan -> backend calculation / forecast / RAG
         -> final-answer generation -> answer plus optional chart/table data

PDF RAG path:
PDF -> extracted text -> overlapping chunks -> embeddings -> MongoDB/GridFS
    -> retrieve top matching chunks for the user and dataset -> final answer
```

------------------------------------------------------------------------

# 🎯 Project Objective

BusinessPulse aims to provide one application where users can:

1. Analyze historical business performance.
2. Monitor key performance indicators.
3. Explore patterns across product categories, customers, reviews, payments, and time.
4. Upload and analyze custom CSV datasets.
5. Preview files and map incoming fields to standardized fields.
6. Inspect common data-quality issues before relying on analytics.
7. Generate dataset-aware business observations.
8. Forecast revenue, orders, and customer satisfaction.
9. Compare historical observations with future predictions.
10. Ask natural-language questions about a selected dataset through AI Analytics.
11. Ask document-grounded questions using uploaded PDF knowledge sources.
12. Access features through REST APIs.
13. Protect endpoints and scope user datasets/knowledge documents to the authenticated account.

------------------------------------------------------------------------

# ⭐ Key Engineering Highlights

### Full-stack development

- React and Vite frontend
- FastAPI REST API backend
- MongoDB and GridFS persistence
- Axios frontend/backend communication
- Interactive visualizations using Recharts

### Software architecture

- Route/service/repository separation
- Pydantic request and response schemas
- Dedicated machine-learning modules
- Reusable frontend components
- Shared utility functions
- Centralized backend exception handling

### Data engineering and analytics

- CSV ingestion and file validation
- Preview and column mapping
- Standardized field names and dataset selection
- Missing-value, duplicate-row, date, and negative-value checks
- KPI calculations, historical trends, category/payment/review analysis
- Data-aware business insights

### Machine learning

- Linear Regression
- Polynomial Regression (degree 2)
- Random Forest Regression
- Four-month monthly forecasts
- MAE, RMSE, and R² metrics
- Historical-versus-predicted charts

### AI and RAG

- Groq API using `openai/gpt-oss-20b`
- LLM-generated structured tool plans
- Metadata and analytical tool execution on backend data
- Forecasting tool routing
- PDF text extraction and overlapping chunking
- Sentence Transformer embeddings using `all-MiniLM-L6-v2`
- Similarity-based retrieval scoped by user and dataset
- Natural-language final-answer generation based on backend results

### Authentication and security

- Password hashing and verification
- JWT access tokens with expiration
- Protected frontend routes
- Protected backend endpoints
- Axios bearer-token interceptor
- User-scoped dataset and knowledge retrieval
- Environment-based secrets

------------------------------------------------------------------------

# ⚠️ Implementation Notes and Limitations

- **Custom CSV assumptions:** column mapping renames mapped fields; it does not infer units or prove that differently named columns have identical business meaning. Features need the expected standardized fields to be present.
- **Forecast input requirements:** at least two monthly observations are required. Custom revenue forecasting expects `date` and `revenue`; order forecasting expects `date` and `orders`; the customer-satisfaction forecast expects `date` and `review_score`.
- **Forecast target terminology:** the active UI calls the third target “Customer Satisfaction Forecast.” The API key remains `customers`, but for the built-in Olist data the series is the monthly mean `review_score`, not the number of customers.
- **Forecast evaluation:** current MAE, RMSE, and R² metrics are calculated on the fitted historical series. They should not be interpreted as independent test-set accuracy.
- **PDF text extraction:** the RAG pipeline extracts embedded/selectable PDF text. Scanned pages may not work because OCR is not part of the current pipeline.
- **RAG performance:** retrieval ranks the user's/dataset's stored chunks in application code. It is not backed by a dedicated MongoDB vector-search index.
- **AI dependency:** AI Analytics requires a working Groq API key and is affected by network availability, model service availability, prompt size, and API rate limits.
- **Automated testing:** a `backend/test_retrieval.py` helper is present in the supplied project. A comprehensive automated unit/integration test suite was not evident in the archive; validate local configuration and perform API/manual checks before treating a deployment as production-hardened.
- **Environment file:** do not commit `.env` or include real credentials in shared ZIP files. Rotate any credentials that have already been exposed.

------------------------------------------------------------------------

# 🔮 Potential Future Enhancements

Potential future improvements include:

- Chronological holdout or rolling evaluation for forecasting models
- Forecast model comparisons using a consistent validation window
- Automated model selection
- Advanced forecasting and anomaly-detection methods
- Cached or optimized LLM planning for faster AI Analytics responses
- Dedicated vector search for larger knowledge bases
- Expanded data-quality rules and downloadable quality reports
- Exportable analytics reports
- Additional built-in dataset templates
- More extensive automated unit and integration tests
- Role-based access control if multi-role permissions are needed

------------------------------------------------------------------------

# 📜 License

This project is intended for educational, portfolio, and learning purposes. Add or update a formal license file if you plan to distribute the source under a specific open-source license.
