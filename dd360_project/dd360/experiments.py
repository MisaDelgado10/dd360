# experiments.py

import pandas as pd
import numpy as np
from typing import Callable
from dd360.config import FEATURE_SETS
import dd360.compare as compare  # Importa los métodos de comparación

class ExperimentScorer:
    def __init__(self, df: pd.DataFrame, n: int = 5):
        self.df = df.copy()
        self.n = n
        self.results = []

        self.compare_methods = {
            "euclidean_standard": compare.get_similars_euclidean_standard,
            "euclidean_minmax": compare.get_similars_euclidean_minmax,
            "hierarchical": compare.get_similars_hierarchical,
            "combined_geo": compare.get_similars_combined_geo,
        }

    def _build_input_dict(self, row, features):
        input_dict = {}
        for f in features + ["neighborhood", "property_type", "latitude", "longitude"]:
            if f in row and pd.notnull(row[f]):
                input_dict[f] = row[f]
        return input_dict

    # MODIFICACIÓN: usar similarity_score en vez de precio
    def _scoring_fn(self, input_dict, similars):
        scores = [s["similarity_score"] for s in similars if pd.notnull(s.get("similarity_score"))]
        return np.mean(scores) if scores else None

    def run(self):
        for method_name, compare_fn in self.compare_methods.items():
            for feature_set_name, features in FEATURE_SETS.items():
                print(f"🚀 Evaluando: {method_name} con features: {feature_set_name}")
                scores = []

                for _, row in self.df.iterrows():
                    try:
                        input_dict = self._build_input_dict(row, features)
                        similars_df = compare_fn(self.df, input_dict, self.n)
                        similars = similars_df.to_dict("records")
                        score = self._scoring_fn(input_dict, similars)
                        scores.append(score)
                    except Exception as e:
                        scores.append(None)

                avg_score = np.nanmean([s for s in scores if s is not None])
                self.results.append({
                    "method": method_name,
                    "features": feature_set_name,
                    "avg_score": avg_score
                })

        self.results_df = pd.DataFrame(self.results).sort_values("avg_score", ascending=True)  # Menor es mejor

    def get_results(self):
        return self.results_df
