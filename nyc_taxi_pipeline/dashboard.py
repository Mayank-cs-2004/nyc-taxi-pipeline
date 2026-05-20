import streamlit as st
import pandas as pd
import psycopg2
import boto3
import json
from config import DB_CONFIG

st.set_page_config(page_title="NYC Data & Crypto Hub", layout="wide")
st.title("📊 Enterprise Data Hub")
st.markdown("Powered by **Spark, Postgres, dbt, Airflow, and AWS S3**")

# --- TAB 1: NYC TAXI DATA (From Postgres) ---
st.header("🚕 NYC Taxi Analytics (from dbt)")

@st.cache_data(ttl=600)
def load_taxi_data():
    conn = psycopg2.connect(**DB_CONFIG)
    # Query the facts table dbt built for us!
    query = """
        SELECT pickup_day_of_week, COUNT(*) as trip_count, AVG(fare_amount) as avg_fare
        FROM analytics.fct_taxi_trips
        GROUP BY pickup_day_of_week
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    taxi_df = load_taxi_data()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trips by Day")
        st.bar_chart(taxi_df.set_index('pickup_day_of_week')['trip_count'])
        
    with col2:
        st.subheader("Average Fare by Day")
        st.line_chart(taxi_df.set_index('pickup_day_of_week')['avg_fare'])
except Exception as e:
    st.error(f"Postgres connection error: {e}")

st.divider()

# --- TAB 2: CRYPTO DATA (From AWS S3) ---
st.header("📈 Live Crypto Market (from AWS S3)")

@st.cache_data(ttl=60)
def load_s3_crypto_data():
    s3 = boto3.client('s3')
    bucket = "nyc-taxi-pipeline-kuro-2026"
    
    # Get the latest file in the raw/crypto/ folder
    objects = s3.list_objects_v2(Bucket=bucket, Prefix="raw/crypto/")
    if 'Contents' not in objects:
        return pd.DataFrame()
        
    # Sort by last modified
    latest_file = sorted(objects['Contents'], key=lambda x: x['LastModified'])[-1]['Key']
    
    # Read the JSON directly out of S3 into memory
    response = s3.get_object(Bucket=bucket, Key=latest_file)
    data = json.loads(response['Body'].read().decode('utf-8'))
    
    df = pd.DataFrame(data)
    return df[['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']]

try:
    crypto_df = load_s3_crypto_data()
    if not crypto_df.empty:
        # Format the numbers to look pretty
        crypto_df['current_price'] = crypto_df['current_price'].apply(lambda x: f"${x:,.2f}")
        crypto_df['market_cap'] = crypto_df['market_cap'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(crypto_df.head(20), use_container_width=True)
    else:
        st.info("No crypto data found in S3 yet. Run the Airflow DAG!")
except Exception as e:
    st.error(f"S3 connection error: {e}")
