# 🎤 Presentation Guide: String Matching Algorithms Analysis

This guide provides a combined breakdown of group responsibilities and a deep dive into the frontend architecture for your presentation.

---

## Part 1: Group Contributions (Bifurcation)

To ensure a balanced 5-person presentation, the project is divided by architectural layers:

### 👤 Member 1: Basic Algorithms (Theory & Logic)
*   **Domain:** Naive & KMP
*   **Key File:** `algorithms.py`
*   **Presentation Points:**
    *   Explain the **Naive** approach (simple sliding window).
    *   Explain **KMP** (Knuth-Morris-Pratt) and the **LPS (Longest Proper Prefix-Suffix)** array.
    *   Discuss the leap from $O(n \times m)$ to $O(n+m)$ complexity.

### 👤 Member 2: Advanced Algorithms (Hashing & Jumps)
*   **Domain:** Rabin-Karp & Boyer-Moore-Horspool
*   **Key File:** `algorithms.py`
*   **Presentation Points:**
    *   Explain **Rabin-Karp** and the concept of a **Rolling Hash**.
    *   Explain **Boyer-Moore-Horspool** and the **Bad Character Table**.
    *   Discuss why these are preferred for large-scale natural language search.

### 👤 Member 3: Visualization & Interactive Simulation
*   **Domain:** Visual Logic & State Generators
*   **Key File:** `visualizations.py`
*   **Presentation Points:**
    *   Explain how the app "steps" through code using **Python Generators**.
    *   Show the color-coding logic (Yellow=Comparison, Red=Mismatch, Green=Match).
    *   Demo the "Interactive Lab" live.

### 👤 Member 4: Data Analysis & Performance Benchmarking
*   **Domain:** Synthetic Data & Statistical Visualization
*   **Key Files:** `streamlit_app.py` (Tabs 1-3), `utils.py`
*   **Presentation Points:**
    *   Explain the benchmarking engine (Random vs. Repetitive text types).
    *   Interpret the **Matplotlib/Seaborn charts** (Time vs. Text Length).
    *   Discuss standard deviation and performance stability across runs.

### 👤 Member 5: UI/UX Architecture & Recommendation Logic
*   **Domain:** Frontend Design & Decision Support
*   **Key Files:** `config.py`, `streamlit_app.py` (Layout), `utils.py`
*   **Presentation Points:**
    *   Explain the **Streamlit** framework and custom **Premium CSS**.
    *   Explain the **Recommendation System** (how the app picks the best algorithm).
    *   Act as the "Moderator" for the live demo.

---

## Part 2: Frontend Deep Dive (Technical Explanation)

For Member 5 and the group to explain the "face" of the project:

### 1. Technology Choice: Streamlit
*   **Reasoning:** Chosen for its ability to create data-driven web apps entirely in Python.
*   **Execution:** The app is "reactive"—any change in the sidebar configuration triggers an immediate re-run of the benchmarking or visualization logic.

### 2. The "Premium" Design System
*   **Glassmorphism:** The `PREMIUM_CSS` in `config.py` uses semi-transparent backgrounds and radial gradients to create a modern, dark-mode aesthetic.
*   **Typography:** Custom fonts and letter-spacing are injected via CSS to move away from the standard browser look.
*   **Responsive Layout:** Uses `st.columns` to create the Hero section and side-by-side metric cards.

### 3. Interactive Component Logic
*   **HTML Rendering:** The frontend doesn't just print text; it uses `unsafe_allow_html=True` to render the search windows as color-coded spans. This allows the user to *see* the pattern sliding over the text.
*   **Navigation State:** The app uses `st.session_state` to remember which step the user is on in the visualization, allowing for smooth "Next" and "Previous" transitions without losing data.

### 4. Decision Support (The Recommendation Engine)
*   **Heuristic Logic:** The `recommend_algorithm` function acts as a "mini-AI." It analyzes:
    *   **Text Type:** Repetitive text (like DNA) favors KMP.
    *   **Pattern Length:** Long patterns favor Boyer-Moore.
    *   **Scale:** Small patterns favor Naive due to low overhead.

---

## Part 3: Live Presentation Tips
1.  **The Hook:** Start with a "DNA Sequence" or "Worst Case" predefined test to show a dramatic difference in performance.
2.  **The Visualization:** Use a short string (e.g., "ABCABC", Pattern: "ABC") for the interactive demo so the audience can follow along easily.
3.  **The Conclusion:** Use the "Complexity Summary" tab to tie the empirical benchmark results back to the theoretical Big-O notation.
