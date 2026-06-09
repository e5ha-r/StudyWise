"""
app.py — StudyWise entry point
================================
Run with:  streamlit run app.py

Project layout
──────────────
app.py                   ← this file (page config + routing only)
core/
  document.py            ← indexing, embeddings, QA chain, LLM utilities
ui/
  styles.py              ← global CSS (inject_css)
  sidebar.py             ← sidebar: API key, file upload, stats
  landing.py             ← onboarding screen (no document loaded)
tools/
  ask.py                 ← Tab 1: RAG Q&A
  quiz.py                ← Tab 2: MCQ quiz
  summarise.py           ← Tab 3: structured summary
  flashcards.py          ← Tab 4: flip-card review
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="StudyWise",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports ──────────────────────────────────────────────────────────
from ui.styles    import inject_css
from ui.sidebar   import init_session_state, render_sidebar
from ui.landing   import render_landing
from tools.ask        import render_ask_tab
from tools.quiz       import render_quiz_tab
from tools.summarise  import render_summarise_tab
from tools.flashcards import render_flashcards_tab

# ── Bootstrap ─────────────────────────────────────────────────────────────────
inject_css()
init_session_state()
render_sidebar()

# ── Routing ───────────────────────────────────────────────────────────────────
if not st.session_state.doc_name:
    render_landing()
else:
    # ── Document header ────────────────────────────────────────────────────
    st.markdown(
        f"""
<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;">
  <p style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#f8f5f0;margin:0;">
    {st.session_state.doc_name.rsplit(".", 1)[0]}
  </p>
  <span style="background:#0f172a;border:1px solid #334155;border-radius:6px;
    padding:3px 10px;font-size:0.75rem;color:#64748b;">
    {st.session_state.doc_pages} pages · {st.session_state.doc_chunks} chunks indexed
  </span>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Tool tabs ──────────────────────────────────────────────────────────
    tab_ask, tab_quiz, tab_summary, tab_flash = st.tabs([
        "💬  Ask",
        "🧠  Quiz Me",
        "📝  Summarise",
        "📄  Flashcards",
    ])

    with tab_ask:
        render_ask_tab()

    with tab_quiz:
        render_quiz_tab()

    with tab_summary:
        render_summarise_tab()

    with tab_flash:
        render_flashcards_tab()