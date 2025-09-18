#!/bin/bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <target-dir>" >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/build-production.sh" "$tmp" --force
rm -rf "$1"
mkdir -p "$1"
rsync -a "$tmp/" "$1/"

echo "✅ Exported package to $1"
