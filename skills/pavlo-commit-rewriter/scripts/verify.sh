#!/usr/bin/env bash
# Verify rewritten commits: check count and compare against BACKUP.
#
# Usage:
#   bash scripts/verify.sh <branch-point> <branch> <expected-count>
#
# Example:
#   bash scripts/verify.sh f0aceed2 LDS3-1290-simple-logics-PR3 18

set -euo pipefail

BRANCH_POINT="$1"
BRANCH="$2"
EXPECTED="$3"
BACKUP="${BRANCH}-BACKUP"

echo "=== Commit count ==="
ACTUAL=$(git --no-pager log --oneline "${BRANCH_POINT}..${BRANCH}" | wc -l | tr -d ' ')
echo "Expected: ${EXPECTED}  Actual: ${ACTUAL}"
if [ "$ACTUAL" -ne "$EXPECTED" ]; then
    echo "ERROR: commit count mismatch"
    exit 1
fi
echo "OK"

echo ""
echo "=== Rewritten messages ==="
git --no-pager log --oneline "${BRANCH_POINT}..${BRANCH}"

echo ""
echo "=== BACKUP comparison ==="
DIFF=$(git --no-pager diff --stat "${BRANCH}" "${BACKUP}" 2>/dev/null || true)
if [ -z "$DIFF" ]; then
    echo "OK — branches are code-identical (only messages differ)"
else
    echo "WARNING — the following files differ from BACKUP:"
    echo "$DIFF"
    echo ""
    echo "Inspect manually before proceeding."
fi

