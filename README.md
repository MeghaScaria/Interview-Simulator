# 🤖 AI Live Interview Simulator

A professional, state-of-the-art interactive mock interview simulator. This application leverages extremely fast open-weights LLMs via the Groq API and real-time audio manipulation to instantly deliver realistic, highly personalized mock interviews based on your specific resume!

---

## 🚀 Features

- **Interactive UI (Streamlit)**: Complete modern messaging-app layout mimicking a live chat with an expert HR Recruiter.
- **Two Interview Modes**: Toggle between **Technical** (evaluates deeply on architecture, languages, frameworks) or **Behavioral/HR** (evaluates on soft-skills and conflict resolution).
- **Two-Way Audio Integration**: 
  - **Text-to-Speech (TTS)**: Fully integrated with Microsoft Edge's Neural TTS (`edge-tts`). The AI physically speaks its questions out loud to you using a professional voice at a custom speed.
  - **Speech-to-Text (STT)**: Built-in microphone support. Speak out your answers and the app instantly transcribes them using **Groq's Whisper-Large-V3-Turbo** model!
- **Stateful Grading Loop**: The AI dynamically processes your background, generates specific questions for you, listens to your answers in real time, grades them out of 10, and offers actionable resume-tailored feedback.

---

## 🛠️ Tech Stack 

- **Frontend Framework**: [Streamlit](https://streamlit.io/)
- **Core LLM Engine**: LLaMA-3.3-70b-Versatile (via [Groq SDK](https://groq.com/))
- **Speech-to-Text**: Whisper-Large-V3-Turbo (via [Groq SDK](https://groq.com/))
- **Text-to-Speech**: `edge-tts` (Microsoft Azure Neural TTS)
- **Document Processing**: `pdfplumber`, `python-docx`
- **Environment Management**: `python-dotenv`

---

## ⚙️ How to Setup

1. **Clone the repository** and ensure you have `uv` or `pip` installed.
2. **Install Dependencies** (If using standard python):
   ```bash
   pip install streamlit groq pdfplumber python-docx python-dotenv edge-tts gtts
   ```
3. **Configure Environment Variables**:
   Create a new file in the root folder specifically named `.env` and paste your free Groq API key:
   ```env
   GROQ_API_KEY=your-api-key-here
   ```
4. **Run the App!**
   Execute this command inside your terminal to launch the simulator in your browser:
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Architectural Workflow

1. **`app.py`**: Handles Streamlit session states, constructs the interactive chat UI, and ties all backend functions together.
2. **`prompt_generator.py`**: Interacts with Llama-3 using strict JSON schemas to generate custom technical/behavioral interview questions based solely on your resume background.
3. **`interview_simulator.py`**: Acts as an AI grader that reviews your specific answer against the original question and determines what you missed.
4. **`resume_parser.py`**: Robustly scrapes text arrays from your uploaded `.pdf` or `.docx` file.
5. **`audio_utils.py`**: Asynchronous helper class that handles high-speed Microsoft Neural text-to-speech rendering, and passes Streamlit audio captures into Groq's transcription algorithms.

---

### 🔒 Disclaimer
This tool is strictly for professional development and educational practice. It does not predict real-life hiring outcomes.
