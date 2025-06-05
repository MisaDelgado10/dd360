import pandas as pd
import numpy as np
from typing import Callable, Dict, List, Optional, Any
from dd360.config import FEATURE_SETS
import dd360.compare as compare  # Importa los métodos de comparación

class ExperimentScorer:
    """
    Clase para ejecutar y evaluar diferentes métodos de comparación de inmuebles
    sobre un DataFrame dado usando varios conjuntos de características.
    """

    def __init__(self, df: pd.DataFrame, n: int = 5) -> None:
        """
        Inicializa el experimentador con el DataFrame y número de similares a obtener.

        Args:
            df (pd.DataFrame): DataFrame con los datos de inmuebles.
            n (int, opcional): Número de resultados similares a considerar. Por defecto es 5.
        """
        self.df: pd.DataFrame = df.copy()
        self.n: int = n
        self.results: List[Dict[str, Any]] = []

        self.compare_methods: Dict[str, Callable] = {
            "euclidean_standard": compare.get_similars_euclidean_standard,
            "euclidean_minmax": compare.get_similars_euclidean_minmax,
            "hierarchical": compare.get_similars_hierarchical,
            "combined_geo": compare.get_similars_combined_geo,
        }

    def _build_input_dict(self, row: pd.Series, features: List[str]) -> Dict[str, Any]:
        """
        Construye un diccionario de entrada con las características relevantes de una fila.

        Args:
            row (pd.Series): Fila del DataFrame con los datos de un inmueble.
            features (List[str]): Lista de nombres de columnas a incluir como características.

        Returns:
            Dict[str, Any]: Diccionario con las características y valores presentes en la fila.
        """
        input_dict: Dict[str, Any] = {}
        for f in features + ["neighborhood", "property_type", "latitude", "longitude"]:
            if f in row and pd.notnull(row[f]):
                input_dict[f] = row[f]
        return input_dict

    def _scoring_fn(self, input_dict: Dict[str, Any], similars: List[Dict[str, Any]]) -> Optional[float]:
        """
        Calcula el puntaje promedio basado en la similitud de un conjunto de registros similares.

        Args:
            input_dict (Dict[str, Any]): Diccionario con las características del inmueble objetivo.
            similars (List[Dict[str, Any]]): Lista de diccionarios con resultados similares y sus scores.

        Returns:
            Optional[float]: Puntaje promedio de similitud o None si no hay valores válidos.
        """
        scores = [s["similarity_score"] for s in similars if pd.notnull(s.get("similarity_score"))]
        return np.mean(scores) if scores else None

    def run(self) -> None:
        """
        Ejecuta los experimentos para cada método de comparación y conjunto de características,
        calcula los puntajes promedio y almacena los resultados ordenados.
        """
        for method_name, compare_fn in self.compare_methods.items():
            for feature_set_name, features in FEATURE_SETS.items():
                print(f"🚀 Evaluando: {method_name} con features: {feature_set_name}")
                scores: List[Optional[float]] = []

                for _, row in self.df.iterrows():
                    try:
                        input_dict = self._build_input_dict(row, features)
                        similars_df = compare_fn(self.df, input_dict, self.n)
                        similars = similars_df.to_dict("records")
                        score = self._scoring_fn(input_dict, similars)
                        scores.append(score)
                    except Exception:
                        scores.append(None)

                avg_score = np.nanmean([s for s in scores if s is not None])
                self.results.append({
                    "method": method_name,
                    "features": feature_set_name,
                    "avg_score": avg_score
                })

        self.results_df = pd.DataFrame(self.results).sort_values("avg_score", ascending=True)  # Menor es mejor

    def get_results(self) -> pd.DataFrame:
        """
        Obtiene el DataFrame con los resultados de los experimentos.

        Returns:
            pd.DataFrame: DataFrame con columnas ["method", "features", "avg_score"] ordenado por avg_score ascendente.
        """
        return self.results_df
