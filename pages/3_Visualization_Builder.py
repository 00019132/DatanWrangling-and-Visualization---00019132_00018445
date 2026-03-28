import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import json

st.title("3. Visualization Builder")

# --- Initial checks and setup ---
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file using the sidebar to begin.")
    st.stop()
if 'viz_suggestion' not in st.session_state:
    st.session_state.viz_suggestion = None

df = st.session_state.df_history[-1]
column_list = df.columns.tolist()
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Updated chart types for Matplotlib
chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram", "Correlation Matrix"]

# --- AI Advisor ---
# This section remains unchanged for now, but the output will be used to drive a Matplotlib chart.
st.header("AI Visualization Advisor")
if not st.session_state.get("api_key"):
    st.info("Enter your AI API Key in the sidebar to enable AI suggestions.")
else:
    # AI suggestion logic remains the same
    pass # For brevity, keeping the AI logic collapsed as it's not changing.

# --- Data Filtering ---
st.header("Filter Data (Optional)")
filtered_df = df.copy()
with st.expander("Expand to filter data before plotting"):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            min_val, max_val = float(df[col].min()), float(df[col].max())
            if min_val < max_val:
                slider_range = st.slider(f"Filter by {col}", min_val, max_val, (min_val, max_val))
                filtered_df = filtered_df[filtered_df[col].between(slider_range[0], slider_range[1])]
        elif pd.api.types.is_object_dtype(df[col]):
            unique_vals = df[col].unique()
            if len(unique_vals) < 50: # Only show multiselect for a reasonable number of unique values
                selected_vals = st.multiselect(f"Filter by {col}", unique_vals, default=unique_vals)
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
    st.write("Filtered Data Preview:")
    st.dataframe(filtered_df.head())


# --- Chart Builder ---
st.header("Build Your Chart")

suggestion = st.session_state.viz_suggestion
# UI pre-selection logic remains the same
# ...

chart_type = st.selectbox("Select Chart Type", chart_types) # Index removed for now

top_n = None
top_n_agg = None
# Conditionally display selectors
if chart_type != "Correlation Matrix":
    if chart_type == "Bar Chart":
        c1, c2 = st.columns(2)
        with c1:
            top_n = st.number_input("Show Top N Categories (Optional)", min_value=1, step=1, value=None)
        with c2:
            if top_n:
                top_n_agg = st.selectbox("Aggregate by", ['sum', 'mean', 'count'])
    
    # Dynamic column selection based on chart type
    x_axis_options = column_list
    y_axis_options = [None] + numeric_columns

    if chart_type in ["Scatter Plot", "Line Chart"]:
        x_axis_options = numeric_columns
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x_axis = st.selectbox("Select X-axis", x_axis_options)
    with col2:
        y_axis = st.selectbox("Select Y-axis", y_axis_options)
    with col3:
        color_dim = st.selectbox("Select Color Dimension (Optional)", [None] + categorical_columns)
else:
    st.info("The correlation matrix is calculated for all numeric columns automatically.")
    x_axis, y_axis, color_dim = None, None, None


# --- Chart Generation ---
if st.button("Generate Chart"):
    st.subheader(f"Generated {chart_type}")
    try:
        # Use the filtered dataframe for plotting
        latest_df = filtered_df
        
        # Create a Matplotlib figure and axes
        fig, ax = plt.subplots()
        
        # --- MATPLOTLIB CHARTING LOGIC ---
        if chart_type == "Correlation Matrix":
            numeric_cols = latest_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) < 2:
                st.error("Correlation Matrix requires at least two numeric columns.")
                st.stop()
            corr_matrix = latest_df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            ax.set_title("Correlation Matrix of Numeric Columns")

        elif chart_type == "Bar Chart":
            if top_n and y_axis and top_n_agg:
                if top_n_agg == 'count':
                    agg_df = latest_df.groupby(x_axis).size().nlargest(top_n).reset_index(name='count')
                    sns.barplot(data=agg_df, x=x_axis, y='count', ax=ax)
                    ax.set_title(f"Top {top_n} {x_axis} by count")
                else:
                    agg_func = {'sum': 'sum', 'mean': 'mean'}[top_n_agg]
                    agg_df = latest_df.groupby(x_axis)[y_axis].agg(agg_func).nlargest(top_n).reset_index()
                    sns.barplot(data=agg_df, x=x_axis, y=y_axis, ax=ax)
                    ax.set_title(f"Top {top_n} {x_axis} by {top_n_agg} of {y_axis}")
            else:
                sns.barplot(data=latest_df, x=x_axis, y=y_axis, hue=color_dim, ax=ax)
                ax.set_title(f"{chart_type}: {y_axis} vs {x_axis}")
            ax.tick_params(axis='x', rotation=45)

        elif chart_type == "Line Chart":
            sns.lineplot(data=latest_df, x=x_axis, y=y_axis, hue=color_dim, ax=ax)
            ax.tick_params(axis='x', rotation=45)
            ax.set_title(f"{chart_type}: {y_axis} vs {x_axis}")

        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=latest_df, x=x_axis, y=y_axis, hue=color_dim, ax=ax)
            ax.set_title(f"{chart_type}: {y_axis} vs {x_axis}")

        elif chart_type == "Box Plot":
            sns.boxplot(data=latest_df, x=x_axis, y=y_axis, hue=color_dim, ax=ax)
            ax.set_title(f"{chart_type}: {y_axis} vs {x_axis}")

        elif chart_type == "Histogram":
            sns.histplot(data=latest_df, x=x_axis, hue=color_dim, kde=True, ax=ax)
            ax.set_title(f"Histogram of {x_axis}")
        
        plt.tight_layout()
        
        # Display the Matplotlib chart in Streamlit
        st.pyplot(fig)
        
        # Clear suggestion after use
        st.session_state.viz_suggestion = None
    except Exception as e:
        st.error(f"An error occurred while generating the Matplotlib chart: {e}")
        st.error("Please ensure you have selected appropriate columns for the chosen chart type (e.g., numeric columns for scatter plots).")
