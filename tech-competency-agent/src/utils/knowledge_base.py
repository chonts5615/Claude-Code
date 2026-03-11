"""Knowledge base management for reference documents."""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json
import hashlib
from pydantic import BaseModel
import anthropic


class DocumentMetadata(BaseModel):
    """Metadata for a knowledge base document."""
    doc_id: str
    title: str
    file_path: Path
    file_type: str
    upload_timestamp: str
    file_hash: str
    tags: List[str] = []
    category: str = "general"
    description: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None


class DocumentChunk(BaseModel):
    """A chunk of text from a document."""
    chunk_id: str
    doc_id: str
    content: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    chunk_index: int


class KnowledgeBase:
    """Manages reference documents for competency benchmarking."""

    def __init__(self, kb_path: Path):
        """
        Initialize knowledge base.

        Args:
            kb_path: Path to knowledge base directory
        """
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)

        self.docs_path = self.kb_path / "documents"
        self.docs_path.mkdir(exist_ok=True)

        self.index_path = self.kb_path / "index.json"
        self.chunks_path = self.kb_path / "chunks.json"

        self.index = self._load_index()
        self.chunks = self._load_chunks()

    def _load_index(self) -> Dict[str, DocumentMetadata]:
        """Load document index."""
        if self.index_path.exists():
            with open(self.index_path, 'r') as f:
                data = json.load(f)
                return {k: DocumentMetadata(**v) for k, v in data.items()}
        return {}

    def _save_index(self):
        """Save document index."""
        data = {k: v.dict() for k, v in self.index.items()}
        # Convert Path to str for JSON serialization
        for doc_id, doc_data in data.items():
            doc_data['file_path'] = str(doc_data['file_path'])

        with open(self.index_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_chunks(self) -> Dict[str, List[DocumentChunk]]:
        """Load document chunks."""
        if self.chunks_path.exists():
            with open(self.chunks_path, 'r') as f:
                data = json.load(f)
                return {k: [DocumentChunk(**c) for c in v] for k, v in data.items()}
        return {}

    def _save_chunks(self):
        """Save document chunks."""
        data = {k: [c.dict() for c in v] for k, v in self.chunks.items()}
        with open(self.chunks_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_document(
        self,
        file_path: Path,
        title: str,
        category: str = "general",
        tags: List[str] = None,
        description: str = None
    ) -> str:
        """
        Add a document to the knowledge base.

        Args:
            file_path: Path to document file
            title: Document title
            category: Category (e.g., 'framework', 'standard', 'reference')
            tags: Optional tags
            description: Optional description

        Returns:
            Document ID
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Check if already exists
        for doc_id, metadata in self.index.items():
            if metadata.file_hash == file_hash:
                print(f"Document already exists: {doc_id}")
                return doc_id

        # Generate document ID
        doc_id = f"DOC_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file_hash[:8]}"

        # Copy file to knowledge base
        dest_path = self.docs_path / f"{doc_id}{file_path.suffix}"
        import shutil
        shutil.copy2(file_path, dest_path)

        # Extract text and create chunks
        chunks = self._extract_and_chunk_document(dest_path, doc_id)
        self.chunks[doc_id] = chunks

        # Create metadata
        metadata = DocumentMetadata(
            doc_id=doc_id,
            title=title,
            file_path=dest_path,
            file_type=file_path.suffix,
            upload_timestamp=datetime.utcnow().isoformat(),
            file_hash=file_hash,
            tags=tags or [],
            category=category,
            description=description,
            word_count=sum(len(c.content.split()) for c in chunks)
        )

        self.index[doc_id] = metadata

        # Save
        self._save_index()
        self._save_chunks()

        return doc_id

    def _extract_and_chunk_document(self, file_path: Path, doc_id: str) -> List[DocumentChunk]:
        """
        Extract text from document and split into chunks.

        Args:
            file_path: Path to document
            doc_id: Document ID

        Returns:
            List of document chunks
        """
        suffix = file_path.suffix.lower()
        chunks = []

        if suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            chunks = self._chunk_text(text, doc_id)

        elif suffix == '.pdf':
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages, start=1):
                    text = page.extract_text()
                    page_chunks = self._chunk_text(text, doc_id, page_number=page_num)
                    chunks.extend(page_chunks)
            except Exception as e:
                print(f"Error extracting PDF: {e}")

        elif suffix in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
                chunks = self._chunk_text(text, doc_id)
            except Exception as e:
                print(f"Error extracting Word document: {e}")

        elif suffix in ['.xlsx', '.xls', '.csv']:
            # For structured data, store as JSON chunks
            try:
                import pandas as pd
                if suffix == '.csv':
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                # Convert to text representation
                text = df.to_string()
                chunks = self._chunk_text(text, doc_id)
            except Exception as e:
                print(f"Error extracting structured data: {e}")

        return chunks

    def _chunk_text(
        self,
        text: str,
        doc_id: str,
        page_number: Optional[int] = None,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[DocumentChunk]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            doc_id: Document ID
            page_number: Optional page number
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks

        Returns:
            List of document chunks
        """
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunk_id = f"{doc_id}_C{chunk_index:04d}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=chunk_text,
                page_number=page_number,
                chunk_index=chunk_index
            ))

            start = end - overlap
            chunk_index += 1

        return chunks

    def search_documents(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search knowledge base for relevant chunks.

        Args:
            query: Search query
            category: Optional category filter
            tags: Optional tag filter
            top_k: Number of results to return

        Returns:
            List of relevant chunks with metadata
        """
        # Filter documents
        relevant_docs = []
        for doc_id, metadata in self.index.items():
            if category and metadata.category != category:
                continue
            if tags and not any(tag in metadata.tags for tag in tags):
                continue
            relevant_docs.append(doc_id)

        # Get chunks from relevant documents
        all_chunks = []
        for doc_id in relevant_docs:
            if doc_id in self.chunks:
                all_chunks.extend(self.chunks[doc_id])

        # Simple text matching (in production, use embeddings)
        query_lower = query.lower()
        scored_chunks = []

        for chunk in all_chunks:
            # Simple scoring based on keyword presence
            score = 0
            chunk_lower = chunk.content.lower()

            for word in query_lower.split():
                if word in chunk_lower:
                    score += chunk_lower.count(word)

            if score > 0:
                scored_chunks.append((score, chunk))

        # Sort by score and take top k
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_chunks = scored_chunks[:top_k]

        # Format results
        results = []
        for score, chunk in top_chunks:
            metadata = self.index[chunk.doc_id]
            results.append({
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "doc_title": metadata.title,
                "content": chunk.content,
                "page_number": chunk.page_number,
                "relevance_score": score,
                "category": metadata.category,
                "tags": metadata.tags
            })

        return results

    def get_document(self, doc_id: str) -> Optional[DocumentMetadata]:
        """Get document metadata by ID."""
        return self.index.get(doc_id)

    def list_documents(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[DocumentMetadata]:
        """
        List documents in knowledge base.

        Args:
            category: Optional category filter
            tags: Optional tag filter

        Returns:
            List of document metadata
        """
        docs = []
        for metadata in self.index.values():
            if category and metadata.category != category:
                continue
            if tags and not any(tag in metadata.tags for tag in tags):
                continue
            docs.append(metadata)

        return docs

    def remove_document(self, doc_id: str) -> bool:
        """
        Remove a document from the knowledge base.

        Args:
            doc_id: Document ID to remove

        Returns:
            True if removed, False if not found
        """
        if doc_id not in self.index:
            return False

        metadata = self.index[doc_id]

        # Remove file
        if metadata.file_path.exists():
            metadata.file_path.unlink()

        # Remove from index and chunks
        del self.index[doc_id]
        if doc_id in self.chunks:
            del self.chunks[doc_id]

        # Save
        self._save_index()
        self._save_chunks()

        return True

    def get_statistics(self) -> Dict:
        """Get knowledge base statistics."""
        return {
            "total_documents": len(self.index),
            "total_chunks": sum(len(chunks) for chunks in self.chunks.values()),
            "categories": list(set(m.category for m in self.index.values())),
            "total_words": sum(m.word_count or 0 for m in self.index.values()),
            "documents_by_category": {
                cat: len([m for m in self.index.values() if m.category == cat])
                for cat in set(m.category for m in self.index.values())
            }
        }
