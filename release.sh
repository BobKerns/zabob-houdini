#!/usr/bin/env bash

# Release management script for zabob-houdini
# Helps with version bumping and release preparation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYPROJECT_FILE="$SCRIPT_DIR/pyproject.toml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Zabob-Houdini Release Manager${NC}"
echo "==============================="

get_current_version() {
    grep '^version = ' "$PYPROJECT_FILE" | sed 's/version = "\(.*\)"/\1/'
}

bump_version() {
    local current_version="$1"
    local bump_type="$2"

    # Parse version components
    local major minor patch
    IFS='.' read -ra VERSION_PARTS <<< "$current_version"
    major="${VERSION_PARTS[0]}"
    minor="${VERSION_PARTS[1]}"
    patch="${VERSION_PARTS[2]}"

    case "$bump_type" in
        "major")
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        "minor")
            minor=$((minor + 1))
            patch=0
            ;;
        "patch")
            patch=$((patch + 1))
            ;;
        *)
            echo -e "${RED}Invalid bump type: $bump_type${NC}"
            echo "Use: major, minor, or patch"
            exit 1
            ;;
    esac

    echo "$major.$minor.$patch"
}

case "${1:-help}" in
    "status"|"s")
        current_version=$(get_current_version)
        echo -e "${GREEN}Current version:${NC} $current_version"
        echo ""
        echo -e "${YELLOW}Git status:${NC}"
        git status --porcelain
        echo ""
        echo -e "${YELLOW}Recent tags:${NC}"
        git tag --sort=-version:refname | head -5
        ;;

    "test"|"t")
        current_version=$(get_current_version)
        echo -e "${YELLOW}Testing release workflow for version $current_version${NC}"
        echo ""
        echo "This will:"
        echo "1. Run unit tests locally"
        echo "2. Build package locally"
        echo "3. Show you the manual steps for TestPyPI release"
        echo ""
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 0; fi

        echo -e "${BLUE}Running tests...${NC}"
        ./test.sh unit

        echo -e "${BLUE}Building package...${NC}"
        uv build

        echo -e "${GREEN}Package built successfully!${NC}"
        echo ""
        echo -e "${YELLOW}To release to TestPyPI:${NC}"
        echo "1. Go to: https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml"
        echo "2. Click 'Run workflow'"
        echo "3. Select branch: main"
        echo "4. Select repository: testpypi"
        echo "5. Click 'Run workflow'"
        echo ""
        echo -e "${YELLOW}Then test install with:${NC}"
        echo "pip install -i https://test.pypi.org/simple/ zabob-houdini==$current_version"
        ;;

    "bump")
        bump_type="$2"
        if [ -z "$bump_type" ]; then
            echo -e "${RED}Error: Specify bump type${NC}"
            echo "Usage: $0 bump [major|minor|patch]"
            exit 1
        fi

        current_version=$(get_current_version)
        new_version=$(bump_version "$current_version" "$bump_type")

        echo -e "${YELLOW}Version bump: $current_version → $new_version${NC}"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 0; fi

        # Update pyproject.toml
        sed -i.bak "s/version = \"$current_version\"/version = \"$new_version\"/" "$PYPROJECT_FILE"
        rm "$PYPROJECT_FILE.bak"

        echo -e "${GREEN}Version updated to $new_version${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "1. Review changes: git diff"
        echo "2. Test: $0 test"
        echo "3. Commit: git add pyproject.toml && git commit -m 'Bump version to $new_version'"
        echo "4. Release: $0 release"
        ;;

    "release"|"r")
        current_version=$(get_current_version)

        # Check if working directory is clean
        if [ -n "$(git status --porcelain)" ]; then
            echo -e "${RED}Working directory is not clean!${NC}"
            echo "Commit your changes first."
            exit 1
        fi

        echo -e "${YELLOW}Creating release for version $current_version${NC}"
        echo ""
        echo "This will:"
        echo "1. Create git tag v$current_version"
        echo "2. Push tag to origin (triggers automated PyPI release)"
        echo "3. Create GitHub Release"
        echo ""
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 0; fi

        # Create and push tag
        git tag "v$current_version"
        git push origin main
        git push origin "v$current_version"

        echo -e "${GREEN}Release v$current_version created!${NC}"
        echo ""
        echo -e "${YELLOW}Monitor progress:${NC}"
        echo "https://github.com/BobKerns/zabob-houdini/actions"
        echo ""
        echo -e "${YELLOW}Once published, install with:${NC}"
        echo "pip install zabob-houdini==$current_version"
        ;;

    "changelog"|"c")
        current_version=$(get_current_version)
        echo -e "${YELLOW}Recent commits since last tag:${NC}"
        last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
        if [ -n "$last_tag" ]; then
            git log "$last_tag..HEAD" --oneline --no-merges
        else
            echo "No previous tags found"
            git log --oneline --no-merges -10
        fi
        echo ""
        echo -e "${YELLOW}Current CHANGELOG.md entry for v$current_version:${NC}"
        if [ -f "CHANGELOG.md" ]; then
            # Extract changelog section for current version
            changelog_section=$(awk "/^## \[?v?$current_version\]?/,/^## \[?v?[0-9]/ { if (/^## \[?v?[0-9]/ && !/^## \[?v?$current_version\]?/) exit; print }" CHANGELOG.md)
            if [ -n "$changelog_section" ]; then
                echo "$changelog_section"
            else
                echo "No changelog entry found for v$current_version"
                echo "Consider updating CHANGELOG.md before release"
            fi
        else
            echo "CHANGELOG.md not found"
        fi
        ;;

    "prepare-changelog"|"pc")
        current_version=$(get_current_version)
        echo -e "${YELLOW}Preparing changelog for version $current_version${NC}"

        # Check if keep-a-changelog is available
        if ! uv run --group release python -c "import keepachangelog" 2>/dev/null; then
            echo -e "${RED}keepachangelog not available. Installing...${NC}"
            uv sync --group release
        fi

        # Use keepachangelog command to release
        if uv run --group release keepachangelog release "$current_version" -f CHANGELOG.md; then
            echo -e "${GREEN}✅ Moved [Unreleased] changes to [$current_version]${NC}"
        else
            echo -e "${RED}Error: Failed to prepare changelog. Make sure there are unreleased changes.${NC}"
            exit 1
        fi
        ;;

    "help"|"h"|*)
        current_version=$(get_current_version)
        echo ""
        echo -e "${GREEN}Current version: $current_version${NC}"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status, s        Show current version and git status"
        echo "  test, t          Test release workflow (TestPyPI preparation)"
        echo "  bump [type]      Bump version (major, minor, or patch)"
        echo "  release, r       Create production release (git tag → PyPI)"
        echo "  changelog, c     Show recent commits and CHANGELOG.md entry"
        echo "  prepare-changelog Prepare changelog entry for current version"
        echo "  help, h          Show this help"
        echo ""
        echo "Typical workflow:"
        echo "  1. $0 status           # Check current state"
        echo "  2. $0 bump patch       # Bump version"
        echo "  3. $0 test            # Test on TestPyPI"
        echo "  4. $0 changelog       # Review changes"
        echo "  5. $0 release         # Create production release"
        echo ""
        echo "Quick test release:"
        echo "  $0 test               # No version bump, test current version"
        ;;
esac
