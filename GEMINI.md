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

