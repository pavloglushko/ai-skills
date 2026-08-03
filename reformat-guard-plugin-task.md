# Task: Turn the ai-skills repo into a plugin marketplace with three plugins

Run this task in the `pavloglushko/ai-skills` repository.

## Goal

Restructure this repo into a Claude Code plugin marketplace that exposes three plugins,
so a user can install exactly the slice they want:

- `pavlo-skills` — all my skills, and nothing else.
- `pavlo-hooks` — my hooks only, starting with a "reformat only changed functions" hook.
- `pavlo-toolkit` — a thin meta-plugin that installs everything
  by declaring `pavlo-skills` and `pavlo-hooks` as dependencies (no copied files).

The marketplace is named `pavlo` (set this as the `name` field in `marketplace.json`;
use this exact name everywhere an install command needs the `@<marketplace>` suffix).

**Hard constraint — do not break the existing skills installer.**
I currently install these skills with the `npx skills` tool (the existing, documented way in this repo),
and that MUST keep working exactly as before after this restructuring.
Before moving anything, determine how that tool discovers skills in this repo
(check the README, any config it reads, and where it expects `SKILL.md` files to live).
If moving skills under `plugins/pavlo-skills/skills/` would change the path the installer relies on,
do NOT silently break it — preserve compatibility (e.g. keep the installer's expected entry point,
adjust its config to the new location, or keep skills discoverable at both paths),
and call out in your plan exactly how you kept `npx skills` working.
If you cannot guarantee both the plugin marketplace and `npx skills` work, stop and ask me
before moving files rather than choosing one over the other.

Install behaviors this must produce:

- `/plugin install pavlo-toolkit@pavlo` installs everything.
- `/plugin install pavlo-hooks@pavlo` installs only the hooks.
- `/plugin install pavlo-skills@pavlo` installs only the skills.

## Important architecture facts (already verified — do not re-litigate)

- A single repo can be a marketplace hosting multiple plugins.
- Plugins install as atomic units; there is no flag to install only some components of one plugin.
- Individual skills inside a plugin cannot be disabled by users, so selecting a subset of skills
  is only possible by splitting skills across plugins (hence `pavlo-skills` as its own plugin).
- A plugin manifest supports a `dependencies` array; a manifest with only `name` and `dependencies`
  is a valid meta-plugin that pulls in its dependencies on install. This is how `pavlo-toolkit` works.
- Do not physically copy skills or hooks into `pavlo-toolkit`; it references the other two by dependency.
- Skills are namespaced per plugin (`plugin-name:skill-name`) and hooks from multiple plugins coexist,
  so there is no collision even if a user installs a leaf plugin and the meta-plugin together.

## Steps

1. **Verify current schemas first.**
   Before writing anything, fetch the current Claude Code docs and confirm the exact field names for:
   (a) `plugin.json` (including the `dependencies` field and its version-constraint syntax),
   (b) the marketplace manifest (`.claude-plugin/marketplace.json`),
   (c) the hooks reference — specifically the `PostToolUse` event
   and the exact JSON output field for injecting context back to the model
   (e.g. `hookSpecificOutput.additionalContext`),
   and (d) the `userConfig` schema and the `CLAUDE_PLUGIN_OPTION_*` env-var naming.
   Use the real, current names from the docs; do not assume.

2. **Inspect the current repo layout.**
   Find where my existing skills currently live in this repo
   and how many there are.
   Note the existing README and any existing `.claude-plugin/` files.
   Show me the plan before moving files if the layout is ambiguous.

3. **Create `pavlo-skills`** at `plugins/pavlo-skills/`:
   - `.claude-plugin/plugin.json` — name `pavlo-skills`, description, `version` `0.1.0`, my author info.
   - `skills/` — move (do not copy) all my existing skills here,
     each as its own `skills/<name>/SKILL.md` subdirectory,
     preserving their current names and front matter.
   - This plugin ships skills only; no hooks.
   - **Pre-approve each skill's own bundled files** to stop permission prompts on install.
     For every skill, inspect what bundled resources it actually references
     (scripts, examples, references, templates, or any file it reads or executes),
     and add an `allowed-tools` entry to that skill's `SKILL.md` front matter
     granting only what it needs, using the `${CLAUDE_SKILL_DIR}` variable.
     Examples:
     - A skill that only reads bundled docs: `allowed-tools: Read(${CLAUDE_SKILL_DIR}/*)`.
     - A skill that also runs a bundled script:
       `allowed-tools: Read(${CLAUDE_SKILL_DIR}/*) Bash(${CLAUDE_SKILL_DIR}/scripts/*.sh *)`.
     Confirm the exact front-matter key name (`allowed-tools`)
     and the `${CLAUDE_SKILL_DIR}` variable against the skills docs from step 1.
     Do not over-grant: scope each rule to the paths and commands that skill genuinely uses,
     and do not add grants to skills that reference no bundled files.
     Note in your summary that this grant applies for the turn the skill is invoked
     (it clears on the next user message and re-applies when the skill runs again).

