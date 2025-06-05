import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
from bs4 import BeautifulSoup
from streamlit_folium import st_folium
from dd360.compare import get_similars_hierarchical
from dd360.extract import extract_data

@st.cache_data(show_spinner=False)
def obtener_imagen_principal(url: str) -> str:
    """
    Extrae la imagen principal (meta og:image) de un anuncio de propiedad.

    Args:
        url (str): URL del anuncio web.

    Returns:
        str: URL de la imagen encontrada o una imagen por defecto si no se encuentra o hay un error.
    """
    try:
        if not url or not isinstance(url, str):
            return "https://cdn.prod.website-files.com/61e9b342b016364181c41f50/63e6833197ca517367b6be46_6%20(1).png"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                img_url = og_image["content"]
                if img_url and img_url.strip():
                    return img_url
    except Exception as e:
        st.write(f"⚠️ Error obteniendo imagen de {url}: {e}")
    return "https://cdn.prod.website-files.com/61e9b342b016364181c41f50/63e6833197ca517367b6be46_6%20(1).png"

# --- Carga de datos procesados ---
df = extract_data("../data/processed/final_df.parquet")

# --- Interfaz de usuario ---
st.title("Encuentra propiedades similares 🏘️")
st.markdown("Selecciona las características de la propiedad que buscas y te mostraremos las más similares.")

with st.form("comparables_form"):
    neighborhood = st.selectbox("Colonia", sorted(df["neighborhood"].unique()))
    property_type = st.selectbox("Tipo", df["property_type"].unique())

    # Sliders para filtros numéricos
    min_price, max_price = int(df["price_per_m2"].min()), int(df["price_per_m2"].max())
    price_per_m2 = st.slider("Precio por m²", min_price, max_price, int(df["price_per_m2"].min()), format="$%d")

    min_beds, max_beds = int(df["num_bedrooms"].min()), int(df["num_bedrooms"].max())
    num_bedrooms = st.slider("Dormitorios", min_beds, max_beds, int(df["num_bedrooms"].min()))

    min_baths, max_baths = int(df["num_bathrooms"].min()), int(df["num_bathrooms"].max())
    num_bathrooms = st.slider("Baños", min_baths, max_baths, int(df["num_bathrooms"].min()))

    min_age, max_age = int(df["age"].min()), int(df["age"].max())
    age = st.slider("Antigüedad del inmueble en años", min_age, max_age, int(df["age"].min()))

    amenities_option = st.radio("¿Con amenidades? (gym o jardín)", ["Sí", "No"])
    has_amenities = 1 if amenities_option == "Sí" else 0

    submitted = st.form_submit_button("Buscar comparables")

# --- Lógica para buscar propiedades comparables ---
if submitted:
    input_data = {
        "neighborhood": neighborhood,
        "property_type": property_type,
        "price_per_m2": price_per_m2,
        "num_bedrooms": num_bedrooms,
        "num_bathrooms": num_bathrooms,
        "age": age,
        "has_amenities": has_amenities,
    }

    # Obtener propiedades similares usando búsqueda jerárquica
    comparables = get_similars_hierarchical(df, input_data)
    comparables = comparables.head(5)  # limitar a máximo 5

    # Guardar comparables e imágenes en session_state
    st.session_state["comparables"] = comparables

    imagenes = []
    for _, row in comparables.iterrows():
        img_url = obtener_imagen_principal(row["url_ad"])
        imagenes.append(img_url)
    st.session_state["imagenes"] = imagenes

# --- Mostrar resultados si existen en session_state ---
if "comparables" in st.session_state and "imagenes" in st.session_state:
    comparables = st.session_state["comparables"]
    imagenes = st.session_state["imagenes"]

    st.markdown("### 🏡 Propiedades similares:")
    for i, (_, row) in enumerate(comparables.iterrows()):
        title_str = f"{row['property_type']} con {row['num_bedrooms']} recámaras en {row['neighborhood']}"
        st.markdown(f"**[{title_str}]({row['url_ad']})**")
        st.image(imagenes[i], width=300)
        st.markdown(f"- Precio: ${int(row['price']):,}")
        st.markdown(f"- Superficie: {row['total_surface']} m²")
        st.markdown("---")

    # Mapa con ubicación de propiedades
    st.markdown("### 🗺️ Mapa:")
    m = folium.Map(location=[comparables.iloc[0]['latitude'], comparables.iloc[0]['longitude']], zoom_start=14)

    marker_cluster = MarkerCluster().add_to(m)
    for _, row in comparables.iterrows():
        title_str = f"{row['property_type']} en {row['neighborhood']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<a href='{row['url_ad']}' target='_blank'>{title_str}</a>",
            tooltip=row['neighborhood']
        ).add_to(marker_cluster)

    st_folium(m, width=700, height=500)
