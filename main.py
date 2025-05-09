# main.py

from resume_parser import parse_resume
from prompt_generator import generate_interview_questions
from interview_simulator import simulate_interview
from transcript_saver import save_transcript_as_text, save_transcript_as_pdf

resume_path = "sample_resume.pdf"
job_title = "Java Developer"
years_experience = "5 years"

try:
    resume_text = parse_resume(resume_path)
    print("✅ Resume parsed.")

    questions = generate_interview_questions(resume_text, job_title, years_experience)
    print("\n🧠 Interview Questions Generated.")

    simulated_convo = simulate_interview(resume_text, job_title, years_experience, questions)
    print("\n🎤 Simulated Interview:")
    print("-" * 40)
    print(simulated_convo)

except Exception as e:
    print("❌ Error:", str(e))

save_transcript_as_text(simulated_convo)
save_transcript_as_pdf(simulated_convo)