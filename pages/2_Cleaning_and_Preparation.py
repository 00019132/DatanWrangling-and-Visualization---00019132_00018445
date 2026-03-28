import streamlit as st
import pandas as pd
import numpy as np
import re
from sidebar_utils import render_sidebar

# Page configuration
st.set_page_config(layout="wide", page_title="Cleaning & Preparation Studio")

# Render the shared sidebar
render_sidebar()

st.title("2. Cleaning & Preparation Studio")

# --- Helper Functions ---
def log_action(log_message):
    """Adds a timestamped message to the session state log."""
    full_message = f"[{pd.Timestamp.now()}] {log_message}"
    st.session_state.log.append(full_message)
    st.success(full_message)

def update_dataframe(new_df, message):
    """Adds the new dataframe to the history and logs the action."""
    st.session_state.df_history.append(new_df)
    log_action(message)
    # Clear the preview state after a successful update
    if 'df_preview' in st.session_state:
        del st.session_state.df_preview
    if 'log_preview' in st.session_state:
        del st.session_state.log_preview
    st.rerun()

def get_numeric_columns(df):
    """Returns a list of numeric columns in the dataframe."""
    return df.select_dtypes(include=np.number).columns.tolist()

def get_categorical_columns(df):
    """Returns a list of categorical columns in the dataframe."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def display_preview():
    """
    Displays a preview of the proposed changes and handles user confirmation
    or cancellation. This function acts as a modal dialog.
    """
    st.header("Preview Changes")
    preview_df = st.session_state.df_preview
    log_message = st.session_state.log_preview
    original_df = st.session_state.df_history[-1]

    with st.container(border=True):
        st.subheader("Summary of Changes")
        row_diff = len(preview_df) - len(original_df)
        col_diff = len(preview_df.columns) - len(original_df.columns)
        st.write(f"Operation: **{log_message}**")
        st.metric("Row Change", f"{row_diff:+,}", help="Number of rows that will be added or removed.")
        st.metric("Column Change", f"{col_diff:+,}", help="Number of columns that will be added or removed.")
        
        st.subheader("Data Diff / Summary")
        
        # Special case for scaling/normalization: show describe()
        if any(keyword in log_message for keyword in ["Scaled", "Standardized", "Encoded"]):
             st.write("Current Data Summary")
             st.dataframe(preview_df.describe(include='all').T, use_container_width=True)
        else:
            try:
                # Use pandas compare to highlight differences
                diff_df = original_df.compare(preview_df, align_axis=0).rename(columns={'self': 'Original', 'other': 'New'}, level=-1)
                st.dataframe(diff_df, use_container_width=True)
            except Exception as e:
                st.warning("Could not generate a direct comparison. Displaying sample of new data instead.")
                st.write("New Data (Head)")
                st.dataframe(preview_df.head(), use_container_width=True)

        st.subheader("Confirm Action")
        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            if st.button("✅ Confirm", use_container_width=True, type="primary"):
                update_dataframe(preview_df, log_message)
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state.df_preview
                del st.session_state.log_preview
                st.rerun()

# --- Initial Check ---
if 'df_history' not in st.session_state or not st.session_state.df_history:
    st.warning("Please upload a file using the sidebar to begin.")
    st.stop()

# --- Preview Modal Logic ---
if 'df_preview' in st.session_state:
    display_preview()
    st.stop()

# Initialize log if it doesn't exist
if 'log' not in st.session_state:
    st.session_state.log = []

# Get the current dataframe
df = st.session_state.df_history[-1]

# --- 0. Transformation Activity Log ---
with st.expander("📋 Transformation Activity Log", expanded=False):
    if not st.session_state.log:
        st.info("No transformations applied yet.")
    else:
        # Show recent actions first
        for entry in reversed(st.session_state.log):
            st.text(entry)

# --- 1. Handle Missing Values ---
with st.expander("1. Handle Missing Values", expanded=False):
    st.header("Handle Missing Values")

    missing_data = pd.DataFrame({
        'Missing Count': df.isnull().sum(),
        'Missing Percentage (%)': (df.isnull().sum() / len(df)) * 100
    }).loc[lambda d: d['Missing Count'] > 0]

    if missing_data.empty:
        st.success("No missing values found in the dataset!")
    else:
        st.dataframe(missing_data, use_container_width=True)
        st.markdown("---")
        
        cols_with_missing = df.columns[df.isnull().any()].tolist()
        
        st.subheader("Per-Column Actions")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            numeric_cols = get_numeric_columns(df)

            with col1:
                selected_col = st.selectbox("Select a column to clean:", cols_with_missing, key="mv_col")
            
            action_options = ["Drop rows", "Fill with Mode", "Forward Fill (ffill)", "Backward Fill (bfill)", "Fill with Constant"]
            if selected_col in numeric_cols:
                action_options.insert(1, "Fill with Median")
                action_options.insert(1, "Fill with Mean")

            with col2:
                action = st.selectbox("Select an action:", action_options, key="mv_action")

            if action == "Fill with Constant":
                constant_value = st.text_input("Enter constant value", key="mv_const")

            if st.button("Apply Per-Column Action", key="mv_apply_col"):
                df_cleaned = df.copy()
                log_msg = ""
                try:
                    if action == "Drop rows":
                        rows_before = len(df_cleaned)
                        df_cleaned.dropna(subset=[selected_col], inplace=True)
                        log_msg = f"Dropped {rows_before - len(df_cleaned)} rows with missing values in '{selected_col}'."
                    elif action == "Forward Fill (ffill)":
                        df_cleaned[selected_col].ffill(inplace=True)
                        log_msg = f"Forward-filled missing values in '{selected_col}'."
                    elif action == "Backward Fill (bfill)":
                        df_cleaned[selected_col].bfill(inplace=True)
                        log_msg = f"Backward-filled missing values in '{selected_col}'."
                    elif action in ["Fill with Mean", "Fill with Median"]:
                        fill_val = df_cleaned[selected_col].mean() if action == "Fill with Mean" else df_cleaned[selected_col].median()
                        df_cleaned[selected_col].fillna(fill_val, inplace=True)
                        log_msg = f"Filled missing values in '{selected_col}' with {action.lower()} ({fill_val:.2f})."
                    elif action == "Fill with Mode":
                        mode_val = df_cleaned[selected_col].mode()[0]
                        df_cleaned[selected_col].fillna(mode_val, inplace=True)
                        log_msg = f"Filled missing values in '{selected_col}' with mode ('{mode_val}')."
                    elif action == "Fill with Constant":
                        if 'constant_value' in locals() and constant_value:
                             df_cleaned[selected_col].fillna(constant_value, inplace=True)
                             log_msg = f"Filled missing values in '{selected_col}' with constant ('{constant_value}')."
                        else:
                            st.error("Please provide a constant value.")
                            st.stop()
                    
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = log_msg
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        st.subheader("Whole-DataFrame Actions")
        with st.container(border=True):
            threshold = st.slider("Drop columns with missing values > threshold (%)", 0, 100, 50, key="mv_thresh")
            if st.button("Drop Columns by Threshold", key="mv_drop_thresh"):
                df_cleaned = df.copy()
                cols_before = set(df_cleaned.columns)
                limit = len(df_cleaned) * (1 - threshold / 100)
                df_cleaned.dropna(thresh=limit, axis=1, inplace=True)
                dropped_cols = list(cols_before - set(df_cleaned.columns))
                if dropped_cols:
                    log_msg = f"Dropped columns with >{threshold}% missing values: {', '.join(dropped_cols)}"
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = log_msg
                    st.rerun()
                else:
                    st.info("No columns met the threshold.")

# --- 2. Handle Duplicates ---
with st.expander("2. Handle Duplicates", expanded=False):
    st.header("Handle Duplicates")
    subset_cols = st.multiselect("Select subset of columns to check (leave empty for all)", df.columns.tolist(), key="dup_subset")
    subset = None if not subset_cols else subset_cols
    duplicate_count = df.duplicated(subset=subset).sum()
    st.metric("Number of duplicate rows found", duplicate_count)

    if duplicate_count > 0:
        with st.container(border=True):
            if st.button("🔍 Show Duplicate Rows", key="dup_show"):
                dupes = df[df.duplicated(subset=subset, keep=False)]
                st.dataframe(dupes, use_container_width=True)
            
            st.markdown("---")
            keep_option = st.radio("Which duplicate to keep?", ["first", "last", False], format_func=lambda x: str(x) if x else "Remove all", horizontal=True, key="dup_keep")
            if st.button("Remove Duplicates", key="dup_remove", type="primary"):
                df_cleaned = df.copy()
                rows_before = len(df_cleaned)
                df_cleaned.drop_duplicates(subset=subset, keep=keep_option, inplace=True)
                log_msg = f"Removed {rows_before - len(df_cleaned)} duplicate rows."
                st.session_state.df_preview = df_cleaned
                st.session_state.log_preview = log_msg
                st.rerun()
    else:
        st.success("No duplicate rows found!")

# --- 3. Manage Data Types ---
with st.expander("3. Manage Data Types", expanded=False):
    st.subheader("Convert Column Type")
    col1, col2 = st.columns(2)
    with col1:
        col_to_convert = st.selectbox("Column to convert", df.columns.tolist(), key="type_col")
    with col2:
        new_type = st.selectbox("New data type", ["string", "numeric", "datetime"], key="type_new")
    if st.button("Convert Data Type", key="type_convert"):
        df_cleaned = df.copy()
        try:
            if new_type == "numeric":
                df_cleaned[col_to_convert] = pd.to_numeric(df_cleaned[col_to_convert], errors='coerce')
            elif new_type == "datetime":
                df_cleaned[col_to_convert] = pd.to_datetime(df_cleaned[col_to_convert], errors='coerce')
            else:
                df_cleaned[col_to_convert] = df_cleaned[col_to_convert].astype(str)
            log_msg = f"Converted column '{col_to_convert}' to {new_type}."
            st.session_state.df_preview = df_cleaned
            st.session_state.log_preview = log_msg
            st.rerun()
        except Exception as e:
            st.error(f"Failed to convert: {e}")

# --- 4. Handle Categorical Data ---
with st.expander("4. Handle Categorical Data", expanded=False):
    categorical_columns = get_categorical_columns(df)
    if not categorical_columns:
        st.info("No categorical columns found.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["Standardization", "Mapping", "Rare Grouping", "Encoding"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                cat_col_std = st.selectbox("Select column", categorical_columns, key="std_col")
            with col2:
                std_action = st.radio("Action", ["Trim Whitespace", "Lowercase", "Title Case"], key="std_action")
            if st.button("Apply Standardization"):
                df_cleaned = df.copy()
                if std_action == "Trim Whitespace":
                    df_cleaned[cat_col_std] = df_cleaned[cat_col_std].str.strip()
                elif std_action == "Lowercase":
                    df_cleaned[cat_col_std] = df_cleaned[cat_col_std].str.lower()
                else:
                    df_cleaned[cat_col_std] = df_cleaned[cat_col_std].str.title()
                st.session_state.df_preview = df_cleaned
                st.session_state.log_preview = f"Applied '{std_action}' to '{cat_col_std}'."
                st.rerun()

        with tab2:
            map_col = st.selectbox("Select column to map", categorical_columns, key="map_col")
            if map_col:
                unique_values = df[map_col].dropna().unique()
                if len(unique_values) > 50:
                    st.warning(f"This column has {len(unique_values)} unique values. Manual mapping might be difficult.")
                
                map_df = pd.DataFrame({"Original": unique_values, "New": unique_values})
                st.write("Edit 'New' column to map values:")
                edited_map_df = st.data_editor(map_df, key="v_map_ed", use_container_width=True, height=300)
                if st.button("Apply Value Map"):
                    mapping = edited_map_df[edited_map_df["New"] != edited_map_df["Original"]].set_index("Original")["New"].to_dict()
                    if mapping:
                        df_cleaned = df.copy()
                        df_cleaned[map_col] = df_cleaned[map_col].replace(mapping)
                        st.session_state.df_preview = df_cleaned
                        st.session_state.log_preview = f"Mapped {len(mapping)} values in '{map_col}'."
                        st.rerun()

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                group_col = st.selectbox("Select column", categorical_columns, key="group_col")
            with col2:
                threshold = st.slider("Frequency threshold (%)", 1, 50, 5, key="group_thresh")
            if st.button("Group Rare Categories"):
                df_cleaned = df.copy()
                counts = df_cleaned[group_col].value_counts(normalize=True)
                rare_cats = counts[counts < (threshold / 100)].index.tolist()
                if rare_cats:
                    df_cleaned[group_col] = df_cleaned[group_col].replace(rare_cats, 'Other')
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = f"Grouped {len(rare_cats)} rare categories in '{group_col}'."
                    st.rerun()

        with tab4:
            st.subheader("One-Hot Encoding")
            cols_to_encode = st.multiselect("Select columns to encode", categorical_columns, key="encode_cols")
            if st.button("Apply One-Hot Encoding"):
                if cols_to_encode:
                    df_cleaned = pd.get_dummies(df, columns=cols_to_encode)
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = f"One-hot encoded: {', '.join(cols_to_encode)}."
                    st.rerun()

# --- 5. Clean Numeric Data (Outliers) ---
with st.expander("5. Clean Numeric Data (Outliers)", expanded=False):
    numeric_columns = get_numeric_columns(df)
    if not numeric_columns:
        st.info("No numeric columns found.")
    else:
        selected_num_col = st.selectbox("Select column:", numeric_columns, key="outlier_col")
        Q1, Q3 = df[selected_num_col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        outliers = df[(df[selected_num_col] < lower) | (df[selected_num_col] > upper)]
        st.metric("Total Outliers", len(outliers))
        if not outliers.empty:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Remove Outliers"):
                    df_cleaned = df[(df[selected_num_col] >= lower) & (df[selected_num_col] <= upper)].copy()
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = f"Removed outliers from '{selected_num_col}'."
                    st.rerun()
            with col2:
                if st.button("Cap Outliers"):
                    df_cleaned = df.copy()
                    df_cleaned[selected_num_col] = df_cleaned[selected_num_col].clip(lower, upper)
                    st.session_state.df_preview = df_cleaned
                    st.session_state.log_preview = f"Capped outliers in '{selected_num_col}'."
                    st.rerun()

# --- 6. Normalize and Scale Data ---
with st.expander("6. Normalize and Scale Data", expanded=False):
    numeric_columns = get_numeric_columns(df)
    if not numeric_columns:
        st.info("No numeric columns found.")
    else:
        cols_to_scale = st.multiselect("Select columns:", numeric_columns, key="scale_cols")
        method = st.radio("Method:", ["Min-Max Scaling", "Z-Score Standardization"], key="scale_method")
        if st.button("Apply Scaling"):
            if cols_to_scale:
                df_cleaned = df.copy()
                for col in cols_to_scale:
                    if method == "Min-Max Scaling":
                        df_cleaned[col] = (df_cleaned[col] - df_cleaned[col].min()) / (df_cleaned[col].max() - df_cleaned[col].min())
                    else:
                        df_cleaned[col] = (df_cleaned[col] - df_cleaned[col].mean()) / df_cleaned[col].std()
                st.session_state.df_preview = df_cleaned
                st.session_state.log_preview = f"Applied {method} to {', '.join(cols_to_scale)}."
                st.rerun()

# --- 7. Column Operations ---
with st.expander("7. Column Operations", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Drop/Rename", "Arithmetic", "Concatenate"])
    
    with tab1:
        st.subheader("Drop Columns")
        cols_to_drop = st.multiselect("Select to drop", df.columns.tolist(), key="drop_cols")
        if st.button("Drop Selected"):
            st.session_state.df_preview = df.drop(columns=cols_to_drop)
            st.session_state.log_preview = f"Dropped: {', '.join(cols_to_drop)}."
            st.rerun()
            
    with tab2:
        st.subheader("Arithmetic Column")
        num_cols = get_numeric_columns(df)
        col_name = st.text_input("New name:", key="arith_name")
        c1, c2, c3 = st.columns(3)
        op1 = c1.selectbox("Op 1", num_cols, key="arith_op1")
        op = c2.selectbox("Operation", ["+", "-", "*", "/"], key="arith_op")
        op2 = c3.selectbox("Op 2", num_cols, key="arith_op2")
        if st.button("Create Arithmetic Column"):
            df_cleaned = df.copy()
            if op == "+": df_cleaned[col_name] = df[op1] + df[op2]
            elif op == "-": df_cleaned[col_name] = df[op1] - df[op2]
            elif op == "*": df_cleaned[col_name] = df[op1] * df[op2]
            else: df_cleaned[col_name] = df[op1] / df[op2]
            st.session_state.df_preview = df_cleaned
            st.session_state.log_preview = f"Created arithmetic column '{col_name}'."
            st.rerun()

    with tab3:
        st.subheader("Concatenate Text Columns")
        cat_cols = get_categorical_columns(df)
        new_name = st.text_input("New column name:", value="joined_text", key="concat_name")
        c1, c2 = st.columns(2)
        col_a = c1.selectbox("First column", cat_cols, key="concat_a")
        col_b = c2.selectbox("Second column", cat_cols, key="concat_b")
        sep = st.text_input("Separator:", value=" ", key="concat_sep")
        if st.button("Create Concatenated Column"):
            df_cleaned = df.copy()
            df_cleaned[new_name] = df_cleaned[col_a].astype(str) + sep + df_cleaned[col_b].astype(str)
            st.session_state.df_preview = df_cleaned
            st.session_state.log_preview = f"Concatenated '{col_a}' and '{col_b}' into '{new_name}'."
            st.rerun()
