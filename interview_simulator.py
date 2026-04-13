# interview_simulator.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_answer(resume_text, job_title, question, user_answer):
    prompt = f"""
    You are an expert HR Interviewer evaluating a candidate for the role of "{job_title}".
    
    The candidate's resume:
    {resume_text}
    
    You asked the candidate this question:
    "{question}"
    
    The candidate replied with:
    "{user_answer}"
    
    Please evaluate their answer on a scale out of 10.
    Provide constructive feedback on what they did well and how they can improve. 
    Format your response cleanly using bullet points.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content
