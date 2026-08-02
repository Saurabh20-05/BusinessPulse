# BusinessPulse — Business Analytics & Forecast Dashboard

A full-stack analytics dashboard built for a Week 3 Software Engineering internship
project, using an Olist-style e-commerce dataset.

## Stack
- **Backend:** Python, FastAPI, Pandas, NumPy, Scikit-learn
- **Frontend:** React (Vite), Tailwind CSS, React Router, Axios, Recharts

## Project structure
```
backend/
  app/
    routes/       API endpoints (dashboard, historical, current, forecast, charts)
    services/      business logic (KPI calculations, chart data prep)
    ml/            forecasting models
    utils/         data loading & cleaning
    data/          CSV dataset + generator script
  main.py          -> actually app/main.py, FastAPI app entrypoint
  requirements.txt

frontend/
  src/
    components/    Navbar, Sidebar, Footer, StatCard, ChartCard, DataTable, etc.
    charts/         Recharts wrapper components (line, bar, pie, scatter, histogram, area, heatmap)
    pages/          Home, Dashboard (with 3 tabs)
    services/       Axios API client
```

## Dataset
The real Olist dataset from Kaggle isn't downloadable from this environment, so
`backend/app/data/generate_dataset.py` generates a synthetic dataset that mirrors
Olist's schema (customers, sellers, products, orders, order_items, payments, reviews),
with a built-in seasonal/upward trend so the forecasting charts have real signal.
The CSVs are already generated and included in `backend/app/data/`.

To regenerate them:
```
cd backend/app/data
python generate_dataset.py
```

## Running locally

### Backend
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API docs available at http://127.0.0.1:8000/docs

### Frontend
```
cd frontend
npm install
npm run dev
```
App available at http://127.0.0.1:5173

The frontend expects the API at `http://127.0.0.1:8000` (see `frontend/.env`).

## API routes
- `GET /` — health check
- `GET /dashboard` — combined summary (KPIs, revenue trend, revenue forecast)
- `GET /historical` — all Historical Analytics chart data
- `GET /current` — KPI cards + recent orders + top categories tables
- `GET /forecast` — revenue, orders, customer forecasts
- `GET /forecast/revenue`, `/forecast/orders`, `/forecast/customers`
- `GET /charts/revenue`, `/charts/orders`, `/charts/categories`, `/charts/payments`, `/charts/reviews`, `/charts/heatmap`

## Notes
- No authentication is implemented — "Sign In" in the navbar is a UI placeholder only, per project scope.
- Forecasting uses a simple linear regression on monthly aggregates (plus a moving-average
  baseline in the ML module) — intentionally simple, as specified for this project.
