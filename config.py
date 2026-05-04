# Subtle, premium-looking dark-on-light theme overrides
PREMIUM_CSS = """
<style>
/* Global */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}

.main {
    padding: 2rem 3rem 3rem 3rem;
    background: radial-gradient(circle at top left, #0f172a 0, #020617 40%, #020617 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #020617 40%, #020617 100%);
}

/* Cards */
.premium-card {
    padding: 1.2rem 1.4rem;
    border-radius: 0.9rem;
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 18px 45px rgba(15,23,42,0.55);
}

.premium-card-light {
    padding: 1.1rem 1.3rem;
    border-radius: 0.9rem;
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 18px 45px rgba(15,23,42,0.55);
}

.metric-card {
    padding: 0.9rem 1.1rem;
    border-radius: 0.8rem;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,64,175,0.88));
    border: 1px solid rgba(129,140,248,0.55);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 650 !important;
    letter-spacing: -0.02em;
}

.stMarkdown, .stText, p {
    color: #e5e7eb !important;
}

/* Tabs */
div[data-baseweb="tab-list"] {
    gap: 0.5rem;
}

button[data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: 0.5rem 1rem !important;
    background-color: rgba(15,23,42,0.7) !important;
    border: 1px solid rgba(148,163,184,0.55) !important;
    color: #e5e7eb !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #22c55e) !important;
    color: #0b1120 !important;
    border-color: transparent !important;
}

/* Sidebar widgets */
section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] label {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] .stTextInput > div > div > input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: #020617 !important;
    border-radius: 0.5rem;
    border: 1px solid rgba(148,163,184,0.55);
    color: #e5e7eb !important;
}

/* Buttons */
button[kind="primary"] {
    border-radius: 999px !important;
    padding: 0.4rem 1.1rem !important;
    background: linear-gradient(135deg, #4f46e5, #22c55e) !important;
    border: none !important;
    color: #0f172a !important;
    font-weight: 600 !important;
}

button[kind="secondary"] {
    border-radius: 999px !important;
}

/* Tables */
.stDataFrame table {
    border-radius: 0.8rem;
    overflow: hidden;
}

.stDataFrame table thead tr {
    background: #020617 !important;
}

.stDataFrame table tbody tr:nth-child(even) {
    background: rgba(15,23,42,0.55) !important;
}

.stDataFrame table tbody tr:nth-child(odd) {
    background: rgba(15,23,42,0.85) !important;
}
</style>
"""

# Predefined test cases
PREDEFINED_TESTS = {
    "DNA Sequence": {
        "text": "GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC",
        "pattern": "GATCGATC",
        "description": "Repetitive DNA sequence with multiple matches"
    },
    "Worst Case - Naive": {
        "text": "a" * 100,
        "pattern": "a" * 9 + "b",
        "description": "Worst case for Naive algorithm - pattern almost matches at every position"
    },
    "Best Case - Boyer-Moore": {
        "text": "b" * 100,
        "pattern": "a" * 10,
        "description": "Best case for Boyer-Moore - immediate mismatch at every position"
    },
    "Natural Language": {
        "text": "the quick brown fox jumps over the lazy dog the quick brown fox",
        "pattern": "quick",
        "description": "Natural English text with common word pattern"
    },
    "Code Search": {
        "text": "def function(): return value; def another_function(): return value;",
        "pattern": "return",
        "description": "Searching for keyword in code"
    },
    "No Match": {
        "text": "abcdefghijklmnopqrstuvwxyz" * 4,
        "pattern": "xyz123",
        "description": "Pattern not present in text"
    }
}
