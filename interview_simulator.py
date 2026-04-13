# interview_simulator.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content
