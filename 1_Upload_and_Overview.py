import streamlit as st
import pandas as pd
import os
import sys
from io import StringIO

st.set_page_config(layout="wide")

st.title("AI-Assisted Data Wrangler & Visualizer")

# Initialize session state
if 'df_history' not in st.session_state:
    st.session_state.df_history = []
if 'log' not in st.session_state:
    st.session_state.log = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

with st.sidebar:
    st.header("Upload your Data")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

    st.header("AI Assistant")
    st.session_state.api_key = st.text_input("Enter your AI API Key:", type="password", help="Your key is used for AI features and is not stored.")

    st.header("Session Management")
    if st.button("Reset Session"):
        st.session_state.df_history = []
        st.session_state.log = []
        st.rerun()

if uploaded_file is not None:
    try:
        # Get the file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]

        if file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(uploaded_file)
        elif file_extension == ".json":
            df = pd.read_json(uploaded_file)
        
        # Store the dataframe and initialize the log
        st.session_state.df_history = [df]
        st.session_state.log = []
        
        # We need to rerun to ensure the app state is updated immediately after upload
        st.rerun()

    except Exception as e:
        st.error(f"Error reading the file: {e}")

# Display the content if a dataframe is loaded
if st.session_state.df_history:
    df = st.session_state.df_history[-1]
    st.header("Data Overview")
    st.dataframe(df)

    st.header("Data Profile")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shape")
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.subheader("Duplicate Rows")
        st.write(f"Total duplicate rows: {df.duplicated().sum()}")

    with col2:
        st.subheader("Missing Values")
        missing_data = pd.DataFrame({
            'Missing Count': df.isnull().sum(),
            'Missing Percentage (%)': (df.isnull().sum() / df.shape[0]) * 100
        }).loc[lambda d: d['Missing Count'] > 0]
        st.dataframe(missing_data)
        
    st.subheader("Column Information")
    
    profile_data = []
    for col in df.columns:
        profile_data.append({
            "Column Name": col,
            "Data Type": str(df[col].dtype),
            "Non-Null Values": int(df[col].count()),
            "Filled (%)": f"{100 * df[col].count() / len(df):.2f}%"
        })
    profile_df = pd.DataFrame(profile_data)
    st.dataframe(profile_df)

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include='all'))
