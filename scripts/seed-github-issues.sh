#!/usr/bin/env bash
# Fallback for participants without a Jira site: create the workshop tickets as
# GitHub issues on YOUR FORK.
#
#   ./scripts/seed-github-issues.sh
#
# Reads every docs/workshop/exercises/{exercise,stretch}-*.md, creates one issue
# per file, and writes my-tickets.md mapping exercises to your issue numbers.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXERCISES_DIR="$REPO_ROOT/docs/workshop/exercises"
MAPPING_FILE="$REPO_ROOT/my-tickets.md"

command -v gh >/dev/null 2>&1 || { echo "gh not found — install from https://cli.github.com" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh not authenticated — run: gh auth login" >&2; exit 1; }

repo="$(cd "$REPO_ROOT" && gh repo view --json nameWithOwner --jq .nameWithOwner)"
if [ "$repo" = "scholtenmartijn/schiphol-cop-workshop" ]; then
    echo "origin is the upstream workshop repo — fork it first: gh repo fork --clone" >&2
    exit 1
fi

files=()
for f in "$EXERCISES_DIR"/exercise-*.md "$EXERCISES_DIR"/stretch-*.md; do
    [ -e "$f" ] && files+=("$f")
done
[ "${#files[@]}" -gt 0 ] || { echo "no exercise files found in $EXERCISES_DIR" >&2; exit 1; }

echo "About to create ${#files[@]} issues on $repo:"
for f in "${files[@]}"; do
    echo "  - $(head -1 "$f" | sed 's/^# //')"
done
printf 'Continue? [y/N] '
read -r answer
case "$answer" in y|Y|yes|YES) ;; *) echo "aborted."; exit 0 ;; esac

# Forks are created without issues enabled more often than not — flip it on.
gh repo edit "$repo" --enable-issues >/dev/null 2>&1 || true
gh label create bug --repo "$repo" --color d73a4a >/dev/null 2>&1 || true
gh label create feature --repo "$repo" --color a2eeef >/dev/null 2>&1 || true

{
    echo "# My workshop tickets"
    echo
    echo "Created $(date +%Y-%m-%d) as GitHub issues on \`$repo\`."
    echo
    echo "| Exercise | Issue | Summary |"
    echo "|----------|-------|---------|"
} > "$MAPPING_FILE"

for f in "${files[@]}"; do
    title="$(head -1 "$f" | sed 's/^# //')"
    summary="${title#* — }"
    exercise="${title% — *}"
    type="$(grep -m1 '^\*\*Type:\*\*' "$f" | sed 's/^\*\*Type:\*\* *//' | tr -d '[:space:]')"
    label="feature"
    [ "$type" = "Bug" ] && label="bug"

    echo "Creating [$label] $summary ..."
    url="$(gh issue create --repo "$repo" --title "$summary" --label "$label" --body-file <(tail -n +2 "$f"))"
    number="#${url##*/}"
    echo "  -> $number"
    echo "| $exercise | $number | $summary |" >> "$MAPPING_FILE"
done

echo
echo "Done. Your exercise → issue mapping is in my-tickets.md (gitignored)."
echo "Where a ticket says 'acli …', use the gh equivalent (gh issue view/comment)."
