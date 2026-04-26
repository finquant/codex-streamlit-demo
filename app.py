import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from services.data_validation import build_validation_report

from services.data_analysis import (
    get_dataset_overview,
    get_numeric_columns,
    get_summary_statistics,
    run_threshold_analysis
)


st.set_page_config(
    page_title="Codex Streamlit Demo",
    layout="wide"
)

st.title("Codex Streamlit Demo")
st.markdown(
    """
    This application demonstrates a controlled interactive workflow.
    Users can upload a CSV file, inspect the data, visualize numeric variables,
    and run a threshold analysis only after pressing a submit button.
    """
)

st.sidebar.header("Control Panel")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a CSV file from the sidebar to begin the analysis.")
else:
    try:
        df = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty. Please upload a CSV file with at least one data row.")
        st.stop()
    except Exception as exc:
        st.error(f"Could not read the uploaded CSV file: {exc}")
        st.stop()

    if df.empty:
        st.warning("The uploaded CSV file has no data rows. Please upload a CSV file with at least one data row.")
        st.stop()

    overview = get_dataset_overview(df)
    numeric_columns = get_numeric_columns(df)
    validation_report = build_validation_report(df)

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", overview["rows"])

    with col2:
        st.metric("Columns", overview["columns"])

    with col3:
        st.metric("Missing Values", overview["missing_values"])

    st.subheader("Data Validation Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Duplicated Rows", validation_report["duplicated_rows"])

    with col2:
        st.metric("Numeric Columns", len(validation_report["numeric_columns"]))

    with col3:
        st.metric("Non-numeric Columns", len(validation_report["non_numeric_columns"]))

    with st.expander("Show column type details"):
        st.write("Numeric columns")
        st.write(validation_report["numeric_columns"])

        st.write("Non-numeric columns")
        st.write(validation_report["non_numeric_columns"])

    st.subheader("Data Preview")

    if len(df) < 5:
        st.info("The uploaded CSV file has fewer than 5 rows. Displaying all available rows.")
        number_of_rows = len(df)
    else:
        number_of_rows = st.slider(
            "Number of rows to display",
            min_value=2,
            max_value=min(100, len(df)),
            value=min(10, len(df))
        )

    st.dataframe(df.head(number_of_rows))

    st.subheader("Summary Statistics")

    summary_df = get_summary_statistics(df)

    if summary_df.empty:
        st.warning("No numeric columns were found for summary statistics.")
    else:
        st.dataframe(summary_df)

    st.subheader("Visualization")

    if len(numeric_columns) == 0:
        st.warning("No numeric columns were found in the uploaded file.")
    else:
        selected_column = st.selectbox(
            "Select a numeric column for visualization",
            numeric_columns
        )

        chart_type = st.radio(
            "Select chart type",
            ["Line chart", "Histogram"],
            horizontal=True
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

        st.subheader("Threshold Analysis")

        with st.form("threshold_form"):
            threshold_column = st.selectbox(
                "Select a column for threshold analysis",
                numeric_columns
            )

            default_threshold = float(df[threshold_column].mean())

            threshold_value = st.number_input(
                "Set threshold value",
                value=default_threshold
            )

            submitted = st.form_submit_button("Run threshold analysis")

        if submitted:
            result_df, count_above, ratio_above = run_threshold_analysis(
                df=df,
                column=threshold_column,
                threshold=threshold_value
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Observations Above Threshold", count_above)

            with col2:
                st.metric("Ratio Above Threshold", f"{ratio_above:.2%}")

            st.subheader("Threshold Result Preview")
            st.dataframe(result_df.head(20))
        else:
            st.info("Set the threshold parameters and press the button to run the analysis.")
