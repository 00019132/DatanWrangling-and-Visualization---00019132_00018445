import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

st.set_page_config(layout="wide")

st.title("Visualization Builder")

# --- Initial checks and setup ---
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file on the 'Upload and Overview' page first.")
    st.stop()
if 'viz_suggestion' not in st.session_state:
    st.session_state.viz_suggestion = None

df = st.session_state.df_history[-1]
column_list = df.columns.tolist()
chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram"]

# --- AI Advisor ---
st.header("AI Visualization Advisor")
if not st.session_state.get("api_key"):
    st.info("Enter your AI API Key on the 'Upload and Overview' page to enable AI suggestions.")
else:
    if st.button("Get AI Suggestion"):
        with st.spinner("🤖 AI is thinking of a cool chart..."):
            try:
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')

                profile = f"Columns: {df.columns.tolist()}\nData Types:\n{df.dtypes.to_string()}"

                prompt = f"""
                You are a helpful data analyst. Your goal is to suggest an insightful chart to help a user understand their data.
                The user's data has the following profile:
                ---
                {profile}
                ---
                Based on the data profile, suggest a single chart that would reveal an interesting relationship. Consider the data types. For example, a bar chart for categorical data, a scatter plot for two numeric columns, or a line chart for time series.
                Respond ONLY with a single JSON object in the following format. Choose from these chart types: {chart_types}.

                JSON format:
                {{
                  "explanation": "A bar chart showing the average height by player position could reveal which positions have the tallest players.",
                  "chart_type": "Bar Chart",
                  "x_axis": "player_position",
                  "y_axis": "height",
                  "color": null
                }}
                """
                response = model.generate_content(prompt)
                json_response = response.text.strip().replace("```json", "").replace("```", "")
                st.session_state.viz_suggestion = json.loads(json_response)
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred with the AI model: {e}")

# --- Chart Builder ---
st.header("Build Your Chart")

# Handle UI pre-selection based on AI suggestion
suggestion = st.session_state.viz_suggestion
default_chart_type = chart_types.index(suggestion['chart_type']) if suggestion and suggestion.get('chart_type') in chart_types else 0
default_x = column_list.index(suggestion['x_axis']) if suggestion and suggestion.get('x_axis') in column_list else 0
default_y = column_list.index(suggestion['y_axis']) if suggestion and suggestion.get('y_axis') in column_list else 1
default_color = (column_list.index(suggestion['color']) + 1) if suggestion and suggestion.get('color') in column_list else 0

if suggestion:
    st.info(f"✨ **AI Suggestion:** {suggestion.get('explanation')}")

chart_type = st.selectbox("Select Chart Type", chart_types, index=default_chart_type)

col1, col2, col3 = st.columns(3)
with col1:
    x_axis = st.selectbox("Select X-axis", column_list, index=default_x)
with col2:
    y_axis_options = [None] + column_list if chart_type in ["Box Plot", "Histogram"] else column_list
    y_axis = st.selectbox("Select Y-axis", y_axis_options, index=default_y if chart_type not in ["Box Plot", "Histogram"] else 0)
with col3:
    color_dim = st.selectbox("Select Color Dimension (Optional)", [None] + column_list, index=default_color)

# --- Chart Generation ---
if st.button("Generate Chart"):
    st.subheader(f"Generated {chart_type}")
    try:
        latest_df = st.session_state.df_history[-1]
        fig = px.bar(latest_df, x=x_axis, y=y_axis, color=color_dim) if chart_type == "Bar Chart" else \
              px.line(latest_df, x=x_axis, y=y_axis, color=color_dim) if chart_type == "Line Chart" else \
              px.scatter(latest_df, x=x_axis, y=y_axis, color=color_dim) if chart_type == "Scatter Plot" else \
              px.box(latest_df, x=x_axis, y=y_axis, color=color_dim) if chart_type == "Box Plot" else \
              px.histogram(latest_df, x=x_axis, y=y_axis, color=color_dim)
        
        st.plotly_chart(fig, use_container_width=True)
        # Clear suggestion after use
        st.session_state.viz_suggestion = None
    except Exception as e:
        st.error(f"An error occurred: {e}")
