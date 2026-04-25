import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Codex Streamlit Demo",
    page_icon="📊",
    layout="wide"
)

st.title("Codex Streamlit Demo")
st.markdown(
    """
    This web application demonstrates a basic workflow for CSV-based data analysis.
    Users can upload a dataset, inspect its structure, review summary statistics,
    and visualize selected numeric variables.
    """
)

st.sidebar.header("Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

show_preview = st.sidebar.checkbox("Show data preview", value=True)
show_summary = st.sidebar.checkbox("Show summary statistics", value=True)
show_plot = st.sidebar.checkbox("Show visualization", value=True)

if uploaded_file is None:
    st.info("Please upload a CSV file from the sidebar to begin the analysis.")
else:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isna().sum().sum()))

    if show_preview:
        st.subheader("Data Preview")
        st.dataframe(df.head())

    if show_summary:
        st.subheader("Summary Statistics")
        st.dataframe(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if show_plot:
        st.subheader("Visualization")

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