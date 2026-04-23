"""Loop detection utilities for panel orchestration."""

from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable


class LoopDetector:
    """Detect repeated analysis content using embeddings or keyword fallback."""

    def __init__(self, threshold: float = 0.65) -> None:
        self.threshold = threshold
        self._embedding_cache: dict[str, list[float]] = {}
        self._embedder = self._try_load_embedder()

    @staticmethod
    def _try_load_embedder() -> object | None:
        """Load sentence transformer lazily when available."""
        try:
            from sentence_transformers import SentenceTransformer

            return SentenceTransformer("BAAI/bge-m3")
        except Exception:
            return None

    @staticmethod
    def _norm(vector: list[float]) -> float:
        return math.sqrt(sum(value * value for value in vector))

    def _embed(self, text: str) -> list[float] | None:
        if self._embedder is None:
            return None
        key = hashlib.md5(text.encode("utf-8")).hexdigest()
        if key in self._embedding_cache:
            return self._embedding_cache[key]
        vector = self._embedder.encode(text, normalize_embeddings=True).tolist()
        self._embedding_cache[key] = vector
        return vector

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        numerator = sum(a * b for a, b in zip(left, right))
        denom = self._norm(left) * self._norm(right)
        if denom == 0:
            return 0.0
        return numerator / denom

    def is_loop(
        self,
        analyst_id: str,
        new_content: str,
        prior_positions: Iterable[str],
    ) -> tuple[bool, str | None, float]:
        """Detect if a new contribution is semantically repetitive."""
        priors = [content for content in prior_positions if content.strip()]
        if not priors:
            return False, None, 0.0

        new_embedding = self._embed(new_content)
        if new_embedding is not None:
            max_similarity = 0.0
            match: str | None = None
            for prior in priors:
                prior_embedding = self._embed(prior)
                if prior_embedding is None:
                    continue
                similarity = self._cosine_similarity(new_embedding, prior_embedding)
                if similarity > max_similarity:
                    max_similarity = similarity
                    match = prior
            if max_similarity >= self.threshold:
                return True, match, max_similarity
            return False, match, max_similarity

        return self._keyword_fallback(new_content, priors)

    def find_least_covered_section(self, report_content: str, covered_topics: Iterable[str]) -> str:
        """Suggest an uncovered section to redirect analyst focus."""
        candidates = [
            "behavioral indicators",
            "network analysis",
            "threat assessment",
            "timeline events",
            "entity relationships",
            "source reliability",
            "gaps and uncertainties",
        ]
        covered = {topic.lower().strip() for topic in covered_topics}
        content = report_content.lower()
        for section in candidates:
            if section not in covered and section in content:
                return section
        for section in candidates:
            if section not in covered:
                return section
        return "gaps and uncertainties"

    def _keyword_fallback(self, new_content: str, priors: Iterable[str]) -> tuple[bool, str | None, float]:
        """Fallback loop check using keyword overlap."""
        pattern = re.compile(r"[a-zA-Z]{3,}")

        def tokenize(value: str) -> set[str]:
            return {token.lower() for token in pattern.findall(value)}

        new_tokens = tokenize(new_content)
        if not new_tokens:
            return False, None, 0.0

        best_score = 0.0
        best_match: str | None = None
        for prior in priors:
            prior_tokens = tokenize(prior)
            if not prior_tokens:
                continue
            intersection = len(new_tokens.intersection(prior_tokens))
            union = len(new_tokens.union(prior_tokens))
            score = intersection / union if union else 0.0
            if score > best_score:
                best_score = score
                best_match = prior

        return best_score >= self.threshold, best_match, best_score
