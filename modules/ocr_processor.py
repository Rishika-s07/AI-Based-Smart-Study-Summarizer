"""OCR helpers. Tesseract must be installed separately on Windows."""
from __future__ import annotations

import io
from typing import BinaryIO


def ocr_image(file_obj: BinaryIO) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Install pytesseract and Pillow to use OCR.") from exc

    data = file_obj.read()
    image = Image.open(io.BytesIO(data))
    return pytesseract.image_to_string(image).strip()


def tesseract_available() -> bool:
    try:
        import pytesseract
        return bool(pytesseract.get_tesseract_version())
    except Exception:
        return False
