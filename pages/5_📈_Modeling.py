import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("📈 Predictive Modeling")

st.write("Model results and feature importance.")

fig = px.bar(
    df[["age", "annual_income_k", "genre_male"]].corr()["annual_income_k"],
    color_discrete_sequence=["#1F6FEB"]
)
st.plotly_chart(fig, use_container_width=True)
