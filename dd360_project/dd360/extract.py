from pathlib import Path
from typing import Union

import pandas as pd


def extract_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Extract data from a CSV or Parquet file.

    Parameters
    ----------
    file_path : str or Path
        Path to the input data file (.csv or .parquet).

    Returns
    -------
    pd.DataFrame
        Data loaded into a pandas DataFrame.

    Raises
    ------
    ValueError
        If file extension is not supported.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.suffix.lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext == ".parquet":
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Only .csv and .parquet supported.")

    return df
