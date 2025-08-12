import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from tools.parse_documents import *
from agents.resume_processing_agent import extract_resume_to_json

st.title("Resume Processing & ATS Scoring System")

uploaded_files = st.file_uploader(
    label="Upload your resume(s)",
    accept_multiple_files=True,
    type=["pdf", "doc", "docx", "txt"],
)

if uploaded_files:
    st.success(
        f"{len(uploaded_files)} file(s) uploaded. Click 'Process Resumes' to continue."
    )

    if st.button("Process Resumes"):
        for uploaded_file in uploaded_files:
            try:
                file_name = uploaded_file.name.lower()

                if file_name.endswith(".pdf"):
                    text = parse_pdf(uploaded_file)
                elif file_name.endswith(".docx") or file_name.endswith(".doc"):
                    text = parse_docx(uploaded_file)
                elif file_name.endswith(".txt"):
                    text = parse_textfile(uploaded_file)
                else:
                    st.error(f"Unsupported file type: {file_name}")
                    continue

                parsed_resume_json = (
                    asyncio.run(extract_resume_to_json(text))
                )
                st.subheader(f"Extracted JSON for {file_name}")
                st.json(parsed_resume_json)

            except Exception as e:
                st.error(f"Error processing {file_name}: {str(e)}")
