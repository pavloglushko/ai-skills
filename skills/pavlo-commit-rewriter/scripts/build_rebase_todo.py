"""Parse commit_rewrite_mapping.md and generate rebase todo + message mapping.

Usage:
    python3 -u scripts/build_rebase_todo.py \
        --mapping  commit_rewrite_mapping.md \
        --branch-point <hash> \
        --todo-output /tmp/rebase_todo.txt \
        --msg-mapping-output /tmp/commit_msg_mapping.json
"""

import argparse
import json
import os
import re
import subprocess  # nosec B404
import tempfile

_MIN_COLUMNS = 5
_DEFAULT_TODO_OUTPUT = os.path.join(tempfile.gettempdir(), "rebase_todo.txt")
_DEFAULT_MSG_MAPPING_OUTPUT = os.path.join(tempfile.gettempdir(), "commit_msg_mapping.json")


def parse_mapping_table(path: str) -> list[dict[str, str]]:
    """Parse the markdown table into a list of row dicts."""
    rows: list[dict[str, str]] = []
    with open(path) as f:
        raw_lines = f.readlines()

    header_found = False
    for raw_line in raw_lines:
        stripped = raw_line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        if not header_found:
            header_found = True
            continue
        # Skip separator row (e.g., |---|---|...)
        if all(re.fullmatch(r"-+", c) for c in cells):
            continue
        if len(cells) < _MIN_COLUMNS:
            continue
        rows.append(
            {
                "num": cells[0].strip(),
                "old_msg": cells[1].strip().strip("`"),
                "new_msg": cells[2].strip().strip("`"),
                "plan_commit": cells[3].strip(),
                "comments": cells[4].strip(),
            }
        )
    return rows


def get_commits(branch_point: str) -> list[dict[str, str]]:
    """Get commits oldest-first as [{hash, subject}]."""
    result = subprocess.run(  # nosec B603 B607
        ["git", "--no-pager", "log", "--reverse", "--format=%H|%s", f"{branch_point}..HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        h, s = line.split("|", 1)
        commits.append({"hash": h, "subject": s})
    return commits


def parse_merge_target(comments: str) -> str | None:
    """Extract target row number from 'merge with #X' or 'squash into #X'."""
    m = re.search(r"(?:merge with|squash into)\s+#(\d+)", comments, re.IGNORECASE)
    return m.group(1) if m else None


def is_delete(comments: str) -> bool:
    return "delete" in comments.lower()


def match_commit_to_row(subject: str, rows: list[dict[str, str]]) -> dict[str, str] | None:
    """Match a git commit subject to a mapping row by old_msg prefix."""
    for row in rows:
        old = row["old_msg"]
        if old and subject.startswith(old):
            return row
    return None


def _classify_rows(rows: list[dict[str, str]]) -> tuple[dict[str, str], set[str]]:
    """Return (merge_sources, delete_rows) from the mapping table."""
    merge_sources: dict[str, str] = {}
    delete_rows: set[str] = set()
    for row in rows:
        target = parse_merge_target(row["comments"])
        if target:
            merge_sources[row["num"]] = target
        if is_delete(row["comments"]):
            delete_rows.add(row["num"])
    return merge_sources, delete_rows


def _build_todo_lines(
    commits: list[dict[str, str]],
    rows: list[dict[str, str]],
    merge_sources: dict[str, str],
    delete_rows: set[str],
) -> list[str]:
    """Build rebase todo lines from commits and classification."""
    todo_lines: list[str] = []
    for commit in commits:
        row = match_commit_to_row(commit["subject"], rows)
        short_hash = commit["hash"][:7]
        subject = commit["subject"][:72]
        if row is None:
            todo_lines.append(f"pick {short_hash} {subject}")
        elif row["num"] in delete_rows:
            todo_lines.append(f"drop {short_hash} {subject}")
        elif row["num"] in merge_sources:
            todo_lines.append(f"fixup {short_hash} {subject}")
        else:
            todo_lines.append(f"pick {short_hash} {subject}")
    return todo_lines


def _build_msg_mapping(
    rows: list[dict[str, str]],
    merge_sources: dict[str, str],
    delete_rows: set[str],
) -> dict[str, str]:
    """Build old-prefix → new-title mapping for non-deleted, non-merged rows."""
    msg_mapping: dict[str, str] = {}
    for row in rows:
        if row["num"] in delete_rows or row["num"] in merge_sources:
            continue
        old = row["old_msg"]
        new = row["new_msg"]
        if old and new and new != "—":
            msg_mapping[old] = new
    return msg_mapping


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--branch-point", required=True)
    parser.add_argument("--todo-output", default=_DEFAULT_TODO_OUTPUT)
    parser.add_argument("--msg-mapping-output", default=_DEFAULT_MSG_MAPPING_OUTPUT)
    args = parser.parse_args()

    rows = parse_mapping_table(args.mapping)
    commits = get_commits(args.branch_point)
    merge_sources, delete_rows = _classify_rows(rows)
    todo_lines = _build_todo_lines(commits, rows, merge_sources, delete_rows)

    with open(args.todo_output, "w") as f:
        f.write("\n".join(todo_lines) + "\n")
    print(f"Wrote {len(todo_lines)} lines to {args.todo_output}")

    msg_mapping = _build_msg_mapping(rows, merge_sources, delete_rows)
    with open(args.msg_mapping_output, "w") as f:
        json.dump(msg_mapping, f, indent=2)
    print(f"Wrote {len(msg_mapping)} mappings to {args.msg_mapping_output}")

    picks = sum(1 for entry in todo_lines if entry.startswith("pick"))
    fixups = sum(1 for entry in todo_lines if entry.startswith("fixup"))
    drops = sum(1 for entry in todo_lines if entry.startswith("drop"))
    print(f"Summary: {picks} pick, {fixups} fixup, {drops} drop")
    print(f"Expected commit count after rebase: {picks}")


if __name__ == "__main__":
    main()
