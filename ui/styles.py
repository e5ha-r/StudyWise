"""
ui/styles.py
────────────
All global CSS for StudyWise.
Call inject_css() once at the top of app.py.
"""

import streamlit as st


CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500;600;700&display=swap');

  /* ── Reset & Base ─────────────────────────────── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f172a !important;
    color: #f8f5f0 !important;
  }
  .block-container { padding: 2rem 2.5rem 3rem 2.5rem !important; max-width: 1200px; }

  /* ── Sidebar ──────────────────────────────────── */
  [data-testid="stSidebar"] {
    background: #1e293b !important;
    border-right: 1px solid #334155;
  }
  [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

  /* ── Brand wordmark ───────────────────────────── */
  .brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    color: #f8f5f0;
    letter-spacing: -0.5px;
    line-height: 1.1;
  }
  .brand-dot { color: #f59e0b; }

  /* ── Tool nav tabs ────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    background: #1e293b;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #334155;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #94a3b8 !important;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
    border: none;
  }
  .stTabs [aria-selected="true"] {
    background: #f59e0b !important;
    color: #0f172a !important;
    font-weight: 700 !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

  /* ── Buttons ──────────────────────────────────── */
  .stButton > button {
    background: #f59e0b;
    color: #0f172a;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.4rem;
    transition: background 0.15s;
  }
  .stButton > button:hover { background: #d97706; color: #0f172a; }

  /* ── Inputs ───────────────────────────────────── */
  .stTextInput > div > div > input,
  .stTextArea textarea {
    background: #1e293b !important;
    color: #f8f5f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea textarea:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 2px rgba(245,158,11,0.2) !important;
  }

  /* ── Cards ────────────────────────────────────── */
  .sw-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
  }
  .sw-card-amber {
    background: #1e293b;
    border: 1px solid #f59e0b;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
  }
  .sw-answer-block {
    background: #162032;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    font-size: 0.97rem;
    line-height: 1.7;
  }
  .sw-source-pill {
    display: inline-block;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: #94a3b8;
    margin: 2px 3px;
  }

  /* ── Quiz ─────────────────────────────────────── */
  .quiz-q {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f8f5f0;
    margin-bottom: 0.8rem;
  }
  .option-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    margin-bottom: 0.45rem;
    cursor: pointer;
    color: #cbd5e1;
    font-size: 0.93rem;
    transition: all 0.15s;
  }
  .option-btn:hover { border-color: #f59e0b; color: #f8f5f0; }
  .option-correct { border-color: #10b981 !important; background: #052e16 !important; color: #6ee7b7 !important; font-weight: 600; }
  .option-wrong   { border-color: #ef4444 !important; background: #2a0d0d !important; color: #fca5a5 !important; }
  .score-badge {
    display: inline-block;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    font-size: 1.1rem;
    border-radius: 999px;
    padding: 4px 18px;
  }

  /* ── Flashcards ───────────────────────────────── */
  .flashcard-front {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%);
    border: 1px solid #3b82f6;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .flashcard-back {
    background: linear-gradient(135deg, #292524 0%, #1e293b 100%);
    border: 1px solid #f59e0b;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .flashcard-term {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #f8f5f0;
    margin-bottom: 0.5rem;
  }
  .flashcard-def {
    font-size: 0.97rem;
    color: #cbd5e1;
    line-height: 1.6;
  }
  .fc-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.8rem;
  }
  .fc-counter {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.8rem;
  }

  /* ── Summary ──────────────────────────────────── */
  .summary-section {
    border-left: 2px solid #f59e0b;
    padding-left: 1rem;
    margin-bottom: 1.5rem;
  }
  .key-concept-pill {
    display: inline-block;
    background: #0f172a;
    border: 1px solid #f59e0b;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.82rem;
    color: #f59e0b;
    margin: 3px;
    font-weight: 500;
  }
  .concept-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.6rem;
  }

  /* ── Progress & misc ──────────────────────────── */
  .stProgress > div > div { background: #f59e0b !important; }
  .stRadio label { color: #cbd5e1 !important; }
  .stSelectbox label { color: #94a3b8 !important; }
  [data-testid="stFileUploader"] {
    background: #1e293b;
    border: 2px dashed #334155;
    border-radius: 10px;
    padding: 1rem;
  }
  .stAlert { border-radius: 8px !important; }
  .stat-chip {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    text-align: center;
  }
  .stat-num { font-size: 1.5rem; font-weight: 700; color: #f59e0b; }
  .stat-lbl { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }

  h1,h2,h3,h4 { color: #f8f5f0 !important; }
  p, li { color: #cbd5e1; line-height: 1.7; }
  hr { border-color: #334155 !important; }
  .stMarkdown a { color: #f59e0b; }

  /* File uploader text */
  [data-testid="stFileUploadDropzone"] * { color: #94a3b8 !important; }
</style>
"""


def inject_css():
    """Inject global CSS into the Streamlit app."""
    st.markdown(CSS, unsafe_allow_html=True)