import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Cleaning & Preparation Studio")

# Check if a dataframe exists in the session state
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file on the 'Upload and Overview' page first.")
    st.stop()

# Initialize log if it doesn't exist
if 'log' not in st.session_state:
    st.session_state.log = []

# Get the current dataframe from the end of the history
df = st.session_state.df_history[-1]

# --- Sidebar for Undo ---
with st.sidebar:
    st.header("History")
    if st.button("Undo Last Action", use_container_width=True, disabled=len(st.session_state.df_history) <= 1):
        # Remove the last dataframe and log entry
        st.session_state.df_history.pop()
        if st.session_state.log:
            st.session_state.log.pop()
        st.success("Last action undone.")
        st.rerun()

# --- Missing Value Handling ---
st.header("Handle Missing Values")

# Display missing values summary
st.subheader("Missing Values Summary")
missing_data = pd.DataFrame({
    'Missing Count': df.isnull().sum(),
    'Missing Percentage': (df.isnull().sum() / df.shape[0]) * 100
}).loc[lambda d: d['Missing Count'] > 0]
st.dataframe(missing_data)

st.subheader("Select Cleaning Action")

# Get columns with missing values
cols_with_missing = df.columns[df.isnull().any()].tolist()

if not cols_with_missing:
    st.success("No missing values found in the dataset!")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    selected_col = st.selectbox("Select a column to clean:", cols_with_missing)

with col2:
    action = st.selectbox("Select an action:", 
                          ["Drop rows with missing values", 
                           "Fill with Mean", 
                           "Fill with Median", 
                           "Fill with Mode", 
                           "Fill with Constant"])

constant_value = None
if action == "Fill with Constant":
    constant_value = st.text_input("Enter the constant value:")

if st.button("Apply"):
    # Create a copy to avoid modifying the current df directly
    df_cleaned = df.copy()
    log_entry = f"[{pd.Timestamp.now()}] "
    
    try:
        if action == "Drop rows with missing values":
            rows_before = len(df_cleaned)
            df_cleaned.dropna(subset=[selected_col], inplace=True)
            rows_after = len(df_cleaned)
            log_entry += f"Dropped {rows_before - rows_after} rows with missing values in column '{selected_col}'."
            st.success(log_entry)

        elif action in ["Fill with Mean", "Fill with Median"]:
            if pd.api.types.is_numeric_dtype(df_cleaned[selected_col]):
                fill_value = df_cleaned[selected_col].mean() if action == "Fill with Mean" else df_cleaned[selected_col].median()
                df_cleaned[selected_col].fillna(fill_value, inplace=True)
                log_entry += f"Filled missing values in '{selected_col}' with {action.lower()} ({fill_value:.2f})."
                st.success(log_entry)
            else:
                st.error(f"Cannot calculate {action.lower()} for non-numeric column '{selected_col}'.")
                log_entry = None # Do not log failed actions

        elif action == "Fill with Mode":
            mode_value = df_cleaned[selected_col].mode()[0]
            df_cleaned[selected_col].fillna(mode_value, inplace=True)
            log_entry += f"Filled missing values in '{selected_col}' with mode ('{mode_value}')."
            st.success(log_entry)

        elif action == "Fill with Constant":
            if constant_value is not None and constant_value.strip() != "":
                try:
                    fill_value = pd.Series([constant_value]).astype(df_cleaned[selected_col].dtype).iloc[0]
                except (ValueError, TypeError):
                    fill_value = constant_value
                df_cleaned[selected_col].fillna(fill_value, inplace=True)
                log_entry += f"Filled missing values in '{selected_col}' with constant ('{fill_value}')."
                st.success(log_entry)
            else:
                st.warning("Please enter a constant value.")
                log_entry = None
        
        if log_entry:
            # Append the new state to the history
            st.session_state.df_history.append(df_cleaned)
            st.session_state.log.append(log_entry)
            st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.write("---")
