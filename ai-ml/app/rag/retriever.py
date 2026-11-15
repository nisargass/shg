import os
from typing import Any, Dict, List, Tuple
from app.core.config import settings
from app.rag.document_loader import DocumentLoader
from app.rag.chunking import TextChunker
from app.rag.embeddings import LocalEmbeddingProvider
from app.rag.vector_store import SimpleVectorStore


class RAGRetriever:
    """Orchestrates document loading, chunking, embedding, and semantic retrieval."""

    def __init__(self, knowledge_base_dir: str = settings.KNOWLEDGE_BASE_DIR):
        self.knowledge_base_dir = knowledge_base_dir
        self.loader = DocumentLoader(knowledge_base_dir)
        self.chunker = TextChunker(chunk_size=450, chunk_overlap=80)
        self.embeddings = LocalEmbeddingProvider()
        self.vector_store = SimpleVectorStore()
        self._is_indexed = False

    def build_index(self) -> int:
        """Loads all knowledge base documents and builds the vector search index."""
        docs = self.loader.load_documents()
        if not docs:
            return 0

        all_chunks = []
        for doc in docs:
            chunks = self.chunker.chunk_document(doc)
            all_chunks.extend(chunks)

        if not all_chunks:
            return 0

        texts = [c["text"] for c in all_chunks]
        self.embeddings.fit(texts)
        vectors = self.embeddings.transform(texts)
        self.vector_store.add_documents(all_chunks, vectors)
        self._is_indexed = True
        return len(all_chunks)

    def retrieve(self, query: str, top_k: int = 3, min_score_threshold: float = 0.08) -> List[Tuple[Dict[str, Any], float]]:
        """Retrieves top-k relevant document chunks for the given query."""
        if not self._is_indexed:
            self.build_index()

        if not self._is_indexed:
            return []

        try:
            q_vec = self.embeddings.embed_query(query)
            results = self.vector_store.similarity_search(q_vec, top_k=top_k)
            # Filter results by relevance threshold
            filtered = [r for r in results if r[1] >= min_score_threshold]
            return filtered
        except Exception:
            return []


# Global singleton retriever instance
rag_retriever = RAGRetriever()

