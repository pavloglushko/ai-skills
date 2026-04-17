# Synchronize Agent Skills Specification

The specification file `agentskills-specification.md` mirrors the official spec at
<https://agentskills.io/specification>. Follow the steps below to refresh it.

## Steps

1. Run the fetch script:

   ```bash
   skills/pavlo-agent-skill-creator/scripts/fetch-specification.sh
   ```

   This downloads the latest page as `agentskills-specification.html`.

2. Read the downloaded `agentskills-specification.html`.
   Extract the main content (skip navigation, footers, and scripts)
   and convert it to Markdown in memory.

3. Compare the converted content against the existing `agentskills-specification.md`.
   If there are **no meaningful changes**, delete `agentskills-specification.html`
   and stop here — nothing else to update.

4. If changes are detected, overwrite `agentskills-specification.md` with the new content.
   Preserve clean Markdown formatting: headings, code blocks, tables, and lists.

5. Delete `agentskills-specification.html` — it is no longer needed.

6. Compare the updated specification against `SKILL.md` in this skill's root.
   If any instructions in `SKILL.md` contradict the new specification
   (e.g., changed field constraints, renamed fields, new required sections),
   update `SKILL.md` to align with the specification and bump the `version`
   patch number in the front matter.

7. Scan every other skill directory under `skills/`.
   For each `SKILL.md` found, validate it against the updated specification.
