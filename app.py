import streamlit as st
import google.generativeai as genai
import docx
import io
from fpdf import FPDF
import os



# Function to read DOCX
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read PDF
def read_pdf(file):
    import fitz  # PyMuPDF
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

# Function to create DOCX file in memory
def create_docx(text):
    buffer = io.BytesIO()
    document = docx.Document()
    document.add_paragraph(text)
    document.save(buffer)
    buffer.seek(0)
    return buffer

# Function to create PDF file in memory
def create_pdf(text):
    buffer = io.BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Make sure this file exists
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.title("AI Resume Optimizer")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description here (optional)")

if uploaded_file:
    if st.button("✨ Optimize Resume" if job_description else "✨ Process Resume"):
        if uploaded_file.type == "application/pdf":
            resume_text = read_pdf(uploaded_file)
        else:
            resume_text = read_docx(uploaded_file)

        if job_description.strip():
            # If job description is provided → optimize
            prompt = f"""
            You are an AI resume optimization assistant.
            Optimize the following resume to match the given job description.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume_text}
            """
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            final_resume = response.text
        else:
            # If no job description → just return original
            final_resume = resume_text

        st.subheader("Processed Resume")
        st.write(final_resume)

        # --- DOWNLOAD BUTTONS ---
        docx_file = create_docx(final_resume)
        pdf_file = create_pdf(final_resume)

        st.download_button(
            label="📄 Download as DOCX",
            data=docx_file,
            file_name="optimized_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        st.download_button(
            label="📄 Download as PDF",
            data=pdf_file,
            file_name="optimized_resume.pdf",
            mime="application/pdf"
        )
