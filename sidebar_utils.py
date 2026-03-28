"""
This module contains the shared sidebar component for the Streamlit app.
"""
import os
import re
import streamlit as st
import pandas as pd
import numpy as np

# --- Cached Data Loading Functions ---
@st.cache_data
def _load_data(uploaded_file):
    """
    Loads data from an uploaded file into a Pandas DataFrame.
    """
    try:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(uploaded_file)
        elif file_extension == ".json":
            df = pd.read_json(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
        return df
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

@st.cache_data
def _load_from_gdrive(gdrive_url: str):
    """
    Loads data from a public Google Sheet URL into a Pandas DataFrame.
    """
    try:
        # Extract the sheet ID from the URL
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', gdrive_url)
        if match:
            sheet_id = match.group(1)
            export_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
            df = pd.read_csv(export_url)
            return df
        else:
            st.error("Invalid Google Sheet URL. Please provide a valid share link.")
            return None
    except Exception as e:
        st.error(f"Failed to load from Google Sheet. Ensure it's public. Error: {e}")
        return None

def render_sidebar():
    """
    Renders the main sidebar of the application, including data uploaders,
    AI assistant controls, and session management buttons. This function
    also contains the logic for processing data from the selected source.
    """
    # Initialize uploaded_file to None to ensure it's always defined
    uploaded_file = None

    with st.sidebar:
        st.title("Smash Data")
        st.header("1. Upload your Data")

        # --- Conditional UI for Data Upload ---
        if not st.session_state.get('df_history'):
            # "NO DATA" state: Show uploaders
            def clear_gdrive_url_on_file_upload():
                """Callback to clear the gdrive url when a file is uploaded."""
                st.session_state.gdrive_url = ""

            uploaded_file = st.file_uploader(
                "Choose a CSV, XLSX, or JSON file", 
                type=["csv", "xlsx", "json"],
                help="Upload your data file to get started.",
                on_change=clear_gdrive_url_on_file_upload
            )
            st.divider()
            st.text_input("Or enter Google Sheet URL", key="gdrive_url", placeholder="https://docs.google.com/spreadsheets/d/...")
        else:
            # "DATA LOADED" state: Show active data source and a remove button
            active_source = ""
            if st.session_state.get('last_uploaded_file'):
                active_source = st.session_state.last_uploaded_file
            elif st.session_state.get('last_gdrive_url'):
                # Truncate long URLs for display
                url = st.session_state.last_gdrive_url
                active_source = url[:40] + "..." if len(url) > 40 else url

            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.info(f"Active: {active_source}")
            with col2:
                if st.button("X", key="clear_data_x", use_container_width=True):
                    st.session_state.clear()
                    st.success("Session reset.")
                    st.rerun()

        st.divider()

        # --- AI and Session Management (always visible) ---
        st.header("2. AI Assistant")
        use_ai_assistant = st.toggle("Enable AI Assistant")

        if use_ai_assistant:
            # ... (rest of AI assistant logic is unchanged)
            st.radio(
                "Select your API Key source:",
                ("Use Default Key", "Use My Own Key"),
                key="api_key_source",
                label_visibility="collapsed"
            )
            if st.session_state.api_key_source == "Use Default Key":
                try:
                    st.session_state.api_key = st.secrets["GEMINI_API_KEY"]
                    st.success("Default AI key is active.")
                except (KeyError, FileNotFoundError):
                    st.session_state.api_key = None
            
            elif st.session_state.api_key_source == "Use My Own Key":
                user_api_key = st.text_input(
                    "Enter your Gemini API Key:",
                    type="password",
                    help="Your key is used for AI features and is not stored."
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key
                    st.success("API Key saved for this session.")
                else:
                    st.session_state.api_key = None
        else:
            st.session_state.api_key = None

        st.header("3. Session Management")
        if st.button("Reset Session", use_container_width=True):
            st.session_state.clear()
            st.success("Session has been reset.")
            st.rerun()

        if st.button("Undo Last Action", use_container_width=True, disabled=len(st.session_state.get('df_history', [])) <= 1):
            st.session_state.df_history.pop()
            if st.session_state.log:
                st.session_state.log.pop()
            st.success("Last action undone.")
            st.rerun()

    # --- Data Source Processing Logic (runs regardless of UI state) ---
    if uploaded_file is not None and uploaded_file.name != st.session_state.get('last_uploaded_file'):
        df = _load_data(uploaded_file)
        if df is not None:
            # Selectively reset data-related state instead of clearing the whole session
            st.session_state.df_history = [df]
            st.session_state.log = ["Started new session with file: " + uploaded_file.name]
            st.session_state.last_uploaded_file = uploaded_file.name
            st.session_state.last_gdrive_url = None
            st.success(f"Successfully loaded {uploaded_file.name}")
            st.rerun()

    elif st.session_state.get('gdrive_url') and st.session_state.gdrive_url != st.session_state.get('last_gdrive_url'):
        url = st.session_state.gdrive_url
        df = _load_from_gdrive(url)
        if df is not None:
            # Selectively reset data-related state instead of clearing the whole session
            st.session_state.df_history = [df]
            st.session_state.log = [f"Started new session with Google Sheet: {url}"]
            st.session_state.last_gdrive_url = url
            st.session_state.last_uploaded_file = None
            st.success("Successfully loaded data from Google Sheet.")
            st.rerun()

