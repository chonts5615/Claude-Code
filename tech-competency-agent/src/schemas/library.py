"""23-column Master Library schema for v3.1 deliverable.

Column order is canonical and consumed by `src/deliverables/library_writer.py`.
"""

from typing import List

LIBRARY_COLUMNS: List[str] = [
    "competency_id",         # 1
    "name",                  # 2  (3-6 words)
    "family",                # 3
    "boundary_class",        # 4  V_AND_B|COMMON|TECHNICAL|MIXED
    "definition",            # 5  15-25 words, single sentence
    "why_it_matters",        # 6
    "L1_description",        # 7
    "L1_indicators",         # 8  pipe-delimited (3 items)
    "L2_description",        # 9
    "L2_indicators",         # 10
    "L3_description",        # 11
    "L3_indicators",         # 12
    "L4_description",        # 13
    "L4_indicators",         # 14
    "applied_tools",         # 15
    "applied_standards",     # 16
    "applied_outputs",       # 17
    "criticality_score",     # 18  weighted (0.40/0.30/0.20/0.10)
    "integrity_tag",         # 19  CONFIRMED|CORRECTED|UNVERIFIABLE|FLAGGED
    "source_refs",           # 20  pipe-delimited source_ids
    "rosetta_aliases",       # 21  cross-family aliases
    "first_published_run",   # 22
    "last_modified_run",     # 23
]
