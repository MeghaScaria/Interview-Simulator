import streamlit as st
import os
from resume_parser import parse_resume
from prompt_generator import generate_interview_questions
from interview_simulator import evaluate_answer

# --- 1. SESSION STATE MANAGEMENT ---
# Streamlit re-runs the whole python script every time you interact with the UI.
# To remember past interactions (like current question, list of questions), we use st.session_state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_title" not in st.session_state:
    st.session_state.job_title = ""
if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False

st.title("AI Live Interview Simulator")

# --- PHASE 1: SETUP ---
if not st.session_state.questions:
    st.header("Step 1: Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
    job_title = st.text_input("Job Title", value="Software Engineer")
    experience = st.text_input("Years of Experience", value="2 years")

    if st.button("Start Interview"):
        if uploaded_file and job_title:
            with st.spinner("Analyzing resume and generating tailored questions..."):
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                try:
                    resume_text = parse_resume(temp_file_path)
                    # Instead of getting one string, we now get a List of questions!
                    questions = generate_interview_questions(resume_text, job_title, experience)
                    
                    if questions:
                        st.session_state.questions = questions
                        st.session_state.resume_text = resume_text
                        st.session_state.job_title = job_title
                        st.rerun() # Refresh page to start the interview!
                    else:
                        st.error("Failed to generate questions. Please try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
        else:
            st.warning("Please upload a resume and provide a job title.")

# --- PHASE 2: LIVE INTERVIEW ---
elif not st.session_state.interview_complete:
    st.header("Step 2: Live Conversation")
    
    # Show progress bar
    progress = st.session_state.current_q_index / len(st.session_state.questions)
    st.progress(progress)
    
    # 1. Print all past questions and your answers
    for item in st.session_state.interview_history:
        with st.chat_message("assistant"):
            st.write(f"**Question:** {item['question']}")
        with st.chat_message("user"):
            st.write(item['answer'])
        with st.chat_message("assistant"):
            st.info(f"**HR Feedback:**\n{item['feedback']}")

    # 2. Print current question
    current_question = st.session_state.questions[st.session_state.current_q_index]
    with st.chat_message("assistant"):
        st.write(f"**Question {st.session_state.current_q_index + 1}:** {current_question}")
        
    # 3. User Input Bar
    user_answer = st.chat_input("Type your answer here...")
    
    # 4. If User Submits Answer -> Grade and Move Next!
    if user_answer:
        # Show what the user typed instantly
        with st.chat_message("user"):
            st.write(user_answer)
            
        with st.spinner("Evaluating your response..."):
            feedback = evaluate_answer(
                st.session_state.resume_text, 
                st.session_state.job_title, 
                current_question, 
                user_answer
            )
            
            # Save the result to our session history
            st.session_state.interview_history.append({
                "question": current_question,
                "answer": user_answer,
                "feedback": feedback
            })
            
            # Move to next question
            st.session_state.current_q_index += 1
            if st.session_state.current_q_index >= len(st.session_state.questions):
                st.session_state.interview_complete = True
            
            # Re-run script to show updated state
            st.rerun()

# --- PHASE 3: SUMMARY ---
else:
    st.success("🎉 Interview Complete!")
    st.balloons()
    
    st.header("Interview Summary & Diagnostics")
    for idx, item in enumerate(st.session_state.interview_history):
        with st.expander(f"Q{idx + 1}: {item['question']}"):
            st.write("**Your Answer:**")
            st.write(item['answer'])
            st.write("**AI Feedback:**")
            st.write(item['feedback'])
            
    if st.button("Start New Setup"):
        st.session_state.clear() # Clear all memory!
        st.rerun()
