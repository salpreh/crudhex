#!/usr/bin/env bash
set -e && set -o pipefail

TYPE='minor'
if [[ $# -gt 0 && -n "$1" ]]; then
    TYPE=$1
fi

VERSION=$(poetry version $TYPE | sed -nr 's/.*([0-9]+\.[0-9]+\.[0-9]+).*/\1/p')
echo "New version: $VERSION"

COMMIT_MSG="Bump version to $VERSION"
git add pyproject.toml
git commit -m "$COMMIT_MSG"
echo "New version update commit created: $COMMIT_MSG"

git tag -a "$VERSION" -m "'Release $VERSION'"
echo "Commit tagged"
