import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🧭 Customer Segmentation")
st.markdown("---")

st.subheader("Dynamic Segment Explorer")

col_radio, col_filter = st.columns([2, 1])

with col_radio:
    cluster_model = st.radio(
        "Select Clustering Model:",
        ["2D Segmentation (Income + Score)", "3D Segmentation (Age + Income + Score)"],
        horizontal=True
    )

# Determinar qué columna usar
active_col = 'cluster_2d' if "2D" in cluster_model else 'cluster_3d'

with col_filter:
    # Obtener lista de clusters únicos y añadir opción "Todos"
    cluster_options = ["All"] + sorted(df[active_col].unique().tolist())
    selected_cluster = st.selectbox("Isolate a Specific Cluster:", cluster_options)

# --- 2. FILTRADO DE DATOS ---
if selected_cluster == "All":
    filtered_df = df
    plot_opacity = 0.7
else:
    filtered_df = df[df[active_col] == selected_cluster]
    plot_opacity = 0.9 # Más sólido si está solo

fig_3d = px.scatter_3d(
    filtered_df, 
    x='age', 
    y='annual_income_k', 
    z='spending_score_(1-100)',
    color=active_col,
    title=f"3D View: {cluster_model} | Cluster: {selected_cluster}",
    color_discrete_sequence=px.colors.qualitative.Bold,
    opacity=plot_opacity,
    labels={active_col: "Cluster ID"}
)

# Ajuste de estilo y animaciones de transición
fig_3d.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)', 
    scene=dict(xaxis_title='Age', yaxis_title='Annual Income (k$)', zaxis_title='Spending Score'),
    transition={'duration': 500}
)
st.plotly_chart(fig_3d, use_container_width=True)

# --- 3. CLUSTER PROFILING ---
if selected_cluster != "All":
    st.success(f"### 💡 Cluster {selected_cluster} Insights")
    m1, m2, m3 = st.columns(3)
    
    avg_age = filtered_df['age'].mean()
    avg_inc = filtered_df['annual_income_k'].mean()
    avg_score = filtered_df['spending_score_(1-100)'].mean()
    
    m1.metric("Avg. Age", f"{avg_age:.1f} years")
    m2.metric("Avg. Income", f"${avg_inc:.1f}k")
    m3.metric("Avg. Spending Score", f"{avg_score:.1f}/100")
    
    # Download Button for the isolated cluster
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download Data for Cluster {selected_cluster}",
        data=csv,
        file_name=f'cluster_{selected_cluster}_data.csv',
        mime='text/csv',
    )

st.markdown("---")

st.markdown("---")

st.subheader("Dynamic Segment Explorer")

col_radio, col_filter = st.columns([2, 1])

with col_radio:
    cluster_model = st.radio(
        "Select Clustering Model:",
        ["2D Segmentation (Income + Score)", "3D Segmentation (Age + Income + Score)"],
        horizontal=True
    )

# Determinar qué columna usar
active_col = 'cluster_2d' if "2D" in cluster_model else 'cluster_3d'

with col_filter:
    # Obtener lista de clusters únicos y añadir opción "Todos"
    cluster_options = ["All"] + sorted(df[active_col].unique().tolist())
    selected_cluster = st.selectbox("Isolate a Specific Cluster:", cluster_options)

# --- 2. FILTRADO DE DATOS ---
if selected_cluster == "All":
    filtered_df = df
    plot_opacity = 0.7
else:
    filtered_df = df[df[active_col] == selected_cluster]
    plot_opacity = 0.9 # Más sólido si está solo

fig_3d = px.scatter_3d(
    filtered_df, 
    x='age', 
    y='annual_income_k', 
    z='spending_score_(1-100)',
    color=active_col,
    title=f"3D View: {cluster_model} | Cluster: {selected_cluster}",
    color_discrete_sequence=px.colors.qualitative.Bold,
    opacity=plot_opacity,
    labels={active_col: "Cluster ID"}
)

# Ajuste de estilo y animaciones de transición
fig_3d.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)', 
    scene=dict(xaxis_title='Age', yaxis_title='Annual Income (k$)', zaxis_title='Spending Score'),
    transition={'duration': 500}
)
st.plotly_chart(fig_3d, use_container_width=True)

# --- 3. CLUSTER PROFILING ---
if selected_cluster != "All":
    st.success(f"### 💡 Cluster {selected_cluster} Insights")
    m1, m2, m3 = st.columns(3)
    
    avg_age = filtered_df['age'].mean()
    avg_inc = filtered_df['annual_income_k'].mean()
    avg_score = filtered_df['spending_score_(1-100)'].mean()
    
    m1.metric("Avg. Age", f"{avg_age:.1f} years")
    m2.metric("Avg. Income", f"${avg_inc:.1f}k")
    m3.metric("Avg. Spending Score", f"{avg_score:.1f}/100")
    
    # Download Button for the isolated cluster
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download Data for Cluster {selected_cluster}",
        data=csv,
        file_name=f'cluster_{selected_cluster}_data.csv',
        mime='text/csv',
    )

st.markdown("---")

X_2d = df[["annual_income_k", "spending_score_(1-100)"]].copy()
X_3d = df[["age", "annual_income_k", "spending_score_(1-100)"]].copy()

scaler_2d = StandardScaler()
X_2d_scaled = scaler_2d.fit_transform(X_2d)

scaler_3d = StandardScaler()
X_3d_scaled = scaler_3d.fit_transform(X_3d)

# --- FILA 1: Método del Codo y Métricas ---
col3, col4 = st.columns(2)

with col3:
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

with col4:
    # Cálculos de Silhouette
    sil_2d = silhouette_score(X_2d_scaled, df["cluster_2d"])
    sil_3d = silhouette_score(X_3d_scaled, df["cluster_3d"])
    
    # Mostramos las métricas como tarjetas interactivas
    st.metric(label="Silhouette Score (2D)", value=f"{sil_2d:.3f}", delta="k=5")
    st.metric(label="Silhouette Score (3D)", value=f"{sil_3d:.3f}", delta="k=5")
    
    st.info("A score close to 1 indicates that the clusters are well separated.")

st.divider()

# --- FILA 2: Visualización de Clusters ---
col5, col6 = st.columns(2)

with col5:
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

with col6:
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
