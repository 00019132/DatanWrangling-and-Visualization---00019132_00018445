# **Project Plan: AI-Assisted Data Wrangler & Visualizer**

This document outlines the plan, constraints, and workflow for building the Data Wrangler & Visualizer Streamlit application. It will serve as our central guide.

---

## **1. Our Working Agreement**

This project will be executed based on the following principles, as requested:

*   **Decomposition:** We will break down every task into the smallest possible, actionable steps.
*   **Explain Before Acting:** For every step, I will first explain *what* we are doing, *why* we are doing it, and *how* it fits into the larger picture.
*   **Sequential Action:** We will not proceed with an action until the explanation is clear and we are ready to move forward.
*   **Iterative Building:** We will build the application piece by piece, ensuring each component works before adding the next.
*   **Curriculum Adherence:** We will prioritize using technologies and methods covered in the `Agenda.json` to ensure the work can be fully justified in a *viva voce*.

---

## **2. Technical Constraints & Allowed Tools**

Based on `Agenda.json`, our primary toolkit will be:

*   **Programming Language:** Python
*   **Core Data Libraries:**
    *   **NumPy:** For numerical operations, array creation, and manipulation.
    *   **Pandas:** For handling tabular data (Series, DataFrames), cleaning, aggregation (`groupby`), and manipulation.
*   **Data Visualization:**
    *   **Matplotlib:** For creating basic and advanced charts.
    *   **Plotly:** Mentioned in the coursework, and `Plotly Dash` is covered in Week 11. We will use this for dynamic visualizations.
    *   **Folium:** For any potential geospatial visualizations (covered in Week 12).
*   **Web Framework:**
    *   The coursework explicitly requires **Streamlit**. While the agenda mentions `Plotly Dash`, the primary requirement is Streamlit. We will build the app with Streamlit and use Plotly *within* Streamlit for charting.
*   **Data Sources:**
    *   File I/O for CSV, Excel (`.xlsx`), and JSON.
    *   Google Sheets integration (covered in Week 9).

We will avoid using advanced libraries or techniques not mentioned in the agenda unless absolutely necessary and after a specific discussion.

---

## **3. High-Level Project Roadmap**

We will build the application in the following order, focusing on one page at a time.

*   **Phase 1:  Project Setup & "Page A: Upload & Overview"**
    *   Set up the basic Streamlit application structure.
    *   Implement file uploaders for CSV, Excel, and JSON.
    *   Display data profiling: shape, columns, dtypes, summary stats, missing values, and duplicates count.
    *   Add a "Reset session" button.

*   **Phase 2: "Page B: Cleaning & Preparation Studio"**
    *   **Part 1 (Missing Values):** Implement UI controls to drop or fill missing data.
    *   **Part 2 (Duplicates):** Implement UI to find and remove duplicate rows.
    *   **Part 3 (Data Types):** Implement UI for type conversion.
    *   **Part 4 (Categorical Tools):** Implement UI for whitespace trimming, case standardization, and value mapping.
    *   **Part 5 (Numeric Tools):** Implement UI for outlier handling and normalization/scaling.
    *   **Part 6 (Column Operations):** Implement UI for renaming and dropping columns.

*   **Phase 3: "Page C: Visualization Builder"**
    *   Create a dynamic UI for users to select chart types (Bar, Line, Scatter, etc.).
    *   Allow users to select columns for X-axis, Y-axis, and color.
    *   Render the selected chart using Plotly.

*   **Phase 4: "Page D: Export & Report"**
    *   Implement functionality to export the cleaned DataFrame to CSV.
    *   Develop a system to log every transformation made by the user.
    *   Generate and export a transformation report from the logs.

*   **Phase 5: Finalization & Deployment**
    *   Refine error handling and UI/UX.
    *   Create the required `README.md`, `AI_USAGE.md`, and other documentation.
    *   Record the demo video.
    *   Deploy the application to Streamlit Community Cloud.

---

## **4. Current Task**

Our immediate next step is:

**Task:** Create a detailed, step-by-step plan for **Phase 1: Project Setup & "Page A: Upload & Overview"**.
