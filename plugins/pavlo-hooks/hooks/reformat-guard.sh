#!/usr/bin/env bash
set -euo pipefail

if [ "${CLAUDE_PLUGIN_OPTION_ENABLE_REFORMAT_HOOK:-true}" = "false" ]; then
  exit 0
fi

printf '%s\n' "$(cat <<'JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Reminder: only reformat the function(s) you changed. Do not reformat unrelated functions or introduce whitespace/style churn elsewhere in the file. If you rewrote a whole block, verify that unrelated lines are byte-identical to before."
  }
}
JSON
)"
