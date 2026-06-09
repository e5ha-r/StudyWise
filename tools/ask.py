"""
tools/ask.py
────────────
Tab 1 — Ask: RAG-powered Q&A grounded in the uploaded document.
Call render_ask_tab() inside the tab context in app.py.
"""

import streamlit as st
from core.document import ask


def render_ask_tab():
    st.markdown("#### Ask anything about your document")
    st.markdown(
        '<p style="color:#64748b;font-size:0.88rem;margin-top:-0.5rem;">'
        "Answers are grounded in your PDF — no hallucination.</p>",
        unsafe_allow_html=True,
    )

    # ── Render conversation history ────────────────────────────────────────
    for turn in st.session_state.chat_history:
        st.markdown(
            f"""
<div style="display:flex;gap:0.8rem;margin-bottom:0.6rem;align-items:flex-start;">
  <div style="background:#f59e0b;color:#0f172a;border-radius:50%;width:28px;height:28px;
    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.8rem;
    flex-shrink:0;margin-top:2px;">Q</div>
  <div style="font-size:0.97rem;color:#f8f5f0;padding-top:4px;">{turn["q"]}</div>
</div>
<div class="sw-answer-block">{turn["a"]}</div>
""",
            unsafe_allow_html=True,
        )
        if turn.get("sources"):
            pills = " ".join(
                f'<span class="sw-source-pill">Page {s.metadata.get("page", "?")}</span>'
                for s in turn["sources"]
            )
            st.markdown(
                f'<div style="margin:0.4rem 0 1.2rem;">Sources: {pills}</div>',
                unsafe_allow_html=True,
            )

    # ── Suggested starter questions ────────────────────────────────────────
    if not st.session_state.chat_history:
        st.markdown("**Suggested questions to get started:**")
        suggestions = [
            "What are the main topics covered in this document?",
            "Explain the most important concept in simple terms.",
            "What are the key definitions I need to know?",
            "What are the steps or processes described here?",
        ]
        scols = st.columns(2)
        for i, q in enumerate(suggestions):
            if scols[i % 2].button(q, key=f"sugg_{i}", use_container_width=True):
                st.session_state["prefill_q"] = q
                st.rerun()

    # ── Chat input ─────────────────────────────────────────────────────────
    question = st.chat_input("Ask a question about your document…")
    if "prefill_q" in st.session_state:
        question = st.session_state.pop("prefill_q")

    if question:
        with st.spinner("Searching document…"):
            result = ask(st.session_state.qa_chain, question)
            answer = result["result"]
            sources = result.get("source_documents", [])
        st.session_state.chat_history.append({"q": question, "a": answer, "sources": sources})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑 Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()