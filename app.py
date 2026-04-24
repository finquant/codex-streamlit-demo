import streamlit as st
import pandas as pd

st.title("Codex Streamlit Demo")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())
else:
    st.info("Please upload a CSV file.")