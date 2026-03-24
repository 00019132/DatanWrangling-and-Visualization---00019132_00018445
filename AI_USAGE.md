# AI Usage Declaration

This document outlines the usage of an AI assistant (Google's Gemini) in the development of the "AI-Assisted Data Wrangler & Visualizer" project. The development process was a collaborative effort between the student and the AI, following a strict, conversational, and step-by-step methodology.

## Development Methodology

The core principle of the collaboration was "Explain, then Act." The AI assistant was instructed to break down every task into the smallest possible steps and to provide a detailed explanation of the "what" and "why" before generating or modifying any code. The student was responsible for reviewing the explanation, asking for clarification, and giving the final "go-ahead" for each action.

## Roles & Responsibilities

### AI Assistant (Gemini)

-   **Planning & Strategy:** Broke down the high-level requirements from the coursework (`CW.md`) into a detailed, phased development plan.
-   **Code Generation:** Wrote the Python code for the Streamlit application, including UI components, data processing logic, and Plotly visualizations. All code was generated incrementally, one small feature at a time.
-   **Conceptual Explanation:** Provided detailed explanations for all Python, Pandas, and Streamlit concepts as they were implemented.
-   **Debugging:** Assisted in diagnosing and fixing errors, such as `ModuleNotFoundError` and issues related to library version compatibility (`st.experimental_rerun` vs. `st.rerun`). This involved identifying the root cause and proposing a solution.
-   **File Operations:** Performed file system operations such as creating, writing, and modifying project files (`.py`, `.md`, `.txt`).

### Student (Developer)

-   **Project Oversight:** Guided the overall direction of the project, ensuring the AI's actions were aligned with the coursework requirements and the "viva voce" constraints (e.g., sticking to topics covered in the `Agenda.json`).
-   **Decision Making:** Made key decisions, such as when to skip parts of a planned phase (e.g., skipping most of Phase 2) and when to move on to the next.
-   **Command Execution:** Was responsible for running shell commands in the local terminal, including activating the virtual environment, installing dependencies via `pip`, and running the Streamlit server.
-   **Testing & Verification:** Actively tested the application at each step, reported bugs and errors (e.g., the app not loading, version-compatibility issues), and confirmed when features were working as expected.
-   **Final Authority:** Provided the final confirmation for every step and code modification proposed by the AI.

## Example Workflow

1.  **AI:** Proposes a plan to add a feature (e.g., "Add a download button").
2.  **AI:** Explains the Streamlit widget to be used (`st.download_button`) and the Pandas function needed (`.to_csv()`).
3.  **Student:** Approves the plan.
4.  **AI:** Generates the code to implement the feature and modifies the relevant file.
5.  **Student:** Tests the new button in the running application and confirms it works.
6.  **AI/Student:** Move to the next small step.

This structured interaction ensured that the student understood every line of code and every concept involved in the project's construction.
