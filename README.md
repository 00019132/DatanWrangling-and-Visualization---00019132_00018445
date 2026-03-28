# AI-Assisted Data Wrangler & Visualizer

A multi-page Streamlit web application designed as an interactive "data preparation studio." This tool allows users to upload datasets, perform a wide range of cleaning and transformation operations, build dynamic visualizations, and export the cleaned data along with a detailed report of all actions performed.

This project was developed for the Data Wrangling and Visualization (5COSC038C) coursework.

---

## Key Features

The application is organized into four main modules:

### 1. Upload & Overview
-   **File Upload**: Supports **CSV**, **Excel (.xlsx)**, and **JSON** files.
-   **Data Profiling**: Instantly view key dataset metrics:
    -   Shape (rows, columns).
    -   Data types and column names.
    -   Basic summary statistics (mean, std, quartiles for numeric; counts, unique for categorical).
    -   Missing value counts and percentages per column.
    -   Duplicate row count.
-   **Session Management**: A "Reset Session" button to clear all data and start over.

### 2. Cleaning & Preparation Studio
A comprehensive toolkit for refining data, with a live preview system for all operations:
-   **Missing Values**:
    -   **Per-Column Actions**: Drop rows, fill with mean/median (numeric), mode (categorical), or a constant value.
    -   **DataFrame Actions**: Drop columns exceeding a user-defined missing value threshold (%).
-   **Handle Duplicates**:
    -   Detect duplicates across all columns or a user-selected subset.
    -   Remove duplicates, keeping the `first` or `last` instance.
-   **Data Types & Parsing**:
    -   **Type Conversion**: Convert columns to `numeric`, `string`, or `datetime`.
    -   **Datetime Formatting**: Specify custom date formats for accurate parsing (e.g., `%d/%m/%Y`).
    -   **Clean Numeric Strings**: Remove common and custom-defined non-numeric characters (e.g., `$`, `,`, `%`) from strings before type conversion.
-   **Categorical Data**:
    -   **Standardization**: Trim whitespace, convert to `lowercase` or `Title Case`.
    -   **Value Mapping**: Interactively map values to new ones using an editable table.
    -   **Rare Category Grouping**: Group infrequent categories into an "Other" bucket based on a frequency threshold.
-   **Numeric Cleaning (Outliers)**:
    -   Detect outliers using the IQR method.
    -   **Actions**: Remove outlier rows or cap values at the upper/lower bounds.
-   **Normalization & Scaling**:
    -   Apply **Min-Max Scaling** or **Z-Score Standardization** to selected numeric columns.
-   **Column Operations**:
    -   **Drop Columns**: Remove one or more columns.
    -   **Rename Columns**: Rename multiple columns at once.
    -   **Create Columns**: Generate new columns from arithmetic operations (`Col A + Col B`) or string concatenation.

### 3. Visualization Builder
-   **Dynamic Chart Generation**:
    -   **Chart Types**: Build Histograms, Box Plots, Scatter Plots, Line Charts, Bar Charts, and Correlation Heatmaps.
    -   **Customization**: Select columns for X and Y axes, and optionally a column for color grouping.
-   **Interactive Plots**: Powered by Plotly for a rich, interactive experience.

### 4. Export & Report
-   **Export Cleaned Data**: Download the transformed dataset as a `cleaned_data.csv` file.
-   **Downloadable Reports**:
    -   **Transformation Log**: A `.txt` file with a timestamped log of every action taken.
    -   **Transformation Recipe**: A `recipe.json` file that programmatically captures the entire cleaning workflow.

---

## 🛠️ Tech Stack

-   **Backend & Frontend**: [Streamlit](https://streamlit.io/)
-   **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
-   **Visualization**: [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/)

---

## ⚙️ Local Development

To run this application on your local machine, follow these steps.

**1. Clone the repository:**
```bash
git clone <your-repository-url>
cd DatanWrangling-and-Visualization---00019132_00018445
```

**2. Create and activate a Python virtual environment:**
```bash
# We recommend Python 3.10 or newer
python3 -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit application:**
```bash
streamlit run streamlit_app.py
```
The application should now be running and accessible at `http://localhost:8501`.

---

## ☁️ Deployment

This application is deployed on the Streamlit Community Cloud.

**[Link to your deployed app]** (<- *Replace this with your public app URL after deployment*)

---

## 👥 Authors

-   [Student 1 Name]
-   [Student 2 Name]
