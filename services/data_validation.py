import pandas as pd


def build_validation_report(df: pd.DataFrame) -> dict:
    """Build a basic validation report for an uploaded dataset."""
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    non_numeric_columns = df.select_dtypes(exclude="number").columns.tolist()

    report = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isna().sum().sum()),
        "duplicated_rows": int(df.duplicated().sum()),
        "numeric_columns": numeric_columns,
        "non_numeric_columns": non_numeric_columns,
    }

    return report