4. **Create `pavlo-hooks`** at `plugins/pavlo-hooks/`:
   - `.claude-plugin/plugin.json` — name `pavlo-hooks`, description, `version` `0.1.0`, my author info.
     Declare a `userConfig` boolean `enable_reformat_hook` (default `true`)
     so the reformat hook can be turned off at install time with
     `--config enable_reformat_hook=false`.
   - `hooks/hooks.json` — a `PostToolUse` hook matching `Edit|Write|MultiEdit`
     that runs the script below.
   - `hooks/reformat-guard.sh` — the hook script.
     It first checks the config env var (the `CLAUDE_PLUGIN_OPTION_*` form confirmed in step 1)
     and exits early (no-op) when `enable_reformat_hook` is false.
     Otherwise it emits the reminder via the correct `PostToolUse` output field confirmed in step 1.
     Reminder content, roughly:
     _"Reminder: only reformat the function(s) you changed._
     _Do not reformat unrelated functions or introduce whitespace/style churn elsewhere in the file._
     _If you rewrote a whole block, verify unrelated lines are byte-identical to before."_
     Make the script executable
     and reference it with `${CLAUDE_PLUGIN_ROOT}` (or the correct current variable).
   - This is a hook, not a skill; do not create a reformat skill.
     Name this plugin `pavlo-hooks` (not `pavlo-reformat`) so future hooks have a home here.

5. **Create `pavlo-toolkit`** at `plugins/pavlo-toolkit/`:
   - `.claude-plugin/plugin.json` — name `pavlo-toolkit`, description, `version` `0.1.0`,
     my author info, and a `dependencies` array listing `pavlo-skills` and `pavlo-hooks`.
     Use the version-constraint syntax confirmed in step 1
     (a caret/tilde range is fine; pin to the leaf plugins' current versions).
   - This manifest carries no skills and no hooks — dependencies only.

6. **Wire up the marketplace manifest** at the repo-root `.claude-plugin/marketplace.json`
   so all three plugins are discoverable and installable.
   Set the marketplace `name` field to `pavlo` (this is the `@<marketplace>` suffix used in install commands).
   If a marketplace manifest already exists, extend it rather than overwriting,
   and reuse its existing `name` instead of renaming it (update the install commands to match if it differs).
   Confirm the marketplace add command form:
   `/plugin marketplace add pavloglushko/ai-skills`.

7. **Sanity-check** that all JSON is valid, the hook script is executable,
   and the three plugins reference the correct paths.
   Explicitly re-verify that the `npx skills` installer still resolves and installs the skills
   after the move (per the hard constraint above).
   Note the exact commands I would run to test locally (`claude --plugin-dir ...`)
   and to reload in-session (`/reload-plugins`).

8. **Update the repo README** with a section covering:
   - What each plugin is: `pavlo-skills` (skills), `pavlo-hooks` (hooks),
     `pavlo-toolkit` (everything, via dependencies).
   - Adding the marketplace: `/plugin marketplace add pavloglushko/ai-skills`.
   - The three install commands (everything / hooks only / skills only),
     each shown at all three scopes with the exact flags
     (use the `@pavlo` marketplace suffix, e.g. `pavlo-toolkit@pavlo`):
     - Globally (all projects, default): `/plugin install <name>@pavlo`.
     - Per project (shared via git): `/plugin install <name>@pavlo --scope project`.
     - Locally (only me, only this repo): `/plugin install <name>@pavlo --scope local`.
   - Turning off the reformat hook: `--config enable_reformat_hook=false`.
   - Updating: bump `version` in the relevant `plugin.json`,
     then re-run `/plugin install <name>` (updates are not automatic),
     and `/reload-plugins` to pick up changes in-session.
     Note that bumping `pavlo-skills` or `pavlo-hooks` is enough;
     `pavlo-toolkit` pulls the latest within its version range.

## Maintenance notes to record in the README

- Adding a new skill: add it to `pavlo-skills` only, bump `pavlo-skills` version.
  Never duplicate it into `pavlo-toolkit`.
- Adding a new hook: add it to `pavlo-hooks`, bump that version.
  Only create a new leaf plugin (and add one line to `pavlo-toolkit` dependencies)
  if the hook should be independently installable.

## Conventions

For "my author info" in every `plugin.json`, use my GitHub owner `pavloglushko`
and my git `user.name` / `user.email` from `git config` in this repo;
if a manifest schema expects a specific author shape, follow the docs from step 1.

Follow this repo's existing conventions for skills and README style where they apply
(naming, directory layout, front matter, lowercase-kebab-case names).
Confirm the exact `PostToolUse` output field, the `userConfig` env-var naming,
and the `dependencies` version syntax against the docs from step 1 before writing them in.
