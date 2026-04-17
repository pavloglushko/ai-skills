---
name: pavlo-terminal-commands
description: >
  Safe terminal command patterns for AI coding agents.
  Use when running shell commands, especially Python scripts,
  to avoid hanging terminals and parsing errors.
metadata:
  author: Pavlo Glushko
  version: "1.0.0"
  applies_to:
    - "**/*.sh"
    - "**/*.py"
  triggers:
    - run command
    - terminal command
    - run python
    - execute script
    - shell command
    - run in terminal
  capabilities:
    - enforce safe Python execution via temp files
    - prevent shell quoting issues with inline Python
    - provide terminal command best practices for AI agents
---

# Skill: Terminal Commands

Safe terminal command patterns for AI coding agents.
Prevents common pitfalls like shell quote misparses and hanging terminals.

## Python Execution

**Always write Python scripts to a temp file and run from there.**

### Do

```bash
cat > /tmp/script.py << 'PYEOF'
import json

data = {"key": "value"}
print(json.dumps(data, indent=2))
PYEOF
python3 -u /tmp/script.py
```

- Use `python3 -u` (unbuffered) to ensure output appears immediately.
- Use a heredoc with **quoted delimiter** (`<< 'PYEOF'`)
  so the shell does not expand variables inside the script.
- Use `/tmp/script.py` or another temp path.

### Do Not

```bash
# ❌ Never do this — shell misparses inner quotes and hangs on dquote>
python3 -c "
import json
data = {'key': 'value'}
print(json.dumps(data, indent=2))
"
```

- Never pass multi-line Python via `python3 -c "..."`.
- The shell misparses inner quotes (single inside double, nested strings)
  and hangs waiting for input (`dquote>`).

## General Terminal Rules

- **Disable pagers.** Commands like `git`, `less`, `man` may invoke a pager
  that blocks the agent. Always add flags to disable:
  - `git --no-pager log` instead of `git log`
  - `git --no-pager diff` instead of `git diff`
  - Pipe to `cat` as a fallback: `some-command | cat`

- **Quote variables.** Use `"$var"` instead of `$var`
  to handle paths and values with spaces.

- **Avoid printing credentials.** Never echo secrets, tokens,
  or API keys to the terminal unless absolutely required.

- **Check exit codes.** Use `&& ` to chain dependent commands
  so failures stop the chain:
  ```bash
  command1 && command2 && command3
  ```

