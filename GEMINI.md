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

## Master Plan: Final Features for Page 2

This comprehensive plan addresses all the missing functionalities in `pages/2_Cleaning_and_Preparation.py`. It integrates them smoothly into the existing application structure and ensures that all new actions are compatible with the preview and recipe-logging system.

### Part 1: Implement "Rename Columns"

This feature is required under section 4.7 of the coursework.

1.  **UI Location:** Add a new "Rename" tab inside the **"7. Column Operations"** expander. The tabs will be updated to `["Drop", "Rename", "Arithmetic", "Concatenate"]`.
2.  **UI Design:**
    *   Inside the "Rename" tab, use `st.multiselect` to choose columns to rename.
    *   For each selected column, dynamically create a `st.text_input` to accept the new name.
    *   Add an "Apply Renaming" button.
3.  **Backend Logic:**
    *   Build a mapping dictionary from the UI inputs (e.g., `{'old_name': 'new_name'}`).
    *   Use `df.rename(columns=...)` to create the updated DataFrame.
    *   Generate the recipe step: `{"action": "rename_columns", "parameters": {"mapping": ...}}`.
    *   Trigger the preview modal to confirm changes.

### Part 2: Implement "Handle 'Dirty' Numeric Strings"

This feature is required under section 4.3 to handle real-world messy data.

1.  **UI Location:** Create a new section inside the **"3. Manage Data Types"** expander, titled **"Clean Numeric Strings"**, placing it before type conversion.
2.  **UI Design:**
    *   Use `st.selectbox` to choose the column to clean.
    *   Use `st.multiselect` pre-filled with common characters to remove (e.g., `,`, `$`, `£`, `%`), allowing for custom additions.
    *   Add a "Clean Selected Column" button.
3.  **Backend Logic:**
    *   Use `pandas.Series.str.replace()` to strip out the specified characters.
    *   Generate the recipe step: `{"action": "clean_numeric_string", "parameters": {"column": "col_name", "chars_to_remove": [...]}}`.
    *   Trigger the preview modal.

### Part 3: Implement "Datetime Parsing with Format Selection"

This feature is also required under section 4.3 for robust data type management.

1.  **UI Location:** Enhance the existing UI in the **"3. Manage Data Types"** expander.
2.  **UI Design:**
    *   When `"datetime"` is selected as the data type, a new `st.text_input` will appear for an optional date format string.
    *   Include helper text and a link to the `strftime` documentation. If left blank, pandas' default auto-parsing will be used.
3.  **Backend Logic:**
    *   If a format string is provided, use it in the `pd.to_datetime` function: `pd.to_datetime(df[col], format=user_format, errors='coerce')`.
    *   Update the recipe step to include the format: `{"action": "convert_type", "parameters": {"column": "col_name", "new_type": "datetime", "format": "..."}}`.
    *   Trigger the preview modal.
