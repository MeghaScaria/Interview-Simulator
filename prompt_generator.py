import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_interview_questions(resume_text, job_title, years_experience, interview_type="Behavioral / HR"):
    
    # Conditional logic for prompt type
    if "Technical" in interview_type:
        focus_points = "- Technical architecture and deep system knowledge\n    - Coding logic, tools, and technical problem solving\n    - Specialized frameworks mentioned in the resume"
        role_persona = "an expert Technical Lead / Senior Engineer"
    else:
        focus_points = "- Cultural fit and core behavioral traits\n    - Conflict resolution and teamwork\n    - Soft skills and leadership scenarios"
        role_persona = "an expert Corporate HR Recruiter"

    prompt = f"""
    I have a candidate applying for the position of "{job_title}" with {years_experience} of experience.

    Here is their resume content:
    -----------------------------
    {resume_text}
    -----------------------------

    Based on this information, please generate 5 {interview_type} interview questions.
    Make the questions:
    - Role-specific and closely tied to their experience
    {focus_points}

    You MUST return the output ONLY as a valid JSON object with a single key "questions" which contains a list of string questions.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are {role_persona}. Always output valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    response_text = chat_completion.choices[0].message.content
    try:
        data = json.loads(response_text)
        return data.get("questions", [])
    except json.JSONDecodeError:
        return []
