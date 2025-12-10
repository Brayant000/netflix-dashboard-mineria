import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración básica
st.set_page_config(layout="wide")
st.title("🎬 Netflix Data Analysis Dashboard")

# Cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('netflix-titles.csv')
        df['director'] = df['director'].fillna('Unknown')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # 1. Top 10 Directors
    st.header("📊 1. Top 10 Directors")
    top_directors = df['director'].value_counts().head(10)
    fig1 = px.bar(
        x=top_directors.values,
        y=top_directors.index,
        orientation='h',
        title="Top 10 Directors with most titles"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2. Movies vs TV Shows
    st.header("🎥 2. Movies vs TV Shows")
    type_counts = df['type'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Count by Type"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # 3. Top Categories
    st.header("🏷️ 3. Top 5 Categories")
    categories = df['listed_in'].dropna().str.split(', ').explode()
    top_cats = categories.value_counts().head(5)
    fig4 = px.bar(
        x=top_cats.values,
        y=top_cats.index,
        orientation='h',
        title="Top 5 Categories"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Titles", len(df))
    col2.metric("Movies", len(df[df['type'] == 'Movie']))
    col3.metric("TV Shows", len(df[df['type'] == 'TV Show']))
    col4.metric("Data Points", f"{len(df):,}")
    
    # Data preview
    with st.expander("🔍 View Raw Data (first 10 rows)"):
        st.dataframe(df.head(10))
    
    st.markdown("---")
    st.caption("Created for Data Mining Project | Streamlit Cloud")