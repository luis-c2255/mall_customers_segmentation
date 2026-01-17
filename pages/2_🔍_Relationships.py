import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🔍 Relationships")

fig = px.scatter(
    df, x="annual_income_k", y="spending_score_(1-100)",
    color="genre",
    color_discrete_sequence=["#1F6FEB", "#2EC4B6"]
)
st.plotly_chart(fig, use_container_width=True)

fig = px.imshow(
    df[["age", "annual_income_k", "spending_score_(1-100)"]].corr(),
    color_continuous_scale="Teal"
)
st.plotly_chart(fig, use_container_width=True)
