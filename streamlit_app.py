import streamlit as st
from sidebar_utils import render_sidebar

# --- Page Configuration ---
st.set_page_config(
    page_title="Home",
    layout="wide"
)

# --- Session State Initialization ---
# Initialize required session state keys. The sidebar component will manage the rest.
if 'df_history' not in st.session_state:
    st.session_state.df_history = []
if 'log' not in st.session_state:
    st.session_state.log = []

# --- Render the shared sidebar ---
# This also handles all data loading and session management logic.
render_sidebar()

# --- Main Page Content ---
st.title("Welcome to the AI-Assisted Data Wrangler & Visualizer")
st.markdown("---")
st.header("How to Use This App")
st.info(
    """
    1.  **Upload Data**: Use the sidebar to upload your CSV, Excel, or JSON file, or connect to a Google Sheet.
    2.  **Overview**: Navigate to the `1_Upload_and_Overview` page to see a profile of your data.
    3.  **Clean & Prepare**: Use the tools on the `2_Cleaning_and_Preparation` page to handle missing values, duplicates, and more.
    4.  **Visualize**: Build custom charts on the `3_Visualization_Builder` page.
    5.  **Export**: Download your cleaned data and a report of all transformations on the `4_Export_and_Report` page.
    """
)

# Add a check to prompt user to upload data if the session is new.
if not st.session_state.df_history:
    st.warning("Please upload a dataset using the sidebar to begin.")
