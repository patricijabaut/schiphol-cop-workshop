#!/usr/bin/env bash
# Verify the workshop prerequisites. Run from the repo root: ./scripts/check-setup.sh
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; PASS=$((PASS + 1)); }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; FAIL=$((FAIL + 1)); }
note() { printf '  \033[33m·\033[0m %s\n' "$1"; }

echo "schiphol-cop-workshop — setup check"
echo

echo "Python"
if command -v python3 >/dev/null 2>&1; then
    version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
        ok "python3 $version (>= 3.11)"
    else
        bad "python3 $version found, but 3.11+ is required"
    fi
else
    bad "python3 not found"
fi

if [ -x ".venv/bin/python" ] || [ -x ".venv/Scripts/python.exe" ]; then
    ok ".venv exists"
    VENV_PY=".venv/bin/python"
    [ -x "$VENV_PY" ] || VENV_PY=".venv/Scripts/python.exe"
    if "$VENV_PY" -c 'import schiphol_ops' >/dev/null 2>&1; then
        ok "schiphol-ops installed in .venv"
    else
        bad "schiphol-ops not importable — run: source .venv/bin/activate && pip install -e \".[dev]\""
    fi
    if "$VENV_PY" -m pytest -q >/dev/null 2>&1; then
        ok "pytest green"
    else
        bad "pytest failing — that's not how this repo ships; check your install"
    fi
else
    bad ".venv missing — run: python3 -m venv .venv && source .venv/bin/activate && pip install -e \".[dev]\""
fi

echo
echo "Git & GitHub"
if command -v git >/dev/null 2>&1; then
    ok "git $(git --version | awk '{print $3}')"
else
    bad "git not found"
fi

if command -v gh >/dev/null 2>&1; then
    ok "gh $(gh --version | head -1 | awk '{print $3}')"
    if gh auth status >/dev/null 2>&1; then
        ok "gh authenticated"
    else
        bad "gh not authenticated — run: gh auth login"
    fi
    origin="$(git remote get-url origin 2>/dev/null || true)"
    if [ -n "$origin" ] && ! printf '%s' "$origin" | grep -q "scholtenmartijn/schiphol-cop-workshop"; then
        ok "working on a fork ($origin)"
    else
        note "origin looks like the upstream repo — did you fork? (gh repo fork --clone)"
    fi
else
    bad "gh not found — install from https://cli.github.com"
fi

echo
echo "Jira"
if command -v acli >/dev/null 2>&1; then
    ok "acli found"
    if acli jira auth status >/dev/null 2>&1; then
        ok "acli authenticated"
    else
        bad "acli not authenticated — run: acli jira auth login"
    fi
else
    bad "acli not found — see docs/workshop/00-setup.md (GitHub Issues fallback exists)"
fi

echo
echo "Copilot"
note "can't be checked from a script — confirm the Copilot extension is installed,"
note "you're signed in, agent mode opens, and the extension is up to date (agent skills need a recent version)."

echo
if [ "$FAIL" -eq 0 ]; then
    printf '\033[32mAll %d checks passed — see you at the workshop.\033[0m\n' "$PASS"
else
    printf '\033[31m%d check(s) failed\033[0m (%d passed) — fix the ✗ lines above, docs/workshop/00-setup.md has the details.\n' "$FAIL" "$PASS"
    exit 1
fi
