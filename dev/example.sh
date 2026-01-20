#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")" || exit 0

WALLHAVEN_URL="https://wallhaven.cc/api/v1/search"
SCRYFALL_URL="https://api.scryfall.com/cards/random"

curl "$WALLHAVEN_URL" | jq >wallhaven.json
curl "$SCRYFALL_URL" | jq >scryfall.json
