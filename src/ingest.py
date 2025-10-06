"""Moduł do wczytywania danych sprzedażowych (CSV)"""
import pandas as pd
from pathlib import Path


def read_sales_csv(path: str) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path)
    return df
