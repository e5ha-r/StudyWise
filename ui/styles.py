"""
ui/styles.py
────────────
Global CSS for StudyWise.
"""

import streamlit as st

CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500;600;700&display=swap');


html, body, [class*="css"]{

    font-family:'Inter',sans-serif;
    background:#F6FFEA !important;
    color:#56453f !important;
}

.block-container{
    max-width:1200px;
    padding:2rem 2.5rem 3rem 2.5rem !important;
}


/* Sidebar */

[data-testid="stSidebar"]{

    background:#62C4DA !important;
    border:none;
}

[data-testid="stSidebar"] *{

    color:white !important;
}


/* Brand */

.brand{

    font-family:'Playfair Display',serif;
    font-size:1.8rem;
    color:#C93638;
}

.brand-dot{

    color:#FA855A;
}


/* Tabs */

.stTabs [data-baseweb="tab-list"]{

    background:#FFDE96;
    border-radius:12px;
    padding:5px;
    border:none;
}

.stTabs [data-baseweb="tab"]{

    border-radius:10px;
    color:#8a6844 !important;
    font-weight:600;
}

.stTabs [aria-selected="true"]{

    background:#62C4DA !important;
    color:white !important;
    font-weight:700;
}

.stTabs [data-baseweb="tab-panel"]{

    padding-top:1.5rem;
}


/* Buttons */

.stButton > button{

    background:#C93638;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:600;
    padding:0.6rem 1.5rem;
    transition:.2s;
}

.stButton > button:hover{

    background:#FA855A;
    color:white;
}


/* Inputs */

.stTextInput input,
.stTextArea textarea{

    background:white !important;
    color:#56453f !important;
    border:2px solid #FFDE96 !important;
    border-radius:10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus{

    border-color:#62C4DA !important;
    box-shadow:0 0 0 2px rgba(98,196,218,.2) !important;
}


/* Cards */

.sw-card{

    background:#FFDE96;
    border:none;
    border-radius:18px;
    padding:1.4rem;
    box-shadow:0 5px 15px rgba(0,0,0,.05);
    margin-bottom:1rem;
}

.sw-card-amber{

    background:#FA855A;
    color:white;
    border:none;
    border-radius:18px;
    padding:1.4rem;
    margin-bottom:1rem;
    box-shadow:0 5px 18px rgba(250,133,90,.25);
}


/* Answer block */

.sw-answer-block{

    background:white;
    border-left:6px solid #62C4DA;
    border-radius:10px;
    padding:1rem 1.2rem;
    margin-top:.8rem;
    line-height:1.7;
}


/* Source pills */

.sw-source-pill{

    display:inline-block;

    background:#62C4DA;

    color:white;

    border-radius:999px;

    padding:4px 10px;

    font-size:.75rem;

    margin:2px;
}


/* Quiz */

.quiz-q{

    font-size:1.05rem;

    font-weight:700;

    color:#C93638;

    margin-bottom:1rem;
}

.option-btn{

    width:100%;

    background:white;

    border:2px solid #FFDE96;

    border-radius:10px;

    padding:.8rem 1rem;

    margin-bottom:.5rem;

    color:#56453f;

    transition:.15s;
}

.option-btn:hover{

    border-color:#62C4DA;
}

.option-correct{

    background:#d7f8e6 !important;

    border-color:#27ae60 !important;
}

.option-wrong{

    background:#ffd8d8 !important;

    border-color:#C93638 !important;
}

.score-badge{

    display:inline-block;

    background:#C93638;

    color:white;

    border-radius:999px;

    padding:5px 18px;

    font-weight:700;
}


/* Flashcards */

.flashcard-front{

    background:#62C4DA;

    border-radius:18px;

    padding:2.5rem;

    min-height:180px;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    text-align:center;
}

.flashcard-back{

    background:#FFDE96;

    border-radius:18px;

    padding:2.5rem;

    min-height:180px;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    text-align:center;
}

.flashcard-term{

    font-family:'Playfair Display',serif;

    font-size:1.5rem;

    color:white;
}

.flashcard-back .flashcard-term{

    color:#C93638;
}

.flashcard-def{

    color:#56453f;

    line-height:1.6;
}

.fc-label{

    color:rgba(255,255,255,.8);

    text-transform:uppercase;

    font-size:.7rem;

    letter-spacing:2px;

    margin-bottom:.8rem;
}

.flashcard-back .fc-label{

    color:#C93638;
}

.fc-counter{

    color:#888;

    margin-top:.8rem;
}


/* Summary */

.summary-section{

    border-left:5px solid #62C4DA;

    padding-left:1rem;

    margin-bottom:1.5rem;
}

.key-concept-pill{

    display:inline-block;

    background:#62C4DA;

    color:white;

    padding:6px 12px;

    border-radius:999px;

    font-size:.82rem;

    margin:3px;
}

.concept-grid{

    display:flex;

    flex-wrap:wrap;

    gap:6px;
}


/* Progress */

.stProgress > div > div{

    background:#C93638 !important;
}


/* File uploader */

[data-testid="stFileUploader"]{

    background:white;

    border:3px dashed #62C4DA;

    border-radius:18px;

    padding:1rem;
}


/* Stats */

.stat-chip{

    background:white;

    border-radius:12px;

    padding:.8rem;
}

.stat-num{

    color:#C93638;

    font-size:1.5rem;

    font-weight:700;
}

.stat-lbl{

    color:#888;

    font-size:.75rem;
}


/* Typography */

h1,h2,h3,h4{

    color:#C93638 !important;
}

p,li{

    color:#56453f;
    line-height:1.7;
}

hr{

    border-color:#FFDE96 !important;
}

.stMarkdown a{

    color:#62C4DA;
}

[data-testid="stFileUploadDropzone"] *{

    color:#666 !important;
}

</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)