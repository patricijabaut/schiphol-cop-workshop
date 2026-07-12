#!/usr/bin/env bash
# Create the workshop tickets in YOUR OWN Jira project via acli.
#
#   ./scripts/seed-jira.sh --project OPS
#
# Reads every docs/workshop/exercises/{exercise,stretch}-*.md, creates one work
# item per file, and writes my-tickets.md mapping exercises to your ticket keys.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXERCISES_DIR="$REPO_ROOT/docs/workshop/exercises"
MAPPING_FILE="$REPO_ROOT/my-tickets.md"

PROJECT=""
while [ $# -gt 0 ]; do
    case "$1" in
        --project) PROJECT="${2:?--project needs a value}"; shift 2 ;;
        -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown argument: $1 (try --help)" >&2; exit 2 ;;
    esac
done

if [ -z "$PROJECT" ]; then
    echo "usage: ./scripts/seed-jira.sh --project <KEY>   (e.g. --project OPS)" >&2
    exit 2
fi

command -v acli >/dev/null 2>&1 || { echo "acli not found — see docs/workshop/00-setup.md" >&2; exit 1; }
acli jira auth status >/dev/null 2>&1 || { echo "acli not authenticated — run: acli jira auth login" >&2; exit 1; }

files=()
for f in "$EXERCISES_DIR"/exercise-*.md "$EXERCISES_DIR"/stretch-*.md; do
    [ -e "$f" ] && files+=("$f")
done
[ "${#files[@]}" -gt 0 ] || { echo "no exercise files found in $EXERCISES_DIR" >&2; exit 1; }

echo "About to create ${#files[@]} work items in Jira project '$PROJECT':"
for f in "${files[@]}"; do
    echo "  - $(head -1 "$f" | sed 's/^# //')"
done
printf 'Continue? [y/N] '
read -r answer
case "$answer" in y|Y|yes|YES) ;; *) echo "aborted."; exit 0 ;; esac

{
    echo "# My workshop tickets"
    echo
    echo "Created $(date +%Y-%m-%d) in Jira project \`$PROJECT\`."
    echo
    echo "| Exercise | Ticket | Summary |"
    echo "|----------|--------|---------|"
} > "$MAPPING_FILE"

for f in "${files[@]}"; do
    title="$(head -1 "$f" | sed 's/^# //')"
    summary="${title#* — }"
    exercise="${title% — *}"
    type="$(grep -m1 '^\*\*Type:\*\*' "$f" | sed 's/^\*\*Type:\*\* *//' | tr -d '[:space:]')"
    [ -n "$type" ] || type="Task"
    description="$(tail -n +2 "$f")"

    echo "Creating [$type] $summary ..."
    if output="$(acli jira workitem create \
            --project "$PROJECT" \
            --type "$type" \
            --summary "$summary" \
            --description "$description" 2>&1)"; then
        :
    elif output="$(acli jira workitem create \
            --project "$PROJECT" \
            --type "Task" \
            --summary "$summary" \
            --description "$description" 2>&1)"; then
        echo "  (work item type '$type' not available — created as Task)"
    else
        echo "  FAILED: $output" >&2
        echo "| $exercise | (failed) | $summary |" >> "$MAPPING_FILE"
        continue
    fi

    key="$(printf '%s' "$output" | grep -oE "$PROJECT-[0-9]+" | head -1)"
    [ -n "$key" ] || key="(created — key not parsed)"
    echo "  -> $key"
    echo "| $exercise | $key | $summary |" >> "$MAPPING_FILE"
done

echo
echo "Done. Your exercise → ticket mapping is in my-tickets.md (gitignored)."
echo "Check them with: acli jira workitem search --jql \"project = $PROJECT ORDER BY created ASC\""
