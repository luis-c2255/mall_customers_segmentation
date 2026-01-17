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

fig = px.bar(
    df["gender"].value_counts().reset_index(),
    x="index", y="gender",
    labels={"index": "Gender", "gender": "Count"},
    color_discrete_sequence=["#2EC4B6"]
)
st.plotly_chart(fig, use_container_width=True)
