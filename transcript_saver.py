# transcript_saver.py

from fpdf import FPDF

def save_transcript_as_text(content, filename="interview_transcript.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"✅ Transcript saved as: {filename}")




from fpdf import FPDF

def clean_text_for_pdf(text):
    # Replace problematic characters with basic ASCII equivalents
    replacements = {
        "–": "-",     # en dash
        "—": "-",     # em dash
        "“": '"',     # left double quote
        "”": '"',     # right double quote
        "‘": "'",     # left single quote
        "’": "'",     # right single quote
        "•": "-",     # bullet point
        "→": "->",    # arrow
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text.encode('latin-1', 'ignore').decode('latin-1')  # remove remaining issues


def save_transcript_as_pdf(content, filename="interview_transcript.pdf"):
    content = clean_text_for_pdf(content)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    print(f"✅ Transcript saved as: {filename}")
