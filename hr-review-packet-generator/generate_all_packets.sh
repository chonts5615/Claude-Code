#!/usr/bin/env bash
#
# Generate all three HR Round 2 SME Review Packets:
#   HR_R2_SME_Review_Packet_Total_Rewards.docx
#   HR_R2_SME_Review_Packet_Benefits_Leave.docx
#   HR_R2_SME_Review_Packet_LD_Strategy_Training.docx
#
# Prerequisite: pip install python-docx  (see requirements.txt)
#
set -euo pipefail

# Run from the directory containing this script so the Python imports resolve
# regardless of the caller's working directory.
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

echo "Generating HR R2 SME Review Packets..."
"$PY" generate_packet.py --all "$@"
echo "Done."
