import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Visualization Builder")

# Check if a dataframe exists in the session state
if 'df' not in st.session_state or st.session_state.df is None:
    st.warning("Please upload a file on the 'Upload and Overview' page first.")
    st.stop()

# If a dataframe exists, get it from the session state
df = st.session_state.df
column_list = df.columns.tolist()

st.header("Build Your Chart")

# UI for chart selection
chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram"])

col1, col2, col3 = st.columns(3)

with col1:
    x_axis = st.selectbox("Select X-axis", column_list)

with col2:
    # Some charts only need an X-axis
    y_axis_options = [None] + column_list if chart_type in ["Box Plot", "Histogram"] else column_list
    y_axis = st.selectbox("Select Y-axis", y_axis_options)

with col3:
    color_dim = st.selectbox("Select Color Dimension (Optional)", [None] + column_list)

# Generate Chart button
if st.button("Generate Chart"):
    st.subheader(f"Generated {chart_type}")
    
    try:
        fig = None
        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_dim)
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, color=color_dim)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_dim)
        elif chart_type == "Box Plot":
            fig = px.box(df, x=x_axis, y=y_axis, color=color_dim)
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis, y=y_axis, color=color_dim)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not generate chart.")

    except Exception as e:
        st.error(f"An error occurred while generating the chart: {e}")

st.write("---")
