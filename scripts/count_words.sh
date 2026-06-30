#!/usr/bin/env bash

# Path to the valid_words.json file relative to the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_PATH="$SCRIPT_DIR/../dict/valid_words.json"

LENGTH=$1
if [ -z "$LENGTH" ]; then
  read -p "Enter word length: " LENGTH
fi

if [ ! -f "$JSON_PATH" ]; then
  echo "Error: valid_words.json not found at $JSON_PATH"
  exit 1
fi

jq -r ".\"$LENGTH\" | \"Outbound: \( .outbound_words | length // 0 )\nInbound:  \( .inbound_words | length // 0 )\"" "$JSON_PATH"
