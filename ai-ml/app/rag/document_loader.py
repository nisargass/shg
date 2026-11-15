import os
from typing import Dict, List


class DocumentLoader:
    """Loads knowledge base markdown and text documents for RAG indexing."""

    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def load_documents(self) -> List[Dict[str, str]]:
        """Reads all .md and .txt files from the knowledge base directory."""
        documents = []
        if not os.path.exists(self.directory_path):
            return documents

        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if file.endswith((".md", ".txt")):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Extract first header as title if available
                        lines = content.split("\n")
                        title = file
                        for line in lines:
                            if line.startswith("# "):
                                title = line.replace("# ", "").strip()
                                break

                        documents.append({
                            "file_name": file,
                            "file_path": full_path,
                            "title": title,
                            "content": content
                        })
                    except Exception as e:
                        # Skip unreadable files safely
                        continue

        return documents

