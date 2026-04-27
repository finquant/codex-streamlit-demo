import pandas as pd


def convert_dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to CSV bytes for Streamlit download."""
    return df.to_csv(index=False).encode("utf-8-sig")