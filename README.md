# BusinessPulse

BusinessPulse is a full-stack **Business Analytics & Forecasting Platform** built to transform e-commerce data into actionable business insights. It provides historical analysis, current KPI monitoring, and machine-learning-based forecasting through an interactive web dashboard.

The platform is built around a modular backend architecture with separate **routes, services, repositories, schemas, utilities, database, and machine-learning layers**, following clean-code and **SOLID principles**. It also includes JWT-based authentication and authorization, protected API routes, Axios interceptors, and automatically generated Swagger/OpenAPI documentation.

---

## Features

### 🏠 Home Page

* BusinessPulse platform overview
* Introduction to business analytics capabilities
* Navigation to analytics and forecasting modules
* Authentication-based access to protected features

---

## 📊 Historical Analytics

The Historical Analytics module analyzes past business performance using the Olist Brazilian E-commerce dataset.

It provides insights such as:

* Monthly revenue trends
* Monthly order trends
* Revenue by product category
* Top-performing categories
* Payment method distribution
* Customer distribution by state
* Review score distribution
* Product price distribution
* Revenue vs. orders comparison
* Correlation analysis
* Business performance trends over time
* Interactive charts and data tables

---

## 📈 Current Dashboard

The Current Dashboard provides a real-time-style summary of important business KPIs calculated from the available business data.

### Key Performance Indicators

* Total Revenue
* Total Orders
* Total Customers
* Total Products
* Average Review Score
* Average Payment Value
* Top-Selling Category
* Top Seller
* Most Used Payment Method

### Additional Information

* Recent orders
* Top categories
* Business performance summaries
* Interactive KPI cards
* Charts and tables for quick decision-making

---

## 🔮 Forecasting & Predictions

BusinessPulse includes a dedicated forecasting module for predicting future business performance.

Forecasting is available for:

* Revenue
* Orders
* Customers

The backend contains multiple forecasting models, including:

* Linear Regression
* Polynomial Regression
* Random Forest Regression

The forecasting module provides:

* Historical vs. predicted trends
* Future business projections
* Model-based predictions
* Forecast visualizations
* Model evaluation metrics

### Model Evaluation

Forecasting models can be evaluated using metrics such as:

* Mean Absolute Error (MAE)
* R² Score

---

# 🏗️ System Architecture

BusinessPulse follows a modular full-stack architecture separating the presentation, API, business logic, data-access, database, and machine-learning responsibilities.

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │     Frontend         │
                         └──────────┬───────────┘
                                    │
                              Axios / API
                                    │
                         ┌──────────▼───────────┐
                         │      FastAPI         │
                         │       Routes         │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │       Services       │
                         │   Business Logic     │
                         └──────┬─────────┬─────┘
                                │         │
                    ┌───────────▼───┐ ┌──▼──────────────┐
                    │ Repositories  │ │ Machine Learning│
                    │ Data Access   │ │ Forecast Models │
                    └───────┬───────┘ └─────────────────┘
                            │
                    ┌───────▼────────┐
                    │    Database     │
                    │    MongoDB      │
                    └─────────────────┘

              CSV Dataset ──► Data Processing
```

---

# 📁 Project Structure

```text
BusinessPulse/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── data/
│   │   │   ├── olist_customers.csv
│   │   │   ├── olist_order_items.csv
│   │   │   ├── olist_orders.csv
│   │   │   ├── olist_payments.csv
│   │   │   ├── olist_products.csv
│   │   │   ├── olist_reviews.csv
│   │   └── └── olist_sellers.csv
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── mongodb.py
│   │   │
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── forecast_models.py
│   │   │   ├── linear_forecast.py
│   │   │   ├── polynomial_forecast.py
│   │   │   └── random_forest_forecast.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── sales_repository.py
│   │   │   └── user_repository.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── current.py
│   │   │   ├── forecast.py
│   │   │   └── historical.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── category.py
│   │   │   ├── customer.py
│   │   │   ├── forecast.py
│   │   │   ├── heatmap.py
│   │   │   ├── kpi.py
│   │   │   ├── order.py
│   │   │   ├── payment.py
│   │   │   ├── price.py
│   │   │   ├── revenue.py
│   │   │   └── review.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── category_service.py
│   │   │   ├── customer_service.py
│   │   │   ├── forecast_service.py
│   │   │   ├── heatmap_service.py
│   │   │   ├── kpi_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── price_service.py
│   │   │   ├── revenue_service.py
│   │   │   └── review_service.py
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── data_loader.py
│   │   │   └── security.py
│   │   │
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── main.py
│   │
│   ├── .env
│   ├── .gitignore
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartCard.jsx
│   │   │   ├── CustomTooltip.jsx
│   │   │   ├── DataTable.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Loader.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── PageHeader.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   ├── PublicRoute.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   └── Tabs.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── CurrentDashboard.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ForecastPredictions.jsx
│   │   │   ├── HistoricalAnalytics.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Signup.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
└── README.md
```

---

# 🔄 Backend Architecture

The backend follows a layered architecture where each layer has a specific responsibility.

```text
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

