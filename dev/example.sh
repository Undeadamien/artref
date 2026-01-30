#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")" || exit 0

source ../.env

SCRYFALL_URL="https://api.scryfall.com/cards/search"
UNSPLASH_URL="https://api.unsplash.com/photos/random"
WALLHAVEN_URL="https://wallhaven.cc/api/v1/search"

curl "${WALLHAVEN_URL}?q=guweiz" | jq >wallhaven.json
curl "${SCRYFALL_URL}?q=art:dragon" | jq >scryfall.json
curl "${UNSPLASH_URL}?client_id=${UNSPLASH_KEY}" | jq >unsplash.json
