#!/usr/bin/env bash

set -euo pipefail

# mark-working.sh — Set a floating tag to point at a commit and push it.
#
# Usage:
#   scripts/utilities/mark-working.sh [STATE] [REF]
#
# Examples:
#   scripts/utilities/mark-working.sh            # defaults to STATE=working, REF=HEAD
#   scripts/utilities/mark-working.sh stable     # tag: stable-latest -> HEAD
#   scripts/utilities/mark-working.sh working abc1234
#
# Result:
#   - Creates/moves an annotated tag (e.g., working-latest) to REF
#   - Pushes tag to origin with -f
#   - Tag message includes commit subject and timestamp

STATE=${1:-working}
REF=${2:-HEAD}

case "${STATE,,}" in
  stable|working|wip|hotfix) ;;
  *)
    echo "Invalid STATE: '$STATE' (use stable|working|wip|hotfix)" >&2
    exit 1
    ;;
esac

# Resolve SHA and commit info
SHA=$(git rev-parse --verify "$REF")
SUBJ=$(git log -1 --pretty=%s "$SHA")
DATE=$(git log -1 --pretty=%cd --date=iso-strict "$SHA")

TAG_NAME="${STATE,,}-latest"
TAG_MSG="${STATE^^} latest -> ${SHA}

Subject: ${SUBJ}
When:    ${DATE}"

echo "Tagging ${SHA} as '${TAG_NAME}'"
git tag -f -a "$TAG_NAME" -m "$TAG_MSG" "$SHA"

echo "Pushing tag to origin (force)"
git push -f origin "$TAG_NAME"

echo
echo "Done. View: https://github.com/$(git config --get remote.origin.url | sed -e 's#.*github.com[:/]##' -e 's/.git$//')/releases/tag/${TAG_NAME}"
echo "Or check: git show $TAG_NAME"

