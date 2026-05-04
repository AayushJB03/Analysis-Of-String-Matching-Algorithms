import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import random
import numpy as np

# ==============================
# Global UI configuration
# ==============================

st.set_page_config(
    page_title="String Matching Algorithms Benchmark",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import PREMIUM_CSS, PREDEFINED_TESTS
from algorithms import naive_search, kmp_search, rabin_karp_search, boyer_moore_horspool_search
from utils import recommend_algorithm, calculate_statistics
from visualizations import naive_steps, kmp_steps, rabin_karp_steps, bmh_steps, render_visualization

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# Streamlit App Title & Hero Section
hero_left, hero_right = st.columns([3, 2])
with hero_left:
    st.markdown("### 🔍 String Matching Algorithms Benchmark")
    st.markdown(
        "A premium, interactive lab to **benchmark** and **visualize** classic string "
        "matching algorithms – Naive, KMP, Rabin-Karp, and Boyer-Moore-Horspool – "
        "across realistic scenarios."
    )
with hero_right:
    st.markdown(
        """
        <div class="premium-card">
            <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.16em; color:#9ca3af;">
                Overview
            </div>
            <div style="margin-top:0.4rem; font-size:0.95rem; color:#e5e7eb;">
                • Compare execution time, comparisons, and space usage<br/>
                • Explore worst-, average-, and best-case inputs<br/>
                • Step visually through each algorithm’s internal logic
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Sidebar configuration
st.sidebar.markdown("### ⚙️ Benchmark Configuration")

input_mode = st.sidebar.radio(
    "Input Mode",
    ["Synthetic", "Manual", "Predefined Tests"],
    help="Synthetic is best for large-scale benchmarking; Manual and Predefined are ideal for focused experiments.",
)

# Robust input parsing helpers
def _parse_int_list(raw: str, field_label: str):
    try:
        values = [int(x.strip()) for x in raw.split(",") if x.strip()]
        values = [v for v in values if v > 0]
    except ValueError:
        st.sidebar.error(f"'{field_label}' must be a comma-separated list of positive integers.")
        return []
    if not values:
        st.sidebar.error(f"Please provide at least one positive integer for '{field_label}'.")
    return values

text = ""
pattern = ""

if input_mode == "Manual":
    text = st.sidebar.text_area("Text", "abcabcabcabc", height=120)
    pattern = st.sidebar.text_input("Pattern", "abc")

    if not text.strip() or not pattern:
        st.sidebar.warning("Enter both **Text** and **Pattern** to run a manual benchmark.")

    text_sizes = [len(text)]
    pattern_sizes = [len(pattern)]
    text_types = ["manual"]
    runs = 1
elif input_mode == "Predefined Tests":
    selected_test = st.sidebar.selectbox("Select Test Case", list(PREDEFINED_TESTS.keys()))
    test_info = PREDEFINED_TESTS[selected_test]
    st.sidebar.info(f"**Description:** {test_info['description']}")
    text = test_info["text"]
    pattern = test_info["pattern"]
    text_sizes = [len(text)]
    pattern_sizes = [len(pattern)]
    text_types = ["predefined"]
    runs = st.sidebar.slider("Number of Runs", 1, 10, 5)
else:
    raw_text_sizes = st.sidebar.text_input("Text Sizes (comma-separated)", "1000,5000,10000")
    text_sizes = _parse_int_list(raw_text_sizes, "Text Sizes")

    raw_pattern_sizes = st.sidebar.text_input("Pattern Sizes (comma-separated)", "3,10,50")
    pattern_sizes = _parse_int_list(raw_pattern_sizes, "Pattern Sizes")

    text_types = st.sidebar.multiselect(
        "Text Types",
        ["random", "repetitive"],
        default=["random", "repetitive"],
        help="Random ≈ typical text; Repetitive ≈ worst-case for some algorithms.",
    )
    runs = st.sidebar.slider("Number of Runs", 1, 10, 3)

algorithms = st.sidebar.multiselect(
    "Select Algorithms",
    ["Naive", "KMP", "Rabin-Karp", "Boyer-Moore-Horspool"],
    default=["Naive", "KMP", "Rabin-Karp", "Boyer-Moore-Horspool"]
)

# Algorithm Recommendation
if input_mode != "Synthetic":
    with st.sidebar.expander("🧠 Algorithm Recommendation", expanded=False):
        n_val = text_sizes[0] if text_sizes else 1000
        m_val = pattern_sizes[0] if pattern_sizes else 10
        text_type_val = text_types[0] if text_types else "random"
        expected = st.selectbox("Expected Matches", ["few", "many"], index=0)

        if st.button("Get Recommendation"):
            recs = recommend_algorithm(n_val, m_val, text_type_val, expected)
            st.markdown("### 🏆 Recommendations")
            for i, rec in enumerate(recs, 1):
                st.markdown(f"**{i}. {rec['algorithm']}** &nbsp; | &nbsp; Score: `{rec['score']}/100`")
                st.caption(rec["reason"])
                st.progress(rec["score"] / 100)

run_benchmark_clicked = st.sidebar.button("🚀 Run Benchmark", type="primary")

if run_benchmark_clicked:
    # Basic guard rails before running heavy loops
    if not algorithms:
        st.error("Please select at least **one algorithm** to benchmark.")
    elif input_mode == "Synthetic" and (not text_sizes or not pattern_sizes or not text_types):
        st.error("Please provide valid **text sizes**, **pattern sizes**, and **text types** for synthetic benchmarking.")
    elif input_mode in ("Manual", "Predefined Tests") and (len(pattern) == 0 or len(text) == 0):
        st.error("Text and Pattern must be non-empty to run the benchmark.")
    else:
        algo_map = {
            "Naive": naive_search,
            "KMP": kmp_search,
            "Rabin-Karp": rabin_karp_search,
            "Boyer-Moore-Horspool": boyer_moore_horspool_search,
        }

        results = []
        progress_bar = st.progress(0)
        total_tests = len(text_types) * len(text_sizes) * len(pattern_sizes) * len(algorithms) * runs
        current = 0

        for text_type in text_types:
            for n in text_sizes:
                for m in pattern_sizes:
                    if m > n:
                        continue

                    # Generate text and pattern
                    if input_mode == "Manual" or input_mode == "Predefined Tests":
                        test_text, test_pattern = text, pattern
                    elif text_type == "random":
                        test_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n))
                        start_pos = random.randint(0, n - m)
                        test_pattern = test_text[start_pos:start_pos + m]
                    else:
                        test_text = 'a' * n
                        test_pattern = 'a' * (m - 1) + 'b'

                    # Store sample for first test case
                    if len(results) == 0:
                        st.session_state['sample_text'] = test_text[:100] + ('...' if len(test_text) > 100 else '')
                        st.session_state['sample_pattern'] = test_pattern
                        st.session_state['text_type'] = text_type

                    for run in range(runs):
                        for algo_name in algorithms:
                            result = algo_map[algo_name](test_text, test_pattern)
                            results.append({
                                'Algorithm': algo_name,
                                'Text Type': text_type,
                                'n': n,
                                'm': m,
                                'Run': run + 1,
                                'Time (ms)': result['time_ms'],
                                'Comparisons': result['comparisons'],
                                'Space (bytes)': result['space'],
                                'Matches': len(result['matches']),
                            })
                            current += 1
                            progress_bar.progress(current / total_tests)

        if not results:
            st.warning(
                "No valid test cases were generated (for example, all pattern lengths were larger than the text lengths). "
                "Please adjust your configuration and try again."
            )
        else:
            st.session_state['results'] = pd.DataFrame(results)
            st.success(f"✅ Benchmark completed! {len(results)} tests run.")

            # Show sample text/pattern
            if 'sample_text' in st.session_state:
                with st.expander("📝 View Sample Text/Pattern (First Test Case)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Text Type:** {st.session_state['text_type']}")
                        st.markdown("**Sample Text (first 100 chars):**")
                        st.code(st.session_state['sample_text'], language='text')
                    with col2:
                        st.markdown("**Pattern:**")
                        st.code(st.session_state['sample_pattern'], language='text')

# Step-by-step visualization section
st.sidebar.markdown("---")
st.sidebar.header("🎬 Step-by-Step Visualization")
if st.sidebar.checkbox("Enable Visualization Mode"):
    viz_text = st.sidebar.text_input("Text (max 100 chars)", "abcabcabc")
    viz_pattern = st.sidebar.text_input("Pattern (max 20 chars)", "abc")
    viz_algo = st.sidebar.selectbox("Algorithm", ["Naive", "KMP", "Rabin-Karp", "Boyer-Moore-Horspool"])
    
    if len(viz_text) == 0 or len(viz_pattern) == 0:
        st.sidebar.warning("Provide both a **Text** and **Pattern** to start the visualization.")
    elif len(viz_text) > 100 or len(viz_pattern) > 20:
        st.sidebar.error("Text or pattern too long for visualization — keep text ≤ 100 and pattern ≤ 20 characters.")
    elif len(viz_pattern) > len(viz_text):
        st.sidebar.error("Pattern cannot be longer than the text for visualization.")
    else:
        if 'viz_steps' not in st.session_state:
            st.session_state['viz_steps'] = []
            st.session_state['viz_index'] = 0
        
        if st.sidebar.button("🔄 Reset Visualization"):
            algo_steps = {
                "Naive": naive_steps,
                "KMP": kmp_steps,
                "Rabin-Karp": rabin_karp_steps,
                "Boyer-Moore-Horspool": bmh_steps
            }
            st.session_state['viz_steps'] = list(algo_steps[viz_algo](viz_text, viz_pattern))
            st.session_state['viz_index'] = 0
            st.session_state['viz_text'] = viz_text
            st.session_state['viz_pattern'] = viz_pattern
            st.session_state['viz_algo'] = viz_algo

# Display results or visualization
if 'viz_steps' in st.session_state and len(st.session_state['viz_steps']) > 0 and 'results' not in st.session_state:
    # Show only visualization tab
    st.subheader(f"🎬 {st.session_state['viz_algo']} Algorithm - Step by Step")
    
    total_steps = len(st.session_state['viz_steps'])
    current_step = st.session_state['viz_index']
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    with col1:
        if st.button("⏮️ First"):
            st.session_state['viz_index'] = 0
            st.rerun()
    
    with col2:
        if st.button("◀️ Previous"):
            if st.session_state['viz_index'] > 0:
                st.session_state['viz_index'] -= 1
                st.rerun()
    
    with col3:
        if st.button("▶️ Next"):
            if st.session_state['viz_index'] < total_steps - 1:
                st.session_state['viz_index'] += 1
                st.rerun()
    
    with col4:
        if st.button("⏭️ Last"):
            st.session_state['viz_index'] = total_steps - 1
            st.rerun()
    
    with col5:
        st.markdown(f"**Step {current_step + 1} / {total_steps}**")
    
    st.markdown("---")
    
    state = st.session_state['viz_steps'][current_step]
    
    # Render visualization
    viz_html = render_visualization(st.session_state['viz_text'], st.session_state['viz_pattern'], state)
    st.markdown(viz_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display message
    st.info(f"**{state['message']}**")
    
    # Display algorithm-specific info
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Text Position", state['text_pos'])
        st.metric("Pattern Position", state.get('pattern_pos', 'N/A'))
    
    with col_b:
        if 'lps' in state:
            st.write("**LPS Array:**", state['lps'])
        elif 'pattern_hash' in state:
            st.write(f"**Pattern Hash:** {state['pattern_hash']}")
            st.write(f"**Window Hash:** {state['text_hash']}")
        elif 'bad_char' in state and current_step == 0:
            st.write("**Bad Character Table:**")
            st.json(state['bad_char'])
    
    # Progress bar
    st.progress((current_step + 1) / total_steps)
    
    st.markdown("""
    ### Legend:
    - 🟡 **Yellow**: Currently comparing
    - 🔴 **Red**: Mismatch  
    - 🟢 **Green**: Match found
    - ⬜ **Gray**: Not yet processed
    """)

if 'results' in st.session_state:
    df = st.session_state['results']
    
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Results Overview",
            "📈 Performance Charts",
            "💾 Export & Complexity",
            "🎬 Step-by-Step (Interactive)",
        ]
    )
    
    with tab1:
        st.subheader("📊 Statistical Analysis")
        
        if len(df['Run'].unique()) > 1:
            stats = calculate_statistics(df)
            st.dataframe(stats.style.format({
                'Time Mean': '{:.3f}',
                'Time Median': '{:.3f}',
                'Time Std': '{:.3f}',
                'Time Min': '{:.3f}',
                'Time Max': '{:.3f}',
                'Comp Mean': '{:.0f}',
                'Comp Median': '{:.0f}',
                'Comp Std': '{:.0f}',
                'Comp Min': '{:.0f}',
                'Comp Max': '{:.0f}'
            }), use_container_width=True)
            
            st.markdown("**Key Insights:**")
            best_algo = stats.loc[stats['Time Mean'].idxmin(), 'Algorithm']
            best_time = stats['Time Mean'].min()
            st.success(f"✅ **Fastest Algorithm:** {best_algo} (Avg: {best_time:.3f} ms)")
            
            most_stable = stats.loc[stats['Time Std'].idxmin(), 'Algorithm']
            st.info(f"🎯 **Most Consistent:** {most_stable} (Lowest std deviation)")
            
            least_comp = stats.loc[stats['Comp Mean'].idxmin(), 'Algorithm']
            st.info(f"⚡ **Fewest Comparisons:** {least_comp}")
        else:
            st.info("Run multiple iterations to see statistical analysis (mean, median, std dev)")
        
        st.markdown("---")
        st.subheader("Aggregated Results")
        agg = df.groupby(['Algorithm', 'Text Type', 'n', 'm']).agg({
            'Time (ms)': 'mean',
            'Comparisons': 'mean',
            'Space (bytes)': 'first',
            'Matches': 'first'
        }).reset_index()
        st.dataframe(agg.style.format({
            'Time (ms)': '{:.3f}',
            'Comparisons': '{:.0f}',
            'Space (bytes)': '{:.0f}'
        }), use_container_width=True)
        
        st.markdown("---")
        st.subheader("Detailed Results")
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Performance Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Time vs Text Length**")
            fig, ax = plt.subplots(figsize=(8, 5))
            for algo in df['Algorithm'].unique():
                data = df[df['Algorithm'] == algo].groupby('n')['Time (ms)'].mean()
                ax.plot(data.index, data.values, marker='o', label=algo, linewidth=2)
            ax.set_xlabel('Text Length (n)', fontweight='bold')
            ax.set_ylabel('Time (ms)', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            st.markdown("**Comparisons vs Text Length**")
            fig, ax = plt.subplots(figsize=(8, 5))
            for algo in df['Algorithm'].unique():
                data = df[df['Algorithm'] == algo].groupby('n')['Comparisons'].mean()
                ax.plot(data.index, data.values, marker='o', label=algo, linewidth=2)
            ax.set_xlabel('Text Length (n)', fontweight='bold')
            ax.set_ylabel('Comparisons', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**Time vs Pattern Length**")
            fig, ax = plt.subplots(figsize=(8, 5))
            for algo in df['Algorithm'].unique():
                data = df[df['Algorithm'] == algo].groupby('m')['Time (ms)'].mean()
                ax.plot(data.index, data.values, marker='o', label=algo, linewidth=2)
            ax.set_xlabel('Pattern Length (m)', fontweight='bold')
            ax.set_ylabel('Time (ms)', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col4:
            st.markdown("**Space Usage**")
            fig, ax = plt.subplots(figsize=(8, 5))
            space_data = df.groupby('Algorithm')['Space (bytes)'].first()
            ax.bar(space_data.index, space_data.values, color=['#ef4444', '#3b82f6', '#10b981', '#f59e0b'])
            ax.set_ylabel('Space (bytes)', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
    
    with tab3:
        st.subheader("Export Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="benchmark_results.csv",
            mime="text/csv"
        )
        
        st.subheader("Complexity Summary")
        st.markdown("""
        | Algorithm | Time (Preprocess) | Time (Search) | Space |
        |-----------|-------------------|---------------|-------|
        | Naive | O(1) | O(n×m) | O(1) |
        | KMP | O(m) | O(n+m) | O(m) |
        | Rabin-Karp | O(m) | O(n+m) avg | O(1) |
        | Boyer-Moore-Horspool | O(m+σ) | O(n/m) best | O(σ) |
        """)
    
    with tab4:
        if 'viz_steps' in st.session_state and len(st.session_state['viz_steps']) > 0:
            st.subheader(f"🎬 {st.session_state['viz_algo']} Algorithm - Step by Step")
            
            total_steps = len(st.session_state['viz_steps'])
            current_step = st.session_state['viz_index']
            
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            
            with col1:
                if st.button("⏮️ First"):
                    st.session_state['viz_index'] = 0
                    st.rerun()
            
            with col2:
                if st.button("◀️ Previous"):
                    if st.session_state['viz_index'] > 0:
                        st.session_state['viz_index'] -= 1
                        st.rerun()
            
            with col3:
                if st.button("▶️ Next"):
                    if st.session_state['viz_index'] < total_steps - 1:
                        st.session_state['viz_index'] += 1
                        st.rerun()
            
            with col4:
                if st.button("⏭️ Last"):
                    st.session_state['viz_index'] = total_steps - 1
                    st.rerun()
            
            with col5:
                st.markdown(f"**Step {current_step + 1} / {total_steps}**")
            
            st.markdown("---")
            
            state = st.session_state['viz_steps'][current_step]
            
            # Render visualization
            viz_html = render_visualization(st.session_state['viz_text'], st.session_state['viz_pattern'], state)
            st.markdown(viz_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display message
            st.info(f"**{state['message']}**")
            
            # Display algorithm-specific info
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Text Position", state['text_pos'])
                st.metric("Pattern Position", state.get('pattern_pos', 'N/A'))
            
            with col_b:
                if 'lps' in state:
                    st.write("**LPS Array:**", state['lps'])
                elif 'pattern_hash' in state:
                    st.write(f"**Pattern Hash:** {state['pattern_hash']}")
                    st.write(f"**Window Hash:** {state['text_hash']}")
                elif 'bad_char' in state and current_step == 0:
                    st.write("**Bad Character Table:**")
                    st.json(state['bad_char'])
            
            # Progress bar
            st.progress((current_step + 1) / total_steps)
            
            st.markdown("""
            ### Legend:
            - 🟡 **Yellow**: Currently comparing
            - 🔴 **Red**: Mismatch
            - 🟢 **Green**: Match found
            - ⬜ **Gray**: Not yet processed
            """)
        else:
            st.info("👈 Enable 'Step-by-Step Visualization' in the sidebar and click 'Reset Visualization' to start!")
            st.markdown("""
            ### How to use:
            1. Check **'Enable Visualization Mode'** in sidebar
            2. Enter text (max 100 chars) and pattern (max 20 chars)
            3. Select an algorithm
            4. Click **'Reset Visualization'**
            5. Use navigation buttons to step through the algorithm
            """)
else:
    if 'viz_steps' not in st.session_state or len(st.session_state.get('viz_steps', [])) == 0:
        st.info("👈 Configure settings in the sidebar and click 'Run Benchmark' or enable 'Step-by-Step Visualization' to get started!")
