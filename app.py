import streamlit as st
import pandas as pd

st.title("AI Data Quality Agent")

@st.cache_data
def load_data():
    return pd.read_csv("mock_data.csv")

df = load_data()
st.subheader("Raw Dataset")
st.dataframe(df)

st.subheader("Duplicate Records Detected")
duplicates = df[df.duplicated(keep=False)]
if not duplicates.empty:
    st.error(f"Found {len(duplicates)} duplicate rows.")
    st.dataframe(duplicates)
else:
    st.success("No duplicates found.")
