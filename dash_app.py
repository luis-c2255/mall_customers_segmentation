import streamlit as st
import pandas as pd

st.markdown("""
    <style>
        /* Stylize the search input */
        div[data-testid="stSidebarNavSearch"] input {
            border: 1px solid #4cc9a6 !important;
            border-radius: 5px;
        }
        /* Highlight the navigation links to look like buttons */
        [data-testid="stSidebarNav"] ul {
            padding-top: 2rem;
        }
        [data-testid="stSidebarNav"] li {
            background-color: #1a2c42; /* Darker blue background */
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid #4cc9a6; /* Your Mint Leaf color */
            transition: 0.3s;
        }
        [data-testid="stSidebarNav"] li:hover {
            background-color: #4cc9a6;
            transform: translateX(5px);
        }
        [data-testid="stSidebarNav"] span {
            color: white !important;
            font-weight: bold;
        }

    </style>
""", unsafe_allow_html=True)

# 1. Page Configuration
st.set_page_config(
    page_title="Mall Customers Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# 2. Shared Data Loading
@st.cache_data
def load_data():
    return pd.read_csv("Mall_Customers_cleaned_with_clusters.csv")

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# 3. Define the Navigation Structure
pages = {
    "Overview": [
        st.Page("dash_app.py", title="Main Dashboard", icon="🏠", default=True),
    ],
    "Exploratory Analysis": [
        st.Page("pages/1_📊_Distributions.py", title="Distributions", icon="📊"),
        st.Page("pages/2_🔍_Relationships.py", title="Relationships", icon="🔍"),
    ],
    "Advanced Modeling": [
        st.Page("pages/3_🧭_Segmentation.py", title="Segmentation", icon="🎯"),
        st.Page("pages/4_🧠_Behavioral_Insights.py", title="Behavioral Insights", icon="🧠"),
        st.Page("pages/5_🤖_Modeling.py", title="Modeling", icon="🤖"),
    ]
}

# 4. Run Navigation with SEARCH enabled
# Setting position="sidebar" automatically adds the search bar at the top of the menu
pg = st.navigation(pages, position="sidebar")

# --- CUSTOM SIDEBAR ELEMENTS ---
# You can add a logo or branding above the search bar
with st.sidebar:
    st.markdown("### 🏬 Mall Analytics")
    st.caption("v1.2 | Data-Driven Insights")

# 5. Render Content
if pg.title == "Main Dashboard":
    df = st.session_state.df
    st.title("Mall Customers Analytics Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Age", f"{df.age.mean():.1f}")
    col2.metric("Average Income (k$)", f"{df.annual_income_k.mean():.1f}")
    col3.metric("Average Spending Score", f"{df['spending_score_(1-100)'].mean():.1f}")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)
else:
    pg.run()
