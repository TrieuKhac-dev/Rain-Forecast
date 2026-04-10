import numpy as np
import pandas as pd


def load_csv_as_dataframe(path: str) -> pd.DataFrame:
    """Đọc CSV và trả về DataFrame"""
    return pd.read_csv(path)


def load_csv_as_numpy(path: str, delimiter: str = ",") -> np.ndarray:
    """Đọc CSV và trả về NumPy array"""
    return np.loadtxt(path, delimiter=delimiter, skiprows=1)
