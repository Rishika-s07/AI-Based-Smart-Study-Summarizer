from __future__ import annotations

import io
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from modules.ai_summarizer import summarize_chunks
from modules.document_processor import extract_text
from modules.keyword_extractor import extract_keywords
from modules.ocr_processor import ocr_image, tesseract_available
from modules.text_processor import chunk_text, clean_text

load_dotenv()

st.set_page_config(
    page_title="AI Smart Study Summarizer",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI-Based Smart Study Summarizer")
st.caption("Upload study material or paste text to generate a concise summary, key concepts and keywords.")

with st.sidebar:
    st.header("⚙️ Settings")
    summary_length = st.selectbox("Summary length", ["Short", "Medium", "Detailed"], index=1)
    max_chars = st.slider("Chunk size (characters)", 3000, 10000, 7000, 500)
    st.divider()
    st.subheader("System status")
    st.write("Python target: 3.11.9")
    st.write(f"Gemini API: {'Configured' if os.getenv('GEMINI_API_KEY') else 'Not configured'}")
    st.write(f"Tesseract OCR: {'Available' if tesseract_available() else 'Not detected'}")

uploaded = st.file_uploader(
    "Upload study material",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    help="PDF, DOCX and TXT are supported. Images can be processed using Tesseract OCR.",
)

st.markdown("### Or paste study material")
pasted = st.text_area("Study text", height=260, placeholder="Paste your lecture notes, textbook content or revision material here...")

if st.button("✨ Generate Smart Summary", type="primary", use_container_width=True):
    source_text = ""

    if uploaded is not None:
        try:
            raw = uploaded.getvalue()
            file_obj = io.BytesIO(raw)
            suffix = Path(uploaded.name).suffix.lower()
            if suffix in {".pdf", ".docx", ".txt"}:
                source_text = extract_text(file_obj, uploaded.name)
                if suffix == ".pdf" and not source_text:
                    st.warning("No selectable text was found in this PDF. Upload a page image for OCR, or install a PDF renderer for scanned-PDF OCR.")
            elif suffix in {".png", ".jpg", ".jpeg"}:
                source_text = ocr_image(file_obj)
        except Exception as exc:
            st.error(f"Could not read the uploaded file: {exc}")

    if not source_text.strip() and pasted.strip():
        source_text = pasted

    source_text = clean_text(source_text)

    if not source_text:
        st.error("Please upload a supported document/image or paste study material first.")
        st.stop()

    with st.spinner("Processing study material..."):
        chunks = chunk_text(source_text, max_chars=max_chars)
        summary, mode = summarize_chunks(chunks, summary_length)
        keywords = extract_keywords(source_text, top_n=12)

    st.success(f"Summary generated using: {mode}")

    left, right = st.columns([2, 1])
    with left:
        st.subheader("📝 AI-Generated Summary")
        st.markdown(summary)

        st.subheader("📌 Key Points")
        sentences = [s.strip() for s in summary.replace("•", ".").split(".") if s.strip()]
        for sentence in sentences[:8]:
            st.markdown(f"- {sentence}.")

    with right:
        st.subheader("🔑 Important Keywords")
        for keyword in keywords:
            st.markdown(f"`{keyword}`")

    download_text = (
        "AI-BASED SMART STUDY SUMMARIZER\n"
        "================================\n\n"
        f"SUMMARY\n{summary}\n\n"
        "KEYWORDS\n" + ", ".join(keywords) + "\n"
    )
    st.download_button(
        "⬇️ Download Summary",
        data=download_text,
        file_name="study_summary.txt",
        mime="text/plain",
        use_container_width=True,
    )

with st.expander("ℹ️ How this project works"):
    st.markdown(
        """
        1. **Input:** PDF, DOCX, TXT, image or pasted text.\n
        2. **Extraction:** Text is extracted with PyPDF/python-docx; images use Tesseract OCR.\n
        3. **Preprocessing:** Whitespace and formatting are cleaned and long documents are chunked.\n
        4. **AI summarization:** Gemini is used when `GEMINI_API_KEY` is available. Otherwise, an offline extractive summarizer keeps the application usable for demonstration/testing.\n
        5. **Keywords:** TF-IDF is used to identify important terms.\n
        6. **Output:** Summary, key points, keywords and a downloadable text report are shown.\n        """
    )
