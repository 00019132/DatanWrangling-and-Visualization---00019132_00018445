# AI Usage Report

This document outlines how AI assistance (Gemini) was used during the development of the "AI-Assisted Data Wrangler & Visualizer" project. The AI was primarily used as a guide, a debugging partner, and a source for best practices, not as the primary author of the code. All code suggested by the AI was manually reviewed, tested, and integrated into the project by the development team.

Below is a representative list of prompts that reflect the nature of our interaction with the AI.

### 1. Initial Project Setup and Structuring
1.  "What is a good way to structure a multi-page Streamlit application? Should we use the `pages/` directory convention?"
2.  "My main script is getting crowded. Should I move helper functions to a `sidebar_utils.py` file? How would I import them correctly?"
3.  "Can you provide a template for a `requirements.txt` file for a data science project using Streamlit, pandas, and Plotly?"
4.  "How should we manage the dataset's state across different pages in Streamlit? Is `st.session_state` the right tool?"
5.  "We need to allow users to upload CSV, Excel, and JSON files. What's the best practice for handling each type?"
6.  "I'm trying to read a JSON file that is a list of records. `pd.read_json` is giving an error. How do I load this structure into a DataFrame?"
7.  "When a user uploads a new file, how do I make sure all previous session state data (like the old dataframe and logs) is completely cleared out?"

### 2. Core Data Manipulation (Pandas)
8.  "Can you explain the difference between `.loc`, `.iloc`, and direct indexing `[]` in pandas? When should I use each?"
9.  "What is the pandas equivalent of an SQL `GROUP BY` and `COUNT`? We need to find the frequency of unique values in a column."
10. "We're trying to implement a feature to remove outliers. Can you explain the IQR (Interquartile Range) method and how to apply it to a pandas DataFrame column?"
11. "How can we let a user choose to fill missing values in a column with the mean, median, or mode?"
12. "What's an efficient way to remove currency symbols and commas from a string column to prepare it for numeric conversion?"
13. "What's a good way to implement an 'undo' feature? Should I store a history of dataframes in `st.session_state`?"
14. "I need to apply a custom function to multiple columns at once. Is there a more efficient way than iterating with a for loop?"

### 3. Streamlit UI and Interactivity
15. "How can we create a dynamic UI where selecting a column from a dropdown then populates a second dropdown with relevant options?"
16. "We want to show a preview of changes but not apply them until the user clicks 'Confirm'. What's a good pattern for this using `st.session_state`?"
17. "How do you create tabs inside an `st.expander`? We want to group column operations like 'Rename', 'Drop', and 'Arithmetic'."
18. "What's the best way to let a user rename a selection of columns? We were thinking of generating `st.text_input` fields for each."
19. "How can I use `st.metric` to display the change in row and column count within our preview dialog?"

### 4. Visualization
20. "Can you provide a basic code snippet for creating a histogram from a pandas column using Matplotlib and displaying it in Streamlit?"
21. "How can I customize the axis labels and title of a Matplotlib chart generated within Streamlit?"
22. "We want to build a scatter plot where the user selects the X and Y axes. How can we make the plot update dynamically?"
23. "How can I create a correlation heatmap for all numeric columns using Plotly?"
24. "My Plotly chart takes up too much space. How can I control its height and make it fit the container width in the Streamlit layout?"
25. "How can we generate a downloadable report that contains a summary of all the cleaning operations the user performed?"

### 5. Debugging and Refinement
26. "My app reruns from the top and loses the uploaded data every time I click a button. Why is this happening and how do I fix it using session state?"
27. "I'm getting a `SettingWithCopyWarning` in pandas when I try to modify a dataframe. What does it mean and how can I write the code to avoid it?"
28. "How do I add a `try-except` block to my data conversion function to catch `ValueError` and show a friendly error message in the Streamlit UI instead of crashing?"
29. "How do we use `st.cache_data` correctly to prevent reloading the original dataset every time the script reruns?"
30. "My `requirements.txt` was generated with `pip freeze` and has a lot of extra packages. How can I create a minimal `requirements.txt` for my app for faster deployment?"


### Verification
All code and suggestions provided by the AI were manually verified, tested for correctness, and adapted to fit the project's specific requirements and coding style. The final implementation was a result of the team's direct coding and integration efforts.
