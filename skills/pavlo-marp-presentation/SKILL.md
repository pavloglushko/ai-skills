---
name: pavlo-marp-presentation
description: >
  Create, edit, preview, and export Marp Markdown presentations via CLI.
  Use when creating or working with slide decks, exporting to PDF,
  or previewing presentations. Installs marp-cli via Homebrew if missing.
metadata:
  author: Pavlo Glushko
  version: "1.3.0"
  applies_to:
    - "docs/**/*presentation*.md"
    - "docs/**/*slides*.md"
  triggers:
    - create presentation
    - create slides
    - marp
    - export to pdf
    - export presentation
    - preview presentation
    - preview slides
    - slide deck
    - mermaid diagram
  capabilities:
    - install marp-cli via Homebrew when not present
    - create new Marp Markdown presentations
    - edit existing Marp presentations
    - export presentations to PDF
    - open a live-reload preview in the browser
    - add and position images, tables, and diagrams in slides
    - render Mermaid diagrams to SVG via mermaid-cli (Homebrew) and embed them in slides
---

# Skill: Marp Presentation

Create, edit, preview, and export Marp Markdown slide decks via the CLI.
PyCharm has no native Marp plugin,
so this skill uses `marp-cli` (installed via Homebrew) for all operations.

## Prerequisites — Ensuring `marp-cli` Is Installed

Run `marp` commands directly.
If a command exits with "command not found" (exit code 127),
install via Homebrew and then re-run the original command:

```bash
brew install marp-cli
```

