"""Document extraction for PDF, DOCX and TXT inputs."""
from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader
from docx import Document


def extract_from_pdf(file_obj: BinaryIO) -> str:
    reader = PdfReader(file_obj)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages).strip()


def extract_from_docx(file_obj: BinaryIO) -> str:
    document = Document(file_obj)
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs).strip()


def extract_from_txt(file_obj: BinaryIO) -> str:
    data = file_obj.read()
    if isinstance(data, str):
        return data
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_text(file_obj: BinaryIO, filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return extract_from_pdf(file_obj)
    if suffix == ".docx":
        return extract_from_docx(file_obj)
    if suffix == ".txt":
        return extract_from_txt(file_obj)
    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")
