"""
tools/flashcards.py
───────────────────
Tab 4 — Flashcards: flip-card review of key terms and ideas.
Call render_flashcards_tab() inside the tab context in app.py.
"""

import json
import random
import re

import streamlit as st
from core.document import llm_call, get_doc_sample


CARD_TYPE_MAP = {
    "Term → Definition": "key terms paired with their definitions",
    "Concept → Explanation": "concepts on the front with a clear explanation on the back",
    "Question → Answer": "exam-style questions on the front with answers on the back",
}


def _generate_flashcards(n_cards: int, card_type: str) -> list[dict]:
    """Call the LLM to produce flashcard JSON."""
    sample = get_doc_sample(st.session_state.vectorstore, n=8)
    fc_desc = CARD_TYPE_MAP[card_type]
    prompt = f"""Create {n_cards} study flashcards from the document content below.
Cards should be: {fc_desc}.

DOCUMENT CONTENT:
{sample}

Return a JSON array of {n_cards} objects, each with:
  "front": the term/concept/question (short, max 15 words)
  "back": the definition/explanation/answer (clear and concise, 1-4 sentences)

Return ONLY the JSON array. No markdown, no extra text."""

    raw = llm_call(st.session_state.groq_key, prompt)
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        return json.loads(m.group()) if m else []


def render_flashcards_tab():
    st.markdown("#### Flashcard Review")
    st.markdown(
        '<p style="color:#64748b;font-size:0.88rem;margin-top:-0.5rem;">'
        "Key terms and concepts from your document, one card at a time.</p>",
        unsafe_allow_html=True,
    )

    fcol1, fcol2 = st.columns([2, 1], gap="large")

    # ── Settings panel ─────────────────────────────────────────────────────
    with fcol2:
        st.markdown('<div class="sw-card">', unsafe_allow_html=True)
        st.markdown("**Generate cards**")
        n_cards = st.select_slider("Number of cards", options=[5, 8, 10, 15, 20], value=10)
        card_type = st.radio(
            "Card type",
            list(CARD_TYPE_MAP.keys()),
            index=0,
        )
        gen_fc = st.button("🃏 Generate Flashcards", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Card area ──────────────────────────────────────────────────────────
    with fcol1:
        if gen_fc:
            with st.spinner(f"Creating {n_cards} flashcards…"):
                cards = _generate_flashcards(n_cards, card_type)
                st.session_state.flashcards = cards
                st.session_state.fc_index = 0
                st.session_state.fc_flipped = False
            st.rerun()

        if st.session_state.flashcards:
            cards = st.session_state.flashcards
            idx = st.session_state.fc_index
            card = cards[idx]
            flipped = st.session_state.fc_flipped
            front_label = card_type.split("→")[0].strip()
            back_label = card_type.split("→")[1].strip()

            # ── Card face ──────────────────────────────────────────────────
            if not flipped:
                st.markdown(
                    f"""
<div class="flashcard-front">
  <div class="fc-label">Front · {front_label}</div>
  <div class="flashcard-term">{card.get("front", "")}</div>
  <div class="fc-counter">{idx + 1} / {len(cards)}</div>
</div>
""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
<div class="flashcard-back">
  <div class="fc-label">Back · {back_label}</div>
  <div class="flashcard-def">{card.get("back", "")}</div>
  <div class="fc-counter">{idx + 1} / {len(cards)}</div>
</div>
""",
                    unsafe_allow_html=True,
                )

            # ── Controls ───────────────────────────────────────────────────
            b1, b2, b3, b4 = st.columns(4, gap="small")
            with b1:
                if st.button("← Prev", use_container_width=True, disabled=(idx == 0)):
                    st.session_state.fc_index = idx - 1
                    st.session_state.fc_flipped = False
                    st.rerun()
            with b2:
                label = "👁 Reveal" if not flipped else "🔙 Hide"
                if st.button(label, use_container_width=True):
                    st.session_state.fc_flipped = not flipped
                    st.rerun()
            with b3:
                if st.button("Next →", use_container_width=True, disabled=(idx == len(cards) - 1)):
                    st.session_state.fc_index = idx + 1
                    st.session_state.fc_flipped = False
                    st.rerun()
            with b4:
                if st.button("🔀 Shuffle", use_container_width=True):
                    random.shuffle(st.session_state.flashcards)
                    st.session_state.fc_index = 0
                    st.session_state.fc_flipped = False
                    st.rerun()

            st.progress((idx + 1) / len(cards))

            # ── Card list expander ─────────────────────────────────────────
            with st.expander(f"📋 All {len(cards)} cards"):
                for i, c in enumerate(cards):
                    marker = "→" if i == idx else "  "
                    colour = "#f59e0b" if i == idx else "#64748b"
                    st.markdown(
                        f'<p style="font-size:0.82rem;color:{colour};margin:0.2rem 0;">'
                        f"{marker} {i + 1}. {c.get('front', '')}</p>",
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                """
<div style="text-align:center;padding:3rem 1rem;color:#475569;">
  Configure and click <b style="color:#f59e0b;">Generate Flashcards</b> →
</div>
""",
                unsafe_allow_html=True,
            )