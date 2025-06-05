import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering on the cleaned property dataset.

    Parameters:
        df (pd.DataFrame): Cleaned DataFrame with raw features.

    Returns:
        pd.DataFrame: DataFrame with new engineered features.
    """
    df = df.copy()

    # --- Price per m2 (construction only) ---
    df["price_per_m2"] = df["price"] / df["construction_surface"]
    df["price_per_m2"] = df["price_per_m2"].replace([np.inf, -np.inf], np.nan)

    # --- Total surface (terrain + construction) ---
    df["total_surface"] = df["terrain_surface"].fillna(0) + df["construction_surface"].fillna(0)

    # --- Property age ---
    df["age"] = 2025 - df["built_year"]
    df["age"] = df["age"].clip(lower=0)  # evitar valores negativos por errores

    # --- Has amenities (either garden or gym) ---
    df["has_amenities"] = ((df["has_gym"] == 1) | (df["has_garden"] == 1)).astype(int)

    # --- Fill NaNs in numerical columns where 0 makes sense ---
    for col in ["terrain_surface", "num_bathrooms", "num_bedrooms", "num_parking_lots"]:
        df[col] = df[col].fillna(0)

    # --- One-hot encoding for categorical variables ---
    if "property_type" in df.columns:
        # Crear dummies aparte
        dummies = pd.get_dummies(df["property_type"], prefix="type").astype(float)
        
        # Concatenar con el DataFrame original
        df = pd.concat([df, dummies], axis=1)

    # --- One-hot encoding for categorical variables ---
    if "neighborhood" in df.columns:
        # Crear dummies aparte
        neigh_ohe = pd.get_dummies(df['neighborhood'], prefix='neigh').astype(float)
        
        # Concatenar con el DataFrame original
        df = pd.concat([df, neigh_ohe], axis=1)

    return df
