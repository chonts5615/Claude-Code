"""Stage routing for v3.1 R1/R2/FINAL/Resume."""

from enum import Enum


class Stage(str, Enum):
    R1 = "R1"        # full pipeline (Phases 1-5)
    R2 = "R2"        # feedback ingestion + 6E-bis/ter/quater + CTIC + output
    FINAL = "FINAL"  # R2 + Phase 7 learning synthesis
    RESUME = "RESUME"
