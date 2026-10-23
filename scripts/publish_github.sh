#!/usr/bin/env bash
# Publish this new, dedicated academic homepage without touching other repositories.
set -euo pipefail
homepage_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$homepage_root"

for homepage_cmd in git gh; do
  if ! command -v "$homepage_cmd" >/dev/null 2>&1; then
    printf 'Missing command: %s. Install it before publishing.\n' "$homepage_cmd" >&2
    exit 1
  fi
done

gh auth status >/dev/null 2>&1 || { printf 'Complete GitHub login first: gh auth login\n' >&2; exit 1; }
homepage_owner="$(gh api user --jq .login)"
if [[ "$(printf '%s' "$homepage_owner" | tr '[:upper:]' '[:lower:]')" != "jack-lizhixin" ]]; then
  printf 'Expected GitHub account Jack-lizhiXin; active account is %s. Stopping.\n' "$homepage_owner" >&2
  exit 1
fi
homepage_repo="Jack-lizhiXin/jack-lizhixin.github.io"
if gh repo view "$homepage_repo" >/dev/null 2>&1; then
  printf 'Repository %s already exists. No files were changed. Review it before updating.\n' "$homepage_repo" >&2
  exit 1
fi
if [[ -e .git ]]; then
  printf 'This folder already has Git history. No files were changed. Review the checkout first.\n' >&2
  exit 1
fi

git init -b main
git config --local user.name 'Zhixin Li'
git config --local user.email '28438818+Jack-lizhiXin@users.noreply.github.com'
git add -- .gitignore .nojekyll index.html chinese english assets content scripts publications.bib README.md
git commit -m 'Add bilingual academic homepage for Zhixin Li'
gh repo create "$homepage_repo" --public --description 'Zhixin Li | Fudan University — Academic Homepage' --source . --remote origin --push

if ! gh api --method POST "repos/$homepage_repo/pages" -f 'source[branch]=main' -f 'source[path]=/' >/dev/null; then
  printf '\nSource files were uploaded. Enable Pages in repository Settings → Pages: main / (root).\n' >&2
  exit 1
fi
printf '\nRepository: https://github.com/%s\n' "$homepage_repo"
printf 'Pages is configured. Expected URL after GitHub finishes deployment: https://jack-lizhixin.github.io/\n'
