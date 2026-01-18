import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🧠 Behavioral Insights")

st.subheader("Profile Summary by Cluster")

# Lógica de agrupación
cluster_profile = df.groupby("cluster_3d").agg(
    count=("customerid", "count"),
    avg_age=("age", "mean"),
    avg_income=("annual_income_k", "mean"),
    avg_score=("spending_score_(1-100)", "mean"),
    male_share=("gender", lambda x: (x == "Male").mean())
).reset_index()

# Formateo para mostrar en Streamlit
st.dataframe(
    cluster_profile.style.format({
        'avg_age': '{:.1f}',
        'avg_income': '${:.1f}k',
        'avg_score': '{:.1f}',
        'male_share': '{:.1%}'
    }).background_gradient(cmap='Blues', subset=['count', 'avg_score']),
    use_container_width=True
)

st.divider()

# --- FILA DE CUADRANTES E INGRESOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Quadrant Analysis")
    
    # Cálculo de medianas
    income_median = df["annual_income_k"].median()
    score_median = df["spending_score_(1-100)"].median()

    # Gráfico de Cuadrantes
    fig_quad = px.scatter(
        df, x="annual_income_k", y="spending_score_(1-100)",
        color="quadrant",
        title="Income vs. Spending (Quadrants)",
        color_discrete_sequence=px.colors.qualitative.Set2,
        opacity=0.7
    )
    
    # Añadir líneas de mediana para definir los cuadrantes
    fig_quad.add_hline(y=score_median, line_dash="dash", line_color="grey", annotation_text="Median Income")
    fig_quad.add_vline(x=income_median, line_dash="dash", line_color="grey", annotation_text="Median Spending")
    
    fig_quad.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_quad, use_container_width=True)

with col2:
    st.subheader("Spending by Income Level")
    
    # Gráfico de Boxplot por Income Tier
    fig_tier = px.box(
        df, x="income_tier", y="spending_score_(1-100)",
        color="income_tier",
        title="Spending Score by Income Range",
        color_discrete_sequence=["#4cc9a6", "#5a6a7a", "#3a8dff"],
        category_orders={"income_tier": ["Low", "Medium", "High"]}
    )
    
    fig_tier.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tier, use_container_width=True)

# --- Métricas de Cuadrantes ---
st.write("### Quadrant Count")
q_counts = df["quadrant"].value_counts().reset_index()
q_counts.columns = ["Quadrant", "Amount of Customers"]

# Mostrar como columnas de métricas pequeñas
m1, m2, m3, m4 = st.columns(4)
quadrants_list = df["quadrant"].unique()
cols = [m1, m2, m3, m4]

for i, quad in enumerate(df["quadrant"].value_counts().index):
    count = df["quadrant"].value_counts()[quad]
    cols[i].metric(label=quad, value=count)