If Homebrew itself is missing, stop and ask the user to install it first
([https://brew.sh](https://brew.sh)).

## File Location & Naming

- Presentation files live in `docs/` (or a subdirectory of `docs/`).
- Name files descriptively in snake_case:
  `docs/presentation_deep_dive.md`, `docs/slides_m4_review.md`.
- Exported PDFs are written next to the source file by default
  (e.g., `docs/presentation_deep_dive.pdf`).

## Creating a New Presentation

### Front Matter

Every Marp file **must** start with a YAML front-matter block:

```yaml
---
marp: true
theme: default
paginate: true
html: true
style: |
  section {
    font-size: 24px;
  }
---
```

Required fields:

| Field      | Value                              | Purpose                  |
|------------|------------------------------------|--------------------------|
| `marp`     | `true`                             | Enables Marp rendering   |
| `theme`    | `default` or `gaia` or `uncover`   | Visual theme             |
| `paginate` | `true`                             | Shows slide numbers      |
| `html`     | `true`                             | Enables inline HTML — **always include** (see note below) |

> **Why `html: true` is required:**
> Without it, Marp silently strips `style` attributes from all inline HTML
> (e.g. `<span style="color: grey;">`), so coloured or styled text
> renders as plain black text in the exported PDF.

Optional but recommended:

| Field | Value | Purpose |
|-------|-------|---------|
| `header` | any string | Repeated header on every slide |
| `footer` | any string | Repeated footer on every slide |
| `style` | CSS block | Custom styling (font size, colors, etc.) |

### Slide Separators

Use `---` on its own line to separate slides.
The first slide starts immediately after the front-matter closing `---`.

### Slide Structure

```markdown
---
marp: true
theme: default
paginate: true
html: true
---

# Presentation Title

Subtitle or tagline

---

## Section Heading

- Bullet point one
- Bullet point two

---
```

## Marp Syntax Quick Reference

### Images

```markdown
![bg](path/to/image.png)          <!-- full-slide background -->
![bg right:40%](path/to/img.png)  <!-- right 40% background, content on left -->
![bg left:50%](path/to/img.png)   <!-- left 50% background, content on right -->
![w:400](path/to/img.png)         <!-- inline image, 400px wide -->
```

Use relative paths from the Markdown file's directory.
The `--allow-local-files` flag is required for local images during export.

### Speaker Notes

```markdown
<!-- This is a speaker note. It won't appear on the slide. -->
```

### Text Sizing (per-slide directive)

```markdown
<!-- _class: lead -->       <!-- centers content, larger title -->
<!-- _fontSize: 20px -->
```

### Columns via Background Images

Marp does not have native columns.
Use `![bg right:50%]` or `![bg left:50%]` to split the slide.

### Scoped Directives

Prefix a directive with `_` to apply it only to the current slide:

```markdown
<!-- _paginate: false -->   <!-- hide page number on this slide only -->
<!-- _header: "" -->        <!-- hide header on this slide only -->
<!-- _backgroundColor: #1a1a2e --> <!-- dark background for this slide -->
<!-- _color: #ffffff -->    <!-- white text for this slide -->
```

### Fitting Text

Use `<!-- fit -->` after a heading to auto-scale it to fill the slide width:

```markdown
# <!-- fit --> This Heading Scales to Fit
```

### Custom Colours

Marp's HTML sanitiser **strips `style` attributes** from all inline elements,
even when `html: true` is set in the front matter.
This means `<span style="color: grey;">` will render as plain black text in the PDF.

Use **CSS classes** via `<style scoped>` instead:

```markdown
<style scoped>
  .grey { color: #aaa; }
  .red  { color: #c0392b; }
</style>

Normal text and <span class="grey">grey text</span> side by side.
```

This works inside table cells too:

```markdown
| <span class="grey">Outside scope</span> | — | <span class="grey">Future work</span> |
```

> **Rule:** Never use `style="..."` on inline elements.
> Always define a named class in `<style scoped>` and apply it via `class="..."`.

## Mermaid Diagrams

marp-core does **not** render ` ```mermaid ` code blocks natively —
they appear as raw text in the exported PDF/HTML.
Use the following workaround instead.

### Prerequisites — Ensuring `mermaid-cli` Is Installed

Run `mmdc` commands directly.
If a command exits with "command not found" (exit code 127),
install via Homebrew and then re-run the original command:

```bash
brew install mermaid-cli
```

### Workflow

1. **Write the diagram** to a `.mmd` file
   in the same directory as the presentation:

   ```
   docs/my_presentation/architecture.mmd
   ```

2. **Render to SVG** using `mmdc`:

   ```bash
   mmdc -i docs/my_presentation/architecture.mmd \
        -o docs/my_presentation/architecture.svg \
        -b transparent
   ```

3. **Embed the SVG** in the presentation Markdown
   using a standard image reference:

   ```markdown
   ![architecture diagram](./architecture.svg)
   ```

4. **Re-export the presentation** with `--allow-local-files`
   so the SVG is embedded in the PDF:

   ```bash
   marp docs/my_presentation/my_presentation.md \
        --pdf --allow-local-files
   ```

### File Conventions

- The `.mmd` source and the rendered `.svg` live
  **in the same directory** as the presentation `.md` file.
- Name both files identically (minus extension):
  `ecosystem_diagram.mmd` → `ecosystem_diagram.svg`.
- Commit **both** the `.mmd` source and the `.svg` output
  so the diagram stays editable and the presentation renders
  without requiring a build step.

### Re-rendering After Edits

When the `.mmd` source changes,
re-run the `mmdc` command to regenerate the `.svg`
before re-exporting the presentation.

## Exporting to PDF

Run:

```bash
marp <source>.md --pdf --allow-local-files
```

If the command fails with "command not found", run `brew install marp-cli` and retry.

The `--allow-local-files` flag allows embedding local images.
The output PDF is written to the same directory as the source file
(e.g., `docs/presentation.md` → `docs/presentation.pdf`).

To specify a custom output path:

```bash
marp <source>.md --pdf --allow-local-files -o <output>.pdf
```

## Previewing in Browser

Since PyCharm has no Marp preview plugin,
open a live-reload preview in the default browser:

```bash
marp --preview <source>.md
```

If the command fails with "command not found", run `brew install marp-cli` and retry.

This starts a local server and opens the slides in a browser tab.
Changes to the `.md` file are reflected automatically on save.

**This is a background command** — run it with `isBackground: true`
so the agent does not block waiting for the server to exit.

## Exporting to HTML

For a self-contained HTML file (useful for sharing without PDF):

```bash
marp <source>.md --html --allow-local-files
```

## Workflow

### When asked to create a presentation

1. Ask for or infer the target file path (default: `docs/` directory).
2. Create the `.md` file with correct Marp front matter.
3. Write slides using `---` separators.
4. Follow the Markdown Editor skill rules for prose within slides
   (120-char line limit, meaning-boundary wrapping).
5. If the user has images, use relative paths from the file's location
   and the `![bg ...]` syntax for backgrounds.

### When asked to export to PDF

1. Run `marp <source>.md --pdf --allow-local-files`.
2. If the command fails with "command not found", install via `brew install marp-cli` and retry.
3. Report the output file path to the user.

### When asked to preview

1. Run `marp --preview <source>.md` as a **background process**.
2. If the command fails with "command not found", install via `brew install marp-cli` and retry.
3. Tell the user the preview is open in their browser
   and will live-reload on file save.

### When asked to edit an existing presentation

1. Read the existing file in full before making changes.
2. Apply edits surgically — do not rewrite unchanged slides.
3. After editing, offer to re-export or re-preview if appropriate.

## Themes

Marp ships with three built-in themes:

| Theme | Style |
|-------|-------|
| `default` | Clean, minimal, white background |
| `gaia` | Warm tones, slightly more opinionated |
| `uncover` | Modern, dark-friendly |

To use a theme, set `theme: <name>` in front matter.

Custom CSS can be added via the `style` field in front matter
for font sizes, colors, and spacing adjustments.

## Tips

- **Title slides**: use `# Heading` with no bullets for a clean title slide.
- **Dense content slides**: reduce font size via `style` in front matter
  (e.g., `font-size: 20px`) for content-heavy slides.
- **Image-heavy slides**: use `![bg]` syntax rather than inline `![]`
  for better positioning control.
- **Consistent aspect ratio**: Marp defaults to 16:9 (1280×720).
  Override with `size: 4:3` in front matter if needed.

