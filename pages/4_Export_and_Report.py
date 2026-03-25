import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Export & Report")

# Check if a dataframe exists in the session state
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload and process a file first.")
    st.stop()

# Get the most recent dataframe from the history
df = st.session_state.df_history[-1]

# --- Data Export ---
st.header("Export Cleaned Data")
st.write("Below is a preview of the cleaned data. Click the button to download it as a CSV file.")
st.dataframe(df.head())

@st.cache_data
def convert_df_to_csv(df_to_convert):
    return df_to_convert.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='cleaned_data.csv',
    mime='text/csv',
)

st.write("---")

# --- Transformation Report ---
st.header("Transformation Report")

if 'log' in st.session_state and st.session_state.log:
    st.write("The following transformations were performed:")
    
    # Display the log
    log_content = "\n".join(st.session_state.log)
    st.text_area("Log", log_content, height=200)

    # Download button for the log
    st.download_button(
        label="Download Report",
        data=log_content.encode('utf-8'),
        file_name='transformation_report.txt',
        mime='text/plain',
    )
else:
    st.info("No transformations have been logged yet.")
