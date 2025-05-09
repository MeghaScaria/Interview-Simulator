# Interview-Simulator
# 🤖 AI-Powered Interview Simulator

This Python project simulates a realistic HR-style interview using Google Gemini 1.5 Flash and your resume.

---

## 🚀 Features

- Upload your **resume** (PDF or DOCX)
- Enter your **target job title** and **years of experience**
- AI (Gemini) generates:
  - Tailored interview questions
  - Simulated answers (based on your resume)
- Saves the interview as:
  - `interview_transcript.txt`
  - `interview_transcript.pdf`

---

## 🛠️ Requirements

- Python 3.8+
- Google Gemini API key (free from [Makersuite](https://makersuite.google.com/app/apikey))

### 📦 Install Dependencies

### 🧠 How It Works
resume_parser.py – Extracts text from your resume

prompt_generator.py – Uses Gemini to create interview questions

interview_simulator.py – Simulates the candidate's answers

transcript_saver.py – Saves the interview to TXT and PDF

main.py – Runs the full workflow

---

### 🧪 Run the Project
Replace your-api-key-here in prompt_generator.py and interview_simulator.py with your Gemini key.

Put your resume file (e.g., sample_resume.pdf) in the same folder.

Open terminal and run:

bash
Copy
Edit
python main.py
###📁 Output
After running, you'll get:

✅ Printed Q&A in your terminal

📄 interview_transcript.txt

📄 interview_transcript.pdf

---

### 🔒 Disclaimer
This tool is for educational and simulation purposes. It does not guarantee hiring outcomes.

---

### 📌 Example Use Case
text
Copy
Edit
Job Title: Java Developer
Experience: 5 years
Resume: sample_resume.pdf

→ Gemini generates 5 role-specific questions.
→ Simulates smart answers based on your resume.
→ Saves everything as a transcript in both text file and pdf file format.

---

### 🤝 License
MIT License. Free to use and modify.

--- 

### 🧑‍💻 Author
Built using Python and Gemini 1.5 Flash.
