import streamlit as st
import pandas as pd
import io
import json
from sidebar_utils import render_sidebar

# Render the shared sidebar
render_sidebar()

st.title("4. Export and Report")

# Check if a dataframe exists in the session state
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload and process a file first.")
    st.stop()

# Get the most recent dataframe from the history
df = st.session_state.df_history[-1]

# --- Data Export ---
st.header("Export Cleaned Data")
st.write("Below is a preview of the cleaned data. Click a button to download it.")
st.dataframe(df.head())

@st.cache_data
def convert_df_to_csv(df_to_convert):
    return df_to_convert.to_csv(index=False).encode('utf-8')

@st.cache_data
def convert_df_to_excel(df_to_convert):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_to_convert.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

csv_data = convert_df_to_csv(df)
excel_data = convert_df_to_excel(df)

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download data as CSV",
        data=csv_data,
        file_name='cleaned_data.csv',
        mime='text/csv',
        use_container_width=True
    )

with col2:
    st.download_button(
        label="Download data as Excel",
        data=excel_data,
        file_name='cleaned_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True
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

st.write("---")

# --- Transformation Recipe ---
st.header("Transformation Recipe")

if 'recipe' in st.session_state and st.session_state.recipe:
    st.write("The following machine-readable recipe can be used to replay the transformations:")
    st.json(st.session_state.recipe)

    recipe_json = json.dumps(st.session_state.recipe, indent=4)
    st.download_button(
        label="Download Recipe as JSON",
        data=recipe_json,
        file_name='transformation_recipe.json',
        mime='application/json',
    )
else:
    st.info("No recipe generated. Apply some cleaning steps on Page 2 first.")
