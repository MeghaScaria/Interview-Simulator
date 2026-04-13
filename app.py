import streamlit as st
import os
from resume_parser import parse_resume
from prompt_generator import generate_interview_questions
from interview_simulator import simulate_interview

st.title("AI Interview Simulator")
uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
job_title = st.text_input("Job Title", value="Java Developer")
experience = st.text_input("Years of Experience", value="5 years")

if st.button("Generate Mock Interview"):
    if uploaded_file is not None and job_title:
        with st.spinner("Processing..."):
            # 1. Save uploaded file temporarily to disk (because resume_parser expects a file path)
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # 2. Parse the resume text
                st.info("Parsing resume...")
                resume_text = parse_resume(temp_file_path)
                
                # 3. Generate questions
                st.info("Generating tailored interview questions...")
                questions = generate_interview_questions(resume_text, job_title, experience)
                
                st.subheader("Questions specifically for you:")
                st.write(questions)
                
                # 4. Simulate the interview
                st.info("Generating a simulated mock interview based on your resume...")
                simulated_convo = simulate_interview(resume_text, job_title, experience, questions)
                
                st.subheader("Simulated Mock Interview Session")
                st.write(simulated_convo)
                
            except Exception as e:
                st.error(f"Error during simulation: {str(e)}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
    else:
        st.warning("Please make sure to both upload a PDF/DOCX and type a Job Title.")
