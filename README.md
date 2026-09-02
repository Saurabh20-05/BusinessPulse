# BusinessPulse

### Business Analytics & Forecasting Platform

BusinessPulse is a full-stack business analytics platform that transforms e-commerce data into actionable insights through **historical analytics, current KPI monitoring, and machine-learning-based forecasting**.

The platform supports both the built-in **Olist Brazilian E-Commerce dataset** and **user-uploaded CSV datasets**, allowing users to upload, map, analyze, and forecast their own business data.

Built with **React, FastAPI, Python, MongoDB, Pandas, Scikit-Learn, JWT, and Tailwind CSS**, BusinessPulse follows a modular architecture with separate routes, services, repositories, schemas, utilities, database, and machine-learning layers.

---

## 🚀 Key Features

### 📊 Historical Analytics

Analyze historical business performance through interactive visualizations.

- Monthly revenue trends
- Monthly order trends
- Revenue by product category
- Top-performing categories
- Payment method distribution
- Customers by state
- Review score distribution
- Product price distribution
- Revenue vs. orders analysis
- Correlation heatmap
- Historical business trends
- Interactive charts and tables

---

### 📈 Current Dashboard

Monitor important business KPIs through a centralized dashboard.

#### Key Performance Indicators

- Total Revenue
- Total Orders
- Total Customers
- Total Products
- Average Review Score
- Average Payment Value
- Top-Selling Category
- Top Seller
- Most Used Payment Method

#### Additional Insights

- Recent orders
- Top categories
- Business performance summaries
- Interactive KPI cards
- Charts and data tables

---

### 🔮 Forecast & Predictions

Predict future business performance using multiple machine-learning models.

Forecasting is available for:

- Revenue
- Orders
- Customers

#### Machine Learning Models

- Linear Regression
- Polynomial Regression
- Random Forest Regression

#### Forecasting Capabilities

- Historical vs. predicted trends
- Future business projections
- Model-based predictions
- Forecast visualizations
- Model evaluation metrics

#### Evaluation Metrics

- Mean Absolute Error (MAE)
- R² Score

---

## 📂 Custom Dataset Management

BusinessPulse is not limited to the built-in Olist dataset.

Users can upload their own CSV business or sales data and configure it for analysis.

### Custom Dataset Workflow

```text
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
Historical Analytics
    ↓
Current KPIs
    ↓
Forecasting
```

### Dataset Features

- CSV file upload
- File validation
- Dataset preview
- Column mapping
- Data normalization
- Dataset selection
- Dataset deletion
- Multiple uploaded datasets
- User-specific dataset access
- Built-in Olist dataset
- Custom dataset analysis
- Dataset-aware forecasting

Each authenticated user can access their own uploaded datasets.

---

# 🏗️ System Architecture

BusinessPulse follows a layered full-stack architecture that separates presentation, API handling, business logic, data access, persistence, and machine learning.

```text
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

---

# 🔄 Backend Architecture

The backend follows a modular layered architecture:

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

## Routes

The route layer handles HTTP requests and API endpoints.

```text
routes/
├── auth.py
├── current.py
├── dataset.py
├── forecast.py
└── historical.py
```

Responsibilities:

- Receive HTTP requests
- Validate request data
- Authenticate users
- Invoke services
- Return API responses

---

## Services

The service layer contains business logic.

```text
services/
├── auth_service.py
├── category_service.py
├── customer_service.py
├── dataset_data_service.py
├── dataset_service.py
├── forecast_service.py
├── heatmap_service.py
├── kpi_service.py
├── order_service.py
├── payment_service.py
├── price_service.py
├── revenue_service.py
└── review_service.py
```

Each service focuses on a specific business responsibility, improving maintainability and separation of concerns.

---

## Repositories

The repository layer isolates data-access operations from business logic.

```text
repositories/
├── dataset_repository.py
├── sales_repository.py
└── user_repository.py
```

Responsibilities include:

- User data access
- Dataset persistence
- Dataset retrieval
- Dataset deletion
- Business data access

---

## Schemas

Pydantic schemas provide structured request and response models.

They help provide:

- Input validation
- Response validation
- Consistent API contracts
- Structured data models
- Type-safe request and response handling

---

## Database

MongoDB is used for application-level persistence.

The database layer manages:

- User records
- Uploaded datasets
- Dataset metadata
- Normalized dataset information

---

# 🔐 Authentication & Authorization

BusinessPulse implements JWT-based authentication and protected resources.

### Authentication Features

- User registration
- User login
- Password hashing
- JWT access tokens
- Authenticated API requests
- Protected frontend routes
- Protected backend routes

### Frontend Protection

```text
ProtectedRoute.jsx
PublicRoute.jsx
```

Protected pages require authentication before access.

### Backend Protection

Protected FastAPI routes validate the authenticated user before allowing access to application resources.

---

# 🔑 JWT Authentication Flow

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

The Axios interceptor automatically attaches the JWT access token to protected API requests.

---

# 🛡️ User Data Isolation

Uploaded datasets are associated with the authenticated user.

```text
User A
 │
 ├── Dataset A1
 └── Dataset A2

