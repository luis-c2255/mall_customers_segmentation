import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mall Customers Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

df = load_data()

st.title("Mall Customers Analytics Dashboard")
st.write("Explore customer demographics, spending behavior, segmentation, and predictive modeling.")

col1, col2, col3 = st.columns(3)
col1.metric("Average Age", f"{df.age.mean():.1f}")
col2.metric("Average Income (k$)", f"{df.annual_income_k.mean():.1f}")
col3.metric("Average Spending Score", f"{df['spending_score_(1-100)'].mean():.1f}")

st.subheader("Dataset Preview")
st.dataframe(df.head())
