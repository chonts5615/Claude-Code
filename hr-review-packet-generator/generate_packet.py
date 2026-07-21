#!/usr/bin/env python3
"""CLI to generate a single HR Round 2 SME Review Packet (.docx).

Usage:
    python generate_packet.py --spec total_rewards
    python generate_packet.py --spec benefits_leave --out custom_name.docx
    python generate_packet.py --all

Specialization keys: total_rewards, benefits_leave, ld_strategy_training
"""

from __future__ import annotations

import argparse
import sys

from hr_content import JOB_FAMILY, SPECIALIZATIONS
from packet_builder import build_packet

DEFAULT_SESSION_DATE = "To be scheduled"


def _default_filename(spec: dict) -> str:
    return f"HR_R2_SME_Review_Packet_{spec['file_slug']}.docx"


def generate(spec_key: str, out: str | None, session_date: str) -> str:
    if spec_key not in SPECIALIZATIONS:
        valid = ", ".join(SPECIALIZATIONS)
        raise SystemExit(f"Unknown specialization '{spec_key}'. Valid keys: {valid}")
    spec = SPECIALIZATIONS[spec_key]
    out_path = out or _default_filename(spec)
    build_packet(spec, JOB_FAMILY, session_date, out_path)
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate HR R2 SME Review Packet(s).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--spec",
        choices=list(SPECIALIZATIONS),
        help="Which specialization packet to generate.",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Generate all specialization packets.",
    )
    parser.add_argument("--out", help="Output filename (only valid with --spec).")
    parser.add_argument(
        "--session-date",
        default=DEFAULT_SESSION_DATE,
        help="Session date shown on the cover page.",
    )
    args = parser.parse_args(argv)

    if args.all:
        if args.out:
            parser.error("--out cannot be combined with --all")
        for key in SPECIALIZATIONS:
            path = generate(key, None, args.session_date)
            print(f"Wrote {path}")
    else:
        path = generate(args.spec, args.out, args.session_date)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