User B
 │
 ├── Dataset B1
 └── Dataset B2
```

A user can only access, select, or delete datasets belonging to their account.

This prevents unauthorized cross-user dataset access.

---

# 🧠 Machine Learning Architecture

Forecasting logic is separated into a dedicated machine-learning module.

```text
ml/
├── forecast_models.py
├── linear_forecast.py
├── polynomial_forecast.py
└── random_forest_forecast.py
```

The forecasting workflow is:

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
     └── Random Forest Regression
```

---

## Linear Regression

Used for modeling approximately linear historical business trends and generating future predictions.

---

## Polynomial Regression

Used to model non-linear relationships in historical business trends.

---

## Random Forest Regression

Used to model more complex non-linear relationships and business patterns.

---

# 🗃️ Data Sources

BusinessPulse supports:

### Built-in Dataset

The platform includes the **Olist Brazilian E-Commerce Public Dataset**.

The dataset contains information related to:

- Customers
- Orders
- Order Items
- Payments
- Products
- Reviews
- Sellers

### Custom Dataset

Users can upload their own CSV files and map their columns to BusinessPulse fields.

---

# ⚙️ Data Processing Pipeline

```text
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
Business Metrics
     │
     ├── Historical Analytics
     ├── Current KPIs
     └── Forecasting
```

The data-processing layer handles tasks such as:

- Loading CSV data
- Validating uploaded files
- Mapping user-defined columns
- Renaming fields into standardized fields
- Data transformation
- Preparing business metrics
- Preparing forecasting data

---

# 🌐 API Architecture

BusinessPulse exposes its functionality through REST APIs built using FastAPI.

```text
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

---

# 📚 API Documentation

FastAPI automatically generates API documentation using **Swagger/OpenAPI**.

The documentation allows developers to:

- View available endpoints
- Inspect request parameters
- Inspect response schemas
- Test APIs directly
- Understand API contracts

When the backend is running, open:

```text
http://127.0.0.1:8000/docs
```

---

# 🖥️ Frontend Architecture

The frontend is developed using React with a component-based architecture.

```text
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

- Navigation
- Sidebar
- Tabs
- Page headers
- Charts
- Tables
- KPI cards
- Tooltips
- Loaders
- Route protection
- Dataset mapping

This reduces duplication and improves maintainability.

---

# 📄 Application Pages

### Home

Provides an overview of the BusinessPulse platform and its capabilities.

### Login

Handles user authentication.

### Signup

Allows users to create an account.

### Dataset

Provides:

- Olist dataset selection
- CSV upload
- Dataset preview
- Column mapping
- Uploaded dataset management
- Dataset selection
- Dataset deletion

### Dashboard

Acts as the main analytics area.

It contains:

- Historical Analytics
- Current Dashboard
- Forecast & Predictions

### Historical Analytics

Provides detailed analysis of historical business performance.

### Current Dashboard

Displays business KPIs, recent orders, categories, and operational metrics.

### Forecast Predictions

Displays machine-learning-based predictions for future business trends.

---

# 📊 Dashboard Visualizations

BusinessPulse uses interactive visualizations to make business data easier to understand.

The platform includes:

- Line charts
- Bar charts
- Pie charts
- Scatter charts
- Correlation heatmaps
- KPI cards
- Data tables
- Historical vs. predicted charts

---

# 🧩 SOLID Principles

The backend is structured around the **SOLID principles** to improve maintainability, modularity, and separation of responsibilities.

### Single Responsibility Principle

Each layer has a focused responsibility:

```text
Routes        → HTTP/API handling
Services      → Business logic
Repositories  → Data access
Schemas       → Data validation
ML            → Forecasting
Utils         → Shared functionality
Database      → Persistence
```

### Open/Closed Principle

New business services, endpoints, and forecasting models can be added without significantly modifying unrelated modules.

### Liskov Substitution Principle

Forecasting components are structured so that different prediction models can participate in the forecasting workflow.

### Interface Segregation Principle

The application is divided into focused modules rather than large, tightly coupled interfaces.

### Dependency Inversion Principle

Business logic is separated from lower-level data-access and implementation details through service and repository layers.

---

# 🛡️ Error Handling

The backend provides centralized exception handling through:

```text
app/exceptions.py
```

This helps maintain consistent API error responses and keeps business logic separated from HTTP-specific error handling.

The frontend also provides user-facing notifications for operations such as:

- Dataset upload
- Dataset deletion
- Dataset selection
- Column mapping
- Authentication failures

