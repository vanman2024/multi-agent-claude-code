#!/bin/bash
# Thin wrapper around deploy-to-production.sh for compatibility.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/deploy-to-production.sh" "$@"
