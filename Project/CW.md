Module name and code, Data Wrangling and visualization ( 5COSC038C )
CW number and weighting, 50% of module grade
Contact details and office hours of the lecturer setting the task, Hamid Reza Shahbazkia Office hours: Wednesdays 16.00 -18.00
Submission deadline, March 28th at 23:59
Results date and type of feedback, 12th April 2026
. Learning outcomes, "LO1 - Use a programming environment to develop medium level structured data (Extract, Transform and Load) and prepare data for analysis.", "LO2 - Use different types of data such as Tabular (Excel, CSV, TSV etc.).", LO3 - Implement conditional search and manipulation of data by broadcasting., LO4 - Structure a data extraction program by using existing Python modules., LO5 - Explain the data by visualization in dynamic patterns., LO6 - Demonstrate advanced techniques of dashboarding and their deployment.

Work Mode: Group of 2
Expected Product: See section deliverables below

“AI-Assisted Data Wrangler & Visualizer”
READ the Instructions carefully, there are 6 required points in the submission. All should be submitted. If any is missing your work will not be evaluated. A work is considered done when all is done! This is a comprehensive work and can be deployed after completion, Start soon and do not aim at minimal. Minimal or just required means minimal pass point. Aim at excellence check design, test, real market demands etc.

Format: group project (2 students, Random group)
Time window: 2–4 weeks
Allowed: AI assistance (LLMs), documentation, web search
Required: A working Streamlit app that lets a user upload a dataset and interactively clean, transform, and visualize it, ending with a final exported dataset + dashboard.

1) Goal
Build a Streamlit application that behaves like a mini “data preparation studio”:
* User uploads a file (CSV/Excel/JSON; plus optional Google Sheets).
* App profiles the data (types, missingness, duplicates, outliers).
* User selects cleaning & preparation actions from the UI.
* App applies transformations to a working copy of the dataset.
* User dynamically creates visualizations from the transformed data.
* User exports the final dataset + a report of transformations performed.
* Your app must support repeatable workflows: the same sequence of operations should be reproduced (via an exported “recipe” or logged steps).

2) Data Inputs (Required)
Your app must accept at least:
* CSV upload (required)
* Excel upload (.xlsx) (required)
* JSON upload (required)
* Google Sheets (via service account or OAuth) (optional)

Minimum dataset constraints for testing:
Your app must handle datasets with:
* ≥ 1,000 rows
* ≥ 8 columns
* Mixed types (numeric + categorical + datetime)
* At least some missing values
* You must include at least 2 sample datasets in your repo for demonstration.

3) App Structure (Required Pages)
Your Streamlit app must have these pages (tabs or sidebar navigation):
* Page A — Upload & Overview: Upload file / connect to Sheets. Display: shape (rows, cols), column names & inferred dtypes, basic summary stats (numeric + categorical), missing values by column (count + %), duplicates count, always add one box and show number of columns. Must include a “Reset session” button.
* Page B — Cleaning & Preparation Studio: This is the core. Provide UI controls for the operations below, and apply them to the dataset.
* Page C — Visualization Builder: Let the user build charts dynamically from chosen columns, plot type, and optional grouping/aggregation.
* Page D — Export & Report: Export cleaned dataset (CSV + optionally Excel). Export a transformation report: list of steps, parameters used, timestamp. Export either: a JSON “recipe” (recommended), or a Python script snippet that replays the pipeline (stretch).

4) Cleaning & Prep Options (Required Feature Set)
4.1 Missing Values (Null Handling) Required
The app must:
* Show missing value summary (count + % per column)
* Offer per-column actions:
    * Drop rows with missing values (selected columns)
    * Drop columns with missing values above a threshold (%)
    * Replace with: constant value (user input), mean/median/mode (numeric), most frequent (categorical), forward fill / backward fill (time series).
* Must show a before/after preview (e.g., row count + affected columns).

4.2 Duplicates Required
* Detect duplicates: full-row duplicates, duplicates by subset of columns (user-selected keys).
* Provide actions: remove duplicates (keep first / keep last), show duplicate groups in a table.

4.3 Data Types & Parsing Required
Provide tools to:
* Convert column types: numeric, categorical, datetime
* Datetime parsing with format selection (or auto parse with errors coerced)
* Handle “dirty numeric” strings (commas, currency signs)

