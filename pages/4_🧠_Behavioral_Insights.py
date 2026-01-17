import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🧠 Behavioral Insights")

fig = px.scatter(
    df,
    x="annual_income_k",
    y="spending_score_(1-100)",
    color="quadrant",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig, use_container_width=True)
