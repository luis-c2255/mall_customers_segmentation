import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("📊 Distributions")

numeric_cols = ["age", "annual_income_k", "spending_score_(1-100)"]

for col in numeric_cols:
    clean_title = col.replace("_", " ").title()

    fig = px.histogram(
        df, x=col, nbins=20, marginal="box",
        title=f"Distribution of {clean_title}",
        color_discrete_sequence=["#4cc9a6"]
    )
    fig.update_traces(
        opacity=0.75,
        marker_line_width=1,
        marker_line_color='white'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=20,
        xaxis_title=clean_title,
        yaxis_title='Frequency',
        margin=dict(t=50, b=50, l=25, r=25),
        hovermode="x unified", # Crea una línea vertical de guía al pasar el mouse
        # Esto hace que las barras crezcan suavemente al cargar
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig, use_container_width=True)

gender_counts = df['gender'].value_counts().reset_index()

fig = px.bar(
    gender_counts,
    x='gender',
    y='count',
    title='Customer Distribution by Gender',
    labels={'gender': 'Gender', 'count': 'Total Customers'},
    color='gender',
    color_discrete_sequence=['#4cc9a6', '#5a6a7a'],
    opacity=0.85
)
fig.bar.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)    
fig.update_layout(
    margin=dict(t=50, b=50, l=25, r=25),
    hovermode="x unified", # Crea una línea vertical de guía al pasar el mouse
    # Esto hace que las barras crezcan suavemente al cargar
    transition={'duration': 1000, 'easing': 'cubic-in-out'}
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Visualización de Segmentos en 3D")

# Usamos tus columnas específicas
fig_3d = px.scatter_3d(
    df, 
    x='age', 
    y='annual_income_k', 
    z='spending_score_(1-100)',
    color='cluster_3d',      # Tu columna precalculada
    symbol='cluster_3d',     # Diferentes formas para cada cluster
    opacity=0.7,
    title="Análisis Espacial de Clientes",
    color_discrete_sequence=px.colors.qualitative.Bold # Paleta vibrante para modo oscuro
)

# Ajuste de estilo y animaciones de transición
fig_3d.update_layout(
    template="plotly_dark",
    margin=dict(l=0, r=0, b=0, t=40), # Aprovechar todo el ancho
    scene=dict(
        xaxis_title='Edad',
        yaxis_title='Ingresos ($k)',
        zaxis_title='Puntuación Gasto',
        # Fondo de los ejes para que combine con tu config.toml
        xaxis=dict(gridcolor="#2c3e50"),
        yaxis=dict(gridcolor="#2c3e50"),
        zaxis=dict(gridcolor="#2c3e50")
    ),
    # Esta es la animación de entrada suave
    transition={'duration': 1000, 'easing': 'back-in-out'}
)

# Mejoramos los puntos (traces) para que resalten
fig_3d.update_traces(
    marker=dict(size=5, line=dict(width=1, color='White')),
    selector=dict(mode='markers')
)

st.plotly_chart(fig_3d, use_container_width=True)