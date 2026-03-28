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

### Phase 2: Cleaning & Preparation Studio Overhaul

This phase addresses the functional and quality gaps in `pages/2_Cleaning_and_Preparation.py` to meet all requirements for a perfect score.

#### **Part 1: Foundational Refactoring (Improving Existing Features)**

This part focuses on adding the required safety and usability features to the components that are already in place.

*   [ ] **1.1: Implement "Guardrails" for Type-Specific Operations**
    *   [ ] Modify the "Handle Missing Values" section. The options "Fill with Mean" and "Fill with Median" should only be selectable if the chosen column's `dtype` is numeric.
    *   [ ] Create a helper function `get_numeric_columns(df)` and `get_categorical_columns(df)` to be used throughout the page.
    *   [ ] Update all select boxes to use these helper functions to provide only valid column choices.

*   [ ] **1.2: Implement "Preview and Confirm" Workflow**
    *   [ ] Create a reusable function or pattern for previewing changes. This function will take the original `df` and the proposed `new_df`.
    *   [ ] It should display a `st.expander("Preview Changes")` that shows:
        *   A summary of the change (e.g., "Will remove 50 rows.", "Will modify 2 columns.").
        *   A `st.dataframe(df.compare(new_df))` to highlight the exact cells that will change (for a sample of the data if it's large).
    *   [ ] A "Confirm" button must be present inside the expander to apply the change to the session state.
    *   [ ] Refactor the *existing* "Handle Missing Values" feature to use this new "Preview and Confirm" workflow.
    *   [ ] Refactor the *existing* "Handle Duplicates" feature to use this workflow.
    *   [ ] Refactor the *existing* "Manage Data Types" and "Categorical Data" features to use this workflow.

*   [ ] **1.3: Fulfill "Show Duplicates" Requirement**
    *   [ ] In the "Handle Duplicates" expander, add a new button: "Show Duplicate Rows".
    *   [ ] When clicked, this button should display a dataframe containing all rows identified as duplicates based on the selected subset of columns, keeping all duplicates for inspection (`keep=False`).

#### **Part 2: Implementing Missing Core Features**

This part adds the major functional blocks that are completely missing from the page. Each will be a new `st.expander`.

*   [ ] **2.1: Implement "Numeric Cleaning" (Outliers)** (Rubric 4.5)
    *   [ ] Create a new expander: "5. Clean Numeric Data (Outliers)".
    *   [ ] Add a UI to select a numeric column.
    *   [ ] Display an outlier summary for the selected column (e.g., using the IQR method to count outliers below Q1 - 1.5*IQR and above Q3 + 1.5*IQR). Show the number of low/high outliers.
    *   [ ] Provide an action to **Remove Outlier Rows**. This should use the "Preview and Confirm" workflow.
    *   [ ] Provide an action to **Cap/Winsorize Outliers**. The user should be able to cap them at the calculated IQR bounds. This should also use the "Preview and Confirm" workflow.

*   [ ] **2.2: Implement "Normalization / Scaling"** (Rubric 4.6)
    *   [ ] Create a new expander: "6. Normalize and Scale Data".
    *   [ ] Add a `st.multiselect` to allow the user to choose one or more numeric columns to scale.
    *   [ ] Provide an option for **Min-Max Scaling**.
    *   [ ] Provide an option for **Z-Score Standardization**.
    *   [ ] When an action is selected, use the "Preview and Confirm" workflow. The preview should show summary statistics (`.describe()`) of the columns before and after the proposed change.

*   [ ] **2.3: Implement "Column Operations"** (Rubric 4.7)
    *   [ ] Create a new expander: "7. Column Operations".
    *   [ ] **Drop Columns:**
        *   [ ] Add a `st.multiselect` for users to select columns to drop.
        *   [ ] Use the "Preview and Confirm" workflow to show which columns will be removed.
    *   [ ] **Rename Columns:**
        *   [ ] Add a UI that dynamically generates `st.text_input` fields for each column in the dataframe, showing the old name and allowing the user to type a new one.
        *   [ ] Use "Preview and Confirm" to apply the renaming.
    *   [ ] **Create New Column (Stretch Goal):** If time permits, add a simple UI for creating a new column from basic arithmetic on two existing numeric columns.

#### **Part 3: Final Polish**

*   [ ] **3.1: Review and Refine UI**
    *   [ ] Ensure all sections are clearly labeled and follow a consistent design pattern.
    *   [ ] Add help text (`st.markdown` or tooltips) where operations are complex.
*   [ ] **3.2: Comprehensive Testing**
    *   [ ] Test every feature with a variety of datasets (including the provided sample data).
    *   [ ] Intentionally try to break the app (e.g., select invalid columns, enter bad input) to ensure all guardrails and error messages work as expected.



## Last done

I have successfully completed Part 1.1 and have made significant progress into Part 1.2 of the plan in GEMINI.md.

  Here is exactly where I stopped:

  Part 1: Foundational Refactoring

   * [x] 1.1: Implement "Guardrails" for Type-Specific Operations (COMPLETED)
       * Created get_numeric_columns and get_categorical_columns.
       * Updated all select boxes to use these helpers.
       * Added dynamic action filtering for missing values.

   * [ ] 1.2: Implement "Preview and Confirm" Workflow (IN PROGRESS)
       * [x] Create reusable function/pattern (display_preview and modal logic): COMPLETED.
       * [x] Refactor "Handle Missing Values" feature to use workflow: COMPLETED. (Both per-column and whole-dataframe actions now trigger the preview).
       * [ ] Refactor "Handle Duplicates" feature: NEXT TASK.
       * [ ] Refactor "Manage Data Types" and "Categorical Data": PENDING.

  Summary: I have just finished making the "Handle Missing Values" section safe with the new preview system. My next move is to apply the same logic to the "Handle Duplicates" section.
