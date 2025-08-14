import os
import sys
import asyncio
import streamlit as st
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.parse_documents import *
from agents.resume_processing_agent import extract_resume_to_json
from agents.jd_processing_agent import extract_jd_to_json
from teams.resume_scoring_team import run_resume_team

st.title("Resume Processing & ATS Scoring System")

uploaded_resume_files = st.file_uploader(
    label="Upload your resume(s)",
    accept_multiple_files=True,
    type=["pdf", "doc", "docx", "txt"],
)

uploaded_jobdescription_file = st.file_uploader(
    label="Upload the Job Description file",
    type=["pdf", "doc", "docx", "txt"],
)


async def process_documents():

    for uploaded_file in uploaded_resume_files:
        try:
            file_name = uploaded_file.name.lower()

            if file_name.endswith(".pdf"):
                text = parse_pdf(uploaded_file)
            elif file_name.endswith((".docx", ".doc")):
                text = parse_docx(uploaded_file)
            elif file_name.endswith(".txt"):
                text = parse_textfile(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_name}")
                continue

            # parsed_resume_json = await extract_resume_to_json(text)
            # st.success(f"Extracted Resume JSON for {file_name}")
            # st.json(parsed_resume_json)
            get_resume_score, resume_score_dict = await run_resume_team(text)
            st.json(get_resume_score)
            st.json(resume_score_dict)

        except Exception as e:
            st.error(f"Error processing {file_name}: {str(e)}")

    try:
        file_name = uploaded_jobdescription_file.name.lower()
        if file_name.endswith(".pdf"):
            text = parse_pdf(uploaded_jobdescription_file)
        elif file_name.endswith((".docx", ".doc")):
            text = parse_docx(uploaded_jobdescription_file)
        elif file_name.endswith(".txt"):
            text = parse_textfile(uploaded_jobdescription_file)
        else:
            st.error(f"Unsupported file type: {file_name}")
            return

        # parsed_jd_json = await extract_jd_to_json(text)
        # st.success(f"Extracted JD JSON for {file_name}")
        # st.json(parsed_jd_json)

    except Exception as e:
        st.error(f"Error while processing JD {file_name}: {str(e)}")


if uploaded_resume_files and uploaded_jobdescription_file:
    unique_files = []
    for f in uploaded_resume_files:
        if all(f.name != uf.name for uf in unique_files):
            unique_files.append(f)

    uploaded_resume_files = unique_files
    success_msg = st.success(
        f"{len(uploaded_resume_files)} resume(s) and a JD uploaded. Click 'Process' to continue."
    )
    time.sleep(3)
    success_msg.empty()

    if st.button("Process"):
        with st.spinner("Getting parsed resumes and JD"):
            asyncio.run(process_documents())