### Routes

The `routes` layer handles HTTP requests and API endpoints.

Examples:

* `auth.py`
* `historical.py`
* `current.py`
* `forecast.py`

Routes are responsible for receiving requests, validating input, invoking the appropriate service, and returning responses.

### Services

The `services` layer contains the application's business logic.

Separate services are maintained for different business domains:

* Authentication
* Categories
* Customers
* Forecasting
* Heatmaps
* KPIs
* Orders
* Payments
* Prices
* Revenue
* Reviews

This separation keeps business logic modular and maintainable.

### Repositories

The repository layer handles data-access operations.

```text
repositories/
├── sales_repository.py
└── user_repository.py
```

Repositories separate data-access logic from the application's business logic.

### Schemas

The `schemas` layer defines structured request and response models for different API operations.

This helps provide:

* Input validation
* Response validation
* Consistent API contracts
* Type-safe data structures

### Database

BusinessPulse uses MongoDB for application data persistence.

```text
database/
└── mongodb.py
```

### Utilities

The utility layer contains reusable functionality such as:

* Authentication helpers
* Security utilities
* Data loading and preprocessing
* Common backend functionality

---

# 🔐 Authentication & Authorization

BusinessPulse implements authentication and authorization to protect application resources.

### Authentication

The authentication system includes:

* User registration
* User login
* JWT-based authentication
* Secure token handling

### Authorization

Protected resources are accessible only to authenticated users.

The frontend uses route protection through:

```text
ProtectedRoute.jsx
PublicRoute.jsx
```

The backend also validates authenticated requests before allowing access to protected endpoints.

---

# 🔑 JWT Security Flow

```text
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
Authorization Header
 │
 ▼
Protected FastAPI Route
 │
 ▼
Authentication Validation
 │
 ▼
Service
```

The Axios interceptor automatically handles authentication-related API requests so that protected endpoints can receive the required authorization information.

---

# 🌐 API Architecture

BusinessPulse exposes its functionality through REST APIs built using FastAPI.

The API structure is divided according to business functionality instead of placing all logic into a single endpoint.

```text
Frontend
    │
    ▼
Axios API Client
    │
    ▼
FastAPI
    │
    ├── Authentication
    ├── Historical Analytics
    ├── Current Dashboard
    └── Forecasting
          │
          ▼
       Services
```

---

# 📚 API Documentation

The backend provides automatically generated **Swagger/OpenAPI documentation** through FastAPI.

The documentation allows developers to:

* View available API endpoints
* Inspect request parameters
* Inspect response schemas
* Test APIs directly
* Understand API contracts

When the backend is running, the Swagger documentation can be accessed through the FastAPI documentation route.

---

# 🧠 Machine Learning Architecture

BusinessPulse separates forecasting logic from the rest of the application through the dedicated `ml` module.

```text
ml/
├── forecast_models.py
├── linear_forecast.py
├── polynomial_forecast.py
└── random_forest_forecast.py
```

### Forecasting Models

#### Linear Regression

Used to model a linear relationship between historical business trends and future values.

#### Polynomial Regression

Used when historical business trends exhibit non-linear patterns.

#### Random Forest Regression

Used to model more complex relationships and non-linear business patterns.

The forecasting service acts as the bridge between the API layer and the machine-learning models.

```text
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
     └── Random Forest
```

---

# 🗃️ Data Sources

BusinessPulse uses the **Olist Brazilian E-commerce Public Dataset**.

The backend contains separate datasets for:

* Customers
* Orders
* Order Items
* Payments
* Products
* Reviews
* Sellers

These datasets are processed and combined to generate business metrics and analytics.

---

# ⚙️ Data Processing Pipeline

```text
Olist CSV Dataset
       │
       ▼
Data Loader
       │
       ▼
Data Cleaning & Preprocessing
       │
       ▼
Data Transformation
       │
       ▼
Business Metrics
       │
       ├── Historical Analytics
       ├── Current KPIs
       └── Forecasting Data
```

The data-processing layer handles tasks such as:

* Loading CSV datasets
* Handling missing values
* Converting date fields
* Combining related datasets
* Preparing business metrics
* Preparing historical data for forecasting

---

# 🖥️ Frontend Architecture

The frontend is developed using React and follows a component-based architecture.

```text
src/
│
├── components/
│   └── Reusable UI Components
│
├── pages/
│   └── Application Pages
│
├── services/
│   └── API Communication
│
├── App.jsx
└── main.jsx
```

### Reusable Components

The application contains reusable components for:

* Charts
* Tables
* KPI cards
* Navigation
* Sidebar
* Page headers
* Tooltips
* Loaders
* Tabs
* Route protection

