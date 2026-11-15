import streamlit as st
import pandas as pd

st.title("AI Data Quality Agent")
st.write("Scanning for duplicate, missing, inconsistent, and suspicious data...")

# We removed the cache line here so your data updates instantly!
def load_data():
    return pd.read_csv("mock_data.csv")

df = load_data()

st.subheader("1. Raw Dataset")
st.dataframe(df)

# --- 1. DUPLICATE DATA ---
st.subheader("2. Duplicate Records Detected")
duplicates = df[df.duplicated(keep=False)]
if not duplicates.empty:
    st.error(f"Found {len(duplicates)} duplicate rows.")
    st.dataframe(duplicates)
    st.info("💡 Recommendation: Keep the first scan and delete the exact duplicates to prevent double-counting attendance.")
else:
    st.success("No duplicates found.")

# --- 2. MISSING DATA ---
st.subheader("3. Missing Data Detected")
missing_data = df[df.isnull().any(axis=1)]
if not missing_data.empty:
    st.warning(f"Found {len(missing_data)} rows with missing fields.")
    st.dataframe(missing_data)
    st.info("💡 Recommendation: Fill missing 'Status' with 'Unknown', or drop the row entirely if the 'Timestamp' is missing.")
else:
    st.success("No missing values found.")

# --- 3. SUSPICIOUS / INCONSISTENT DATA ---
st.subheader("4. Suspicious or Inconsistent Data")
# Checking for weird data, like unrecognized scanner locations
if 'Scanner_Location' in df.columns:
    # Flag anything that isn't a standard Gate
    suspicious = df[~df['Scanner_Location'].isin(['Gate_A', 'Gate_B', 'Gate_C']) & df['Scanner_Location'].notnull()]
    if not suspicious.empty:
        st.error(f"Found {len(suspicious)} rows with unrecognized Scanner Locations.")
        st.dataframe(suspicious)
        st.info("💡 Recommendation: Verify if a new scanner was installed. If not, this is a hardware glitch and the records should be quarantined.")
    else:
        st.success("No suspicious locations found.")
