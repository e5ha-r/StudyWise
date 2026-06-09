"""
tools/summarise.py
──────────────────
Tab 3 — Summarise: structured document summary + key concepts.
Call render_summarise_tab() inside the tab context in app.py.
"""

import json
import re

import streamlit as st
from core.document import llm_call, get_doc_sample


def _generate_summary(n_sections: int) -> dict:
    """Call the LLM to produce a structured JSON summary."""
    sample = get_doc_sample(st.session_state.vectorstore, n=10)
    prompt = f"""Summarise the following academic/study document content.

DOCUMENT CONTENT:
{sample}

Return a JSON object with:
  "title": concise document title (string),
  "overview": 2-3 sentence high-level overview (string),
  "sections": array of {n_sections} objects, each with:
    "heading": section heading (string),
    "content": 3-5 sentence detailed paragraph (string)
  "key_concepts": array of 10-15 important terms/concepts (short strings, 1-4 words each)
  "exam_tips": array of 3-5 short strings with things most likely to appear in exams

Return ONLY valid JSON. No markdown, no preamble."""

    raw = llm_call(st.session_state.groq_key, prompt)
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        return json.loads(m.group()) if m else {}


def render_summarise_tab():
    st.markdown("#### Document Summary")
    st.markdown(
        '<p style="color:#64748b;font-size:0.88rem;margin-top:-0.5rem;">'
        "A structured overview + key concepts extracted by AI.</p>",
        unsafe_allow_html=True,
    )

    if not st.session_state.summary:
        # ── Generation controls ────────────────────────────────────────────
        detail = st.radio(
            "Summary depth",
            ["Quick (3 sections)", "Standard (5 sections)", "Detailed (7 sections)"],
            index=1,
            horizontal=True,
        )
        depth_map = {
            "Quick (3 sections)": 3,
            "Standard (5 sections)": 5,
            "Detailed (7 sections)": 7,
        }

        if st.button("📝 Generate Summary", type="primary"):
            with st.spinner("Analysing document…"):
                data = _generate_summary(depth_map[detail])
                st.session_state.summary = data
                st.session_state.key_concepts = data.get("key_concepts", [])
            st.rerun()

    else:
        s = st.session_state.summary

        # ── Title + overview ───────────────────────────────────────────────
        st.markdown(
            f"""
<div class="sw-card-amber">
  <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#f8f5f0;margin-bottom:0.6rem;">
    {s.get("title", "Document Summary")}
  </div>
  <p style="color:#cbd5e1;margin:0;line-height:1.7;">{s.get("overview", "")}</p>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Key concepts ───────────────────────────────────────────────────
        if st.session_state.key_concepts:
            st.markdown("**Key concepts**")
            pills = "".join(
                f'<span class="key-concept-pill">{c}</span>'
                for c in st.session_state.key_concepts
            )
            st.markdown(f'<div class="concept-grid">{pills}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # ── Sections ───────────────────────────────────────────────────────
        for sec in s.get("sections", []):
            st.markdown(
                f"""
<div class="summary-section">
  <p style="font-weight:700;color:#f8f5f0;margin-bottom:0.3rem;">{sec.get("heading", "")}</p>
  <p style="color:#94a3b8;font-size:0.93rem;margin:0;">{sec.get("content", "")}</p>
</div>
""",
                unsafe_allow_html=True,
            )

        # ── Exam tips ──────────────────────────────────────────────────────
        tips = s.get("exam_tips", [])
        if tips:
            st.markdown("**📌 Likely exam points**")
            st.markdown('<div class="sw-card">', unsafe_allow_html=True)
            for tip in tips:
                st.markdown(
                    f'<p style="color:#cbd5e1;margin:0.3rem 0;font-size:0.9rem;">• {tip}</p>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("↩ Regenerate summary"):
            st.session_state.summary = None
            st.session_state.key_concepts = []
            st.rerun()