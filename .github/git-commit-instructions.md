# Git Commit Message Convention

## Format

```
<type>(<scope>): <short description>

<body — why we did it, not *what*>
```

## Type

| Type | When to use |
|------|-------------|
| `feat` | New functionality or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `perf` | Performance improvement |
| `chore` | Build, CI, tooling, or housekeeping |

## Scope

The skill name without the `pavlo-` prefix, or a repo-level area.
Examples: `commit-rewriter`, `jira-ticket-writer`, `markdown-editor`, `readme`.

## Temporary Commits

Plan files (`plan-*.md`), ticket descriptions, and other working documents
committed during development are considered **temporary**.
They should be prefixed with `[temp]`:

```
[temp] docs(plan): add plan for new skill
[temp] docs(ticket): save ticket contents
```

## Rules

- **Subject line**: imperative mood, no period, max ~72 characters.
- **Body**: explain *why* the change was made,
  not *what* was changed (the diff shows that).
- One logical change per commit.
  If the commit touches unrelated things, split it.

## Examples

```
feat(commit-rewriter): add Phase 4 support

Enable rewriting commits created after the initial rebase
so users can clean up follow-up fixes in the same workflow.
```

```
fix(jira-ticket-writer): correct forJira stripping of Details blocks

The regex stopped too early when a blockquote appeared
between Target and Details, leaving stale content in the output.
```

```
docs(readme): add PyCharm installation instructions

Users on JetBrains IDEs need the --agent github-copilot flag;
document both project-level and global install commands.
```
