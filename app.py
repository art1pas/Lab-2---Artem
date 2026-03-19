import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random
import time
st.set_page_config(page_title="A/B Testing: Chart Effectiveness", layout="centered")
st.title("📊 Data Viz A/B Testing Lab")
st.sidebar.header("⚙️ Configuration")
uploaded_file = st.sidebar.file_uploader("Upload a CSV dataset", type="csv")
@st.cache_data
def load_default_data():
    return sns.load_dataset('tips')
df = pd.read_csv(uploaded_file) if uploaded_file else load_default_data()
categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
if not categorical_cols or not numeric_cols:
    st.error("⚠️ The dataset needs at least one categorical and one numerical column to work.")
    st.stop()
cat_var = st.sidebar.selectbox("Categorical Variable (X-axis)", categorical_cols)
num_var = st.sidebar.selectbox("Numerical Variable (Y-axis)", numeric_cols)
st.header("The Business Question:")
st.info(f"**How does {num_var} vary across different {cat_var}s?**")
if 'chart_picked' not in st.session_state:
    st.session_state.chart_picked = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'time_taken' not in st.session_state:
    st.session_state.time_taken = None
if st.session_state.time_taken is not None or st.session_state.chart_picked is None:
    if st.button("Show one chart or the other (at random)"):
        st.session_state.chart_picked = random.choice(["A", "B"])
        st.session_state.start_time = time.time()
        st.session_state.time_taken = None
        st.rerun()
if st.session_state.chart_picked is not None and st.session_state.time_taken is None:
    st.divider()
    fig, ax = plt.subplots(figsize=(8, 5))
    if st.session_state.chart_picked == 'A':
        sns.barplot(data=df, x=cat_var, y=num_var, ax=ax, errorbar=None, palette="viridis")
        ax.set_title("Chart A")
    else:
        sns.boxplot(data=df, x=cat_var, y=num_var, ax=ax, palette="Set2")
        ax.set_title("Chart B")
    st.pyplot(fig)
    if st.button("Did I answer your question"):
        st.session_state.time_taken = time.time() - st.session_state.start_time
        st.rerun()
if st.session_state.time_taken is not None:
    st.success("Test completed! Thank you for your feedback.")
    st.metric(label=f"Time to answer using Chart {st.session_state.chart_picked}", value=f"{st.session_state.time_taken:.2f} seconds")