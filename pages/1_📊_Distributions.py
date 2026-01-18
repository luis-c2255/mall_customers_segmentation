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

fig_bar = px.bar(
    gender_counts,
    x='gender',
    y='count',
    title='Customer Distribution by Gender',
    labels={'gender': 'Gender', 'count': 'Total Customers'},
    color='gender',
    color_discrete_sequence=['#4cc9a6', '#5a6a7a'],
    opacity=0.85
)
fig_bar.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)    
fig_bar.update_layout(
    margin=dict(t=50, b=50, l=25, r=25),
    hovermode="x unified", # Crea una línea vertical de guía al pasar el mouse
    # Esto hace que las barras crezcan suavemente al cargar
    transition={'duration': 1000, 'easing': 'cubic-in-out'}
)
st.plotly_chart(fig_bar, use_container_width=True)
