"""
Cargill Brand Terminology - Approved and problematic term mappings.

Source: Cargill_BrandBook_digital_version_December_2025.pdf
"""

import re
from dataclasses import dataclass


@dataclass
class TermCorrection:
    """A terminology correction with context."""
    original: str
    replacement: str
    severity: str  # "high", "medium", "low"
    context: str


# Approved terminology - use these terms
APPROVED_TERMS = {
    "farmers_ranchers_growers": "farmers, ranchers, growers and producers",
    "customers_partners": "customers and partners",
    "sustainability": "sustainable",
    "purpose": "Nourishing the world in a safe, responsible and sustainable way",
}

# Problematic terminology with replacements
TERM_REPLACEMENTS: dict[str, TermCorrection] = {
    "suppliers": TermCorrection(
        original="suppliers",
        replacement="partners",
        severity="medium",
        context="Use 'partners' instead of 'suppliers'"
    ),
    "consumers": TermCorrection(
        original="consumers",
        replacement="customers",
        severity="medium",
        context="In B2B context, use 'customers' instead of 'consumers'"
    ),
    "eco-friendly": TermCorrection(
        original="eco-friendly",
        replacement="sustainable",
        severity="medium",
        context="Use 'sustainable' not 'eco-friendly'"
    ),
    "green": TermCorrection(
        original="green",
        replacement="sustainable",
        severity="low",
        context="Use 'sustainable' instead of 'green' (except for color references)"
    ),
}

# Corporate jargon to avoid
JARGON_TERMS = {
    "synergy": "collaboration",
    "leverage": "use",
    "circle back": "follow up",
    "move the needle": "make progress",
    "low-hanging fruit": "quick opportunities",
    "bandwidth": "capacity",
    "deep dive": "detailed analysis",
    "pivot": "shift",
    "drill down": "examine closely",
    "boil the ocean": "take on too much",
}

# Overly corporate terms to avoid
OVERLY_CORPORATE = {
    "solutions provider": "partner",
    "best-in-class": "leading",
    "world-class": "exceptional",
    "cutting-edge": "innovative",
    "game-changer": "transformative",
    "disruptive": "innovative",
    "paradigm shift": "significant change",
    "thought leader": "expert",
    "value-add": "benefit",
    "actionable insights": "practical findings",
}

# Brand personality indicator words
PERSONALITY_INDICATORS = {
    "optimistic": {
        "positive": [
            "possibility", "opportunity", "future", "create", "enable",
            "potential", "growth", "progress", "achieve", "succeed",
            "advance", "thrive", "flourish", "build", "develop",
        ],
        "negative": [
            "problem", "challenge", "difficulty", "obstacle", "barrier",
            "threat", "risk", "concern", "issue", "failure",
        ],
    },
    "curious": {
        "positive": [
            "explore", "discover", "question", "what if", "how might",
            "consider", "investigate", "imagine", "wonder", "learn",
        ],
        "negative": [
            "always", "never", "absolutely", "definitely", "certainly",
            "obviously", "clearly",
        ],
    },
    "courageous": {
        "positive": [
            "commit", "bold", "leading", "innovative", "transform",
            "pioneer", "dedicated", "determined", "ambitious",
        ],
        "negative": [
            "might", "perhaps", "possibly", "uncertain", "hopefully",
            "tentatively",
        ],
    },
    "compassionate": {
        "positive": [
            "partner", "support", "together", "care", "people",
            "community", "families", "nourish", "serve", "empower",
        ],
        "negative": [
            "dominate", "control", "force", "demand", "dictate",
            "impose", "exploit",
        ],
    },
    "humble": {
        "positive": [
            "collaborate", "listen", "learn", "respect", "together",
            "appreciate", "grateful", "share",
        ],
        "negative": [
            "best", "superior", "dominate", "leader", "unmatched",
            "unrivaled", "number one", "#1",
        ],
    },
}

PERSONALITY_WEIGHTS = {
    "optimistic": 0.20,
    "curious": 0.15,
    "courageous": 0.20,
    "compassionate": 0.25,
    "humble": 0.20,
}


def check_terminology(text: str) -> list[TermCorrection]:
    """Check text for problematic terminology and return corrections."""
    corrections = []

    text_lower = text.lower()

    # Check replacements
    for term, correction in TERM_REPLACEMENTS.items():
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text_lower):
            # Skip 'green' when used as a color reference
            if term == "green" and any(
                w in text_lower
                for w in ["green color", "green palette", "leaf green", "deep green"]
            ):
                continue
            corrections.append(correction)

    # Check jargon
    for jargon, replacement in JARGON_TERMS.items():
        pattern = r"\b" + re.escape(jargon) + r"\b"
        if re.search(pattern, text_lower):
            corrections.append(TermCorrection(
                original=jargon,
                replacement=replacement,
                severity="medium",
                context=f"Corporate jargon: replace '{jargon}' with '{replacement}'"
            ))

    # Check overly corporate language
    for corporate, replacement in OVERLY_CORPORATE.items():
        pattern = r"\b" + re.escape(corporate) + r"\b"
        if re.search(pattern, text_lower):
            corrections.append(TermCorrection(
                original=corporate,
                replacement=replacement,
                severity="medium",
                context=f"Overly corporate: replace '{corporate}' with '{replacement}'"
            ))

    return corrections


def analyze_personality(text: str) -> dict[str, dict]:
    """Analyze text for brand personality trait alignment."""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words) if words else 1

    results = {}
    for trait, indicators in PERSONALITY_INDICATORS.items():
        positive_count = sum(
            1 for word in indicators["positive"]
            if word in text_lower
        )
        negative_count = sum(
            1 for word in indicators["negative"]
            if word in text_lower
        )

        # Score between 0 and 1
        positive_density = min(positive_count / max(word_count / 100, 1), 1.0)
        negative_penalty = min(negative_count / max(word_count / 100, 1), 0.5)
        score = max(0.0, min(1.0, positive_density - negative_penalty + 0.5))

        if score >= 0.8:
            assessment = "Excellent"
        elif score >= 0.65:
            assessment = "Good"
        elif score >= 0.5:
            assessment = "Moderate"
        else:
            assessment = "Needs improvement"

        results[trait] = {
            "score": round(score, 2),
            "assessment": assessment,
            "positive_indicators_found": positive_count,
            "negative_indicators_found": negative_count,
            "weight": PERSONALITY_WEIGHTS[trait],
        }

    return results


def apply_corrections(text: str, corrections: list[TermCorrection]) -> str:
    """Apply terminology corrections to text."""
    result = text
    for correction in corrections:
        pattern = re.compile(re.escape(correction.original), re.IGNORECASE)
        result = pattern.sub(correction.replacement, result)
    return result
