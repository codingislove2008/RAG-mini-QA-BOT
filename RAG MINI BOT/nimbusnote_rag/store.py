# Simple in-memory vector store using numpy for similarity search
from __future__ import annotations

import numpy as np

from .config import CACHE_PATH, MIN_SCORE, TOP_K
from .embed import embed_query, embed_texts


class VectorStore:
    def __init__(self, chunks: list[dict], embeddings: np.ndarray):
        self.chunks = chunks
        self.embeddings = embeddings  # L2-normalized matrix (n, dim)

    def search(self, question: str, top_k: int = TOP_K, min_score: float = MIN_SCORE) -> list[dict]:
        q = question.strip()
        if not q or len(self.chunks) == 0:
            return []

        query_vec = embed_query(q)
        # normalized dot product gives cosine similarity directly
        scores = self.embeddings @ query_vec
        ranked_idx = np.argsort(scores)[::-1][:top_k]

        hits = []
        for idx in ranked_idx:
            score = float(scores[idx])
            if score < min_score:
                continue
            hit = dict(self.chunks[idx])
            hit["score"] = round(score, 4)
            hits.append(hit)
        return hits

    def save(self, path=CACHE_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            embeddings=self.embeddings,
            sources=np.array([c["source"] for c in self.chunks], dtype=object),
            sections=np.array([c["section"] for c in self.chunks], dtype=object),
            texts=np.array([c["text"] for c in self.chunks], dtype=object),
        )

    @classmethod
    def load(cls, path=CACHE_PATH) -> VectorStore:
        data = np.load(path, allow_pickle=True)
        chunks = [
            {"source": s, "section": sec, "text": t}
            for s, sec, t in zip(data["sources"], data["sections"], data["texts"])
        ]
        return cls(chunks, data["embeddings"].astype(np.float32))


def build_store(chunks: list[dict]) -> VectorStore:
    embeddings = embed_texts([c["text"] for c in chunks])
    return VectorStore(chunks, embeddings)
