"""
tools/quiz.py
─────────────
Tab 2 — Quiz Me: AI-generated MCQs with instant scoring.
Call render_quiz_tab() inside the tab context in app.py.
"""

import json
import re

import streamlit as st
from core.document import llm_call, get_doc_sample


def _generate_questions(n_qs: int, difficulty: str, topic: str) -> list[dict]:
    """Call the LLM to produce MCQ questions and parse the JSON response."""
    sample = get_doc_sample(st.session_state.vectorstore, n=8)
    topic_s = f"Focus specifically on: {topic}." if topic.strip() else ""
    prompt = f"""You are a professor creating a multiple-choice quiz.
Use ONLY the content below to write {n_qs} {difficulty.lower()}-difficulty MCQs. {topic_s}

DOCUMENT CONTENT:
{sample}

Return a JSON array with exactly {n_qs} objects. Each object must have:
  "question" (string),
  "options" (array of exactly 4 strings, labelled A/B/C/D inline e.g. "A. Paris"),
  "answer" (string: "A", "B", "C", or "D"),
  "explanation" (string: 1-2 sentences)

Return ONLY the JSON array. No preamble, no markdown fences."""

    raw = llm_call(st.session_state.groq_key, prompt)
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        return json.loads(m.group()) if m else []


def render_quiz_tab():
    st.markdown("#### Test your knowledge")
    st.markdown(
        '<p style="color:#64748b;font-size:0.88rem;margin-top:-0.5rem;">'
        "AI generates MCQs from your document. Answer them to see your score.</p>",
        unsafe_allow_html=True,
    )

    qcol1, qcol2 = st.columns([2, 1], gap="large")

    # ── Settings panel ─────────────────────────────────────────────────────
    with qcol2:
        st.markdown('<div class="sw-card">', unsafe_allow_html=True)
        st.markdown("**Quiz settings**")
        n_qs = st.select_slider("Number of questions", options=[3, 5, 8, 10], value=5)
        topic = st.text_input("Focus topic (optional)", placeholder="e.g. recursion, photosynthesis")
        diff = st.radio("Difficulty", ["Easy", "Medium", "Hard"], index=1, horizontal=True)
        gen_btn = st.button("🎲 Generate Quiz", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Quiz area ──────────────────────────────────────────────────────────
    with qcol1:
        if gen_btn:
            with st.spinner(f"Generating {n_qs} questions…"):
                qs = _generate_questions(n_qs, diff, topic)
                st.session_state.quiz_questions = qs
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False

        if st.session_state.quiz_questions:
            qs = st.session_state.quiz_questions
            ans = st.session_state.quiz_answers
            done = st.session_state.quiz_submitted

            for i, q in enumerate(qs):
                correct = q.get("answer", "A").strip().upper()
                st.markdown(
                    f'<div class="quiz-q">Q{i+1}. {q["question"]}</div>',
                    unsafe_allow_html=True,
                )

                for opt in q.get("options", []):
                    label = opt[0].upper() if opt else "?"
                    chosen = ans.get(i) == label
                    is_corr = label == correct

                    if done:
                        css = "option-correct" if is_corr else ("option-wrong" if chosen else "option-btn")
                        prefix = "✅ " if is_corr else ("❌ " if chosen else "   ")
                        st.markdown(f'<div class="{css}">{prefix}{opt}</div>', unsafe_allow_html=True)
                    else:
                        if st.button(opt, key=f"opt_{i}_{label}", use_container_width=True):
                            st.session_state.quiz_answers[i] = label
                            st.rerun()
                        if chosen:
                            st.markdown(
                                '<p style="font-size:0.75rem;color:#f59e0b;margin-top:-0.3rem;">▲ Selected</p>',
                                unsafe_allow_html=True,
                            )

                if done:
                    exp = q.get("explanation", "")
                    if exp:
                        st.markdown(
                            f'<div style="background:#0f172a;border-radius:6px;padding:0.6rem 0.8rem;'
                            f'margin-bottom:0.3rem;font-size:0.85rem;color:#94a3b8;">💡 {exp}</div>',
                            unsafe_allow_html=True,
                        )
                st.markdown("<hr>", unsafe_allow_html=True)

            if not done:
                answered = len(ans)
                st.progress(answered / len(qs))
                st.markdown(
                    f'<p style="font-size:0.82rem;color:#64748b;">{answered}/{len(qs)} answered</p>',
                    unsafe_allow_html=True,
                )
                if answered == len(qs):
                    if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                        st.session_state.quiz_submitted = True
                        st.rerun()
            else:
                score = sum(
                    1 for i, q in enumerate(qs)
                    if ans.get(i) == q.get("answer", "A").strip().upper()
                )
                pct = int(score / len(qs) * 100)
                grade = (
                    "🏆 Excellent!" if pct >= 80
                    else ("👍 Good work!" if pct >= 60 else "📖 Keep studying")
                )
                st.markdown(
                    f"""
<div class="sw-card-amber" style="text-align:center;padding:1.5rem;">
  <div style="font-size:2rem;margin-bottom:0.3rem;">{grade.split()[0]}</div>
  <div style="font-size:1rem;font-weight:600;color:#f8f5f0;margin-bottom:0.5rem;">{grade[1:].strip()}</div>
  <span class="score-badge">{score}/{len(qs)} · {pct}%</span>
</div>
""",
                    unsafe_allow_html=True,
                )
                if st.button("🔄 New Quiz", use_container_width=True):
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
        else:
            st.markdown(
                """
<div style="text-align:center;padding:3rem 1rem;color:#475569;">
  Configure settings and click <b style="color:#f59e0b;">Generate Quiz</b> →
</div>
""",
                unsafe_allow_html=True,
            )