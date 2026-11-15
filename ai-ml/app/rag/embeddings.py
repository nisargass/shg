from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class LocalEmbeddingProvider:
    """Local, lightweight statistical embedding generator using TF-IDF.

    Operates 100% offline without requiring paid API keys or external GPU dependencies.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True
        )
        self._is_fitted = False

    def fit(self, texts: List[str]) -> None:
        """Fits the vectorizer on the corpus chunks."""
        if texts:
            self.vectorizer.fit(texts)
            self._is_fitted = True

    def transform(self, texts: List[str]) -> np.ndarray:
        """Transforms a list of text strings into embedding vectors."""
        if not self._is_fitted:
            raise RuntimeError("Embedding model has not been fitted on any documents.")
        sparse_mat = self.vectorizer.transform(texts)
        return sparse_mat.toarray()

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single search query."""
        return self.transform([query])[0]

