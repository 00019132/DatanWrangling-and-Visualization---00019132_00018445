# AI-Assisted Data Wrangler & Visualizer

This project is a Streamlit web application designed as a "data preparation studio" for the Data Wrangling and Visualization (5COSC038C) coursework. It allows a user to upload a dataset, interactively clean and transform it, build visualizations, and export the results.

## Features

The application is organized into four main pages:

### 1. Upload & Overview
-   Upload data files in **CSV**, **Excel (.xlsx)**, or **JSON** formats.
-   View a comprehensive data profile including:
    -   Dataset shape (rows and columns).
    -   Column data types and information.
    -   Summary statistics for all columns.
    -   Missing value counts and percentages.
    -   Total count of duplicate rows.
-   Reset the session to start over with a new file.

### 2. Cleaning & Preparation
-   **Handle Missing Values:**
    -   Select any column that contains missing data.
    -   Choose an action: Drop rows, or fill with the mean, median, mode, or a user-defined constant value.
    -   Changes are applied and logged instantly.

### 3. Visualization Builder
-   **Dynamically Create Charts:**
    -   Select from various chart types: Bar, Line, Scatter, Box Plot, and Histogram.
    -   Choose columns from the dataset for the X-axis, Y-axis, and an optional color dimension.
    -   Generate and interact with plots created using Plotly.

### 4. Export & Report
-   **Export Data:** Download the current, cleaned dataset as a `cleaned_data.csv` file.
-   **Transformation Report:**
    -   View a complete, timestamped log of all cleaning actions performed during the session.
    -   Download the report as a `transformation_report.txt` file.

## Setup & Running the Application

This project uses a Python virtual environment to manage dependencies.

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

**2. Create and activate the virtual environment:**
```bash
# Create the venv
python3 -m venv venv

# Activate the venv (on Linux/macOS)
source venv/bin/activate
```

**3. Install dependencies:**
Make sure the virtual environment is active, then run:
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit app:**
```bash
streamlit run 1_Upload_and_Overview.py
```

The application will be available at `http://localhost:8501`.
