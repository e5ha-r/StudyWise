"""
ui/landing.py
Landing page for StudyWise.
"""

import streamlit as st

TOOLS = [

    ("💬","Ask","Chat with your document and get source-backed answers."),

    ("🧠","Quiz Me","Generate AI-powered MCQs and test your understanding."),

    ("📝","Summarise","Receive structured summaries and key concepts instantly."),

    ("🃏","Flashcards","Review automatically generated flashcards for active recall."),
]


def render_landing():

    st.markdown("""

<div style="text-align:center;padding-top:2rem;padding-bottom:2rem;">

<p style="
font-family:'Playfair Display',serif;
font-size:3.6rem;
font-weight:700;
line-height:1.05;
margin-bottom:0.6rem;
color:#C93638;
">

Study smarter,<br>

<span style="color:#62C4DA;">

not harder.

</span>

</p>

<p style="
max-width:620px;
margin:auto;
font-size:1.05rem;
color:#7b6b64;
line-height:1.8;
">

Upload textbooks, lecture slides, research papers, or notes and let AI transform them into quizzes, flashcards, summaries, and interactive conversations in seconds.

</p>

</div>

""", unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")

    for col, (icon, title, desc) in zip(cols, TOOLS):

        col.markdown(f"""

<div class="sw-card" style="height:190px;text-align:center;">

<div style="font-size:2.4rem;margin-bottom:0.7rem;">

{icon}

</div>

<div style="font-weight:700;font-size:1.1rem;color:#C93638;margin-bottom:.5rem;">

{title}

</div>

<div style="font-size:.86rem;color:#56453f;line-height:1.6;">

{desc}

</div>

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div style="text-align:center;padding-top:1.5rem;">

<p style="font-size:.95rem;color:#888;">

📄 Enter your Groq API key and upload a PDF to begin your personalized study session.

</p>

</div>

""", unsafe_allow_html=True)