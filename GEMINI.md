# Gemini Project Configuration

This file instructs the Gemini agent on how to behave within this project.

## Core Principles

1.  **Detailed Planning:**
    *   Before starting any task, I will create a detailed, step-by-step plan.
    *   The plan will be broken down into the smallest possible actions.
    *   I will present the plan to you for approval before executing any steps.
    *   For each step, I will create a sub-plan if the task can be broken down further.
    *   I will not proceed with any action without your explicit confirmation.

2.  **Educate and Collaborate:**
    *   I will explain every action I take, providing context and reasoning.
    *   Our interaction will be a collaborative process. I will guide you through the project, but we will make decisions together.

## Technical Constraints

The following constraints are derived from the project's `Agenda.json` and `CW.md` and must be strictly followed.

### Allowed Libraries and Technologies:

*   **Web Framework:** Streamlit (`streamlit`)
*   **Data Manipulation:**
    *   `pandas`
    *   `numpy`
*   **Data Visualization:**
    *   `matplotlib` (Required for core visualizations)
    *   `plotly` (Optional, for dynamic charts)
    *   `folium` (Optional, for geospatial visualizations)
*   **File I/O:**
    *   CSV files
    *   Excel files (`.xlsx`)
    *   JSON files

### Prohibited Technologies:

*   Unless explicitly listed in the "Allowed Libraries and Technologies" section or the `Project/Agenda.json`, no other libraries or frameworks should be used without prior discussion and your approval.
*   We must only use techniques and concepts covered in the `Project/Agenda.json`.

## Project Workflow

1.  **Analyze:** I will start by analyzing the user's request and the existing codebase.
2.  **Plan:** I will create a detailed plan and get your approval.
3.  **Execute:** I will execute the plan step-by-step, explaining each action.
4.  **Verify:** I will verify the changes with you to ensure they meet the requirements.

This `GEMINI.md` file will serve as our contract for working on this project.

## Master Plan: Road to 100/100

This plan details the steps required to complete the "4. Export and Report" page to meet all requirements for a top grade.

### Part 1: Add Excel Export to `pages/4_Export_and_Report.py`

1.  **Import `io` Library:** Add `import io` at the top of the file to handle the in-memory Excel file.
2.  **Create Excel Conversion Function:** Define a new function, `@st.cache_data def convert_df_to_excel(df):`, that does the following:
    *   Creates an in-memory byte stream: `output = io.BytesIO()`.
    *   Uses a `with pd.ExcelWriter(output, engine='xlsxwriter') as writer:` block.
    *   Writes the DataFrame to the writer: `df.to_excel(writer, index=False, sheet_name='Sheet1')`.
    *   Retrieves the content of the stream: `processed_data = output.getvalue()`.
    *   Returns `processed_data`.
3.  **Restructure Download Buttons:**
    *   Create two columns: `col1, col2 = st.columns(2)`.
    *   Move the existing CSV `st.download_button` inside `with col1:`.
4.  **Add Excel Download Button:**
    *   Inside `with col2:`, add a new `st.download_button`.
    *   Set its `label` to "Download data as Excel".
    *   Set its `data` to the result of calling `convert_df_to_excel(df)`.
    *   Set `file_name` to `'cleaned_data.xlsx'`.
    *   Set `mime` to `'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'`.

### Part 2: Implement Structured Recipe Logging in `pages/2_Cleaning_and_Preparation.py`

1.  **Initialize Recipe in Session State:** At the top of the script, where `st.session_state.log` is initialized, add a line: `if 'recipe' not in st.session_state: st.session_state.recipe = []`.
2.  **Modify `update_dataframe` and `display_preview` functions:**
    *   Update the function signatures to accept a new parameter, `recipe_step`.
    *   `def update_dataframe(new_df, message, recipe_step):`
    *   Inside `update_dataframe`, add the line `st.session_state.recipe.append(recipe_step)` to store the structured step.
    *   The `display_preview` function calls `update_dataframe`. We need to store the `recipe_step` in the session state along with the preview.
    *   The new preview signature will be `st.session_state.log_preview, st.session_state.recipe_preview = log_msg, recipe_step`.
    *   Inside `display_preview`, when the user confirms, the call to `update_dataframe` will now be `update_dataframe(preview_df, log_message, st.session_state.recipe_preview)`.
