# AI Resume Optimizer 

A professional Streamlit application that uses Google Gemini AI to optimize and
reformat resumes, tailored to job descriptions.

## Features

- Upload resumes in **PDF** or **DOCX** format
- Paste a job description for role-specific optimization
- Choose tone (Professional / Confident / Technical / Creative)
- Focus on full resume, summary, skills, or work experience
- **ATS-optimized** output mode (keyword-rich, scannable)
- Inline editor to refine AI output before downloading
- Download result as **DOCX** or **PDF**
- Word-count metrics (original vs. optimized)

<img width="1280" height="584" alt="WhatsApp Video 2026-05-18 at 10 57 18 PM" src="https://github.com/user-attachments/assets/7c34d848-3bd0-4feb-ad07-5450abcd9bd2" />


## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and paste your Gemini API key

# 3. Run
streamlit run app.py
```

## Getting a Gemini API Key

Free keys are available at <https://aistudio.google.com/app/apikey>.

## Fixes applied over original version

| Issue | Fix |
|---|---|
| Missing `GEMINI_API_KEY` configuration | Added `.env` loading + in-app key entry |
| No error handling on PDF read | Dual fallback: PyMuPDF → PyPDF2 |
| No loading states | Full spinner coverage for each stage |
| No way to edit AI output | Added inline editable text area |
| Download buttons always visible | Only shown after successful generation |
| No API key feedback | Status strip shows connection state |
| Hardcoded font path could crash | Graceful fallback to Helvetica |
| Single Gemini model, no fallback | Tries 4 models before failing |
| `PyPDF2` deprecated in requirements | Replaced with `PyMuPDF` as primary |

## Architecture

```
app.py              ← single-file Streamlit app (all logic + UI)
requirements.txt    ← pinned dependencies
.env.example        ← environment variable template
DejaVuSans.ttf      ← Unicode font for PDF export
```
