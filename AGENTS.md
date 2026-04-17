# AI Skills Repository — Agent Instructions

This repository contains reusable AI coding agent skills.
Each skill is a standalone `SKILL.md` file that teaches an AI agent
a specific workflow.

Skills follow the [Agent Skills specification](https://agentskills.io/specification).
A local mirror lives at `skills/pavlo-agent-skill-creator/references/agentskills-specification.md`.
See `pavlo-agent-skill-creator` for the full authoring guide.

## Short Commands

DNE means "Do not edit anything"
If user mentions it in the prompt, you should not edit files, i.e., work in question - answer mode.

DNI means "Do not implement". If user mentions it in the prompt,
you should not implement any code but can change the plan .md, ticket .md or similar planning files.

## Project Structure

```
ai-skills/
├── AGENTS.md                          # This file — project-wide agent instructions
├── README.md                          # Public-facing documentation
├── LICENSE                            # MIT license
├── .gitignore
├── .github/
│   └── git-commit-instructions.md     # Commit message conventions
└── skills/                            # All skills live here
    └── <skill-name>/
        ├── SKILL.md                   # Skill definition (YAML frontmatter + instructions)
        ├── scripts/                   # Optional: executable helper scripts
        ├── references/                # Optional: additional documentation
        ├── examples/                  # Optional: real-world reference outputs
        └── assets/                    # Optional: templates, images, data files
```

## Skill Naming

- Directory names follow the pattern: `pavlo-<kebab-case-topic>`
- The `name` field in YAML frontmatter must exactly match the directory name
- `name` must be 1-64 lowercase alphanumeric characters and hyphens,
  no leading/trailing/consecutive hyphens

## SKILL.md Format

Every skill file must have:

1. **YAML frontmatter** between `---` delimiters with:
   - `name` *(required)* — matches the directory name
   - `description` *(required)* — 1-1024 chars; include a "Use when …" clause
   - `metadata.author` — `Pavlo Glushko`
   - `metadata.version` — semver string (e.g., `"1.0.0"`)
   - `metadata.applies_to` — glob patterns for target files
   - `metadata.triggers` — lower-case phrases that activate the skill
   - `metadata.capabilities` — concrete actions the skill can perform
   - Optional spec fields: `license`, `compatibility`, `allowed-tools`

2. **Body** — procedural instructions the agent follows

See `pavlo-agent-skill-creator` for the full specification of this format.

## When Adding a New Skill

1. Create a directory: `skills/pavlo-<topic>/`
2. Write `SKILL.md` with YAML frontmatter and procedural body
3. Add optional subdirectories (`examples/`, `scripts/`, `references/`, `assets/`) as needed
4. Add the skill to the table in `README.md`

## When Editing an Existing Skill

1. Read the full `SKILL.md` before making changes
2. Make surgical updates — don't rewrite sections that are still accurate
3. Bump `metadata.version` in the frontmatter (minor for additions, patch for fixes)
4. Update the description in `README.md` if it changed

## Writing Guidelines

- **Be prescriptive, not descriptive.** Write "use X" not "X is commonly used"
- **Include examples.** Concrete examples eliminate ambiguity
- **Keep skills project-agnostic.** No company names, internal project keys,
  or proprietary references — these skills are public
- **No local file links in examples.** Use plain text references instead
  of Markdown links to local files

## Markdown Rules

- Maximum line length: 120 characters
- Break lines at meaning boundaries (end of sentence, after comma, after conjunction)
- Use ATX-style headings (`#`, `##`, `###`)
- Use `-` for unordered lists, `1.` for ordered lists
- One blank line before and after headings and code blocks

## Commit Convention

Follow `.github/git-commit-instructions.md`:

```
<type>(<scope>): <short description>
```

- `feat` — new skill or new capability in an existing skill
- `fix` — correction to a skill
- `docs` — README, AGENTS.md, or example updates
- `refactor` — restructuring without behavior change
- `chore` — tooling, CI, or housekeeping

Scope is the skill name without the `pavlo-` prefix
(e.g., `feat(commit-rewriter): add Phase 4 support`).
