import os
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

    Based on this information, please generate 5 HR-style interview questions that are:
    - Role-specific
    - Behavior-based or situational
    - Based on the resume content
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
