# interview_simulator.py

import google.generativeai as genai

# Make sure this matches your prompt_generator.py
GEMINI_API_KEY = "AIzaSyBxa8LFSriN8RvsH-F6C40XmJ7FCUPFh6g"

genai.configure(api_key=GEMINI_API_KEY)


def simulate_interview(resume_text, job_title, years_experience, questions_text):
    prompt = f"""
    You are simulating a candidate in a job interview for the role of "{job_title}" with {years_experience} of experience.

    The candidate's resume is:
    -----------------------------
    {resume_text}
    -----------------------------

    Here are the interview questions:
    -----------------------------
    {questions_text}
    -----------------------------

    Please answer each question as the candidate, based on their resume. Format the output like a conversation:
    
    Interviewer: [question]
    Candidate: [answer]
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
