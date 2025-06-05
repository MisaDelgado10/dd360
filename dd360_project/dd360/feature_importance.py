import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import statsmodels.api as sm

class FeatureSelectionPipeline:
    def __init__(self, df_features: pd.DataFrame, target: pd.Series = None):
        self.df_features = df_features.copy()
        self.target = target
        self.scaler = StandardScaler()
        self.X_scaled = None
        self.pca = None

    def plot_correlations(self):
        corr_matrix = self.df_features.corr()
        plt.figure(figsize=(10,8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Matriz de Correlación entre Features')
        plt.show()

        if self.target is not None:
            corr_target = self.df_features.corrwith(self.target)
            print("\nCorrelación de cada feature con el target:")
            print(corr_target.sort_values(ascending=False))

    def run_pca(self):
        self.X_scaled = self.scaler.fit_transform(self.df_features)
        self.pca = PCA()
        self.pca.fit(self.X_scaled)

        plt.figure(figsize=(8,5))
        plt.plot(range(1, len(self.pca.explained_variance_ratio_) + 1),
                 self.pca.explained_variance_ratio_.cumsum(), marker='o')
        plt.xlabel('Número de componentes')
        plt.ylabel('Varianza explicada acumulada')
        plt.title('PCA - Varianza explicada')
        plt.grid(True)
        plt.show()

        loadings = pd.DataFrame(self.pca.components_.T,
                                columns=[f'PC{i+1}' for i in range(len(self.pca.components_))],
                                index=self.df_features.columns)
        print("\nLoadings (importancia de features en cada componente):")
        print(loadings)

    def run_clustering(self, max_clusters=10):
        if self.X_scaled is None:
            self.X_scaled = self.scaler.fit_transform(self.df_features)

        silhouette_scores = []
        for k in range(2, max_clusters+1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(self.X_scaled)
            score = silhouette_score(self.X_scaled, labels)
            silhouette_scores.append(score)
            print(f"Silhouette Score para {k} clusters: {score:.4f}")

        plt.figure(figsize=(8,5))
        plt.plot(range(2, max_clusters+1), silhouette_scores, marker='o')
        plt.xlabel('Número de clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Evaluación de clustering con diferentes k')
        plt.grid(True)
        plt.show()

    def select_features(self, df):
        """
        Separa las variables predictoras y la variable objetivo del DataFrame.
        Guarda en self.features y self.target.
        """
        cols_to_exclude = ['property_id', 'listing_type', 'property_type', 'url_ad', 'neighborhood']
        df = df.drop(columns=cols_to_exclude, errors='ignore')

        # Opcional: seleccionar solo columnas numéricas y bool (convertidas a float después)
        df = df.select_dtypes(include=[np.number, 'bool'])

        self.features = df
        self.target = df['price']  # o la variable objetivo que estés usando
        self.features = df.drop(columns=['price'])  # o cualquier otra columna que no quieras usar como feature

    def run_linear_regression(self):

        X = self.features
        y = self.target

        # Asegúrate de que X esté completamente en tipo float
        X = sm.add_constant(X)
        X = X.astype(float)

        model = sm.OLS(y, X).fit()
        print(model.summary())

    def run_regression_with_pca_components(self, n_components=5):
        if self.target is None:
            print("No hay target para regresión lineal.")
            return

        if self.pca is None:
            if self.X_scaled is None:
                self.X_scaled = self.scaler.fit_transform(self.df_features)
            self.pca = PCA(n_components=n_components)
            X_pca = self.pca.fit_transform(self.X_scaled)
        else:
            X_pca = self.pca.transform(self.X_scaled)[:, :n_components]

        X = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(n_components)])
        y = self.target

        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        print(f"\nRegresión con {n_components} componentes principales:")
        print(model.summary())
