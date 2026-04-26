import pandas as pd


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """Return basic dataset-level information."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isna().sum().sum())
    }


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return a list of numeric columns in the dataset."""
    return df.select_dtypes(include="number").columns.tolist()


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics for numeric columns."""
    numeric_columns = get_numeric_columns(df)

    if len(numeric_columns) == 0:
        return pd.DataFrame()

    return df[numeric_columns].describe()


def run_threshold_analysis(
    df: pd.DataFrame,
    column: str,
    threshold: float
) -> tuple[pd.DataFrame, int, float]:
    """Run a simple threshold analysis on a selected numeric column."""
    above_threshold = df[column] > threshold
    count_above = int(above_threshold.sum())
    ratio_above = count_above / len(df)

    result_df = df.copy()
    result_df["above_threshold"] = above_threshold

    return result_df, count_above, ratio_above