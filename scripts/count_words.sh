#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Not in a git repository or git is not installed."
  exit 1
fi
JSON_PATH="$REPO_ROOT/dict/valid_words.json"

set +u
LENGTH=$1
if [ -z "$LENGTH" ]; then
  read -p "Enter word length: " LENGTH
fi
set -u

if [ ! -f "$JSON_PATH" ]; then
  echo "Error: valid_words.json not found at $JSON_PATH"
  exit 1
fi

jq -r ".\"$LENGTH\" | \"Outbound: \( .outbound_words | length // 0 )\nInbound:  \( .inbound_words | length // 0 )\"" "$JSON_PATH"
