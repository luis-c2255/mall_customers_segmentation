import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🧭 Customer Segmentation")

# --- FILA 1: Método del Codo y Métricas ---
col1, col2 = st.columns(2)

with col1:
    # El código de tu lógica de inercia
    inertias = []
    K_range = range(2, 11)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        km.fit(X_2d_scaled) # Asegúrate de tener X_2d_scaled definido
        inertias.append(km.inertia_)
    
    # Gráfico interactivo con Plotly
    fig_elbow = px.line(
        x=list(K_range), y=inertias, 
        markers=True,
        labels={'x': 'Nunber of Clusters (k)', 'y': 'Inertia'},
        title='Elbow Method (2D: Income + Score)'
    )
    fig_elbow.update_traces(line_color='#4cc9a6', marker=dict(size=10, color='white'))
    fig_elbow.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_elbow, use_container_width=True)

with col2:
    # Cálculos de Silhouette
    sil_2d = silhouette_score(X_2d_scaled, df["cluster_2d"])
    sil_3d = silhouette_score(X_3d_scaled, df["cluster_3d"])
    
    # Mostramos las métricas como tarjetas interactivas
    st.metric(label="Silhouette Score (2D)", value=f"{sil_2d:.3f}", delta="k=5")
    st.metric(label="Silhouette Score (3D)", value=f"{sil_3d:.3f}", delta="k=5")
    
    st.info("A score close to 1 indicates that the clusters are well separated.")

st.divider()

# --- FILA 2: Visualización de Clusters ---
col3, col4 = st.columns(2)

with col3:
    # Usamos Plotly Express para el scatter de clusters
    fig_2d = px.scatter(
        df, x="annual_income_k", y="spending_score_(1-100)",
        color=df["cluster_2d"].astype(str),
        title="Segmentation: Income vs. Spending",
        color_discrete_sequence=px.colors.qualitative.Bold,
        opacity=0.8
    )
    fig_2d.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
    fig_2d.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title="Cluster")
    st.plotly_chart(fig_2d, use_container_width=True)

with col4:
    # Reducción de dimensionalidad PCA
    pca = PCA(n_components=2, random_state=42)
    X_3d_pca = pca.fit_transform(X_3d_scaled)
    pca_df = pd.DataFrame(X_3d_pca, columns=['PC1', 'PC2'])
    pca_df['cluster'] = df["cluster_3d"].astype(str)

    fig_pca = px.scatter(
        pca_df, x="PC1", y="PC2",
        color="cluster",
        title="PCA of Age, Incomes and Spending",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        opacity=0.8
    )
    fig_pca.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
    fig_pca.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title="Cluster")
    st.plotly_chart(fig_pca, use_container_width=True)
