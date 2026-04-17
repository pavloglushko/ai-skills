---
name: pavlo-pr-writer
description: >
  Generates professional PR descriptions in Markdown format based on ticket, plan, and rewritten commits.
  Use after Phases 1 & 2 when you're ready to prepare a pull request for code review.
metadata:
  author: Pavlo Glushko
  version: "1.1.0"
  applies_to:
    - "**/.github/skills/pavlo-pr-writer/**"
  triggers:
    - rewrite commits phase 3
    - generate pr message
    - pr description
    - create pr message
    - pull request message
  capabilities:
    - identify ticket ID from branch name
    - extract ticket context and acceptance criteria
    - synthesize changes from commits and diff stats
    - generate structured PR messages in Markdown
    - group changes by theme (not by commit)
    - present PR descriptions via show_content tool
---

# Skill: PR Writer

Generates a professional PR description in Markdown format based on the ticket, plan document, rewritten commit messages, and code changes. The PR message is multi-audience: suitable for code reviewers and also serves as a record of intent.

## When to Use

After rewriting commit messages (Phase 1 & 2), when you're ready to prepare a pull request for code review. Typically triggered after the user confirms the rewritten commits are acceptable.

## Process Overview

1. **Identify the ticket**: Extracts ticket ID from branch name (e.g., `PROJ-123-feature-name`) or asks user
2. **Gather context**: Collects ticket description, acceptance criteria, and plan document content
3. **Synthesize changes**: Groups code changes by theme/domain (not by individual commits)
4. **Generate PR description** with:
   - Title: `<ticket_id>: <short summary>`
   - Summary: 2–3 sentences explaining what and why
   - Changes: Themed list of changes with commit type labels (feat/fix/refactor/test/docs)
   - Notes: Caveats, follow-ups, or reviewer attention points
5. **Present to user** via `show_content` tool in Markdown format

## PR Description Structure

```markdown
# <ticket_id>: <Short summary>

## Summary
<2–3 sentences on what this PR does and why>

## Changes
- **feat**: <description of feature additions>
- **fix**: <description of bug fixes>
- **refactor**: <description of code improvements>
- **test**: <description of test additions/updates>
- **docs**: <description of documentation updates>

## Notes
<any caveats, follow-ups, or things reviewers should pay attention to>
```

## Key Details

- **Audience**: Primarily code reviewers (technical)
- **Grouping**: By theme or domain, not by individual commit
- **Commit type labels**: Reference the standard types (feat/fix/refactor/test/docs)
- **Alignment**: Must bridge the ticket intent with actual implementation
- **No file paths**: Include semantic descriptions, not just file listings

## Implementation Notes

- Extract ticket ID robustly from branch names with various patterns
- If ticket ID not found in branch, ask user explicitly
- Synthesize rewritten commit messages + diff stats to identify themes
- Ensure all commits are represented in the PR message
- Call `show_content` with format name `pr-message.md`

## Related

- Phase 1 & 2 (message rewriting) produces the commit messages this uses
- Phase 4 (Slack announcement) for end-user communication from same data

