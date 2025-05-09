# prompt_generator.py

import google.generativeai as genai

# Replace with your own Gemini API key
GEMINI_API_KEY = "AIzaSyBxa8LFSriN8RvsH-F6C40XmJ7FCUPFh6g"

genai.configure(api_key=GEMINI_API_KEY)


def generate_interview_questions(resume_text, job_title, years_experience):
    prompt = f"""
    I have a candidate applying for the position of "{job_title}" with {years_experience} of experience.

    Here is their resume content:
    -----------------------------
    {resume_text}
    -----------------------------

    Based on this information, please generate 5 HR-style interview questions that are:
    - Role-specific
    - Behavior-based or situational
    - Based on the resume content
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
