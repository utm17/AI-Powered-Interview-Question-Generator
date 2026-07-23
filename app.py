"""
Nutrabay Process Analyst Assignment - Part 1
AI-Powered Interview Question Generator (Streamlit + Google Gemini API)

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import io
import json
import os
from datetime import datetime

import pandas as pd
import streamlit as st
import google.generativeai as genai

CATEGORIES = [
    ("Intent", "Why this role, why now, what they're optimising for in their career", "2-3"),
    ("Quant Ability", "Numerical reasoning, estimation, basic analytics math", "2-3"),
    ("Job Competency", "Skills directly named in the JD - tools, methods, domain knowledge", "3-4"),
    ("Core Competency", "Transferable skills: structured thinking, RCA, communication, ownership", "3-4"),
    ("EQ", "Self-awareness, handling failure, working with others, pressure situations", "2-3"),
]

SYSTEM_PROMPT = """You are an expert technical interviewer and hiring consultant.
You will be given a Job Description (JD). Generate 10 to 15 interview questions
that are SPECIFIC to this JD - referencing the actual tools, metrics, responsibilities,
and context named in it. Do not produce generic questions that could apply to any job.

Bucket the questions into exactly these 5 categories, respecting the suggested count range:

1. Intent (2-3 questions) - Why this role, why now, what they're optimising for in their career
2. Quant Ability (2-3 questions) - Numerical reasoning, estimation, basic analytics math
3. Job Competency (3-4 questions) - Skills directly named in the JD - tools, methods, domain knowledge
4. Core Competency (3-4 questions) - Transferable skills: structured thinking, RCA, communication, ownership
5. EQ (2-3 questions) - Self-awareness, handling failure, working with others, pressure situations

Return ONLY valid JSON, no markdown fences, no preamble, in exactly this shape:
{{
  "questions": [
    {{"category": "Intent", "question": "..."}},
    {{"category": "Quant Ability", "question": "..."}}
  ]
}}

Job Description:
---
{jd_text}
---
"""

st.set_page_config(page_title="Nutrabay Interview Question Generator", layout="wide")
st.title("AI-Powered Interview Question Generator")
st.caption("Part 1 of the Founder's Office system - JD in, categorized questions out.")

with st.sidebar:
    st.header("Setup")
    default_key = os.environ.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=default_key, type="password",
                             help="Get one at https://aistudio.google.com/apikey")
    model_name = st.selectbox("Model", ["gemini-flash-latest", "gemini-flash-latest", "gemini-1.5-flash"], index=0)
    st.divider()
    st.markdown("**Category guide**")
    for name, desc, count in CATEGORIES:
        st.markdown(f"- **{name}** ({count}): {desc}")

st.subheader("1. Provide the Job Description")
tab_upload, tab_paste = st.tabs(["Upload a file", "Paste text"])

jd_text = ""
with tab_upload:
    uploaded = st.file_uploader("Upload JD (.txt or .pdf)", type=["txt", "pdf"])
    if uploaded is not None:
        if uploaded.name.lower().endswith(".pdf"):
            try:
                from pypdf import PdfReader
                reader = PdfReader(uploaded)
                jd_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                st.error(f"Could not read PDF: {e}")
        else:
            jd_text = uploaded.read().decode("utf-8", errors="ignore")
        if jd_text:
            st.text_area("Extracted JD text", jd_text, height=200, disabled=True)

with tab_paste:
    pasted = st.text_area("Paste JD text here", height=250)
    if pasted.strip():
        jd_text = pasted

st.subheader("2. Generate questions")
generate = st.button("Generate Interview Questions", type="primary", disabled=not jd_text.strip())

if "results_df" not in st.session_state:
    st.session_state.results_df = None

if generate:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    else:
        with st.spinner("Calling Gemini and structuring the question set..."):
            try:
                genai.configure(api_key=api_key)
                for model in genai.list_models():
                    if "generateContent" in model.supported_generation_methods:
                     print(model.name)
                model = genai.GenerativeModel(model_name)
                prompt = SYSTEM_PROMPT.format(jd_text=jd_text)
                response = model.generate_content(prompt)
                raw = response.text.strip()
                raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                parsed = json.loads(raw)
                rows = parsed["questions"]
                df = pd.DataFrame(rows)
                df["Include?"] = True
                cat_order = {c[0]: i for i, c in enumerate(CATEGORIES)}
                df["_order"] = df["category"].map(cat_order).fillna(99)
                df = df.sort_values("_order").drop(columns="_order").reset_index(drop=True)
                df = df.rename(columns={"category": "Category", "question": "Question"})
                st.session_state.results_df = df
            except Exception as e:
                st.error(f"Generation failed: {e}")

if st.session_state.results_df is not None:
    st.subheader("3. Generated questions (grouped by category)")
    df = st.session_state.results_df
    for cat, _, _ in CATEGORIES:
        subset = df[df["Category"] == cat]
        if len(subset):
            st.markdown(f"### {cat}  \n*{len(subset)} question(s)*")
            for _, row in subset.iterrows():
                st.markdown(f"- {row['Question']}")

    st.divider()
    st.subheader("4. Download for the review layer (Part 2)")
    csv_buf = io.StringIO()
    df[["Category", "Question", "Include?"]].to_csv(csv_buf, index=False)
    fname = f"nutrabay_interview_questions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    st.download_button(
        "Download questions as CSV",
        data=csv_buf.getvalue(),
        file_name=fname,
        mime="text/csv",
    )
    st.info(
        "Next step: import this CSV into the Google Sheet review template "
        "(File > Import > Replace/Append). The hiring manager edits, removes, "
        "or rewords rows there, and ticks 'Include?' to finalize the set "
        "before it feeds into the Apps Script scoring interface (Part 3)."
    )