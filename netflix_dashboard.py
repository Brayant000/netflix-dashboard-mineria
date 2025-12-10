import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Configuración de página
st.set_page_config(
    page_title="Dashboard Netflix - Minería de Datos",
    page_icon="🎬",
    layout="wide"
)

# Título principal
st.title("🎬 Dashboard de Análisis de Netflix")
st.markdown("---")

# Cargar datos con manejo de errores
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('netflix-titles.csv')
        # Limpieza básica
        df['director'] = df['director'].fillna('Desconocido')
        df['cast'] = df['cast'].fillna('Desconocido')
        df['country'] = df['country'].fillna('Desconocido')
        df['rating'] = df['rating'].fillna('NR')
        return df
    except FileNotFoundError:
        st.error("❌ Error: No se encontró el archivo 'netflix-titles.csv'")
        st.info("Asegúrate de que el archivo CSV esté en la misma carpeta que este script.")
        return None

df = load_data()

if df is not None:
    # ===== SECCIÓN 1: TOP 10 DIRECTORES =====
    st.header("1. Top 10 Directores con más Películas/Series")
    
    # Contar directores (excluyendo 'Desconocido')
    director_counts = df[df['director'] != 'Desconocido']['director'].value_counts().head(10)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig1 = px.bar(
            x=director_counts.values,
            y=director_counts.index,
            orientation='h',
            title="Top 10 Directores",
            labels={'x': 'Cantidad de Títulos', 'y': 'Director'},
            color=director_counts.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Datos")
        for i, (director, count) in enumerate(director_counts.items(), 1):
            st.metric(label=f"{i}. {director[:20]}...", value=count)
    
    st.markdown("---")
    
    # ===== SECCIÓN 2: SERIES vs PELÍCULAS =====
    st.header("2. Comparación: Series vs Películas")
    
    type_counts = df['type'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico circular
        fig2 = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Distribución por Tipo",
            color=type_counts.index,
            color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'},
            hole=0.3
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Gráfico de barras
        fig3 = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Cantidad por Tipo",
            labels={'x': 'Tipo', 'y': 'Cantidad'},
            color=type_counts.index,
            color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'},
            text=type_counts.values
        )
        fig3.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Métricas
        st.metric("Películas", type_counts.get('Movie', 0))
        st.metric("Series", type_counts.get('TV Show', 0))
    
    st.markdown("---")
    
    # ===== SECCIÓN 3: TOP 5 CATEGORÍAS =====
    st.header("3. Top 5 Categorías (listed_in)")
    
    # Separar categorías
    categories_series = df['listed_in'].dropna().str.split(', ').explode()
    top_categories = categories_series.value_counts().head(5)
    
    fig4 = px.bar(
        x=top_categories.values,
        y=top_categories.index,
        orientation='h',
        title="Top 5 Categorías con más Títulos",
        labels={'x': 'Cantidad de Títulos', 'y': 'Categoría'},
        color=top_categories.values,
        color_continuous_scale='Plasma',
        text=top_categories.values
    )
    fig4.update_traces(texttemplate='%{text}', textposition='outside')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
    
    # ===== SECCIÓN 4: RESUMEN GENERAL =====
    st.markdown("---")
    st.header("📊 Resumen General del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Títulos", len(df))
    
    with col2:
        st.metric("Películas", len(df[df['type'] == 'Movie']))
    
    with col3:
        st.metric("Series", len(df[df['type'] == 'TV Show']))
    
    with col4:
        st.metric("Años Cubiertos", f"{df['release_year'].min()} - {df['release_year'].max()}")
    
    # ===== SECCIÓN 5: VISTA DE DATOS =====
    st.markdown("---")
    st.header("📋 Vista Previa de los Datos")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        tipo_filtro = st.selectbox("Filtrar por tipo:", ["Todos", "Movie", "TV Show"])
    
    with col2:
        año_filtro = st.slider("Año de lanzamiento:", 
                               int(df['release_year'].min()), 
                               int(df['release_year'].max()),
                               (int(df['release_year'].min()), int(df['release_year'].max())))
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if tipo_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado['type'] == tipo_filtro]
    
    df_filtrado = df_filtrado[
        (df_filtrado['release_year'] >= año_filtro[0]) & 
        (df_filtrado['release_year'] <= año_filtro[1])
    ]
    
    # Mostrar datos filtrados
    st.dataframe(
        df_filtrado[['title', 'type', 'director', 'country', 'release_year', 'listed_in']].head(20),
        use_container_width=True
    )
    
    # Botón para descargar datos filtrados
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=csv,
        file_name='netflix_filtrado.csv',
        mime='text/csv'
    )
    
    # ===== PIE DE PÁGINA =====
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>Dashboard creado para Minería de Datos | Visual Studio Code | Streamlit</p>
    <p>Dataset: Netflix Titles | Total de registros: {}</p>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

else:
    # Si no hay datos, mostrar instrucciones
    st.warning("No se pudieron cargar los datos.")
    st.markdown("""
    ### Instrucciones:
    1. Asegúrate de que el archivo `netflix-titles.csv` esté en la misma carpeta
    2. Verifica que el nombre del archivo sea correcto
    3. Si el archivo tiene otro nombre, cámbialo a `netflix-titles.csv`
    """)

# Información de depuración (opcional)
with st.expander("🔧 Información de Sistema"):
    st.write(f"Python ejecutándose correctamente")
    st.write(f"Filas en dataset: {len(df) if df is not None else 'No cargado'}")
    st.write(f"Columnas: {list(df.columns) if df is not None else 'N/A'}")