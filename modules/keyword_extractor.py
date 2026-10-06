"""Keyword extraction using TF-IDF with a lightweight fallback."""
from __future__ import annotations

import re
from collections import Counter
from typing import List


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    text = text.strip()
    if not text:
        return []

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
        sentences = [s for s in sentences if s.strip()]
        if len(sentences) >= 2:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                max_features=1000,
            )
            matrix = vectorizer.fit_transform(sentences)
            scores = matrix.mean(axis=0).A1
            terms = vectorizer.get_feature_names_out()
            ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
            return [term for term, _ in ranked[:top_n]]
    except Exception:
        pass

    words = re.findall(r"[A-Za-z][A-Za-z-]{3,}", text.lower())
    stop = {
        "this", "that", "with", "from", "have", "will", "which", "their",
        "about", "there", "these", "those", "into", "using", "used", "also",
        "than", "then", "they", "them", "were", "been", "being", "such",
    }
    counts = Counter(w for w in words if w not in stop)
    return [word for word, _ in counts.most_common(top_n)]
