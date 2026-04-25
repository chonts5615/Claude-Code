"""Level Differentiation Rubric (autonomy / scope / complexity / contribution).

Reference data consumed by agent prompts and the rubric validator. Decoupled
from `competency.py` so prompt authors can iterate without schema churn.
"""

from typing import Dict, List

# Ordered scales: position in list = strength (L1 weakest → L4 strongest).
RUBRIC: Dict[str, Dict[str, List[str]]] = {
    "autonomy": {
        "L1": ["with close supervision", "follows defined procedures", "asks for guidance"],
        "L2": ["independently on routine work", "consults on non-standard cases"],
        "L3": ["independently on complex work", "exercises judgment", "shapes approach"],
        "L4": ["sets direction", "establishes standards", "delegates and reviews"],
    },
    "scope": {
        "L1": ["single task", "individual contributor", "single artifact"],
        "L2": ["multi-task", "small team", "feature-level"],
        "L3": ["cross-team", "program-level", "multi-stakeholder"],
        "L4": ["enterprise", "cross-function", "industry/external"],
    },
    "complexity": {
        "L1": ["routine", "well-defined", "structured"],
        "L2": ["semi-structured", "moderately ambiguous"],
        "L3": ["highly ambiguous", "novel", "interdependent"],
        "L4": ["unprecedented", "strategic", "multi-domain"],
    },
    "contribution": {
        "L1": ["executes", "completes", "performs"],
        "L2": ["delivers", "supports", "implements"],
        "L3": ["leads", "designs", "advises"],
        "L4": ["sets vision", "transforms", "mentors at scale"],
    },
}
