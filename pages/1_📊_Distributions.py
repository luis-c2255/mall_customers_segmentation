import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("📊 Distributions")

numeric_cols = ["age", "annual_income_k", "spending_score_(1-100)"]

for col in numeric_cols:
    fig = px.histogram(
        df, x=col, nbins=20, marginal="box",
        color_discrete_sequence=["#1F6FEB"]
    )
    st.plotly_chart(fig, use_container_width=True)

gender_counts = df['gender'].value_counts().reset.index()

fig = px.bar(
    gender_counts,
    x='gender',
    y='count',
    labels={'gender': 'Gender', 'count': 'Count'},
    color='gender',
    color_discrete_sequence=['#4cc9a6', '#5a6a7a']
)

st.plotly_chart(fig, use_container_width=True)
