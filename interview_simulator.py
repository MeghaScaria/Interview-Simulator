# interview_simulator.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_answer(resume_text, job_title, question, user_answer, interview_type="Behavioral / HR"):
    
    role_persona = "an expert HR Interviewer" if "Behavioral" in interview_type else "a Senior Technical Lead"

    prompt = f"""
    You are {role_persona} evaluating a candidate for the role of "{job_title}".
    This is a {interview_type} interview round.
    
    The candidate's resume:
    {resume_text}
    
    You asked the candidate this question:
    "{question}"
    
    The candidate replied with:
    "{user_answer}"
    
    Please evaluate their answer on a scale out of 10.
    Provide constructive feedback on what they did well and how they can improve. 
    If this is a technical interview, heavily scrutinize their technical accuracy and problem solving approach.
    If this is behavioral, heavily scrutinize their soft skills and scenario handling (e.g., STAR method).
    Format your response cleanly using bullet points.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content
