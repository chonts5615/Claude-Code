"""Schema validation utilities."""

from typing import Any, List
from pydantic import ValidationError


def validate_schema(data: dict, schema_class: Any) -> tuple[bool, List[str]]:
    """
    Validate data against a Pydantic schema.

    Args:
        data: Dictionary to validate
        schema_class: Pydantic model class

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        schema_class(**data)
        return True, []
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error['loc'])
            msg = error['msg']
            errors.append(f"{field}: {msg}")
        return False, errors


def validate_word_count(text: str, min_words: int, max_words: int) -> tuple[bool, str]:
    """
    Validate text word count is within range.

    Args:
        text: Text to validate
        min_words: Minimum word count
        max_words: Maximum word count

    Returns:
        Tuple of (is_valid, message)
    """
    if not text:
        return False, "Text is empty"

    word_count = len(text.split())

    if word_count < min_words:
        return False, f"Word count ({word_count}) below minimum ({min_words})"

    if word_count > max_words:
        return False, f"Word count ({word_count}) exceeds maximum ({max_words})"

    return True, f"Word count ({word_count}) within range"


def validate_list_length(items: List[Any], min_length: int, max_length: int) -> tuple[bool, str]:
    """
    Validate list length is within range.

    Args:
        items: List to validate
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        Tuple of (is_valid, message)
    """
    length = len(items)

    if length < min_length:
        return False, f"List length ({length}) below minimum ({min_length})"

    if length > max_length:
        return False, f"List length ({length}) exceeds maximum ({max_length})"

    return True, f"List length ({length}) within range"
