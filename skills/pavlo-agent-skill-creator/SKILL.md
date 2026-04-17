---
name: pavlo-agent-skill-creator
description: >
  Create and edit SKILL.md files for AI coding agent skills.
  Use when adding a new skill or improving an existing one.
metadata:
  author: Pavlo Glushko
  version: "1.3.0"
  applies_to:
    - "skills/**/SKILL.md"
  triggers:
    - create skill
    - new skill
    - add skill
    - edit skill
    - update skill
    - improve skill
    - audit skill
    - synchronize specification
  capabilities:
    - create new SKILL.md files with correct structure and metadata
    - edit and improve existing SKILL.md files
    - audit skills for completeness and consistency with conventions
    - synchronize the local specification mirror with agentskills.io
---

# Skill: Agent Skill Creator

Create or edit `SKILL.md` files for AI coding agent skills in this repository.

For the full Agent Skills format specification see
`references/agentskills-specification.md`.
To refresh that file, follow `references/synchronize-specification.md`.

## File Location & Naming

- Every skill lives in its own directory: `skills/<skill-name>/SKILL.md`
- Skill directory names follow the pattern `pavlo-<kebab-case-topic>` (e.g., `pavlo-jira-ticket-writer`).
- Ask for the skill name if the user did not specify one.

## Skill Directory Structure

A skill directory may contain:

```
skills/<skill-name>/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable helper scripts
├── references/       # Optional: additional documentation loaded on demand
├── examples/         # Optional: real-world reference outputs
└── assets/           # Optional: templates, images, data files
```

- **`scripts/`** — self-contained executables (Bash, Python, etc.).
  Include helpful error messages and document dependencies.
- **`references/`** — detailed docs agents read when needed.
  Keep files focused and small to minimise context usage.
- **`assets/`** — static resources: templates, images, lookup tables, schemas.
- **`examples/`** — copies of real project files that demonstrate the skill's output.
  The `SKILL.md` must reference examples explicitly
  (e.g., "See `examples/M2_PR3_plan.md` for a real-world reference.").
  Examples are **snapshots** — they do not need to stay in sync with originals.
  Agents should read examples before generating output to match style and structure.

---

## SKILL.md Structure

Every `SKILL.md` **must** follow this exact structure and section order.

### 1. YAML Frontmatter

YAML frontmatter between `---` delimiters at the very top — no content before it.

#### Required fields

| Field | Constraints |
|---|---|
| `name` | 1-64 chars. Lowercase `a-z`, digits, and hyphens only. No leading/trailing/consecutive hyphens. Must match the directory name. |
| `description` | 1-1024 chars. Describe what the skill does **and** when to use it. Include a "Use when …" clause. |

#### Optional spec-defined fields

| Field | Constraints |
|---|---|
| `license` | License name or reference to a bundled license file. Keep it short. |
| `compatibility` | 1-500 chars. Environment requirements (tools, packages, network). Omit if none. |
| `metadata` | Arbitrary key-value map for additional properties. |
| `allowed-tools` | Space-separated string of pre-approved tools. (Experimental) |

#### Project-specific conventions

Inside `metadata`, this repository uses these keys:

- `metadata.author` — always `Pavlo Glushko`.
- `metadata.version` — semver string (e.g., `"1.0.0"`). Start at `"1.0.0"`,
  increment minor for content additions, patch for corrections.
- `metadata.applies_to` — glob(s) for output or target files
  (e.g., `"docs/ticket_*.md"`, `"skills/**/SKILL.md"`).
- `metadata.triggers` — lower-case phrases a user might say to invoke this skill.
  Include synonyms.
- `metadata.capabilities` — concrete actions the skill can perform,
  not aspirational qualities.

#### Template

```yaml
---
name: <skill-directory-name>
description: >
  <one or two sentences>. Use when …
metadata:
  author: Pavlo Glushko
  version: "1.0.0"
  applies_to:
    - "<glob pattern>"
  triggers:
    - <phrase>
  capabilities:
    - <action>
---
```

### 2. Title

```markdown
# Skill: <Human-Readable Skill Name>
```

One sentence immediately after the heading describing what the skill does
(no heading needed for this sentence).

### 3. File Location & Naming *(if the skill produces output files)*

Explain where output files are created and the naming convention.
Include concrete examples.

### 4. Body Sections

The remaining content is skill-specific.
Structure it so an agent can follow it as a precise procedure.
Common patterns used by existing skills:

- **Structure definition** — when the skill produces a document,
  define every required section with its exact heading, content rules,
  and ordering (see `pavlo-jira-ticket-writer`).
- **Rules / conventions** — when the skill enforces a coding or formatting standard,
  list rules grouped by category with explicit do/don't examples
  (see `pavlo-markdown-editor`).
- **Workflow** — a numbered step-by-step procedure the agent follows.
- **Writing guidelines** — tone, specificity level, privacy constraints,
  and anything else that cannot be inferred from the structure definition alone.

## Progressive Disclosure

Structure skills for efficient context usage:

1. **Frontmatter** (~100 tokens) — `name` and `description` are loaded at startup
   for all skills.
2. **Body** (< 5 000 tokens recommended) — loaded when the skill is activated.
3. **Resources** (as needed) — files in `scripts/`, `references/`, `assets/`
   are loaded only when required.

Keep the main `SKILL.md` under 500 lines.
Move detailed reference material to separate files.
Use relative paths from the skill root when referencing other files
(e.g., `references/REFERENCE.md`, `scripts/extract.py`).
Keep references one level deep — avoid deeply nested chains.

---

## Workflow

### Creating a new skill

1. Determine the skill name: `pavlo-<topic>` in kebab-case.
2. Create the directory `skills/<skill-name>/` and `SKILL.md` inside it.
3. Write the YAML frontmatter first (between `---` delimiters).
4. Add the `# Skill: …` title and one-sentence description.
5. Add a File Location & Naming section if the skill produces output files.
6. Write the body: structure definitions, rules, workflow, guidelines —
   whatever the skill needs to work without further clarification.
7. Keep instructions agent-actionable: avoid vague advice;
   write steps an agent can execute directly.
8. Add a row for the new skill to the skills table in `README.md`.

### Editing an existing skill

1. Read the existing `SKILL.md` in full before making any changes.
2. Identify gaps: missing sections, outdated content,
   or conventions that changed in the codebase.
3. Apply **surgical updates** — do not rewrite sections that are still accurate.
4. Increment `metadata.version` (minor bump for additions, patch for corrections).
5. If the `description` field changed, update the corresponding row
   in the skills table in `README.md` to match exactly.
6. Summarise what was added, modified, or removed
   so the user is aware of the changes.

---

## Writing Guidelines

- **Be prescriptive, not descriptive.** Write "use X" not "X is commonly used".
- **Include examples.** Abstract rules are hard to follow;
  concrete examples eliminate ambiguity.
- **Reference real files.** When a convention is grounded in an existing file,
  cite it by path.
- **One source of truth.** If a convention is already in `AGENTS.md`
  or `copilot-instructions.md`, reference it rather than duplicating it.
- **Privacy.** Do not expose personal workflow rules
  from `copilot-instructions.md` in skill output visible to others.
