import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🔍 Relationships")

col1, col2 = st.columns(2)

with col1:
    fig_age_spending = px.scatter(
        df, x="age", y="spending_score_(1-100)",
        color="gender",
        opacity=0.7,
        title="Spending Score by Age",
        color_discrete_sequence=["#4cc9a6", "#BD3085"],
        labels={'age': 'Age', 'spending_score_(1-100)': 'Spending Score'}
    )
    fig_age_spending.update_traces(marker=dict(size=10, line=dict(width=1, color='white')))
    fig_age_spending.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_age_spending, use_container_width=True)

with col2:

    fig_inc_spending = px.scatter(
        df, x='annual_income_k', y='spending_score_(1-100)',
        color='gender',
        opacity=0.7,
        title="Spending Score by Annual Income",
        color_discrete_sequence=['#4cc9a6', '#BD3085'],
        labels={'annual_income_k': 'Annual Income (k$)', 'spending_score_(1-100)': 'Spending Score'}
    )
    fig_inc_spending.update_traces(marker=dict(size=10, line=dict(width=1, color='white')))
    fig_inc_spending.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_inc_spending, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    fig_inc_gen = px.box(df, x='gender', y='annual_income_k',
        color='gender', points='all',
        title='Income comparison by Gender',
        color_discrete_sequence=["#4cc9a6", "#BD3085"],
        labels={'gender': 'Gender', 'annual_income_k': 'Annual Income (k$)'}
    )
    fig_inc_gen.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_inc_gen, use_container_width=True)

with col4:
    fig_spend_gen = px.box(df, x='gender', y='spending_score_(1-100)',
        color='gender', points='all', 
        title='Spending Score comparison by Gender',
        color_discrete_sequence=['#4cc9a6', '#BD3085'],
        labels={'gender': 'Gender', 'spending_score_(1-100)': 'Spending Score'}
    )
    fig_spend_gen.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_spend_gen, use_container_width=True)

st.divider()

# Seleccionamos solo las 3 numéricas: Age, Income, Spending Score
numeric_cols = ["age", "annual_income_k", "spending_score_(1-100)"]
corr = df[numeric_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    title="Correlation between Age, Incomes and Spending",
    color_continuous_scale='Viridis',
    labels=dict(color="Correlación")
)
fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_corr, use_container_width=True)
