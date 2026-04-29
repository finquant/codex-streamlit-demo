import pandas as pd

def load_csv_from_upload(uploaded_file) -> pd.DataFrame:
    """Load a CSV uploaded through Streamlit's file_uploader."""
    return pd.read_csv(uploaded_file)

