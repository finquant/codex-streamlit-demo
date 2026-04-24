import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Codex Streamlit Demo",
    layout="wide"
)

st.title("Codex Streamlit Demo")
st.write(
    "This application demonstrates how to upload a CSV file, inspect the data, "
    "summarize numeric variables, and visualize a selected column."
)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to begin the analysis.")
else:
    df = pd.read_csv(uploaded_file)

    st.subheader("1. Data Preview")
    st.dataframe(df.head())

    st.subheader("2. Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isna().sum().sum()))

    st.subheader("3. Summary Statistics")
    st.dataframe(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    st.subheader("4. Visualization")

    if len(numeric_columns) == 0:
        st.warning("No numeric columns were found in the uploaded file.")
    else:
        selected_column = st.selectbox(
            "Select a numeric column to plot",
            numeric_columns
        )

        fig, ax = plt.subplots()
        ax.plot(df[selected_column])
        ax.set_title(f"Line Plot of {selected_column}")
        ax.set_xlabel("Observation")
        ax.set_ylabel(selected_column)

        st.pyplot(fig)