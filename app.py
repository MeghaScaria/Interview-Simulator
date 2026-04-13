import streamlit as st
import os
from resume_parser import parse_resume
from prompt_generator import generate_interview_questions
from interview_simulator import evaluate_answer
from audio_utils import generate_tts, transcribe_audio

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
if "interview_type" not in st.session_state:
    st.session_state.interview_type = "Behavioral / HR"
if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False
# States for audio logic
if "last_played_q_index" not in st.session_state:
    st.session_state.last_played_q_index = -1
if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None

st.title("AI Live Interview Simulator")

# --- PHASE 1: SETUP ---
if not st.session_state.questions:
    st.header("Step 1: Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
    job_title = st.text_input("Job Title", value="Software Engineer")
    experience = st.text_input("Years of Experience", value="2 years")
    interview_type = st.selectbox("Interview Mode", ["Behavioral / HR", "Technical"])

    if st.button("Start Interview"):
        if uploaded_file and job_title:
            with st.spinner(f"Analyzing resume and generating tailored {interview_type} questions..."):
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                try:
                    resume_text = parse_resume(temp_file_path)
                    
                    questions = generate_interview_questions(resume_text, job_title, experience, interview_type)
                    
                    if questions:
                        st.session_state.questions = questions
                        st.session_state.resume_text = resume_text
                        st.session_state.job_title = job_title
                        st.session_state.interview_type = interview_type
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
        
        # AI Voice Out (TTS) - Only play once per newly loaded question!
        if st.session_state.last_played_q_index != st.session_state.current_q_index:
            try:
                audio_bytes = generate_tts(current_question)
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                st.session_state.last_played_q_index = st.session_state.current_q_index
            except Exception as e:
                st.error(f"TTS Error: {e}")

    # 3. User Inputs (Microphone & Text)
    st.write("---")
    audio_val = st.audio_input("Speak out your answer")
    text_val = st.chat_input("Or type your answer here...")
    
    user_answer = ""
    if text_val:
        user_answer = text_val
    elif audio_val:
        audio_hash = hash(audio_val.getvalue())
        # Avoid transcribing and submitting the same audio block endlessly when Streamlit reruns
        if st.session_state.processed_audio_hash != audio_hash:
            with st.spinner("AI is listening... transcribing your audio!"):
                try:
                    user_answer = transcribe_audio(audio_val.getvalue(), audio_val.name)
                    st.session_state.processed_audio_hash = audio_hash
                except Exception as e:
                    st.error(f"Microphone Audio Error: {e}")
    
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
                user_answer,
                st.session_state.interview_type
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