---

# 🛠️ Technology Stack

## Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- Recharts
- Lucide React

## Backend

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Pydantic
- Scikit-Learn

## Database

- MongoDB
- PyMongo

## Authentication & Security

- JWT
- Password hashing
- Authorization
- Protected frontend routes
- Protected backend routes
- Axios interceptors
- User-specific dataset access

## Machine Learning

- Linear Regression
- Polynomial Regression
- Random Forest Regression
- MAE
- R² Score

## API Documentation

- Swagger UI
- OpenAPI

## Dataset

- Olist Brazilian E-Commerce Public Dataset

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
│   │   │   └── olist_sellers.csv
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
│   │   │   ├── dataset_repository.py
│   │   │   ├── sales_repository.py
│   │   │   └── user_repository.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── current.py
│   │   │   ├── dataset.py
│   │   │   ├── forecast.py
│   │   │   └── historical.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── category.py
│   │   │   ├── customer.py
│   │   │   ├── dataset.py
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
│   │   │   ├── dataset_data_service.py
│   │   │   ├── dataset_service.py
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
│   │   │   ├── data_validation.py
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
│   │   │   ├── ColumnMapper.jsx
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
│   │   │   ├── Dataset.jsx
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

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Saurabh20-05/BusinessPulse.git

cd BusinessPulse
```

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
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

---

## 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
MONGODB_URL=your_mongodb_connection_string
MONGODB_DATABASE=BusinessPulse

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use your own secure values for production environments.

---

## 4. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend will run on:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available through the Vite development server.

---

# 🔁 Complete Application Workflow

```text
                         USER
                           │
                           ▼
                    React Frontend
                           │
              ┌────────────┴────────────┐
              │                         │
         Login / Signup             Dashboard
              │                         │
              ▼                         ▼
          JWT Auth                Axios API Client
                                        │
                                        ▼
                                  FastAPI Routes
                                        │
                     ┌──────────────────┼──────────────────┐
                     │                  │                  │
                     ▼                  ▼                  ▼
                Dataset            Historical          Current
                Management         Analytics          Dashboard
                     │                  │                  │
                     └──────────────────┼──────────────────┘
                                        │
                                        ▼
                                   Forecasting
                                        │
                                        ▼
                                    Services
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
                   Repositories                  ML Models
                         │                    ┌────────┼────────┐
                         ▼                    ▼        ▼        ▼
                     MongoDB              Linear  Polynomial Random
                                                           Forest
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

# 🎯 Project Objective

BusinessPulse provides a single platform where users can:

1. Analyze historical business performance.
2. Monitor important business KPIs.
3. Explore business patterns and relationships.
4. Upload and analyze custom datasets.
5. Map and normalize uploaded CSV data.
6. Forecast future revenue, orders, and customers.
7. Compare historical and predicted trends.
8. Access functionality through structured REST APIs.
9. Secure application resources using authentication and authorization.
10. Maintain a modular and scalable codebase.

---

# ⭐ Key Engineering Highlights

### Full-Stack Development

- React frontend
- FastAPI backend
- MongoDB persistence
- REST API architecture
- Axios API integration

### Software Architecture

- Layered backend architecture
- Route-service-repository separation
- Reusable frontend components
- Dedicated ML layer
- Pydantic schemas
- Centralized exception handling
- SOLID-oriented design

### Authentication & Security

- JWT authentication
- Password hashing
- Protected frontend routes
- Protected backend endpoints
- Axios authorization interceptor
- User-specific dataset access

### Data Engineering

- CSV ingestion
- Dataset validation
- Dataset preview
- Column mapping
- Data normalization
- Multiple dataset management

### Analytics

- Historical business analytics
- KPI monitoring
- Interactive charts
- Data tables
- Correlation analysis

### Machine Learning

- Linear Regression
- Polynomial Regression
- Random Forest Regression
- Revenue forecasting
- Order forecasting
- Customer forecasting
- MAE
- R² Score

---

# 📌 Why BusinessPulse?

BusinessPulse combines **software engineering, data analytics, database management, authentication, and machine learning** into one end-to-end application.

Instead of simply displaying preprocessed charts, the platform allows users to:

```text
Bring Business Data
        ↓
Process & Normalize It
        ↓
Analyze Historical Performance
        ↓
Monitor Current KPIs
        ↓
Generate Future Predictions
        ↓
Make Data-Driven Decisions
```

---

# 🔮 Future Enhancements

Potential future improvements include:

- Cloud deployment
- Automated model selection
- Advanced forecasting models
- Role-based access control
- Automated data-quality reports
- Scheduled forecasting
- Exportable analytics reports
- Additional business datasets
- Advanced anomaly detection
- Model comparison dashboards

---

# 📜 License

This project is intended for educational, portfolio, and learning purposes.
