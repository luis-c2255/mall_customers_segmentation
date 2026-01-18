import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

st.title("🤖 Predictive Modeling")

# --- 1. MODEL TRAINING LOGIC ---
# We perform this inside the app to show real-time metrics
df_model = df.copy() 
df_model["gender_male"] = (df_model["gender"] == "Male").astype(int) 

features = ["age", "annual_income_k", "gender_male"] 
target = "spending_score_(1-100)" 

X = df_model[features] 
y = df_model[target] 

X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size=0.2, random_state=42 
) 

# Linear Regression 
linreg = LinearRegression() 
linreg.fit(X_train, y_train) 
lr_score = linreg.score(X_test, y_test)

# Random Forest 
rf = RandomForestRegressor(n_estimators=200, random_state=42) 
rf.fit(X_train, y_train) 
rf_score = rf.score(X_test, y_test)

# --- 2. PERFORMANCE METRICS ---
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.metric(label="Linear Regression ($R^2$)", value=f"{lr_score:.3f}")
    
with col_m2:
    # We remove delta_description and keep it simple for compatibility
    st.metric(
        label="Random Forest (R²)", 
        value=f"{rf_score:.3f}", 
        delta=f"{rf_score - lr_score:.3f}"
    )
    st.caption("Delta shows improvement over Linear Regression") # Alternative to description

# --- 3. FEATURE IMPORTANCE & PREDICTION ---
col_plot, col_pred = st.columns([3, 2])

with col_plot:
    st.subheader("What drives Spending?")
    # Extract Feature Importances
    importances = pd.DataFrame({
        'Feature': features,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=True)

    fig_imp = px.bar(
        importances, 
        x='Importance', 
        y='Feature', 
        orientation='h',
        title="Random Forest Feature Importance",
        color_discrete_sequence=["#4cc9a6"]
    )
    fig_imp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_imp, use_container_width=True)

with col_pred:
    st.subheader("Test the Model")
    st.write("Simulate a customer to predict their Spending Score:")
    
    # User Inputs for Prediction
    in_age = st.slider("Age", 18, 70, 30)
    in_income = st.number_input("Annual Income (k$)", 15, 150, 50)
    in_gender = st.selectbox("Gender", ["Female", "Male"])
    
    # Prepare data for prediction
    gender_val = 1 if in_gender == "Male" else 0
    input_data = pd.DataFrame([[in_age, in_income, gender_val]], columns=features)
    
    # Predict using Random Forest
    prediction = rf.predict(input_data)[0]
    
    st.markdown(f"""
    ### Predicted Score: 
    ## <span style='color:#4cc9a6'>{prediction:.1f}</span> / 100
    """, unsafe_allow_html=True)