This reduces code duplication and keeps the frontend modular.

---

# 📄 Application Pages

### Home

Provides an overview of the BusinessPulse platform.

### Dashboard

Acts as the main analytics area of the application.

### Historical Analytics

Provides detailed analysis of historical business performance.

### Current Dashboard

Displays current business KPIs and operational metrics.

### Forecast Predictions

Displays machine-learning-based predictions and future business trends.

### Login & Signup

Provides user authentication and account creation.

---

# 🎨 Dashboard Visualizations

BusinessPulse uses interactive visualizations to make business data easier to understand.

The dashboard includes:

* Line charts
* Bar charts
* Pie charts
* Scatter charts
* Correlation heatmaps
* KPI cards
* Data tables
* Historical vs. predicted charts

---

# 🧩 SOLID Principles

The backend architecture is designed around the **SOLID principles** to improve maintainability, scalability, and separation of responsibilities.

### Single Responsibility Principle

Different modules have focused responsibilities.

```text
Routes       → HTTP/API handling
Services     → Business logic
Repositories → Data access
Schemas      → Data validation
ML           → Forecasting
Utils        → Shared functionality
Database     → Persistence
```

### Open/Closed Principle

New business services, API endpoints, and forecasting models can be added without significantly modifying existing modules.

### Liskov Substitution Principle

Forecasting components can be structured so that different prediction models can be used within the forecasting workflow.

### Interface Segregation Principle

The application separates functionality into focused modules rather than relying on large, tightly coupled interfaces.

### Dependency Inversion Principle

Higher-level business logic is separated from lower-level data-access and implementation details through service and repository layers.

---

# 🛡️ Error Handling

The backend includes centralized exception handling through:

```text
app/exceptions.py
```

This helps maintain consistent error handling across the application and prevents business logic from being tightly coupled with HTTP error handling.

---

# 🛠️ Technology Stack

## Frontend

* React
* Vite
* React Router
* Axios
* Tailwind CSS
* Recharts
* Lucide React

## Backend

* Python
* FastAPI
* Uvicorn
* Pandas
* NumPy
* Pydantic
* Scikit-learn

## Database

* MongoDB

## Authentication & Security

* JWT
* Authorization
* Axios Interceptors
* Protected Routes

## Machine Learning

* Linear Regression
* Polynomial Regression
* Random Forest Regression
* MAE
* R² Score

## API Documentation

* Swagger UI
* OpenAPI

## Dataset

* Olist Brazilian E-commerce Public Dataset

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Saurabh20-05/BusinessPulse.git

cd BusinessPulse
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in the backend `.env` file.

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

---

## 3. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

The frontend will then be available through the Vite development server.

---

# 🔁 Complete Application Workflow

```text
                    USER
                      │
                      ▼
                React Frontend
                      │
          ┌───────────┴───────────┐
          │                       │
      Login/Signup            Dashboard
          │                       │
          ▼                       ▼
      JWT Auth              Axios API Client
                                  │
                                  ▼
                           FastAPI Routes
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
                Historical      Current      Forecast
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
                              Services
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
              Repositories                 ML Models
                    │                    ┌──────┼──────┐
                    ▼                    ▼      ▼      ▼
                MongoDB               Linear Polynomial Random
                                         Regression Forest
                    │
                    ▼
               Business Data
                    │
                    ▼
              Analytics & KPIs
                    │
                    ▼
              React Dashboard
```

---

# 📌 Key Architectural Highlights

BusinessPulse is designed with a focus on **separation of concerns and maintainability**.

### Backend

* Modular FastAPI architecture
* Separate routes for major application modules
* Separate service for each business domain
* Repository layer for data access
* Pydantic schemas for validation
* Dedicated machine-learning module
* MongoDB integration
* Centralized exception handling
* Reusable utility modules

### Frontend

* Component-based React architecture
* Reusable UI components
* Separate pages for application modules
* Dedicated API service layer
* Protected and public routes
* Axios-based API communication
* Axios interceptor for authentication handling

### Security

* JWT authentication
* Authorization for protected resources
* Protected frontend routes
* Secure API communication flow

### Analytics & ML

* Historical business analytics
* Current KPI monitoring
* Multiple forecasting models
* Interactive visualizations
* Forecast evaluation metrics

---

# 🎯 Project Objective

The objective of BusinessPulse is to provide a single platform where businesses can:

1. **Understand past performance** through historical analytics.
2. **Monitor important KPIs** through the current dashboard.
3. **Identify business patterns and relationships** through visual analytics.
4. **Predict future trends** using machine-learning models.
5. **Access analytics through structured APIs**.
6. **Secure application resources** using authentication and authorization.
7. **Maintain a scalable codebase** through modular architecture and SOLID principles.

---

## License

This project is intended for educational, portfolio, and learning purposes.
