# HR Review Packet Generator

Generates Cargill-branded **Round 2 (R2) SME Review Packets** (Word `.docx`) for
the Human Resources job family. Each packet presents draft technical
competencies with L1–L4 behavioral indicators, maps them to band-level essential
functions, and provides structured rating instruments for a 60-minute SME focus
group.

This is a Python (`python-docx`) companion to the repository's
[`sme-validation-package`](../sme-validation-package) skill — it reuses that
skill's document structure, stable boilerplate, and Cargill branding, with the
variable competency content baked in for three HR specializations.

## Specializations / outputs

| Spec key | Specialization | Output file |
|---|---|---|
| `total_rewards` | Total Rewards | `HR_R2_SME_Review_Packet_Total_Rewards.docx` |
| `benefits_leave` | Benefits & Leave | `HR_R2_SME_Review_Packet_Benefits_Leave.docx` |
| `ld_strategy_training` | L&D Strategy & Training | `HR_R2_SME_Review_Packet_LD_Strategy_Training.docx` |

## Quick start

```bash
# 1. Install python-docx (one time)
pip install -r requirements.txt        # or: pip install python-docx

# 2. Make the script executable
chmod +x generate_all_packets.sh

# 3. Run the batch generator
./generate_all_packets.sh
```

This writes all three `.docx` files into the current directory.

## Generating a single packet

```bash
python generate_packet.py --spec total_rewards
python generate_packet.py --spec benefits_leave --out my_packet.docx
python generate_packet.py --spec ld_strategy_training --session-date "2026-07-15"
```

Run `python generate_packet.py --help` for all options.

## Files

| File | Role |
|---|---|
| `generate_packet.py` | CLI entry point (`--spec` / `--all`). |
| `packet_builder.py` | Rendering engine + stable boilerplate (branding, page setup, sections). |
| `hr_content.py` | Variable content — the three specializations' competencies, essential functions, and crosswalks. |
| `generate_all_packets.sh` | Convenience wrapper that builds all three packets. |
| `requirements.txt` | Python dependency (`python-docx`). |

## Document structure

Each packet contains a cover page, then:

1. Project Overview
2. Focus Group Protocol
3. Rating Scales (relevance / clarity / level differentiation)
4. Competency Architecture Reference
5. Technical Competencies Under Review (per-competency L4→L1 indicator tables + rating boxes)
6. Essential Functions Crosswalk (by band + competency × EF matrix)
7. Validation Methodology Note
8. Confidentiality and Data Handling
9. Contact Information
10. Appendix A — Specialization Overview
11. Appendix B — Glossary of Terms

## Branding

Cargill Leaf Green (`#00843D`) for headings, rules, and table headers; White
Green (`#F5F9ED`) for alternating rows. Georgia (headings) and Arial (body) are
used as the documented fallbacks for the licensed Cargill fonts (Big Caslon for
Cargill / Helvetica Now for Cargill), which are not embeddable in this
generation environment.

## Notes

- Not covered by repository CI (CI builds only `tech-competency-agent`).
- Editing competency content: change `hr_content.py` only — the renderer is
  content-agnostic. Each proficiency level must keep exactly three indicators
  (enforced at import time).
