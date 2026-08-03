# AI Skills

A collection of reusable AI coding agent skills.
Each skill is a standalone `SKILL.md` file that teaches an AI agent
a specific workflow — from writing tickets to rewriting git history.

## Skills

| Skill | Description |
|-------|-------------|
| [pavlo-agent-skill-creator](skills/pavlo-agent-skill-creator/SKILL.md) | Create and edit SKILL.md files for AI coding agent skills. |
| [pavlo-commit-by-commit-execution](skills/pavlo-commit-by-commit-execution/SKILL.md) | Systematic approach to implementing multi-step plans with explicit user confirmation between each step. |
| [pavlo-commit-oriented-planning](skills/pavlo-commit-oriented-planning/SKILL.md) | Framework for breaking down a task into logically independent, testable steps. |
| [pavlo-commit-rewriter](skills/pavlo-commit-rewriter/SKILL.md) | Automates commit rewriting: preparation, analysis & message drafting, and rewriting via git filter-branch. |
| [pavlo-jira-ticket-writer](skills/pavlo-jira-ticket-writer/SKILL.md) | Write structured engineering tickets for Jira, output as .md files ready to paste into Jira. |
| [pavlo-markdown-editor](skills/pavlo-markdown-editor/SKILL.md) | Create, edit, and reformat Markdown files following strict line-length and meaning-boundary wrapping rules. |
| [pavlo-pr-writer](skills/pavlo-pr-writer/SKILL.md) | Generates professional PR descriptions in Markdown format based on ticket, plan, and rewritten commits. |
| [pavlo-release-announcer](skills/pavlo-release-announcer/SKILL.md) | Generates non-technical Slack announcements for end users based on ticket, commits, and plan. |
| [pavlo-terminal-commands](skills/pavlo-terminal-commands/SKILL.md) | Safe terminal command patterns for AI coding agents. Use when running shell commands to avoid hanging terminals and parsing errors. |

## Plugins (Claude Code)

This repo is also a Claude Code plugin marketplace named `pavlo`.
It exposes three plugins:

| Plugin | What it installs |
|--------|-----------------|
| `pavlo-skills` | All skills (root plugin — `skills/` is unchanged so `npx skills` keeps working) |
| `pavlo-hooks` | Hooks only — starts with the reformat-guard `PostToolUse` hook |
| `pavlo-toolkit` | Everything: installs `pavlo-skills` + `pavlo-hooks` via dependencies |

## Installation (npx skills)

### Project-Level (Current Repo Only)

Install all skills into the current project for all detected agents:

```bash
npx skills add pavloglushko/ai-skills --all
```

Install a single skill:

```bash
npx skills add pavloglushko/ai-skills --skill pavlo-commit-oriented-planning
```

### Global (All Projects)

Install globally so skills are available in every project:

```bash
npx skills add pavloglushko/ai-skills --all -g
```

### For Specific Agent

Do not use `--all` — it overrides `--agent` with all agents.

#### GitHub Copilot

```bash
# Project-level — installs into .agents/skills/ in your repo
npx skills add pavloglushko/ai-skills --skill '*' --agent github-copilot -y

# Global — installs into ~/.copilot/skills/
npx skills add pavloglushko/ai-skills --skill '*' --agent github-copilot -g -y
```

#### Claude Code

```bash
# Project-level — installs into .agents/skills/ in your repo
npx skills add pavloglushko/ai-skills --skill '*' --agent claude-code -y

# Global — installs into ~/.copilot/skills/
npx skills add pavloglushko/ai-skills --skill '*' --agent claude-code -g -y
```

> **Note:** After installing, restart the agent.

### Updating Skills

Update all installed skills to the latest version:

```bash
# Update project skills
npx skills update -y

# Update global skills
npx skills update -g -y

# Update a single skill
npx skills update pavlo-commit-oriented-planning
```

## Claude Plugin Installation

Add the marketplace (once)

```
/plugin marketplace add pavloglushko/ai-skills
```

### Install Everything

```
# Global — all projects (default)
/plugin install pavlo-toolkit@pavlo

# Per-project — shared via git
/plugin install pavlo-toolkit@pavlo --scope project

# Local — only you, only this repo
/plugin install pavlo-toolkit@pavlo --scope local
```

### Skills only

```
/plugin install pavlo-skills@pavlo
/plugin install pavlo-skills@pavlo --scope project
/plugin install pavlo-skills@pavlo --scope local
```

### Hooks only

```
/plugin install pavlo-hooks@pavlo
/plugin install pavlo-hooks@pavlo --scope project
/plugin install pavlo-hooks@pavlo --scope local
```

### Disable the reformat-guard hook

```
/plugin install pavlo-hooks@pavlo --config enable_reformat_hook=false
```

### Updating plugins

1. Re-run `/plugin install <name>@pavlo` (updates are not automatic).
2Run `/reload-plugins` to pick up changes in the current session.

## How It Works

Each skill is a Markdown file (`SKILL.md`) with:

- **YAML front matter** — name, version, description, triggers, and capabilities
  so the agent knows when to activate the skill.
- **Procedural instructions** — step-by-step workflows the agent follows.
- **Examples** — some skills include an `examples/` directory
  with real-world reference outputs.

Skills are designed to be agent-agnostic.
They work with any AI coding assistant that reads Markdown instructions
(GitHub Copilot, Cursor, Cline, etc.).

## Typical Workflow

The skills are designed to chain together for a full feature lifecycle:

```
Jira Ticket Writer  →  Commit-Oriented Planning  →  Commit-by-Commit Execution
       ↓                                                      ↓
  (ticket.md)                                         Commit Rewriter
                                                           ↓
                                                PR Writer  →  Release Announcer
```

1. **Write a ticket** — structured requirements with acceptance criteria.
2. **Plan the work** — break the ticket into independent, testable steps.
3. **Execute step by step** — implement each step with tests, one commit at a time.
4. **Rewrite commits** — clean up git history with clear, conventional messages.
5. **Write the PR** — generate a professional pull request description.
6. **Announce the release** — produce a non-technical Slack message for stakeholders.

## License

[MIT](LICENSE)

