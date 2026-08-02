# BusinessPulse

BusinessPulse is an interactive business analytics dashboard built to analyze historical business data, monitor key performance indicators (KPIs), and forecast future business trends. The project uses the Olist Brazilian E-commerce dataset and combines data analysis, visualization, and machine learning to provide meaningful business insights through an intuitive web interface.

---

## Features

### Historical Analytics
- Monthly revenue analysis
- Monthly order trends
- Revenue by product category
- Top-performing categories
- Payment method distribution
- Customer distribution by state
- Review score distribution
- Product price distribution
- Revenue vs. Orders comparison
- Correlation heatmap

### Current Dashboard
- Total revenue
- Total orders
- Total customers
- Total products
- Average review score
- Average payment value
- Top-selling category
- Top seller
- Most used payment method
- Recent orders table
- Top categories table

### Forecast & Predictions
- Revenue forecasting
- Order forecasting
- Customer forecasting
- Linear Regression model
- Historical vs Predicted trend visualization
- Model evaluation using MAE and R² Score

---

## Project Architecture

```
BusinessPulse
│
├── backend
│   ├── app
│   │   ├── routes
│   │   ├── services
│   │   ├── ml
│   │   ├── utils
│   │   └── main.py
│   └── data
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── services
│   │   └── App.jsx
│
└── README.md
```

---

## Technology Stack

### Frontend
- React
- React Router
- Axios
- Recharts
- Tailwind CSS
- Lucide React

### Backend
- FastAPI
- Pandas
- NumPy
- Scikit-learn
- Uvicorn

### Machine Learning
- Linear Regression
- Moving Average Forecasting

### Dataset
- Olist Brazilian E-commerce Public Dataset

---

## Data Processing

The backend performs the following preprocessing steps before generating analytics:

- Loads all CSV files
- Cleans missing values
- Converts date columns
- Merges multiple tables
- Removes cancelled orders
- Creates monthly business data
- Calculates total item value (Product Price + Freight)
- Caches processed datasets for faster API responses

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/dashboard` | Dashboard summary |
| `/historical` | Historical analytics |
| `/current` | Current business dashboard |
| `/forecast` | Forecast overview |
| `/charts` | Individual chart APIs |

---

## Machine Learning

BusinessPulse uses a Linear Regression model to forecast:

- Future Revenue
- Future Orders
- Future Customers

The model is evaluated using:

- Mean Absolute Error (MAE)
- R² Score

---

## Dashboard Visualizations

The project includes multiple interactive visualizations such as:

- Line Charts
- Bar Charts
- Pie Charts
- Scatter Charts
- Correlation Heatmap
- Data Tables
- KPI Cards

---

## Installation

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Project Workflow

```
CSV Dataset
      │
      ▼
Data Loading & Cleaning
      │
      ▼
Data Processing
      │
      ▼
Business Analytics
      │
      ▼
Machine Learning Forecasting
      │
      ▼
FastAPI REST APIs
      │
      ▼
React Dashboard
```

---

## Future Improvements

- User authentication
- Export reports (PDF/Excel)
- Interactive filters
- Additional forecasting models
- Live database integration
- Business report generation

---

## License

This project is intended for educational and learning purposes.
