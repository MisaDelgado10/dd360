# compare.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from geopy.distance import geodesic

def get_similars_euclidean_standard(df, input_dict, n=5):
    non_numeric_keys = {"neighborhood", "property_type"}
    features = [k for k in input_dict.keys() if k not in non_numeric_keys]

    df_sub = df[['property_id'] + features].dropna().copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_sub[features])

    input_vec = np.array([input_dict[f] for f in features]).reshape(1, -1)
    input_vec_scaled = scaler.transform(input_vec)[0]

    distances = np.linalg.norm(X_scaled - input_vec_scaled, axis=1)
    df_sub['similarity_score'] = distances

    return df_sub.sort_values('similarity_score').head(n)


def get_similars_euclidean_minmax(df, input_dict, n=5):
    non_numeric_keys = {"neighborhood", "property_type"}
    features = [k for k in input_dict.keys() if k not in non_numeric_keys]

    df_sub = df[['property_id'] + features].dropna().copy()

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df_sub[features])

    input_vec = np.array([input_dict[f] for f in features]).reshape(1, -1)
    input_vec_scaled = scaler.transform(input_vec)[0]

    distances = np.linalg.norm(X_scaled - input_vec_scaled, axis=1)
    df_sub['similarity_score'] = distances

    return df_sub.sort_values('similarity_score').head(n)


def get_similars_hierarchical(df, input_dict, n=5):
    df = df.copy()

    neighborhood = input_dict.get("neighborhood")
    prop_type = input_dict.get("property_type")

    non_numeric_keys = {"neighborhood", "property_type"}
    features = [k for k in input_dict.keys() if k not in non_numeric_keys]

    filters = [
        (df["neighborhood"] == neighborhood) & (df["property_type"] == prop_type),
        (df["neighborhood"] != neighborhood) & (df["property_type"] == prop_type),
        (df["property_type"] != prop_type)
    ]

    selected = pd.DataFrame()

    for condition in filters:
        candidates = df[condition].copy()
        if candidates.empty:
            continue

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(candidates[features])
        target_scaled = scaler.transform(np.array([input_dict[f] for f in features]).reshape(1, -1))
        distances = np.linalg.norm(scaled_data - target_scaled, axis=1)

        candidates["similarity_score"] = distances
        selected = pd.concat([selected, candidates])

        if len(selected) >= n:
            break

    return selected.sort_values("similarity_score").head(n)


def get_similars_combined_geo(df, input_dict, n=5):
    df = df.copy()

    if "neighborhood" not in input_dict or "property_type" not in input_dict:
        raise ValueError("input_dict debe contener 'neighborhood' y 'property_type'")

    if "latitude" not in input_dict or "longitude" not in input_dict:
        neigh_df = df[df["neighborhood"] == input_dict["neighborhood"]]
        input_dict["latitude"] = neigh_df["latitude"].mean()
        input_dict["longitude"] = neigh_df["longitude"].mean()

    non_numeric_keys = {"neighborhood", "property_type", "latitude", "longitude"}
    features = [k for k in input_dict.keys() if k not in non_numeric_keys]

    filters = [
        (df["neighborhood"] == input_dict["neighborhood"]) & (df["property_type"] == input_dict["property_type"]),
        (df["property_type"] == input_dict["property_type"]),
        (df["property_type"] != input_dict["property_type"])
    ]

    selected = pd.DataFrame()

    for condition in filters:
        candidates = df[condition].copy()
        if candidates.empty:
            continue

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(candidates[features])
        target_scaled = scaler.transform(np.array([input_dict[f] for f in features]).reshape(1, -1))

        num_distances = np.linalg.norm(X_scaled - target_scaled, axis=1)

        geo_distances = candidates.apply(
            lambda row: geodesic(
                (input_dict["latitude"], input_dict["longitude"]),
                (row["latitude"], row["longitude"])
            ).kilometers,
            axis=1
        )
        geo_distances_norm = geo_distances / geo_distances.max()

        total_score = 0.5 * num_distances + 0.5 * geo_distances_norm

        candidates["similarity_score"] = total_score
        selected = pd.concat([selected, candidates])

        if len(selected) >= n:
            break

    return selected.sort_values("similarity_score").head(n)
