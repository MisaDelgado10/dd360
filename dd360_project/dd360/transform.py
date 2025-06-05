import pandas as pd
import numpy as np


def fill_numerical_with_group_median(df: pd.DataFrame, column: str, group_col: str) -> pd.Series:
    """
    Fill NaNs in a numerical column with the median value per group,
    falling back to overall median if needed.
    """
    group_median = df.groupby(group_col)[column].transform('median')
    return df[column].fillna(group_median).fillna(df[column].median())


def clip_upper_outliers(df: pd.DataFrame, column: str, upper_quantile: float = 0.99) -> pd.Series:
    """
    Clip values in a column above the specified upper quantile (default 99th percentile).
    """
    upper = df[column].quantile(upper_quantile)
    return np.where(df[column] > upper, upper, df[column])


def clean_property_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess property-level data without dropping rows.

    Parameters:
        df (pd.DataFrame): Raw property-level data.

    Returns:
        pd.DataFrame: Cleaned and preprocessed DataFrame.
    """
    df = df.copy()

    # --- Standardize string columns ---
    df['neighborhood'] = df['neighborhood'].str.upper().str.strip()
    df['property_type'] = df['property_type'].str.lower().str.strip()

    # --- Fill missing categorical values ---
    df['neighborhood'] = df['neighborhood'].fillna('SIN_DATO')
    df['property_type'] = df['property_type'].fillna('desconocido')

    # --- Handle numerical columns ---
    num_cols = [
        'construction_surface', 'terrain_surface',
        'num_bathrooms', 'num_parking_lots',
        'num_bedrooms', 'built_year', 'conservation_status'
    ]

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = fill_numerical_with_group_median(df, col, 'neighborhood')

    # --- Fill binary feature columns with 0 if missing ---
    for col in ['has_garden', 'has_gym']:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # --- Clip outliers instead of removing ---
    for col in ['price', 'construction_surface', 'terrain_surface']:
        if col in df.columns:
            df[col] = clip_upper_outliers(df, col)

    # --- Ensure proper integer types safely ---
    int_cols = ['num_bathrooms', 'num_bedrooms', 'num_parking_lots', 'built_year']
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
            df[col] = df[col].astype(int)

    # --- Reindex if property_id exists ---
    if 'property_id' in df.columns:
        df = df.set_index('property_id')

    return df
