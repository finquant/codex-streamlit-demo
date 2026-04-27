import numpy as np
import pandas as pd


def calculate_simple_return(
    df: pd.DataFrame,
    price_column: str,
    output_column: str = "simple_return"
) -> pd.DataFrame:
    """Calculate simple return from a selected price column."""
    result_df = df.copy()
    result_df[output_column] = result_df[price_column].pct_change()
    return result_df


def calculate_log_return(
    df: pd.DataFrame,
    price_column: str,
    output_column: str = "log_return"
) -> pd.DataFrame:
    """Calculate log return from a selected price column."""
    result_df = df.copy()

    if (result_df[price_column] <= 0).any():
        raise ValueError("Log return requires strictly positive price values.")

    result_df[output_column] = np.log(
        result_df[price_column] / result_df[price_column].shift(1)
    )

    return result_df