3.  **Update All Cleaning Actions to Generate a Recipe Step:** For every button that applies a transformation, we will now create a `recipe_step` dictionary and pass it when we set the preview state.

    *   **Missing Values (Per-Column):**
        *   Inside the `if st.button("Apply Per-Column Action")` block.
        *   Before setting the preview, create the `recipe_step` dict.
        *   Example for "Drop rows": `recipe_step = {"action": "dropna", "parameters": {"subset": [selected_col]}}`
        *   Example for "Fill with Mean": `recipe_step = {"action": "fillna", "parameters": {"column": selected_col, "method": "mean"}}`
        *   Example for "Fill with Constant": `recipe_step = {"action": "fillna", "parameters": {"column": selected_col, "value": constant_value}}`
        *   The call to set the preview will be updated to include the recipe.

    *   **Missing Values (Drop by Threshold):**
        *   `recipe_step = {"action": "drop_by_missing_threshold", "parameters": {"threshold_percent": threshold}}`

    *   **Handle Duplicates:**
        *   `recipe_step = {"action": "drop_duplicates", "parameters": {"subset": subset, "keep": keep_option}}`

    *   **Manage Data Types:**
        *   `recipe_step = {"action": "convert_type", "parameters": {"column": col_to_convert, "new_type": new_type}}`

    *   **Categorical - Standardization:**
        *   `recipe_step = {"action": "standardize_text", "parameters": {"column": cat_col_std, "method": std_action}}`

    *   **Categorical - Mapping:**
        *   `recipe_step = {"action": "map_values", "parameters": {"column": map_col, "mapping": mapping}}`

    *   **Categorical - Rare Grouping:**
        *   `recipe_step = {"action": "group_rare_categories", "parameters": {"column": group_col, "threshold_percent": threshold}}`

    *   **Categorical - One-Hot Encoding:**
        *   `recipe_step = {"action": "one_hot_encode", "parameters": {"columns": cols_to_encode}}`

    *   **Numeric - Outliers:**
        *   Remove: `recipe_step = {"action": "remove_outliers_iqr", "parameters": {"column": selected_num_col}}`
        *   Cap: `recipe_step = {"action": "cap_outliers_iqr", "parameters": {"column": selected_num_col}}`

    *   **Normalization / Scaling:**
        *   `recipe_step = {"action": "scale_data", "parameters": {"columns": cols_to_scale, "method": method}}`

    *   **Column Operations:**
        *   Drop: `recipe_step = {"action": "drop_columns", "parameters": {"columns": cols_to_drop}}`
        *   Arithmetic: `recipe_step = {"action": "create_arithmetic_column", "parameters": {"new_column": col_name, "op1": op1, "operator": op, "op2": op2}}`
        *   Concatenate: `recipe_step = {"action": "concatenate_columns", "parameters": {"new_column": new_name, "col_a": col_a, "col_b": col_b, "separator": sep}}`

### Part 3: Add JSON Recipe Export to `pages/4_Export_and_Report.py`

1.  **Import `json` Library:** Add `import json` at the top of the file.
2.  **Add New Section "Recipe":** Below the "Transformation Report" section, add a new header: `st.header("Transformation Recipe")`.
3.  **Check for and Display Recipe:**
    *   Use an `if 'recipe' in st.session_state and st.session_state.recipe:` block.
    *   Inside, add a message: `st.write("The following machine-readable recipe can be used to replay the transformations:")`.
    *   Display the recipe with `st.json(st.session_state.recipe)`.
4.  **Add Download Button for Recipe:**
    *   Convert the recipe to a JSON string: `recipe_json = json.dumps(st.session_state.recipe, indent=4)`.
    *   Add a `st.download_button` with:
        *   `label="Download Recipe as JSON"`
        *   `data=recipe_json`
        *   `file_name='transformation_recipe.json'`
        *   `mime='application/json'`
5.  **Add Else Block:** If no recipe is found, display a message like `st.info("No recipe generated. Apply some cleaning steps first.")`.

---
This master plan will be our guide. We will tackle it one part at a time.
