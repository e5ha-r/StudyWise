"""
ui/sidebar.py
─────────────
Sidebar for StudyWise.
"""

import streamlit as st
from core.document import index_document, build_qa_chain


DEFAULTS = {
    "vectorstore": None,
    "qa_chain": None,
    "doc_name": None,
    "doc_chunks": 0,
    "doc_pages": 0,
    "chat_history": [],
    "quiz_questions": [],
    "quiz_answers": {},
    "quiz_submitted": False,
    "flashcards": [],
    "fc_index": 0,
    "fc_flipped": False,
    "summary": None,
    "key_concepts": [],
    "groq_key": "",
    "hf_token": "",
}


def init_session_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_tool_states():

    keys = [
        "chat_history",
        "quiz_questions",
        "quiz_answers",
        "quiz_submitted",
        "flashcards",
        "fc_index",
        "fc_flipped",
        "summary",
        "key_concepts",
    ]

    for k in keys:
        st.session_state[k] = DEFAULTS[k]


def _status(ok, ok_msg, warn_msg):

    if ok:

        st.markdown(
            f"""
<div style="
background:#d8f8e7;
padding:8px;
border-radius:8px;
font-size:13px;
color:#1d6d48;
margin-bottom:6px;
">
{ok_msg}
</div>
""",
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
<div style="
background:#fff3cf;
padding:8px;
border-radius:8px;
font-size:13px;
color:#8a6b22;
margin-bottom:6px;
">
{warn_msg}
</div>
""",
            unsafe_allow_html=True,
        )


def render_sidebar():

    with st.sidebar:

        # ------------------------------------------------

        st.markdown(
            """
<div style="text-align:center;padding-top:8px;padding-bottom:10px;">

<div style="
font-family:'Playfair Display',serif;
font-size:34px;
font-weight:700;
color:#C93638;
">

Study<span style="color:white;">Wise</span>

</div>

<div style="
font-size:13px;
color:white;
margin-top:3px;
">

Your AI Study Companion

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ------------------------------------------------

        st.markdown("### 🔑 Groq API")

        st.caption(
            "Get a free API key from https://console.groq.com"
        )

        groq_key = st.text_input(
            "Groq",
            type="password",
            value=st.session_state.groq_key,
            placeholder="gsk_...",
            label_visibility="collapsed",
        )

        if groq_key:

            st.session_state.groq_key = groq_key

            _status(True, "✓ API key saved", "")

        else:

            _status(False, "", "Groq key required")

        st.markdown("")

        # ------------------------------------------------

        st.markdown("### HuggingFace")

        st.caption(
            "Required for document embeddings"
        )

        hf = st.text_input(
            "HF",
            type="password",
            value=st.session_state.hf_token,
            placeholder="hf_...",
            label_visibility="collapsed",
        )

        if hf:

            st.session_state.hf_token = hf

            _status(True, "✓ Token saved", "")

        else:

            _status(False, "", "HF token required")

        st.markdown("---")

        # ------------------------------------------------

        st.markdown("### 📄 Upload Document")

        uploaded = st.file_uploader(
            "Upload",
            type=["pdf", "txt"],
            label_visibility="collapsed",
        )

        ready = (
            st.session_state.groq_key
            and st.session_state.hf_token
        )

        if uploaded and ready:

            label = (
                "Re-index"
                if st.session_state.doc_name
                else " Load Document"
            )

            if st.button(label, use_container_width=True):

                with st.spinner("Processing..."):

                    vs, chunks, pages = index_document(
                        uploaded,
                        st.session_state.hf_token,
                    )

                    st.session_state.vectorstore = vs

                    st.session_state.qa_chain = build_qa_chain(
                        vs,
                        st.session_state.groq_key,
                    )

                    st.session_state.doc_name = uploaded.name

                    st.session_state.doc_chunks = chunks

                    st.session_state.doc_pages = pages

                    _reset_tool_states()

                st.success("✨ Document indexed!")

        elif uploaded and not st.session_state.groq_key:

            st.info("Enter Groq key first.")

        elif uploaded and not st.session_state.hf_token:

            st.info("Enter HuggingFace token first.")

        # ------------------------------------------------

        if st.session_state.doc_name:

            st.markdown("---")

            st.markdown("### 📊 Document")

            c1, c2 = st.columns(2)

            with c1:

                st.markdown(
                    f"""
<div style="
background:#FFDE96;
padding:14px;
border-radius:14px;
text-align:center;
">

<div style="
font-size:28px;
font-weight:700;
color:#C93638;
">

{st.session_state.doc_pages}

</div>

<div style="font-size:12px;">
Pages
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

            with c2:

                st.markdown(
                    f"""
<div style="
background:#FA855A;
padding:14px;
border-radius:14px;
text-align:center;
color:white;
">

<div style="
font-size:28px;
font-weight:700;
">

{st.session_state.doc_chunks}

</div>

<div style="font-size:12px;">
Chunks
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

            st.markdown("")

            st.markdown(
                f"""
<div style="
background:white;
padding:10px;
border-radius:10px;
font-size:13px;
word-break:break-word;
">

📄 {st.session_state.doc_name}

</div>
""",
                unsafe_allow_html=True,
            )

        # ------------------------------------------------

        st.markdown("---")

        st.markdown(
            """
<div style="
text-align:center;
font-size:13px;
line-height:1.8;
color:white;
">

Built with: 

<br>

HuggingFace

<br>

FAISS

<br>

Groq Llama 3

<br>

Streamlit

</div>
""",
            unsafe_allow_html=True,
        )