import numpy as np
import pandas as pd
import streamlit as st
from sidebar_utils import render_sidebar

# Render the shared sidebar
render_sidebar()

st.title("1. Upload and Overview")

# --- Initial Check ---
# Check if a dataframe exists in the session state, and stop if not.
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file using the sidebar to begin.")
    st.stop()

# Get the current dataframe, which is the last one in the history list
df = st.session_state.df_history[-1]

# --- Display Data and Profile ---
st.header("Data Overview")
st.info("Displaying the first 100 rows of the dataset.")
st.dataframe(df.head(100))

st.header("Data Profile")

# --- Metrics Row ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Number of Columns", value=df.shape[1])
with col2:
    st.metric(label="Number of Rows", value=df.shape[0])
with col3:
    st.metric(label="Duplicate Rows", value=df.duplicated().sum())

# --- Detailed Profile Section ---
st.subheader("Column Information & Missing Values")
missing_data = pd.DataFrame({
    'Missing Count': df.isnull().sum(),
    'Missing Percentage (%)': (df.isnull().sum() / df.shape[0]) * 100
})

profile_data = []
for col in df.columns:
    profile_data.append({
        "Column Name": col,
        "Data Type": str(df[col].dtype),
        "Non-Null Values": int(df[col].count()),
        "Filled (%)": f"{100 * df[col].count() / len(df):.2f}%",
        "Missing": f"{missing_data.loc[col, 'Missing Count']} ({missing_data.loc[col, 'Missing Percentage (%)']:.2f}%)"
    })
profile_df = pd.DataFrame(profile_data)
st.dataframe(profile_df)


# --- Summary Statistics ---
st.subheader("Numeric Column Statistics")
numeric_cols = df.select_dtypes(include=np.number)
if numeric_cols.empty:
    st.info("No numeric columns found in the dataset.")
else:
    st.write(numeric_cols.describe())

st.subheader("Categorical Column Statistics")
categorical_cols = df.select_dtypes(include=['object', 'category'])
if categorical_cols.empty:
    st.info("No categorical columns found in the dataset.")
else:
    st.write(categorical_cols.describe())
