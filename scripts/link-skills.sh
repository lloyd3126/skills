#!/usr/bin/env bash
set -euo pipefail

# Preview promoted skills; apply only when local installation is requested.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.agents/skills"
APPLY=false
case "${1:-}" in
  "") ;;
  --apply) APPLY=true ;;
  *) echo "Usage: $0 [--apply]" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [--apply]" >&2
  exit 2
fi

sources=()
names=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  for existing in "${names[@]+"${names[@]}"}"; do
    if [ "$name" = "$existing" ]; then
      echo "Duplicate skill name: $name" >&2
      exit 1
    fi
  done
  sources+=("$src")
  names+=("$name")
done < <(find "$REPO/skills/engineering" "$REPO/skills/productivity" -mindepth 2 -maxdepth 2 -name SKILL.md -type f -print0)

if [ "${#sources[@]}" -eq 0 ]; then
  echo "No promoted skills to link."
  exit 0
fi

# Refuse a redirected destination, and check every conflict before writing.
if [ -L "$HOME/.agents" ] || [ -L "$DEST" ] || { [ -e "$DEST" ] && [ ! -d "$DEST" ]; }; then
  echo "Refusing redirected or invalid skill destination: $DEST" >&2
  exit 1
fi
for i in "${!sources[@]}"; do
  target="$DEST/${names[$i]}"
  if [ -L "$target" ] && [ "$(readlink "$target")" = "${sources[$i]}" ]; then
    continue
  fi
  if [ -e "$target" ] || [ -L "$target" ]; then
    echo "Existing skill left untouched: $target" >&2
    exit 1
  fi
done

for i in "${!sources[@]}"; do
  target="$DEST/${names[$i]}"
  if "$APPLY"; then
    mkdir -p "$DEST"
    if [ ! -L "$target" ]; then
      ln -s "${sources[$i]}" "$target"
    fi
    echo "Linked: $target -> ${sources[$i]}"
  else
    echo "Would link: $target -> ${sources[$i]}"
  fi
done
