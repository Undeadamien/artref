#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")" || exit 0

WALLHAVEN_URL="https://wallhaven.cc/api/v1/search"
SCRYFALL_URL="https://api.scryfall.com/cards/search"

curl "${WALLHAVEN_URL}?q=guweiz" | jq >wallhaven.json
curl "${SCRYFALL_URL}?q=art:dragon" | jq >scryfall.json
