import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Codex Streamlit Demo",
    layout="wide"
)

st.title("Codex Streamlit Demo")
st.markdown(
    """
    This application demonstrates an interactive workflow for CSV-based data analysis.
    Users can upload a dataset, choose variables, control the number of displayed rows,
    select a chart type, and apply a simple threshold-based decision rule.
    """
)

st.sidebar.header("Control Panel")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

show_preview = st.sidebar.checkbox("Show data preview", value=True)
show_summary = st.sidebar.checkbox("Show summary statistics", value=True)
show_plot = st.sidebar.checkbox("Show visualization", value=True)
show_threshold = st.sidebar.checkbox("Show threshold analysis", value=True)

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

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if show_preview:
        st.subheader("Data Preview")

        number_of_rows = st.slider(
            "Number of rows to display",
            min_value=2,
            max_value=min(100, len(df)),
            value=min(10, len(df))
        )

        st.dataframe(df.head(number_of_rows))

    if show_summary:
        st.subheader("Summary Statistics")

        if len(numeric_columns) == 0:
            st.warning("No numeric columns were found for summary statistics.")
        else:
            st.dataframe(df[numeric_columns].describe())

    if show_plot:
        st.subheader("Visualization")

        if len(numeric_columns) == 0:
            st.warning("No numeric columns were found in the uploaded file.")
        else:
            selected_column = st.selectbox(
                "Select a numeric column",
                numeric_columns
            )

            chart_type = st.radio(
                "Select chart type",
                ["Line chart", "Histogram"]
            )

            fig, ax = plt.subplots()

            if chart_type == "Line chart":
                ax.plot(df[selected_column])
                ax.set_xlabel("Observation")
                ax.set_ylabel(selected_column)
                ax.set_title(f"Line Chart of {selected_column}")

            elif chart_type == "Histogram":
                ax.hist(df[selected_column].dropna(), bins=20)
                ax.set_xlabel(selected_column)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Histogram of {selected_column}")

            st.pyplot(fig)

    if show_threshold:
        st.subheader("Threshold Analysis")

        if len(numeric_columns) == 0:
            st.warning("No numeric columns were found for threshold analysis.")
        else:
            threshold_column = st.selectbox(
                "Select a column for threshold analysis",
                numeric_columns,
                key="threshold_column"
            )

            default_threshold = float(df[threshold_column].mean())

            threshold_value = st.number_input(
                "Set threshold value",
                value=default_threshold
            )

            above_threshold = df[threshold_column] > threshold_value
            count_above = int(above_threshold.sum())
            ratio_above = count_above / len(df)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Observations Above Threshold", count_above)

            with col2:
                st.metric("Ratio Above Threshold", f"{ratio_above:.2%}")

            result_df = df.copy()
            result_df["above_threshold"] = above_threshold

            st.dataframe(result_df.head(20))