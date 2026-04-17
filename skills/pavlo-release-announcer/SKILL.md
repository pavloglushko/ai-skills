---
name: pavlo-release-announcer
description: >
  Generates non-technical Slack announcements for end users based on ticket, commits, and plan.
  Use after Phase 3 when you're ready to communicate the release to non-technical stakeholders.
metadata:
  author: Pavlo Glushko
  version: "1.1.0"
  applies_to:
    - "**/.github/skills/pavlo-release-announcer/**"
  triggers:
    - rewrite commits phase 4
    - slack announcement
    - user announcement
    - end user communication
    - slack message
    - release announcement
  capabilities:
    - gather context from ticket and plan
    - synthesize user-visible changes
    - generate non-technical Slack messages
    - ask for affected users, activation date, contact info
    - use Slack emoji markers for structure
    - present announcements via show_content tool
---

# Skill: Release Announcer

Generates a non-technical Slack announcement for end users based on the ticket, commits, and plan. Translates internal implementation details into user-visible changes in plain English.

## When to Use

After completing PR message generation (PR Writer skill), when you're ready to communicate the release to non-technical stakeholders (end users, ops team, business stakeholders). Typically posted to Slack channels after merge.

## Process Overview

1. **Ask for context** from user:
   - Who is affected (e.g., end users, ops team, business stakeholders)
   - Activation date (e.g., "immediately after merge", specific date)
   - Contact person for questions

2. **Synthesize from ticket/plan/commits**:
   - What is the user-visible problem being solved?
   - What is the user-visible solution (what changed for them)?
   - What should they be aware of?

3. **Generate Slack announcement** using the standard template (see below)

4. **Present to user** via `show_content` tool in Markdown format

## Slack Announcement Template

```
**ANNOUNCEMENT: <short user-facing title> (<team / domain>)**

:office_worker: Affected (external) users: <who is affected, e.g., end users, ops team>

Type / Category of release: <New feature | Bug fix | Improvement>

:large_orange_diamond: Description of change:
**Problem:** <1–3 sentences in plain language>

**Solution:** <1–3 sentences describing what changed from the user's perspective>

:spiral_calendar_pad: Activation date: <date or "after merge">

:telephone_receiver: Contact person/s: <names>

:warning: Please note
<any caveats, limitations, or things users should be aware of>
```

## Key Guidelines

- **No code references**: Avoid class names, method names, config keys, or file paths
- **Plain English**: Assume audience is non-technical (they use the product, read reports, don't care about architecture)
- **User perspective**: Focus on "what changed for me?" not "what changed in the code?"
- **Brevity**: Entire message should fit in one Slack post without scrolling
- **Emojis**: Use provided emoji markers for visual structure (`:office_worker:`, `:large_orange_diamond:`, etc.)

## Implementation Notes

- Translate technical changes to user-facing impact (e.g., "Added validation logic" → "The system will now reject invalid input with a clear error message")
- Ask user if affected parties and activation date are not obvious from context
- Verify the announcement is understandable to someone unfamiliar with the codebase
- Use `show_content` with format name `slack-announcement.md`

## Related

- PR Writer skill provides the technical PR description to synthesize from
- Commit Rewriter skill provides the commits and changes

