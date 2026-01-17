"""Semantic similarity utilities using sentence transformers."""

from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Global model instance (lazy loaded)
_model = None


def get_similarity_model() -> SentenceTransformer:
    """Get or initialize the similarity model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity between two texts.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not text1 or not text2:
        return 0.0

    model = get_similarity_model()

    # Encode texts
    embeddings = model.encode([text1, text2])

    # Compute cosine similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # Ensure in range [0, 1]
    return max(0.0, min(1.0, float(similarity)))


def compute_similarity_batch(
    query: str,
    candidates: List[str],
    top_k: int = 5
) -> List[Tuple[int, float]]:
    """
    Compute similarity between a query and multiple candidates.

    Args:
        query: Query text
        candidates: List of candidate texts
        top_k: Number of top matches to return

    Returns:
        List of (index, score) tuples for top k matches
    """
    if not query or not candidates:
        return []

    model = get_similarity_model()

    # Encode query and candidates
    query_embedding = model.encode([query])[0]
    candidate_embeddings = model.encode(candidates)

    # Compute similarities
    similarities = cosine_similarity([query_embedding], candidate_embeddings)[0]

    # Get top k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Return (index, score) pairs
    results = [(int(idx), float(similarities[idx])) for idx in top_indices]

    return results


def compute_pairwise_similarity(texts: List[str]) -> np.ndarray:
    """
    Compute pairwise similarity matrix for a list of texts.

    Args:
        texts: List of texts

    Returns:
        NxN similarity matrix
    """
    if not texts:
        return np.array([])

    model = get_similarity_model()

    # Encode all texts
    embeddings = model.encode(texts)

    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(embeddings)

    return similarity_matrix


def find_near_duplicates(
    texts: List[str],
    threshold: float = 0.88
) -> List[Tuple[int, int, float]]:
    """
    Find near-duplicate pairs in a list of texts.

    Args:
        texts: List of texts
        threshold: Similarity threshold for duplicates

    Returns:
        List of (idx1, idx2, similarity) tuples where similarity >= threshold
    """
    similarity_matrix = compute_pairwise_similarity(texts)

    duplicates = []
    n = len(texts)

    for i in range(n):
        for j in range(i + 1, n):
            if similarity_matrix[i, j] >= threshold:
                duplicates.append((i, j, float(similarity_matrix[i, j])))

    return duplicates
