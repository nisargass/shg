from typing import Any, Dict, List, Tuple
import numpy as np


class SimpleVectorStore:
    """In-memory vector store computing cosine similarity over document chunks."""

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None

    def add_documents(self, chunks: List[Dict[str, Any]], embeddings: np.ndarray) -> None:
        """Stores chunks and their corresponding normalized embedding vectors."""
        self.chunks = chunks
        
        # Normalize vectors for cosine similarity via dot product
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        self.embeddings = embeddings / norms

    def similarity_search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Searches for the most similar chunks using cosine similarity."""
        if self.embeddings is None or len(self.chunks) == 0:
            return []

        # Normalize query vector
        norm = np.linalg.norm(query_embedding)
        if norm == 0.0:
            return []
        q_norm = query_embedding / norm

        # Cosine similarity dot product
        scores = np.dot(self.embeddings, q_norm)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            results.append((self.chunks[idx], score))

        return results

