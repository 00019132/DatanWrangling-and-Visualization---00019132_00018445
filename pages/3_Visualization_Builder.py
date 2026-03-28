import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import numpy as np
import json
from sidebar_utils import render_sidebar

# Render the shared sidebar
render_sidebar()

st.title("3. Visualization Builder")

# --- Initial checks and setup ---
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file using the sidebar to begin.")
    st.stop()
df = st.session_state.df_history[-1]
column_list = df.columns.tolist()
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
...
# Updated chart types
chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram", "Correlation Matrix"]

# --- AI Advisor ---
st.header("🤖 AI Visualization Advisor")
api_key = st.session_state.get("api_key")

if not api_key:
    st.info("💡 Pro Tip: Enter your Gemini API Key in the sidebar to get smart chart recommendations!")
else:
    if st.button("Get AI Recommendations"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare a concise schema description for the AI
            schema = []
            for col in df.columns:
                schema.append(f"- {col} ({df[col].dtype})")
            schema_str = "\n".join(schema)
            
            prompt = f"""
            Given this dataset schema:
            {schema_str}

            Suggest the top 3 most insightful visualizations. 
            For each, provide:
            1. A clear 'title'
            2. 'chart_type' (must be one of: {chart_types})
            3. 'x_axis' (from column names)
            4. 'y_axis' (from column names or null)
            5. 'agg_method' (one of: None, mean, median, sum, count)
            6. 'explanation' (why this is useful)

            Return the response ONLY as a JSON list of objects.
            """
            
            response = model.generate_content(prompt)
            # Clean JSON response (strip markdown code blocks if present)
            raw_json = response.text.strip().replace("```json", "").replace("```", "")
            suggestions = json.loads(raw_json)
            st.session_state.viz_suggestions = suggestions
            
        except Exception as e:
            st.error(f"AI Advisor failed: {e}")

    if st.session_state.get("viz_suggestions"):
        st.subheader("Top AI Recommendations")
        for i, sug in enumerate(st.session_state.viz_suggestions):
            with st.container(border=True):
                st.write(f"**{i+1}. {sug['title']}**")
                st.write(sug['explanation'])
                if st.button(f"Apply Recommendation {i+1}", key=f"apply_sug_{i}"):
                    st.session_state.selected_chart_type = sug['chart_type']
                    st.session_state.selected_x = sug['x_axis']
                    st.session_state.selected_y = sug['y_axis']
                    st.session_state.selected_agg = sug['agg_method']
                    st.success("Recommendation applied! Check the builder below.")

st.divider()

# --- Data Filtering ---
st.header("Filter Data (Optional)")
filtered_df = df.copy()
with st.expander("Expand to filter data before plotting"):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            min_val, max_val = float(df[col].min()), float(df[col].max())
            if min_val < max_val:
                slider_range = st.slider(f"Filter by {col} (Numeric)", min_val, max_val, (min_val, max_val), key=f"filt_{col}")
                filtered_df = filtered_df[filtered_df[col].between(slider_range[0], slider_range[1])]
        
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            min_date, max_date = df[col].min().date(), df[col].max().date()
            if min_date < max_date:
                date_range = st.date_input(
                    f"Filter by {col} (Date Range)",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key=f"filt_{col}"
                )
                if len(date_range) == 2:
                    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                    filtered_df = filtered_df[filtered_df[col].between(start_date, end_date)]

        elif pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
            unique_vals = df[col].dropna().unique().tolist()
            if 0 < len(unique_vals) < 50:
                selected_vals = st.multiselect(f"Filter by {col} (Categories)", unique_vals, default=unique_vals, key=f"filt_{col}")
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
    
    st.write(f"Filtered Rows: {len(filtered_df)} / {len(df)}")
    st.dataframe(filtered_df.head())


# --- Chart Builder ---
st.header("Build Your Chart")

# Use state to store and apply AI suggestions
chart_type = st.selectbox("Select Chart Type", chart_types, 
                          index=chart_types.index(st.session_state.get('selected_chart_type', 'Bar Chart')) if st.session_state.get('selected_chart_type') in chart_types else 0)

# --- Dynamic UI based on Chart Type ---
x_axis_options = column_list
y_axis_options = [None] + numeric_columns

if chart_type == "Correlation Matrix":
    st.info("Correlation Matrix uses all numeric columns.")
    x_axis, y_axis, color_dim = None, None, None
else:
    if chart_type == "Scatter Plot":
        x_axis_options = numeric_columns
        y_axis_options = numeric_columns
    elif chart_type == "Line Chart":
        x_axis_options = numeric_columns + df.select_dtypes(include=['datetime']).columns.tolist()
        y_axis_options = numeric_columns
    elif chart_type == "Box Plot":
        x_axis_options = categorical_columns
        y_axis_options = numeric_columns
    elif chart_type == "Histogram":
        x_axis_options = numeric_columns
        y_axis_options = [None]

    col1, col2, col3 = st.columns(3)
    
    def get_index(options, val):
        try: return options.index(val)
        except: return 0

    with col1:
        x_axis = st.selectbox("Select X-axis", x_axis_options, 
                              index=get_index(x_axis_options, st.session_state.get('selected_x')))
    with col2:
        y_axis = st.selectbox("Select Y-axis (Numeric)", y_axis_options, 
                              index=get_index(y_axis_options, st.session_state.get('selected_y')))
    with col3:
        color_dim = st.selectbox("Select Color Dimension (Optional)", [None] + categorical_columns)

# --- Aggregation and Top N UI ---
agg_method = "None"
top_n = None

if chart_type in ["Bar Chart", "Line Chart"]:
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        agg_options = ["None", "mean", "median", "sum", "count"]
        agg_method = st.selectbox("Aggregation Method", agg_options, 
                                  index=agg_options.index(st.session_state.get('selected_agg', 'None')) if st.session_state.get('selected_agg') in agg_options else 0,
                                  help="Summarize data before plotting.")
    with c2:
        if chart_type == "Bar Chart":
            top_n = st.number_input("Show Top N Categories (based on Y value)", min_value=1, step=1, value=None)

# --- Chart Generation ---
if st.button("Generate Chart", type="primary"):
    if not x_axis and chart_type != "Correlation Matrix":
        st.error("Please select an X-axis.")
        st.stop()

    try:
        plot_df = filtered_df.copy()
        y_col = y_axis
        
        # --- Aggregation Logic ---
        if agg_method != "None" and (y_col or agg_method == "count"):
            group_cols = [x_axis]
            if color_dim:
                group_cols.append(color_dim)
            
            if agg_method == "count":
                plot_df = plot_df.groupby(group_cols).size().reset_index(name='count')
                y_col = 'count'
            else:
                if y_col:
                    plot_df = plot_df.groupby(group_cols)[y_col].agg(agg_method).reset_index()
                else:
                    st.warning("Please select a Y-axis to aggregate (unless using 'count').")
                    st.stop()

        # --- Top N Logic ---
        if top_n and y_col:
            plot_df = plot_df.nlargest(top_n, y_col)

        # --- Plotting ---
        st.subheader(f"{chart_type}")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == "Correlation Matrix":
            numeric_cols = plot_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) < 2:
                st.error("Need at least two numeric columns.")
            else:
                sns.heatmap(plot_df[numeric_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        
        elif chart_type == "Bar Chart":
            if y_col is None: # Fallback to count if no aggregation and no Y
                sns.countplot(data=plot_df, x=x_axis, hue=color_dim, ax=ax)
            else:
                sns.barplot(data=plot_df, x=x_axis, y=y_col, hue=color_dim, ax=ax)
        
        elif chart_type == "Line Chart":
            if not y_col:
                st.error("Numeric Y-axis required for Line Chart.")
            else:
                sns.lineplot(data=plot_df, x=x_axis, y=y_col, hue=color_dim, ax=ax)
        
        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=plot_df, x=x_axis, y=y_col, hue=color_dim, ax=ax)
        
        elif chart_type == "Box Plot":
            sns.boxplot(data=plot_df, x=x_axis, y=y_col, hue=color_dim, ax=ax)
        
        elif chart_type == "Histogram":
            sns.histplot(data=plot_df, x=x_axis, hue=color_dim, kde=True, ax=ax)

        ax.set_title(f"{chart_type} of {y_col if y_col else 'Count'} by {x_axis}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
