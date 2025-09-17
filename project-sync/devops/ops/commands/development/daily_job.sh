#!/usr/bin/env bash
set -euo pipefail

# Daily job: search and reveal using API-only mode.
# Requires SIGNALHIRE_API_KEY in environment (or .env loaded by CLI).

TITLE=${TITLE:-"Engineer"}
LOCATION=${LOCATION:-"San Francisco"}
SIZE=${SIZE:-25}
OUTDIR=${OUTDIR:-"./daily"}
mkdir -p "$OUTDIR"

echo "[daily] Running search..."
signalhire search \
  --title "$TITLE" \
  --location "$LOCATION" \
  --size "$SIZE" \
  --output "$OUTDIR/search.json"

echo "[daily] Revealing contacts (API-only)..."
signalhire reveal \
  --api-only \
  --search-file "$OUTDIR/search.json" \
  --output "$OUTDIR/contacts.csv"

echo "[daily] Done. Outputs in $OUTDIR"

