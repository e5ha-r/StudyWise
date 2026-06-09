"""
ui/sidebar.py
─────────────
Sidebar: API key inputs, file uploader, document stats, stack info.
Call render_sidebar() from app.py — writes to st.session_state only.
"""

import streamlit as st
from core.document import index_document, build_qa_chain


DEFAULTS = {
    "vectorstore":    None,
    "qa_chain":       None,
    "doc_name":       None,
    "doc_chunks":     0,
    "doc_pages":      0,
    "chat_history":   [],
    "quiz_questions": [],
    "quiz_answers":   {},
    "quiz_submitted": False,
    "flashcards":     [],
    "fc_index":       0,
    "fc_flipped":     False,
    "summary":        None,
    "key_concepts":   [],
    "groq_key":       "",
    "hf_token":       "",
}


def init_session_state():
    """Initialise all session-state keys with defaults."""
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_tool_states():
    tool_keys = [
        "chat_history", "quiz_questions", "quiz_answers",
        "quiz_submitted", "flashcards", "fc_index", "fc_flipped",
        "summary", "key_concepts",
    ]
    for k in tool_keys:
        st.session_state[k] = DEFAULTS[k]


def _status(ok: bool, ok_msg: str, warn_msg: str):
    colour, msg = ("#10b981", ok_msg) if ok else ("#f59e0b", warn_msg)
    st.markdown(
        f'<p style="color:{colour};font-size:0.8rem;">{msg}</p>',
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:

        # ── Brand ──────────────────────────────────────────────────────────
        st.markdown(
            '<p class="brand">Study<span class="brand-dot">.</span>Wise</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:0.78rem;color:#475569;'
            'margin-top:-4px;margin-bottom:1.2rem;">AI Study Companion</p>',
            unsafe_allow_html=True,
        )

        # ── Groq API Key ───────────────────────────────────────────────────
        st.markdown("#### 🔑 Groq API Key")
        st.caption("Free at [console.groq.com](https://console.groq.com)")
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            value=st.session_state.groq_key,
            label_visibility="collapsed",
        )
        if groq_key:
            st.session_state.groq_key = groq_key
            _status(True, "✓ Groq key saved", "")
        else:
            _status(False, "", "↑ Required for Q&A, Quiz, Summary, Flashcards")

        st.divider()

        # ── HuggingFace Token ──────────────────────────────────────────────
        st.markdown("#### 🤗 HuggingFace Token")
        st.caption(
            "Free at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) "
            "— needed for embeddings"
        )
        hf_token = st.text_input(
            "HuggingFace Token",
            type="password",
            placeholder="hf_...",
            value=st.session_state.hf_token,
            label_visibility="collapsed",
        )
        if hf_token:
            st.session_state.hf_token = hf_token
            _status(True, "✓ HF token saved", "")
        else:
            _status(False, "", "↑ Required for document indexing")

        st.divider()

        # ── File uploader ──────────────────────────────────────────────────
        st.markdown("#### 📄 Your Document")
        uploaded = st.file_uploader(
            "Upload PDF or TXT",
            type=["pdf", "txt"],
            label_visibility="collapsed",
        )

        both_keys = st.session_state.groq_key and st.session_state.hf_token

        if uploaded and both_keys:
            btn_label = "🔄 Re-index" if st.session_state.doc_name else "📥 Load & Index"
            if st.button(btn_label, use_container_width=True):
                with st.spinner("Indexing document…"):
                    vs, n_chunks, n_pages = index_document(
                        uploaded, st.session_state.hf_token
                    )
                    st.session_state.vectorstore = vs
                    st.session_state.qa_chain    = build_qa_chain(
                        vs, st.session_state.groq_key
                    )
                    st.session_state.doc_name   = uploaded.name
                    st.session_state.doc_chunks = n_chunks
                    st.session_state.doc_pages  = n_pages
                    _reset_tool_states()
                st.success("Ready!")

        elif uploaded and not st.session_state.groq_key:
            st.info("Enter your Groq API key first.")
        elif uploaded and not st.session_state.hf_token:
            st.info("Enter your HuggingFace token first.")

        # ── Document stats ─────────────────────────────────────────────────
        if st.session_state.doc_name:
            st.divider()
            st.markdown("#### 📊 Document Stats")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f'<div class="stat-chip">'
                    f'<div class="stat-num">{st.session_state.doc_pages}</div>'
                    f'<div class="stat-lbl">pages</div></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="stat-chip">'
                    f'<div class="stat-num">{st.session_state.doc_chunks}</div>'
                    f'<div class="stat-lbl">chunks</div></div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<p style="font-size:0.78rem;color:#475569;'
                f'margin-top:0.5rem;word-break:break-all;">📄 {st.session_state.doc_name}</p>',
                unsafe_allow_html=True,
            )

        # ── Stack info ─────────────────────────────────────────────────────
        st.divider()
        st.markdown(
            '<p style="font-size:0.75rem;color:#475569;line-height:1.6;">'
            '<b style="color:#64748b;">Stack:</b><br>'
            "HuggingFace · FAISS<br>"
            "Groq LLaMA-3 · Streamlit</p>",
            unsafe_allow_html=True,
        )