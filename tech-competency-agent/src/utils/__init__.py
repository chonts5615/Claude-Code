"""Shared utilities for the competency extraction system.

Lazy access only — modules are heavy (sentence_transformers, pandas) and
not all callers need them. Import the submodule you need explicitly:
    from src.utils import branding
    from src.utils.similarity import compute_similarity
"""
