import pandas as pd
from services.model_interface import BaseModel


class DummyReturnModel(BaseModel):
    """A simple model that returns the selected return column."""

    def __init__(self, column: str):
        self.column = column
        self.df = None

    def fit(self, df: pd.DataFrame):
        self.df = df.copy()

    def predict(self) -> pd.Series:
        return self.df[self.column]

    def to_frame(self) -> pd.DataFrame:
        return self.df[[self.column]].copy()