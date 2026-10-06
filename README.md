# AI-Based Smart Study Summarizer

A Python 3.11.9 + Streamlit academic project that extracts study material from PDF/DOCX/TXT files or images, summarizes it with Gemini when configured, extracts keywords, and provides a downloadable result.

## Features
- PDF, DOCX and TXT input
- Image OCR using Tesseract
- Gemini AI summarization
- Offline extractive fallback when no API key is configured
- TF-IDF keyword extraction
- Long-document chunking
- Downloadable summary

## Setup on Windows

1. Install **Python 3.11.9**.
2. Open Command Prompt in this project folder.
3. Create a virtual environment:
   `py -3.11 -m venv .venv`
4. Activate it:
   `.venv\\Scripts\\activate`
5. Upgrade pip:
   `python -m pip install --upgrade pip`
6. Install packages:
   `pip install -r requirements.txt`
7. Install Tesseract OCR separately if OCR is required. Ensure `tesseract.exe` is on PATH, or configure `pytesseract.pytesseract.tesseract_cmd` in `modules/ocr_processor.py`.
8. Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.
9. Run tests:
   `python -m pytest -q`
10. Start the app:
   `python -m streamlit run app.py`

## Demo without API key
The application intentionally falls back to a local extractive summarizer if Gemini is not configured or the API call fails. This makes the UI testable without exposing an API key. For the final AI demonstration, configure `GEMINI_API_KEY`.

## Sample input
Use `sample_data/sample.txt` or paste the DBMS text into the app.

## Security
Never commit `.env` or a real API key to GitHub.
