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
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
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
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         dd360 and configuration for tools like black
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip install -r requirements.txt`
├── setup.cfg          <- Configuration file for flake8

```

--------

### 🧠 ¿Cómo definí “comparabilidad”?
Una propiedad es comparable si:

a) Se encuentra en la misma colonia.
b) Es del mismo tipo de propiedad (casa o departamento).
c) Tiene características numéricas similares (precio por metro cuadrado, # dormitorios, # baños,  antigüedad del inmueble y si tiene amenidades como gym o jardín).

Se usó un enfoque mixto:

Filtrado categórico por colonia y tipo y Distancia euclidiana entre variables numéricas normalizadas.

### 📊 Análisis Exploratorio
Se identificó que el precio varía significativamente entre colonias.

El tipo de propiedad tiene fuerte relación con otras variables (casas tienen más superficie, más jardín).

Variables como conservation_status, construction_surface y price presentan correlaciones importantes.

Muchas columnas tienen valores faltantes y la forma en cómo se van a imputar es llenándolas con la mediana de la colonia a la que pertenece el edificio.
Muchas columnas tienen outliers tambien, por lo que se les hará un tratamiento para normalizarlas o limitar sus rangos.

### 🛠️ Transformaciones / Feature Engineering

1. Se imputaron variables con la media
2. Se hizo tratamiento de outliers
3. Se crearon nuevas features con one hot encoding y otras simples como ratios i.e. price per m2

### ⚗️ Fase de Experimentación
Se probaron y compararon distintos enfoques para definir la similitud:

* get_similars_euclidean_standard: Distancia Euclidiana con Escalado Z-score

* get_similars_euclidean_minmax: Distancia Euclidiana con Escalado MinMax

* get_similars_hierarchical: Filtra por colonia y tipo de inmueble + Distancia Euclidiana con Escalado MinMax

* get_similars_combined_geo: Filtra por colonia y tipo de inmueble + Distancia Euclidiana y Geodesica (usando lat y lng) con Escalado MinMax

Se graficaron las métricas y se eligió el modelo con mejor score visual y lógico.

### 🤖 Algoritmo Final (get_similars_combined_geo)

1. Filtra por neighborhood y property_type.

2. Aplica escalado a variables seleccionadas.

3. Calcula la distancia euclidiana.

4. Ordena por menor distancia y devuelve las 5 más cercanas.

(Ver implementación completa en dd360_project/dd360/compare.py)

### 📉 Limitaciones y mejoras posibles
1. Actualmente se hicieron un par de experimentos con distancias euclidianas pero podría valer la pena probar con otros tipos de modelos más fancies
2. Se podrían evaluar otros métodos para checar la importancia de las variables y su impacto
3. Hacer un preprocesamiento más robusto como manejo de valores faltantes y outliers
4. Hacer un pipeline que automatice todo end to end, desde la extracción de datos hasta el cálculo de las 5 propiedades similares
5. Hacer pruebas unitarias

### 🧪 ¿Qué podría escalar mal?
1. Si el dataset crece mucho en tamaño o en cantidad de features, escalar todos los datos en memoria puede ser lento o consumir mucha RAM.
2. Métodos como distancia euclidiana o jerárquica sin optimizaciones pueden ser muy lentos para datasets grandes.
3. Si muchas propiedades tienen valores faltantes, la función puede tardar más o arrojar resultados poco fiables.
4. A mayor número de features para calcular la distancia, mayor será el costo computacional para cada comparación.


### 🧭 Conclusiones y recomendaciones
Este enfoque permite comparar propiedades de forma automática y rápida, ya que antes de calcular similitud se filtra por colonia y tipo de propiedad lo que eficientiza de manera increíble el calculo de las propiedades más similares. También, la estructura del proyecto es funcional y modular, lo que podría fácilmente permitir hacer mejores y pruebas.

Como recomendación:
1. Optimizar el cálculo de propiedades similares, talvez con estructuras de búsqueda eficientes (KDTree, BallTree).
2. Validar y limpiar mejor los datos.
3. Ampliar el análisis con técnicas modernas
4. Considerar integración en un entorno escalable (nube)

### BONUS

Se hizo un dashboard en streamlit para obtener las 5 propiedades más similares en función de 7 features. Puedes correr el proyecto como se indica abajo o puedes ver una prueba de cómo funcciona en reports/figures/webapp_*.jpg

# ▶️ Cómo instalar y correr el proyecto
```
## Clona el repositorio
1. git clone https://github.com/tu_usuario/cuauhtemoc-comparables.git

## Crea un ambiente de conda con python 3.9
2. cd dd360_project
3. conda create -n dd360 python=3.9
4. conda activate dd360

## Instala las dependencias
5. pip install poetry
6. pip install pre-commit
7. pre-commit install
8. pip install -r requirements.txt

## Lanza la app (dashboard)
9. streamlit run webapp/app.py
```
