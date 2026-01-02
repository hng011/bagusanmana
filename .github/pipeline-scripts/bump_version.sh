#!/bin/bash

# 1. Fetch all tags (so we can see the history)
git fetch --tags

# 2. Get the latest tag. Default to v0.0.0 if none exists.
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current Version: $LAST_TAG"

# 3. Analyze commits between Last Tag and HEAD
LOGS=$(git log "$LAST_TAG"..HEAD --pretty=format:%s)

# Remove 'v' for math (v1.0.0 -> 1.0.0)
VERSION_NO_V=${LAST_TAG#v}
IFS='.' read -r major minor patch <<< "$VERSION_NO_V"

# 4. Determine the increment
# Default: Patch (for fixes or misc)
NEW_MAJOR=$major
NEW_MINOR=$minor
NEW_PATCH=$((patch + 1))

if echo "$LOGS" | grep -qE "^BREAKING CHANGE|^feat!:"; then
    NEW_MAJOR=$((major + 1))
    NEW_MINOR=0
    NEW_PATCH=0
    echo "Detected BREAKING CHANGE. Bumping MAJOR."
elif echo "$LOGS" | grep -qE "^feat:"; then
    NEW_MINOR=$((minor + 1))
    NEW_PATCH=0
    echo "Detected feature. Bumping MINOR."
else
    echo "No features detected. Bumping PATCH."
fi

NEW_TAG="v$NEW_MAJOR.$NEW_MINOR.$NEW_PATCH"

# # 5. Output result to GitHub Actions
echo "new_tag=$NEW_TAG"
echo "new_tag=$NEW_TAG" >> $GITHUB_OUTPUT