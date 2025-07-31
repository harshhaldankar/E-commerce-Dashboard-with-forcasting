import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, datetime
import plotly.express as px
import os
import requests
import time

# --- Database Download Function ---
@st.cache_data
def download_database():
    """Download database from external URL if not exists locally"""
    db_path = 'e_commerce.db'
    status_placeholder = st.empty()
    # Check if database already exists
    if os.path.exists(db_path):
        status_placeholder.info(" Database found locally!")
        time.sleep(2)
        status_placeholder.empty()
        return db_path
    
    # Get database URL from secrets or environment
    db_url = None
    try:
        db_url = st.secrets["Database_URL"]
    except:
        try:
            db_url = os.getenv('Database_URL')
        except:
            pass
    
    try:
        status_placeholder.info(" Downloading database... This may take a moment.")
        time.sleep(2)
        status_placeholder.empty()
        
        # Download with progress
        response = requests.get(db_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(db_path, 'wb') as f:
            if total_size > 0:
                downloaded = 0
                progress_bar = st.progress(0)
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = min(downloaded / total_size, 1.0)
                        progress_bar.progress(progress)
                        
                progress_bar.empty()
            else:
                f.write(response.content)
        
        # Verify file was created and has content
        if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
            status_placeholder.success(" Database downloaded successfully!")
            time.sleep(2)
            status_placeholder.empty()
            return db_path
        else:
            st.error("❌ Database download failed - file is empty or missing")
            return None
        
    except Exception as e:
        st.error(f"❌ Failed to download database: {e}")
        st.info("Please check your DATABASE_URL and internet connection")
        return None

# --- Streamlit Page Setup (Must be first) ---
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", initial_sidebar_state="auto")
st.title(" E-Commerce Operations Dashboard")

# Download database after page config
db_path = download_database()

# Safety check
if not db_path or not os.path.exists(db_path):
    st.error("❌ Database not available. Cannot proceed.")
    st.stop()

# --- Database Connection ---
@st.cache_resource
def get_db_connection(database_path):
    """Create database connection with caching"""
    try:
        conn = sqlite3.connect(database_path, check_same_thread=False)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

conn = get_db_connection(db_path)

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("###  Date Filter")
    start_date = st.date_input("Start Date", date(2021, 1, 1))
    end_date = st.date_input("End Date", date(2021, 4, 30))
    
# ----------------------
# 1. ORDERS BY HUB/CITY
# ----------------------

st.header(" Orders by City & Hub")

# SQLite compatible query
query_orders = """
SELECT 
    h.hub_city AS city,
    h.hub_name AS hub,
    COUNT(CASE WHEN o.order_status = 'FINISHED' THEN 1 END) AS total_orders,
    COUNT(CASE WHEN o.order_status = 'CANCELED' THEN 1 END) AS cancelled_orders,
    ROUND(
        100.0 * COUNT(CASE WHEN o.order_status = 'CANCELED' THEN 1 END) 
        / NULLIF(COUNT(*), 0), 2
    ) AS cancelled_percent
FROM orders o
JOIN stores s ON o.store_id = s.store_id
JOIN hubs h ON s.hub_id = h.hub_id
WHERE DATE(
    o.order_created_year || '-' ||
    PRINTF('%02d', o.order_created_month) || '-' ||
    PRINTF('%02d', o.order_created_day)
) BETWEEN ? AND ?
GROUP BY h.hub_city, h.hub_name
ORDER BY h.hub_city;
"""

try:
    # Convert dates to strings for SQLite
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    df_orders = pd.read_sql_query(query_orders, conn, params=[start_date_str, end_date_str])   
except Exception as e:
    st.error(f"Error executing orders query: {e}")
    df_orders = pd.DataFrame()

# KPI Cards for Orders
kpi_query1 = """ 
SELECT 
  COUNT(CASE WHEN order_status = 'FINISHED' THEN 1 END ) AS total_orders,
  COUNT(CASE WHEN order_status = 'CANCELED' THEN 1 END) AS cancelled_orders,
  ROUND(
    100.0 * COUNT(CASE WHEN order_status = 'CANCELED' THEN 1 END) 
    / NULLIF(COUNT(order_id), 0), 2
  ) AS cancelled_percent
FROM orders
WHERE DATE(
    order_created_year || '-' ||
    PRINTF('%02d', order_created_month) || '-' ||
    PRINTF('%02d', order_created_day)
) BETWEEN ? AND ?
"""

try:
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    kpi_df1 = pd.read_sql_query(kpi_query1, conn, params=[start_date_str, end_date_str])
    if not kpi_df1.empty:
        total_orders = int(kpi_df1['total_orders'].iloc[0]) if kpi_df1['total_orders'].iloc[0] else 0
        cancelled_orders = int(kpi_df1['cancelled_orders'].iloc[0]) if kpi_df1['cancelled_orders'].iloc[0] else 0
        cancelled_percent = f"{kpi_df1['cancelled_percent'].iloc[0]}%" if kpi_df1['cancelled_percent'].iloc[0] else "0%"
    else:
        total_orders = 0
        cancelled_orders = 0
        cancelled_percent = "0%"
except Exception as e:
    st.error(f"Error executing KPI query: {e}")
    total_orders = 0
    cancelled_orders = 0
    cancelled_percent = "0%"

col1, col2, col3 = st.columns(3)
col1.metric(" Total Orders", f"{total_orders:,}")
col2.metric(" Cancelled Orders", f"{cancelled_orders:,}")
col3.metric(" Cancellation Rate", cancelled_percent)

if not df_orders.empty:
    st.dataframe(df_orders, use_container_width=True)
    # Download Orders CSV
    csv_orders = df_orders.to_csv(index=False).encode("utf-8")
    st.download_button("Download Orders CSV", csv_orders, "order_metrics.csv", "text/csv")
else:
    st.warning("No order data for selected filters.")

# -------------------------------------
# 2. DRIVER PERFORMANCE METRICS SECTION
# -------------------------------------
st.header("Driver Performance Metrics")

query_driver = """
SELECT 
  o.order_id,
  d.driver_id,
  d.delivery_distance_meters,
  d.delivery_status,
  o.order_moment_collected,
  o.order_moment_delivered
FROM deliveries d
JOIN orders o ON o.order_id = d.delivery_order_id
JOIN drivers dr ON d.driver_id = dr.driver_id
WHERE o.order_moment_collected IS NOT NULL AND o.order_moment_delivered IS NOT NULL
AND o.order_status = 'FINISHED'
"""

try:
    df = pd.read_sql_query(query_driver, conn)
    # Convert timestamps
    df['collected_dt'] = pd.to_datetime(df['order_moment_collected'], errors='coerce')
    df['delivered_dt'] = pd.to_datetime(df['order_moment_delivered'], errors='coerce')

    df = df.dropna(subset=['collected_dt', 'delivered_dt'])
    df = df[(df['collected_dt'].dt.date >= start_date) & (df['collected_dt'].dt.date <= end_date)]

    df['delivery_time_mins'] = (df['delivered_dt'] - df['collected_dt']).dt.total_seconds() / 60

    driver_metrics = df.groupby(['driver_id']).agg(
        total_deliveries=('order_id', 'count'),
        avg_delivery_distance=('delivery_distance_meters', 'mean'),
        delivery_failure_count=('delivery_status', lambda x: (x != 'DELIVERED').sum()),
        delivery_fail_rate_percent=('delivery_status', lambda x: (x != 'DELIVERED').mean() * 100),
        avg_delivery_time_mins=('delivery_time_mins', 'mean')
    ).round(2).reset_index()

    if not driver_metrics.empty:
        st.dataframe(driver_metrics, use_container_width=True)
        csv_driver = driver_metrics.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Driver Metrics CSV", csv_driver, "driver_metrics.csv", "text/csv")
    else:
        st.warning("No driver data available for selected date range.")

except Exception as e:
    st.error(f"Error processing driver data: {e}")

# -------------------------------
# 3. REVENUE & PAYMENT PERFORMANCE
# -------------------------------

st.header("Revenue by City & Hub")

revenue_query = """
SELECT
  h.hub_city AS city,
  h.hub_name AS hub,
  COUNT(o.order_id) AS total_orders,
  SUM(o.order_amount) AS total_revenue,
  ROUND(AVG(o.order_amount), 2) AS avg_payment_amount
FROM orders o 
JOIN stores s ON o.store_id = s.store_id
JOIN hubs h ON s.hub_id = h.hub_id
WHERE o.order_status = 'FINISHED'
AND DATE(
    o.order_created_year || '-' ||
    PRINTF('%02d', o.order_created_month) || '-' ||
    PRINTF('%02d', o.order_created_day)
) BETWEEN ? AND ?
GROUP BY h.hub_city, h.hub_name
ORDER BY h.hub_city;
"""

try:
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    revenue_df = pd.read_sql_query(revenue_query, conn, params=[start_date_str, end_date_str])
except Exception as e:
    st.error(f"Error executing revenue query: {e}")
    revenue_df = pd.DataFrame()
    
# KPI Summary for Revenue
kpi_query2 = """
SELECT
  COUNT(DISTINCT order_id) AS total_orders,
  SUM(order_amount) AS total_revenue,
  ROUND(AVG(order_amount), 2) AS avg_order_value
FROM orders 
WHERE order_status = 'FINISHED'
  AND DATE(
    order_created_year || '-' ||
    PRINTF('%02d', order_created_month) || '-' ||
    PRINTF('%02d', order_created_day)
) BETWEEN ? AND ?;
"""

try:
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    kpi_df2 = pd.read_sql_query(kpi_query2, conn, params=[start_date_str, end_date_str])
    if not kpi_df2.empty:
        total_orders_rev = int(kpi_df2['total_orders'].iloc[0]) if kpi_df2['total_orders'].iloc[0] else 0
        total_revenue = float(kpi_df2['total_revenue'].iloc[0]) if kpi_df2['total_revenue'].iloc[0] else 0.0
        avg_order_value = float(kpi_df2['avg_order_value'].iloc[0]) if kpi_df2['avg_order_value'].iloc[0] else 0.0
    else:
        total_orders_rev = 0
        total_revenue = 0.0
        avg_order_value = 0.0
except Exception as e:
    st.error(f"Error executing revenue KPI query: {e}")
    total_orders_rev = 0
    total_revenue = 0.0
    avg_order_value = 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders_rev:,}")
col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

# Revenue Table & Chart
if not revenue_df.empty:
    st.dataframe(revenue_df, use_container_width=True)

    st.subheader("Total Revenue by City and Hub")
    fig = px.bar(
        revenue_df,
        x="hub",
        y="total_revenue",
        color="city",
        text_auto='.2s',
        title="Total Revenue by Hub (Grouped by City)"
    )
    fig.update_layout(
        xaxis_title="Hub",
        yaxis_title="Total Revenue ($)",
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

    csv_revenue = revenue_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Revenue CSV", csv_revenue, "revenue_metrics.csv", "text/csv")
else:
    st.warning("No revenue data available for selected date range.")
