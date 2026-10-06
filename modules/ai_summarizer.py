"""Gemini summarization with an offline fallback."""
from __future__ import annotations

import os
from typing import List

from .local_summarizer import extractive_summary

DEFAULT_MODEL = "gemini-3.8-flash"


def _gemini_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def summarize_with_gemini(text: str, length: str = "Medium") -> str:
    client = _gemini_client()
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    target = {
        "Short": "Write a concise 5-7 sentence study summary.",
        "Medium": "Write a clear 8-12 sentence study summary.",
        "Detailed": "Write a detailed but focused study summary with headings and important concepts.",
    }.get(length, "Write a clear study summary.")

    prompt = f"""You are an expert academic study assistant.
Summarize the following study material for a CSE student.
{target}
Preserve important definitions, concepts, relationships, formulas, and examples.
Do not invent information that is not present in the source.
Use simple academic language.

STUDY MATERIAL:
{text}
"""
    response = client.models.generate_content(model=model, contents=prompt)
    result = getattr(response, "text", None)
    if not result:
        raise RuntimeError("Gemini returned an empty response.")
    return result.strip()


def summarize(text: str, length: str = "Medium") -> tuple[str, str]:
    """Return (summary, mode). Mode is 'Gemini' or 'Offline fallback'."""
    try:
        return summarize_with_gemini(text, length), "Gemini AI"
    except Exception:
        sentence_count = {"Short": 4, "Medium": 6, "Detailed": 9}.get(length, 6)
        return extractive_summary(text, sentence_count), "Offline fallback"


def summarize_chunks(chunks: List[str], length: str = "Medium") -> tuple[str, str]:
    if not chunks:
        return "", "Offline fallback"
    if len(chunks) == 1:
        return summarize(chunks[0], length)

    partials = []
    modes = []
    for chunk in chunks:
        summary, mode = summarize(chunk, "Short")
        partials.append(summary)
        modes.append(mode)

    combined = "\n\n".join(partials)
    final, final_mode = summarize(combined, length)
    if "Gemini" in modes and final_mode == "Gemini AI":
        return final, "Gemini AI"
    return final, "Offline fallback"
