import streamlit as st
import pandas as pd
import os
from io import StringIO

st.set_page_config(layout="wide")

st.title("AI-Assisted Data Wrangler & Visualizer")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None

with st.sidebar:
    st.header("Upload your Data")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

    if st.button("Reset Session"):
        st.session_state.df = None
        if 'log' in st.session_state:
            st.session_state.log = None
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
        st.session_state.df = df
        st.session_state.log = []

    except Exception as e:
        st.error(f"Error reading the file: {e}")

# Display the content if a dataframe is loaded
if st.session_state.df is not None:
    df = st.session_state.df
    st.header("Data Overview")
    st.dataframe(df)

    st.header("Data Profile")
    
    # Display shape
    st.subheader("Shape")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Display column info
    st.subheader("Column Information")
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Display summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include='all'))

    # Display missing values
    st.subheader("Missing Values")
    missing_data = pd.DataFrame({
        'Missing Count': df.isnull().sum(),
        'Missing Percentage': (df.isnull().sum() / df.shape[0]) * 100
    })
    st.dataframe(missing_data)

    # Display duplicate count
    st.subheader("Duplicate Rows")
    st.write(f"Total duplicate rows: {df.duplicated().sum()}")

