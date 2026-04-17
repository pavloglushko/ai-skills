#!/usr/bin/env bash
# Fetches the Agent Skills specification HTML from agentskills.io
# into the references/ directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFERENCES_DIR="${SCRIPT_DIR}/../references"

mkdir -p "$REFERENCES_DIR"

URL="https://agentskills.io/specification"
HTML_OUT="${REFERENCES_DIR}/agentskills-specification.html"

echo "Fetching ${URL} ..."
curl -fsSL "$URL" -o "$HTML_OUT"
echo "Saved HTML to ${HTML_OUT}"


