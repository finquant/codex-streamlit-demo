from abc import ABC, abstractmethod
import pandas as pd


class BaseModel(ABC):
    """Abstract base class for financial models."""

    @abstractmethod
    def fit(self, df: pd.DataFrame):
        """Train or fit the model using input data."""
        pass

    @abstractmethod
    def predict(self) -> pd.Series:
        """Return model predictions."""
        pass

    @abstractmethod
    def to_frame(self) -> pd.DataFrame:
        """Return results as a DataFrame for display/export."""
        pass