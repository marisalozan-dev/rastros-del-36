import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import plotly.express as px
import numpy as np

# ── Configuración de la página ──────────────────────────────
st.set_page_config(
    page_title="Rastros del 36",
    page_icon="🗂️",
    layout="wide"
)

# ── Estilos ──────────────────────────────────────────────────
st.markdown("""
<style>
.titulo { font-size: 2.5rem; font-weight: bold; color: #8B0000; }
.subtitulo { font-size: 1.1rem; color: #555; margin-bottom: 2rem; }
.metric-box { background: #f8f8f8; padding: 1rem; border-radius: 8px;
              border-left: 4px solid #8B0000; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect('rastros_del_36.db')
    df = pd.read_sql_query("SELECT * FROM personas", conn)
    df_fosas = pd.read_sql_query("SELECT * FROM fosas", conn)
    conn.close()
    return df, df_fosas

df, df_fosas = cargar_datos()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/320px-Flag_of_Spain.svg.png", width=100)
st.sidebar.title("🗂️ Rastros del 36")
st.sidebar.markdown("*Big Data aplicado a la Memoria Histórica de España*")
st.sidebar.markdown("---")

pagina = st.sidebar.radio("Navegar", [
    "🏠 Inicio",
    "🔍 Buscador de personas",
    "🗺️ Mapa interactivo",
    "📊 Análisis y visualizaciones",
    "📂 Sobre el proyecto"
])

# ══════════════════════════════════════════════════════════════
# PÁGINA 1 · INICIO
# ══════════════════════════════════════════════════════════════
if pagina == "🏠 Inicio":
    st.markdown('<p class="titulo">Rastros del 36</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo">Big Data aplicado a la Memoria Histórica de España</p>', unsafe_allow_html=True)

    st.markdown("""
    Esta plataforma reúne y cruza datos sobre las víctimas de la Guerra Civil española 
    y el exilio republicano, combinando técnicas de Big Data con criterio archivístico.
    """)

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Personas registradas", f"{len(df):,}")
    with col2:
        st.metric("⚔️ Víctimas documentadas", f"{len(df[df['tipo_registro']=='victima']):,}")
    with col3:
        st.metric("🚢 Exiliados del Stanbrook", f"{len(df[df['tipo_registro']=='exiliado']):,}")
    with col4:
        st.metric("🗺️ Fosas en Andalucía", f"{len(df_fosas):,}")

    st.markdown("---")
    st.markdown("### 📁 Fuentes de datos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Fase 1**\nVíctimas mortales de la Guerra Civil en Euskadi\n\n*Open Data Euskadi*")
    with col2:
        st.info("**Fase 2**\nFosas comunes de la Guerra Civil en Andalucía\n\n*Junta de Andalucía*")
    with col3:
        st.info("**Fase 3**\nPasajeros del Stanbrook (1939)\n\n*Fundación Pablo Iglesias*")

# ══════════════════════════════════════════════════════════════
# PÁGINA 2 · BUSCADOR
# ══════════════════════════════════════════════════════════════
elif pagina == "🔍 Buscador de personas":
    st.title("🔍 Buscador de personas")
    st.markdown("Busca por nombre, apellidos o profesión en los 23.981 registros de la base de datos.")

    col1, col2, col3 = st.columns(3)
    with col1:
        nombre_busq = st.text_input("Nombre")
    with col2:
        apellido_busq = st.text_input("Apellidos")
    with col3:
        tipo_busq = st.selectbox("Tipo de registro", ["Todos", "victima", "exiliado"])

    df_filtrado = df.copy()
    if nombre_busq:
        df_filtrado = df_filtrado[df_filtrado['nombre'].str.contains(nombre_busq, case=False, na=False)]
    if apellido_busq:
        df_filtrado = df_filtrado[df_filtrado['apellidos'].str.contains(apellido_busq, case=False, na=False)]
    if tipo_busq != "Todos":
        df_filtrado = df_filtrado[df_filtrado['tipo_registro'] == tipo_busq]

    st.markdown(f"**{len(df_filtrado):,} resultados encontrados**")

    columnas_mostrar = ['nombre', 'apellidos', 'edad', 'profesion', 
                        'tipo_registro', 'provincia_fallecimiento', 'causa_muerte', 'fuente']
    st.dataframe(df_filtrado[columnas_mostrar].head(100), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PÁGINA 3 · MAPA
# ══════════════════════════════════════════════════════════════
elif pagina == "🗺️ Mapa interactivo":
    st.title("🗺️ Mapa interactivo")

    coordenadas = {
        'Bizkaia': (43.263, -2.935), 'Gipuzkoa': (43.313, -1.975),
        'Araba/Álava': (42.847, -2.673), 'Asturias': (43.361, -5.859),
        'Cantabria': (43.183, -3.988), 'Burgos': (42.344, -3.697),
        'Madrid': (40.417, -3.704), 'Navarra': (42.695, -1.676),
        'Teruel': (40.346, -1.107), 'Lleida': (41.618, 0.620),
        'Tarragona': (41.119, 1.245), 'Barcelona': (41.385, 2.173),
        'Zaragoza': (41.656, -0.877), 'Rioja (La)': (42.287, -2.540),
        'Sevilla': (37.389, -5.985), 'Huelva': (37.261, -6.945),
        'Cádiz': (36.527, -6.289), 'Granada': (37.177, -3.599),
        'Málaga': (36.721, -4.421), 'Córdoba': (37.888, -4.779),
        'Jaén': (37.780, -3.785), 'Almería': (36.834, -2.464),
    }

    mapa = folium.Map(location=[40.0, -3.5], zoom_start=6, tiles='CartoDB positron')

    muertes = df[df['tipo_registro']=='victima']['provincia_fallecimiento'].value_counts()
    for prov, coords in coordenadas.items():
        vic = muertes.get(prov, 0)
        if vic > 0:
            folium.CircleMarker(
                location=coords, radius=np.log1p(vic) * 2.5,
                color='#d73027', fill=True, fill_color='#d73027', fill_opacity=0.6,
                tooltip=f"{prov}: {vic:,} víctimas"
            ).add_to(mapa)

    st_folium(mapa, width=1000, height=550)

# ══════════════════════════════════════════════════════════════
# PÁGINA 4 · ANÁLISIS
# ══════════════════════════════════════════════════════════════
elif pagina == "📊 Análisis y visualizaciones":
    st.title("📊 Análisis y visualizaciones")

    tab1, tab2, tab3 = st.tabs(["Causas de muerte", "Profesiones", "Edades"])

    with tab1:
        causas = df[df['tipo_registro']=='victima']['causa_muerte'].value_counts().head(10)
        fig = px.bar(causas, orientation='h', title="Top 10 causas de muerte — Euskadi",
                     color_discrete_sequence=['#d73027'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            prof_vic = df[df['tipo_registro']=='victima']['profesion'].value_counts().head(10)
            fig2 = px.bar(prof_vic, orientation='h', title="Profesiones — Víctimas",
                          color_discrete_sequence=['#d73027'])
            st.plotly_chart(fig2, use_container_width=True)
        with col2:
            prof_exi = df[df['tipo_registro']=='exiliado']['profesion'].value_counts().head(10)
            fig3 = px.bar(prof_exi, orientation='h', title="Profesiones — Exiliados",
                          color_discrete_sequence=['#2166ac'])
            st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        fig4 = px.histogram(
            df[df['edad'].between(1,90)], x='edad', color='tipo_registro',
            barmode='overlay', opacity=0.7,
            color_discrete_map={'victima': '#d73027', 'exiliado': '#2166ac'},
            title="Distribución de edades: víctimas vs exiliados"
        )
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PÁGINA 5 · SOBRE EL PROYECTO
# ══════════════════════════════════════════════════════════════
elif pagina == "📂 Sobre el proyecto":
    st.title("📂 Sobre el proyecto")
    st.markdown("""
    ### Rastros del 36
    Proyecto de Big Data aplicado a la Memoria Histórica de España.
    Combina técnicas de análisis de datos con criterio archivístico para 
    construir una plataforma de memoria histórica.

    ### Autora
    Archivera y analista de datos en formación.

    ### Tecnologías
    Python · Pandas · SQLite · Streamlit · Folium · Plotly · Jupyter

    ### Código fuente
    [GitHub — marisalozan-dev/rastros-del-36](https://github.com/marisalozan-dev/rastros-del-36)

    ### Fuentes de datos
    - Open Data Euskadi — Gobierno Vasco
    - Junta de Andalucía — Datos Abiertos
    - Fundación Pablo Iglesias — Lista Stanbrook
    """)