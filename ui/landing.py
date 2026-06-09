"""
ui/landing.py
─────────────
Landing / onboarding screen shown when no document is loaded.
Call render_landing() from app.py.
"""

import streamlit as st


TOOLS = [
    ("💬", "Ask", "Get precise answers from your document, with source references."),
    ("🧠", "Quiz Me", "Generate MCQs on any topic and test yourself instantly."),
    ("📝", "Summarise", "Get a structured summary + key concepts at a glance."),
    ("🃏", "Flashcards", "Flip through AI-generated cards to reinforce recall."),
]


def render_landing():
    st.markdown(
        """
<div style="text-align:center;padding:3rem 1rem 2rem;">
  <p style="font-family:'Playfair Display',serif;font-size:3rem;font-weight:700;
     color:#f8f5f0;line-height:1.1;margin-bottom:0.5rem;">
    Study smarter,<br><span style="color:#f59e0b;">not harder.</span>
  </p>
  <p style="font-size:1.05rem;color:#64748b;max-width:520px;margin:0 auto 2.5rem;">
    Upload any PDF — textbook chapter, lecture slides, past paper — and StudyWise turns it into
    an active study session in seconds.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="medium")
    for col, (icon, name, desc) in zip(cols, TOOLS):
        col.markdown(
            f"""
<div class="sw-card" style="text-align:center;height:160px;">
  <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
  <div style="font-weight:700;color:#f8f5f0;margin-bottom:0.4rem;">{name}</div>
  <div style="font-size:0.82rem;color:#64748b;line-height:1.5;">{desc}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<p style="text-align:center;color:#475569;font-size:0.88rem;margin-top:1rem;">
  ← Enter your Groq API key and upload a PDF to get started
</p>
""",
        unsafe_allow_html=True,
    )