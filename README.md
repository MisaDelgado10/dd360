# dd360

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## 🏠 Reto de Data Science – Comparables Inmobiliarios en Cuauhtémoc, CDMX

📌 Objetivo

Desarrollar una función get_comparables() que, a partir de hasta 7 inputs simples, devuelva una lista con los url_ad de las 5 propiedades más similares (comparables) dentro del dataset proporcionado.
Se busca un enfoque claro, escalable y explicable sobre qué significa que las propiedades sean comparables.


## Contenido del repositorio

```
└── dd360   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes dd360 a Python module
    │
    ├── compare.py              <- has different functions to calculate similar buildings
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── experiments.py          <- This works as a testing file to produce an average similarity score of the functions in compare.py
    │
    ├── extract.py              <- This extracts data stored in the data/ folder
    │
    ├── feature_importance.py   <- It runs different experiments to see the most important variables (correlation, PCA, etc)
    │
    ├── features.py             <- Code to create new features for the similarity experiment
    │
    ├── transform.py             <- Code to imput missing values, trate outliers and standardize feature values
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models (not used in this stage)
    └── ├── train.py            <- Code to train models (not used in this stage)
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries (not used in this stage)
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         `1.EDA.ipynb`.
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         dd360 and configuration for tools like black
│
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip install -r requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8

```

--------

🧠 ¿Cómo definí “comparabilidad”?
Una propiedad es comparable si:

Se encuentra en la misma colonia.

Es del mismo tipo de propiedad (casa o departamento).

Tiene características numéricas similares (número de recámaras, superficie, estado de conservación, etc.).

Se usó un enfoque mixto:

Filtrado categórico por colonia y tipo.

Distancia euclidiana entre variables numéricas normalizadas.

📊 Análisis Exploratorio
Se identificó que el precio varía significativamente entre colonias.

El tipo de propiedad tiene fuerte relación con otras variables (casas tienen más superficie, más jardín).

Variables como conservation_status, construction_surface y price presentan correlaciones importantes.

🛠️ Transformaciones / Feature Engineering
Normalización de variables numéricas.

Imputación de valores nulos.

Ingeniería de variables como:

Densidad de construcción (construction_surface / terrain_surface)

Amenidades combinadas (has_gym o has_garden)

Filtrado previo por neighborhood y property_type para reducir ruido.

⚗️ Fase de Experimentación
Se probaron y compararon distintos enfoques para definir la similitud:

KNN con diferentes distancias.

PCA para reducir dimensiones.

Clustering (KMeans) para ver agrupaciones naturales.

Regresiones lineales para evaluar importancia de variables.

Se graficaron las métricas y se eligió el modelo con mejor score visual y lógico.

🤖 Algoritmo Final (get_comparables())
Filtra por neighborhood y property_type.

Aplica escalado a variables seleccionadas.

Calcula la distancia euclidiana.

Ordena por menor distancia y devuelve las 5 más cercanas.

Ver implementación completa en src/comparables.py.

📉 Limitaciones y mejoras posibles
Si hay pocas propiedades en una colonia, no se obtienen buenos comparables. Podría considerarse usar colonias cercanas con coordenadas geográficas.

Si el dataset crece mucho, se recomienda usar estructuras como KD-Trees para acelerar búsquedas.

Incorporar precios por m² o zonas de alta/baja plusvalía con información externa.

Usar modelos supervisados si se tuviera un target de comparabilidad real.

🧪 ¿Qué podría escalar mal?
Búsquedas lineales con muchos datos (>100,000) se vuelven lentas.

El filtrado por colonia puede limitar demasiado si hay pocos registros.

El uso de distancia euclidiana no captura relaciones no lineales entre variables.

🧭 Conclusiones y recomendaciones
Este enfoque permite comparar propiedades de forma automática y rápida, facilitando su uso en plataformas inmobiliarias, valuaciones o análisis de mercado.
El sistema puede escalar con mejoras de performance y enriquecimiento de datos externos (zonas, dinámicas históricas, etc.).

▶️ Cómo correr el proyecto
```
# 1. Clona el repositorio
git clone https://github.com/tu_usuario/cuauhtemoc-comparables.git
cd cuauhtemoc-comparables

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Ejecuta los notebooks o lanza la app (opcional)
streamlit run app/app.py
```