4.4 Categorical Data Tools Required
At minimum include:
* Value standardization: trim whitespace, lower/title case.
* Mapping/replacement: user provides a mapping dictionary (UI table editor), apply mapping; unmatched values remain unchanged (or optional “set to Other”).
* Rare category grouping: group categories below a frequency threshold into “Other”.
* One-hot encoding (optional but strongly recommended).

4.5 Numeric Cleaning Required
Include:
* Outlier detection summary (simple IQR or z-score).
* User chooses action: cap/winsorize at quantiles, remove outlier rows, do nothing.
* Must show impact (rows removed or values capped).

4.6 Normalization / Scaling Required
* Offer at least two: Min-max scaling, Z-score standardization.
* Must allow user to choose columns and show before/after stats.

4.7 Column Operations Required
Include:
* Rename columns
* Drop columns
* Create new column using: simple formulas (e.g., ColA + ColB) or string concatenation.

5) Interactive Visualization Builder (Required)
Your app must include a “choose your chart” experience:
    • User selects:
        ◦ plot type
        ◦ x and y columns
        ◦ optional color/group column
        ◦ optional aggregation (sum/mean/count/median)
    • Must support at least 6 chart types total:
        1. histogram
        2. box plot
        3. scatter plot
        4. line chart (time series)
        5. bar chart (grouped)
        6. heatmap or correlation matrix (numeric only)
    • Must support:
        ◦ filtering (by category and numeric range at least)
        ◦ showing “top N” categories for bar charts
    • Use matplotlib (required) + you may use Plotly or other modules(optional).

6) Session State & Robustness (Required)
6.1 Transformation Log   Required
Maintain a transformation log stored in session:
    • each step: operation name + parameters + affected columns
    • show log to the user
    • allow “undo last step” OR “reset all” (one is required)
6.2 Performance   Required
    • Must not re-run heavy steps unnecessarily:
        ◦ use st.cache_data for loading and profiling
        ◦ keep a working dataframe in st.session_state
6.3 Safety / Guardrails   Required
    • Don’t crash on bad input.
    • Show user-friendly error messages.
    • Validate column selections (e.g., scaling only numeric columns).

7) AI Assistance (Allowed, Optional Feature)
You may optionally integrate an LLM API (OpenAI or other) to enhance the app. If included, it must be:
    • Optional toggle (“Enable AI assistant”)
    • Works without AI (full required features must still work)
    • Clearly labeled that outputs may be imperfect
Optional AI features (choose any)
    1. Natural language cleaning command
        ◦ user types: “replace nulls in price with median and standardize category casing”
        ◦ app suggests operations + asks user to confirm
    2. Chart suggestion
        ◦ “Given these columns, recommend good visualizations”
    3. Code snippet generator
        ◦ generate pandas code representing the transformation recipe
    4. Data dictionary generator
        ◦ infer column meaning + likely issues

8) Deliverables (What to Submit) READ CAREFULLY  ANY submission with missing part will be rejected, your work should contain all required documents or it will not be evaluated
    1.  ZIP containing:
        ◦ app.py (or streamlit_app.py)
        ◦ requirements.txt
        ◦ README.md
        ◦ sample_data/ with at least two datasets
        ◦ All chat and prompts used from A to Z for the dev
    2. Short demo video (3–5 minutes):
        ◦ upload data
        ◦ clean missing values + categories
        ◦ normalize numeric columns
        ◦ build 2–3 visualizations
        ◦ export cleaned data + report
    3. Transformation report output (example file)
    4. AI_USAGE.md (required even if you didn’t use AI):
        ◦ what you verified manually
    5. The URL of your streamlit app deployed on streamlit site
    6. A 2 page maximum report, where AI use is strictly forbidden. The report should explain your journey as a team during this project, how you did it what was difficult what was easy what you learnt.


9) Grading Rubric (100 points)
Core Functionality (60)
* Upload + overview profiling (10)
* Missing values tools (10)
* Categorical tools + mapping UI (10)
* Scaling/normalization + numeric cleaning (10)
* Visualization builder (10)
* Export + transformation report (10)

Engineering Quality (25)
* Clean code structure (functions/modules) (8)
* Session state + caching done correctly (7)
* Error handling + validations (5)
* Usability: clear UI, helpful instructions (5)

Completeness & Design (15)

Bonus (up to +20)
* Google Sheets integration (+5)
* Undo feature + recipe replay script (+3)
* Optional LLM assistant with confirmation workflow (+12)
