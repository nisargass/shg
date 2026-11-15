import re
from typing import Dict, List


class TextChunker:
    """Splits documents into coherent semantic chunks for retrieval."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, doc: Dict[str, str]) -> List[Dict[str, str]]:
        """Splits a document by markdown section headers and paragraphs."""
        content = doc.get("content", "")
        title = doc.get("title", "")
        file_name = doc.get("file_name", "")

        # Split by markdown headers (# or ## or ###)
        sections = re.split(r"\n(?=#{1,3} )", content)
        chunks = []

        for section in sections:
            section_clean = section.strip()
            if not section_clean:
                continue

            if len(section_clean) <= self.chunk_size:
                chunks.append({
                    "title": title,
                    "source": file_name,
                    "text": section_clean
                })
            else:
                # Split large sections by paragraphs
                paragraphs = section_clean.split("\n\n")
                current_chunk = ""
                for p in paragraphs:
                    p_clean = p.strip()
                    if not p_clean:
                        continue
                    if len(current_chunk) + len(p_clean) < self.chunk_size:
                        current_chunk = f"{current_chunk}\n\n{p_clean}".strip()
                    else:
                        if current_chunk:
                            chunks.append({
                                "title": title,
                                "source": file_name,
                                "text": current_chunk
                            })
                        current_chunk = p_clean

                if current_chunk:
                    chunks.append({
                        "title": title,
                        "source": file_name,
                        "text": current_chunk
                    })

        return chunks

