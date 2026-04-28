import pandas as pd


def read_csv_file(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV file into a pandas DataFrame."""
    return pd.read_csv(uploaded_file)