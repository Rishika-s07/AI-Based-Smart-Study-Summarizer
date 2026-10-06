"""Offline extractive summarizer used when Gemini is not configured."""
from __future__ import annotations

import re
from collections import Counter
from typing import List


def _sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.strip()) >= 25]


def extractive_summary(text: str, sentence_count: int = 5) -> str:
    sentences = _sentences(text)
    if not sentences:
        return text.strip()

    words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", text.lower())
    stop = {
        "the", "and", "for", "are", "with", "that", "this", "from", "into",
        "have", "has", "was", "were", "will", "their", "there", "which",
        "about", "also", "than", "then", "they", "them", "been", "being",
        "using", "used", "such", "can", "may", "not", "but", "you", "your",
    }
    freq = Counter(w for w in words if w not in stop)
    if not freq:
        return " ".join(sentences[:sentence_count])

    scored = []
    for index, sentence in enumerate(sentences):
        sw = re.findall(r"[A-Za-z][A-Za-z-]{2,}", sentence.lower())
        score = sum(freq[w] for w in sw) / max(len(sw), 1)
        scored.append((score, index, sentence))

    chosen = sorted(scored, reverse=True)[:sentence_count]
    chosen.sort(key=lambda item: item[1])
    return " ".join(sentence for _, _, sentence in chosen)
