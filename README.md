# E-commerce Dashboard with Forecasting

An interactive e-commerce operations dashboard built with Streamlit, featuring comprehensive analytics and machine learning-based forecasting for Brazilian delivery center data.

##  Project Overview

This project provides a comprehensive dashboard solution for e-commerce and delivery operations, offering real-time insights into orders, driver performance, and revenue metrics with advanced forecasting capabilities for business optimization.

##  Key Features

### Dashboard Analytics
- ** Orders by City & Hub**: Track order volumes and cancellation rates across different locations
- ** Driver Performance Metrics**: Monitor delivery efficiency, failure rates, and performance KPIs
- ** Revenue Analytics**: Analyze total revenue, average order values, and payment performance
- ** Interactive Visualizations**: Dynamic charts and graphs using Plotly
- ** Date Range Filtering**: Flexible date-based data filtering
- ** CSV Export**: Download detailed reports for further analysis

### Key Metrics Tracked
- Total Orders & Cancellation Rates
- Driver Delivery Performance & Failure Rates
- Revenue by City and Hub
- Average Order Values
- Delivery Time Analysis
- Distance-based Performance Metrics

##  Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web framework for interactive dashboard
- **SQLite**: Database for data storage and queries
- **Pandas**: Data manipulation and analysis
- **Plotly Express**: Interactive data visualizations
- **DateTime**: Date and time handling

##  Dataset Information

**Dataset Source**: [Brazilian Delivery Center - Kaggle](https://www.kaggle.com/api/v1/datasets/download/nosbielcs/brazilian-delivery-center)

The dataset contains comprehensive e-commerce and delivery data including:
- **Orders Data**: Order status, timestamps, amounts, and locations
- **Delivery Information**: Driver performance, delivery distances, and status
- **Hub & Store Data**: Geographic distribution and operational metrics
- **Time Series Data**: Historical data perfect for forecasting models

*This real-world Brazilian e-commerce dataset provides rich operational data for analytics and machine learning model development.*

##  Dashboard Screenshots

### Main Dashboard Interface
![E-commerce Operations Dashboard] <img width="1918" height="861" alt="Screenshot 2025-07-24 213632" src="https://github.com/user-attachments/assets/ad418b0e-f8c8-4a32-8d6d-53e9296ae7e1" />

*Complete dashboard showing orders by city & hub, driver performance metrics, and revenue analytics with KPI cards and interactive filtering*

### Key Dashboard Sections:
- **Orders by City & Hub**: Real-time order tracking with cancellation analysis
- **Driver Performance Metrics**: Comprehensive delivery analytics and performance tracking  
- **Revenue & Payment Performance**: Financial metrics with city-wise revenue breakdown

##  Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/harshhaldankar/E-commerce-Dashboard-with-forcasting.git
cd E-commerce-Dashboard-with-forcasting
```

2. **Install required dependencies**
```bash
pip install streamlit pandas sqlite3 plotly
```

3. **Download the dataset**
```bash
# Download from Kaggle
kaggle datasets download -d nosbielcs/brazilian-delivery-center
```

4. **Run the Streamlit application**
```bash
streamlit run app.py
```


##  Forecasting Models (Currently Working On)

### Machine Learning Models in Development:

#### 1. **Daily Order Volume Prediction**
- **Objective**: Predict daily order volumes across different cities and hubs
- **Features**: Historical order data, seasonal patterns, city demographics
- **Model**: Time series forecasting using ARIMA/Prophet

#### 2. **Daily Revenue Forecasting** 
- **Objective**: Forecast daily revenue for financial planning
- **Features**: Historical revenue, order patterns, seasonal trends
- **Model**: Linear regression with seasonal decomposition

#### 3. **City-wise Daily Demand Prediction**
- **Objective**: Predict demand patterns for each city for resource allocation
- **Features**: Geographic data, historical demand, external factors
- **Model**: Multi-variate time series forecasting

### Planned ML Implementation:
- **Data Preprocessing**: Feature engineering and data cleaning
- **Model Training**: Using scikit-learn and statsmodels
- **Model Evaluation**: Cross-validation and accuracy metrics
- **Integration**: Seamless integration with Streamlit dashboard

##  Value Proposition for Large E-commerce Platforms:

- **Operational Excellence**: Monitor and optimize delivery operations across multiple cities
- **Cost Optimization**: Identify inefficiencies in delivery routes and driver performance
- **Customer Satisfaction**: Reduce delivery failures and improve service quality
- **Strategic Planning**: Data-driven decisions for expansion and resource allocation

##  Project Structure

```
E-commerce-Dashboard-with-forcasting/
│
├── app.py                     # Main Streamlit application
├── e_commerce.db             # SQLite database
├── requirements.txt          # Python dependencies
├── data/                     # Dataset and data files
├── screenshots/              # Dashboard screenshots
├── forecasting/              # ML models and forecasting scripts
└── README.md                # Project documentation
```

##  Links & Resources

- **Dataset**: [Brazilian Delivery Center - Kaggle](https://www.kaggle.com/datasets/nosbielcs/brazilian-delivery-center)
- **Live Dashboard**: [https://e-commerce-dashboard-with-forcasting.streamlit.app/]
---

*This project demonstrates practical application of data analytics, business intelligence, and machine learning in real-world e-commerce and delivery operations.*
