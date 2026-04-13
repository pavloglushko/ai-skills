"""Git filter-branch message filter that reads mapping from a JSON file.

Usage (as git filter-branch --msg-filter):
    git filter-branch --msg-filter \
        'python3 <skill-dir>/scripts/msg_filter.py /tmp/commit_msg_mapping.json'

Reads the commit message from stdin, matches the first line against the
JSON mapping keys (prefix match), and writes the new title to stdout.
Unmatched messages pass through unchanged.
"""

import json
import sys

_EXPECTED_ARGC = 2


def main() -> None:
    if len(sys.argv) != _EXPECTED_ARGC:
        print(f"Usage: {sys.argv[0]} <mapping.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        mapping: dict[str, str] = json.load(f)

    msg = sys.stdin.read()
    first_line = msg.split("\n")[0]

    for prefix, new_title in mapping.items():
        if first_line.startswith(prefix):
            sys.stdout.write(new_title + "\n")
            return

    sys.stdout.write(msg)


if __name__ == "__main__":
    main()
