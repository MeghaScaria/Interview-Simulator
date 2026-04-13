import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_interview_questions(resume_text, job_title, years_experience):
    prompt = f"""
    I have a candidate applying for the position of "{job_title}" with {years_experience} of experience.

    Here is their resume content:
    -----------------------------
    {resume_text}
    -----------------------------

    Based on this information, please generate 5 HR-style interview questions.
    Make the questions:
    - Role-specific
    - Behavior-based or situational
    - Based on the resume content

    You MUST return the output ONLY as a valid JSON object with a single key "questions" which contains a list of string questions.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert HR recruiter. Always output valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    response_text = chat_completion.choices[0].message.content
    try:
        # We parse the JSON output back into a Python List
        data = json.loads(response_text)
        return data.get("questions", [])
    except json.JSONDecodeError:
        return []
