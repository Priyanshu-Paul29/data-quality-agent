import streamlit as st
import pandas as pd

# Set page to be wide and look like a real dashboard
st.set_page_config(page_title="AI Data Quality Agent", layout="wide")

st.title("🚀 AI Data Quality Agent")
st.markdown("Upload raw hardware logs or use the default dataset to instantly detect anomalies.")

# --- SIDEBAR INTERFACE ---
st.sidebar.header("📁 Data Input")
uploaded_file = st.sidebar.file_uploader("Upload your own CSV file", type=["csv"])

# Load data based on user upload or fallback to your mock data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom file loaded successfully!")
else:
    df = pd.read_csv("mock_data.csv")
    st.sidebar.info("Using default mock data. Upload a file above to test your own data.")

# --- 0. RAW DATASET ---
st.subheader("📄 Raw Dataset")
st.dataframe(df, use_container_width=True)

st.divider()

# --- DASHBOARD METRICS ---
st.subheader("📊 Data Overview")
col1, col2, col3, col4 = st.columns(4)

duplicates_count = len(df[df.duplicated(keep=False)])
missing_count = len(df[df.isnull().any(axis=1)])
suspicious_count = len(df[~df['Scanner_Location'].isin(['Gate_A', 'Gate_B', 'Gate_C']) & df['Scanner_Location'].notnull()]) if 'Scanner_Location' in df.columns else 0

col1.metric("Total Rows Analyzed", len(df))
col2.metric("Duplicates Found", duplicates_count, delta_color="inverse")
col3.metric("Missing Fields", missing_count, delta_color="inverse")
col4.metric("Suspicious Scans", suspicious_count, delta_color="inverse")

st.divider()

# --- 1. DUPLICATE DATA ---
st.subheader("🔍 1. Duplicate Records Detected")
duplicates = df[df.duplicated(keep=False)]
if not duplicates.empty:
    st.error(f"Found {duplicates_count} duplicate rows.")
    st.dataframe(duplicates, use_container_width=True)
    st.info("💡 Recommendation: Keep the first scan and delete the exact duplicates to prevent double-counting attendance.")
else:
    st.success("No duplicates found.")

# --- 2. MISSING DATA ---
st.subheader("⚠️ 2. Missing Data Detected")
missing_data = df[df.isnull().any(axis=1)]
if not missing_data.empty:
    st.warning(f"Found {missing_count} rows with missing fields.")
    st.dataframe(missing_data, use_container_width=True)
    st.info("💡 Recommendation: Fill missing 'Status' with 'Unknown', or drop the row entirely if the 'Timestamp' is missing.")
else:
    st.success("No missing values found.")

# --- 3. SUSPICIOUS / INCONSISTENT DATA ---
st.subheader("🚨 3. Suspicious or Inconsistent Data")
if 'Scanner_Location' in df.columns:
    suspicious = df[~df['Scanner_Location'].isin(['Gate_A', 'Gate_B', 'Gate_C']) & df['Scanner_Location'].notnull()]
    if not suspicious.empty:
        st.error(f"Found {suspicious_count} rows with unrecognized Scanner Locations.")
        st.dataframe(suspicious, use_container_width=True)
        st.info("💡 Recommendation: Verify if a new scanner was installed. If not, this is a hardware glitch and the records should be quarantined.")
    else:
        st.success("No suspicious locations found.")
